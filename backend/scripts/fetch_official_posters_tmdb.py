import re
import time
import urllib.parse
import urllib.request

import mysql.connector as m


TMDB_BASE = "https://www.themoviedb.org"
UA = "MovieSenseSeeder/1.0 (contact: local-dev)"


def http_get(url: str) -> str:
  print(f"[GET] {url}", flush=True)
  req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
  with urllib.request.urlopen(req, timeout=30) as resp:
    return resp.read().decode("utf-8", errors="ignore")


def find_tmdb_movie_url(title: str, year: int | None) -> str | None:
  q = urllib.parse.quote_plus(title)
  html = http_get(f"{TMDB_BASE}/search?query={q}")

  # Typical result snippets contain /movie/<id>-<slug> and release year near it.
  candidates: list[tuple[str, int | None]] = []
  for mobj in re.finditer(r'href="(/movie/\d+[^"]*)"', html):
    href = mobj.group(1)
    # attempt to find a year near the match (next ~400 chars)
    chunk = html[mobj.end() : mobj.end() + 500]
    y = None
    ymatch = re.search(r'(\b19\d{2}\b|\b20\d{2}\b)', chunk)
    if ymatch:
      try:
        y = int(ymatch.group(1))
      except ValueError:
        y = None
    candidates.append((href, y))

  if not candidates:
    return None

  if year:
    for href, y in candidates:
      if y == year:
        return f"{TMDB_BASE}{href}"

  return f"{TMDB_BASE}{candidates[0][0]}"


def extract_og_image(movie_url: str) -> str | None:
  html = http_get(movie_url)
  mobj = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
  if not mobj:
    return None
  return mobj.group(1)


def main():
  conn = m.connect(host="localhost", user="root", password="root", database="movie_recommendation")
  cur = conn.cursor()
  try:
    cur.execute("SELECT movie_id, title, release_year FROM movies ORDER BY movie_id")
    rows = cur.fetchall()
    updated = 0

    for movie_id, title, release_year in rows:
      year = int(release_year) if release_year is not None else None
      try:
        tmdb_url = find_tmdb_movie_url(title, year)
      except Exception as e:
        print(f"[SKIP] TMDB fetch failed: {title} ({year}) -> {e}", flush=True)
        continue
      if not tmdb_url:
        print(f"[SKIP] TMDB not found: {title} ({year})")
        continue

      try:
        poster = extract_og_image(tmdb_url)
      except Exception as e:
        print(f"[SKIP] Poster fetch failed: {title} ({year}) -> {e}", flush=True)
        continue
      if not poster:
        print(f"[SKIP] Poster not found: {title} ({year}) -> {tmdb_url}")
        continue

      cur.execute("UPDATE movies SET poster_url=%s WHERE movie_id=%s", (poster, movie_id))
      conn.commit()
      updated += 1
      print(f"[OK] {title} ({year}) -> {poster}", flush=True)
      time.sleep(0.6)  # be polite to TMDB

    print(f"\nUpdated posters for {updated}/{len(rows)} movies.")
  finally:
    cur.close()
    conn.close()


if __name__ == "__main__":
  main()


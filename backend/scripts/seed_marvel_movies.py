import mysql.connector as m


MARVEL_MOVIES = [
  # title, year, duration(min), genres
  ("Iron Man", 2008, 126, ["Action", "Sci-Fi"]),
  ("Captain America: The Winter Soldier", 2014, 136, ["Action", "Thriller"]),
  ("Guardians of the Galaxy", 2014, 121, ["Action", "Sci-Fi", "Comedy"]),
  ("Captain America: Civil War", 2016, 147, ["Action", "Sci-Fi"]),
  ("Thor: Ragnarok", 2017, 130, ["Action", "Sci-Fi", "Comedy"]),
  ("Black Panther", 2018, 134, ["Action", "Sci-Fi", "Drama"]),
  ("Avengers: Infinity War", 2018, 149, ["Action", "Sci-Fi"]),
  ("Avengers: Endgame", 2019, 181, ["Action", "Sci-Fi", "Drama"]),
  ("Spider-Man: No Way Home", 2021, 148, ["Action", "Sci-Fi"]),
  ("Doctor Strange in the Multiverse of Madness", 2022, 126, ["Action", "Sci-Fi", "Horror"]),
]


def short_desc(title: str) -> str:
  return f"{title} is a Marvel superhero film."


def long_desc(title: str, year: int) -> str:
  return (
    f"{title} ({year}) is a Marvel Studios superhero story built around high-stakes action, big emotions, and a central hero facing an impossible choice. "
    "It balances spectacle with character moments—showing what the hero wants, what they fear, and what they’re willing to sacrifice.\n\n"
    "As the conflict escalates, alliances shift, the consequences grow, and the story pushes toward a defining showdown. "
    "Whether it’s a personal battle, a team clash, or a world-level threat, the film aims to deliver iconic set pieces while keeping the heart of the story grounded in the hero’s journey."
  )


def get_or_create_director_id(cur, name: str) -> int:
  cur.execute("SELECT director_id FROM directors WHERE director_name=%s", (name,))
  row = cur.fetchone()
  if row:
    return int(row[0])
  cur.execute("INSERT INTO directors (director_name) VALUES (%s)", (name,))
  return int(cur.lastrowid)


def get_or_create_genre_id(cur, name: str) -> int:
  cur.execute("SELECT genre_id FROM genres WHERE genre_name=%s", (name,))
  row = cur.fetchone()
  if row:
    return int(row[0])
  cur.execute("INSERT INTO genres (genre_name) VALUES (%s)", (name,))
  return int(cur.lastrowid)


def link_movie_genre(cur, movie_id: int, genre_id: int):
  cur.execute(
    "SELECT 1 FROM movie_genres WHERE movie_id=%s AND genre_id=%s LIMIT 1",
    (movie_id, genre_id),
  )
  if cur.fetchone():
    return
  cur.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_id))


def upsert_movie(cur, title: str, year: int, duration: int):
  director_id = get_or_create_director_id(cur, "Marvel Studios")
  cur.execute("SELECT movie_id FROM movies WHERE title=%s AND release_year=%s", (title, year))
  row = cur.fetchone()
  popularity = 90 + (year % 10)  # helps trending sorting

  if row:
    movie_id = int(row[0])
    cur.execute(
      """
      UPDATE movies
      SET description=%s,
          full_description=%s,
          duration=%s,
          language=%s,
          director_id=%s,
          country=%s,
          popularity=%s,
          is_oscar_winner=%s
      WHERE movie_id=%s
      """,
      (
        short_desc(title),
        long_desc(title, year),
        duration,
        "English",
        director_id,
        "United States",
        popularity,
        0,
        movie_id,
      ),
    )
    return movie_id

  cur.execute(
    """
    INSERT INTO movies
      (title, description, full_description, release_year, duration, language, director_id, country, popularity, is_oscar_winner)
    VALUES
      (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
      title,
      short_desc(title),
      long_desc(title, year),
      year,
      duration,
      "English",
      director_id,
      "United States",
      popularity,
      0,
    ),
  )
  return int(cur.lastrowid)


def main():
  conn = m.connect(host="localhost", user="root", password="root", database="movie_recommendation")
  cur = conn.cursor()
  try:
    count = 0
    for title, year, duration, genres in MARVEL_MOVIES:
      movie_id = upsert_movie(cur, title, year, duration)
      for g in genres:
        gid = get_or_create_genre_id(cur, g)
        link_movie_genre(cur, movie_id, gid)
      count += 1
    conn.commit()
    print(f"Seeded/updated {count} Marvel movies.")
  finally:
    cur.close()
    conn.close()


if __name__ == "__main__":
  main()


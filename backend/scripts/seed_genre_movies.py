import mysql.connector as m


MOVIES_BY_GENRE = {
  "Action": [
    ("John Wick", 2014, "English", 101, "United States"),
    ("Mad Max: Fury Road", 2015, "English", 120, "Australia"),
    ("The Dark Knight", 2008, "English", 152, "United States"),
    ("Gladiator", 2000, "English", 155, "United States"),
    ("Extraction", 2020, "English", 116, "United States"),
  ],
  "Comedy": [
    ("The Hangover", 2009, "English", 100, "United States"),
    ("Superbad", 2007, "English", 113, "United States"),
    ("3 Idiots", 2009, "Hindi", 170, "India"),
    ("Jumanji: Welcome to the Jungle", 2017, "English", 119, "United States"),
    ("Mr. Bean’s Holiday", 2007, "English", 90, "United Kingdom"),
  ],
  "Romance": [
    ("Titanic", 1997, "English", 195, "United States"),
    ("La La Land", 2016, "English", 128, "United States"),
    ("The Notebook", 2004, "English", 123, "United States"),
    ("Before Sunrise", 1995, "English", 101, "United States"),
    ("Dilwale Dulhania Le Jayenge", 1995, "Hindi", 189, "India"),
  ],
  "Horror": [
    ("The Conjuring", 2013, "English", 112, "United States"),
    ("Insidious", 2010, "English", 103, "United States"),
    ("The Nun", 2018, "English", 96, "United States"),
    ("Hereditary", 2018, "English", 127, "United States"),
    ("It", 2017, "English", 135, "United States"),
  ],
  "Thriller": [
    ("Inception", 2010, "English", 148, "United States"),
    ("Se7en", 1995, "English", 127, "United States"),
    ("Gone Girl", 2014, "English", 149, "United States"),
    ("Shutter Island", 2010, "English", 138, "United States"),
    ("Prisoners", 2013, "English", 153, "United States"),
  ],
  "Sci-Fi": [
    ("Interstellar", 2014, "English", 169, "United States"),
    ("Avatar", 2009, "English", 162, "United States"),
    ("The Matrix", 1999, "English", 136, "United States"),
    ("Blade Runner 2049", 2017, "English", 164, "United States"),
    ("Arrival", 2016, "English", 116, "United States"),
  ],
  "Drama": [
    ("Forrest Gump", 1994, "English", 142, "United States"),
    ("The Shawshank Redemption", 1994, "English", 142, "United States"),
    ("Fight Club", 1999, "English", 139, "United States"),
    ("Whiplash", 2014, "English", 106, "United States"),
    ("A Beautiful Mind", 2001, "English", 135, "United States"),
  ],
  "Family / Animation": [
    ("Toy Story", 1995, "English", 81, "United States"),
    ("Frozen", 2013, "English", 102, "United States"),
    ("The Lion King", 1994, "English", 88, "United States"),
    ("Coco", 2017, "English", 105, "United States"),
    ("Finding Nemo", 2003, "English", 100, "United States"),
  ],
  "Indian": [
    ("RRR", 2022, "Telugu", 182, "India"),
    ("KGF Chapter 2", 2022, "Kannada", 168, "India"),
    ("Baahubali: The Beginning", 2015, "Telugu", 159, "India"),
    ("Drishyam", 2015, "Hindi", 163, "India"),
    ("Jawan", 2023, "Hindi", 169, "India"),
  ],
}


OSCAR_WINNERS = {
  "The Dark Knight": 0,
  "Gladiator": 1,
  "Forrest Gump": 1,
  "The Shawshank Redemption": 0,
  "Whiplash": 0,
  "A Beautiful Mind": 1,
  "Titanic": 1,
  "Coco": 1,
  "The Lion King": 1,
  "La La Land": 1,
}


def poster_for(title: str) -> str:
  # Deterministic placeholder posters (no API keys needed)
  return f"https://picsum.photos/seed/{title.replace(' ', '%20')}/600/900"


def short_desc(title: str, genre: str) -> str:
  return f"{title} is a {genre.lower()} movie."


def long_desc(title: str, genre: str, year: int) -> str:
  return (
    f"{title} ({year}) is a {genre.lower()} story designed to pull you in quickly and keep the stakes rising. "
    "It blends memorable characters with a clear central goal, building tension through setbacks, twists, and emotional choices.\n\n"
    "As the plot escalates, the film leans into atmosphere and momentum—balancing spectacle with moments that reveal what each character stands to lose. "
    "By the end, it aims to leave you satisfied while still thinking about the journey and the cost of every decision."
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


def upsert_movie(cur, title: str, year: int, language: str, duration: int, country: str, genre: str) -> int:
  director_id = get_or_create_director_id(cur, "Unknown")
  poster_url = poster_for(title)
  popularity = 70 + (year % 30)  # simple seed so sorting works
  is_oscar_winner = 1 if OSCAR_WINNERS.get(title, 0) else 0

  cur.execute("SELECT movie_id FROM movies WHERE title=%s AND release_year=%s", (title, year))
  row = cur.fetchone()
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
          poster_url=%s,
          popularity=%s,
          is_oscar_winner=%s,
          country=%s
      WHERE movie_id=%s
      """,
      (
        short_desc(title, genre),
        long_desc(title, genre, year),
        duration,
        language,
        director_id,
        poster_url,
        popularity,
        is_oscar_winner,
        country,
        movie_id,
      ),
    )
    return movie_id

  cur.execute(
    """
    INSERT INTO movies
      (title, description, full_description, release_year, duration, language, director_id, poster_url, popularity, is_oscar_winner, country)
    VALUES
      (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
    (
      title,
      short_desc(title, genre),
      long_desc(title, genre, year),
      year,
      duration,
      language,
      director_id,
      poster_url,
      popularity,
      is_oscar_winner,
      country,
    ),
  )
  return int(cur.lastrowid)


def link_movie_genre(cur, movie_id: int, genre_id: int):
  cur.execute("SELECT 1 FROM movie_genres WHERE movie_id=%s AND genre_id=%s LIMIT 1", (movie_id, genre_id))
  if cur.fetchone():
    return
  cur.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_id))


def main():
  conn = m.connect(host="localhost", user="root", password="root", database="movie_recommendation")
  cur = conn.cursor()
  try:
    inserted = 0
    for genre, movies in MOVIES_BY_GENRE.items():
      genre_id = get_or_create_genre_id(cur, genre)
      for (title, year, language, duration, country) in movies:
        movie_id = upsert_movie(cur, title, year, language, duration, country, genre)
        link_movie_genre(cur, movie_id, genre_id)
        inserted += 1

    conn.commit()
    print(f"Seeded/updated {inserted} movie entries (with genres).")
  finally:
    cur.close()
    conn.close()


if __name__ == "__main__":
  main()


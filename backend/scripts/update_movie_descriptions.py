import mysql.connector as m


def main():
  updates = {
    "Inception": (
      "Dom Cobb is a skilled thief who steals secrets from deep within the subconscious during shared dreaming. "
      "When a powerful client offers him a chance to clear his past, the job comes with an impossible twist: "
      "instead of taking an idea, Cobb must plant one—an act known as inception.\n\n"
      "To pull it off, Cobb assembles a specialist team and descends through layered dream worlds where time bends "
      "and reality fractures. As the mission grows more dangerous, the line between memory and deception blurs, "
      "forcing Cobb to confront the guilt and loss that threaten to collapse the entire operation."
    ),
    "Interstellar": (
      "With Earth facing ecological collapse, a former pilot is drawn into a secret mission to find a new home for humanity. "
      "Guided by clues from an unexplained gravitational phenomenon, a crew travels through a wormhole to distant star systems "
      "where the rules of time and physics turn survival into a brutal equation.\n\n"
      "As the search for a habitable world intensifies, the journey becomes both a scientific gamble and an emotional test—"
      "especially as time dilation stretches minutes into years for those left behind. Balancing sacrifice, hope, and family, "
      "the mission asks what we’re willing to risk to save the future."
    ),
    "Titanic": (
      "Aboard the grand RMS Titanic, a young artist and a wealthy passenger meet by chance and form a connection that defies "
      "the rigid expectations of class and society. Their brief romance unfolds against the backdrop of luxury, mounting tension, "
      "and the ship’s fateful voyage across the Atlantic.\n\n"
      "When disaster strikes, the story shifts from enchantment to survival as chaos erupts and every decision carries a cost. "
      "Through courage, heartbreak, and moments of human kindness, the film captures both an intimate love story and the scale "
      "of a historic tragedy—reminding us how fragile life can be in the face of the unimaginable."
    ),
  }

  conn = m.connect(
    host="localhost",
    user="root",
    password="root",
    database="movie_recommendation",
  )
  cur = conn.cursor()
  try:
    for title, full in updates.items():
      cur.execute(
        "UPDATE movies SET full_description = %s WHERE title = %s",
        (full, title),
      )

    conn.commit()
    cur.execute("SELECT movie_id, title, LENGTH(full_description) FROM movies ORDER BY movie_id")
    for row in cur.fetchall():
      print(row)
  finally:
    cur.close()
    conn.close()


if __name__ == "__main__":
  main()


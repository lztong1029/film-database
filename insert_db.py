import csv

import pandas as pd
import mysql.connector
import random
from datetime import datetime, timedelta


# =========================================
# DB Connection
# =========================================
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",    # TODO: modify password
        database="filmdb"
    )

# =========================================
# Helpers
# =========================================
def random_datetime(start_year=2019, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return start + timedelta(days=random.randrange((end - start).days))


AWARD_LIST = [
    "Academy Award Best Picture", "Academy Award Best Director",
    "Golden Globe Best Drama", "Golden Globe Best Comedy",
    "BAFTA Best Film", "Cannes Palme d'Or",
    "Berlin Golden Bear", "Venice Golden Lion"
]

DIRECTING_STYLES = [
    "Realism",
    "Surrealism",
    "Documentary-style",
    "Experimental",
    "Character-driven",
    "Action-heavy",
    "Fantasy-oriented",
    "Minimalist",
]

WRITING_STYLES = [
    "Dialogue-focused",
    "Non-linear narrative",
    "Character-driven writing",
    "High-concept storytelling",
    "Comedy writing",
    "Dark drama",
    "Thriller style",
]

# =========================================
# STEP 1: Insert Reviews (Kaggle)
# =========================================
def insert_reviews():
    df = pd.read_csv(
        "filtered_data/imdb_reviews.csv",
        encoding="utf-8-sig",
        header=None,
        names=["review", "sentiment"]
    )
    df["review"] = df["review"].astype(str).str.replace("<br />", " ", regex=False)
    df = df.sample(5000).reset_index(drop=True)

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT userId FROM User")
    user_ids = [x[0] for x in cursor.fetchall()]

    cursor.execute("SELECT movieId FROM Movies")
    movie_ids = [x[0] for x in cursor.fetchall()]

    if not user_ids or not movie_ids:
        print("No users or movies — cannot insert reviews.")
        return

    sql = """
        INSERT INTO Review (userId, movieId, post_time, content, rating)
        VALUES (%s, %s, %s, %s, %s)
    """

    count = 0
    for _, row in df.iterrows():
        cursor.execute(sql, (
            random.choice(user_ids),
            random.choice(movie_ids),
            random_datetime(),
            row["review"],
            random.randint(1, 10)
        ))
        count += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted {count} reviews.")

def open_cursor():
    conn = get_conn()
    cursor = conn.cursor()
    return conn, cursor

def close_cursor(conn, cursor, commit=True):
    if commit:
        conn.commit()
    cursor.close()
    conn.close()

def insert_from_tsv(table_name: str, tsv_path: str):
    conn, cursor = open_cursor()
    with open(tsv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        columns_list = reader.fieldnames
        columns = ", ".join(columns_list)
        values = ", ".join("%s" for _ in columns_list)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        rows = []
        for row in reader:
            rows.append([row[col] if row[col] != r"\N" else None for col in columns_list])
        cursor.executemany(sql, rows)
        conn.commit()
    cursor.close()
    conn.close()



# =========================================
# STEP 2: Insert Movies
# =========================================
def insert_movies():
    conn, cursor = open_cursor()

    with open("filtered_data/movies.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        reader: csv.DictReader
        sql = """
                INSERT INTO Movies (
                    movieId,
                    primaryTitle,
                    originalTitle,
                    titleType,
                    startYear,
                    runtimeMinutes,
                    releaseYear
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        rows = []
        for row in reader:
            movie_id = row.get("tconst")
            primary_title = row.get("primaryTitle")
            original_title = row.get("originalTitle") or primary_title
            title_type = row.get("titleType")
            start_year = int(float(row.get("startYear")))
            runtime_minutes = 120 if row.get("runtimeMinutes") == '' else int(float(row.get("runtimeMinutes")))
            release_year = start_year
            rows.append((
                movie_id,
                primary_title,
                original_title,
                title_type,
                start_year,
                runtime_minutes,
                release_year,
            ))
        cursor.executemany(sql, rows)
        conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(rows)} movies.")


# =========================================
# STEP 3: Insert People
# =========================================
def insert_people():
    conn, cursor = open_cursor()
    cursor.execute("SELECT studioId FROM Studio")
    studio_ids = [x[0] for x in cursor.fetchall()]
    with open("filtered_data/people.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        reader: csv.DictReader
        sql = """
               INSERT INTO People (
                   pId,
                   primaryName,
                   birthYear,
                   deathYear,
                   primaryProfession,
                   currentStudioId
               ) VALUES (%s, %s, %s, %s, %s, %s)
           """
        rows = []
        for row in reader:
            p_id = row.get("nconst")
            primary_name = row.get("primaryName")
            birth_year = None if row.get("birthYear") == '' else int(float(row.get("birthYear")))
            death_year = None if row.get("deathYear") == '' else int(float(row.get("deathYear")))
            primary_profession = row.get("primaryProfession")
            current_studio_id = random.sample(studio_ids, 1)[0]
            rows.append((
                p_id,
                primary_name,
                birth_year,
                death_year,
                primary_profession,
                current_studio_id,
            ))
        cursor.executemany(sql, rows)
        conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(rows)} people.")


# =========================================
# STEP 4: Insert Actor / Director / Writer / Role Relations
# =========================================
def insert_roles():
    conn, cursor = open_cursor()
    with open("filtered_data/principals.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        reader: csv.DictReader
        actors = set()
        directors = set()
        writers = set()
        for row in reader:
            movie_id = row.get("tconst")
            person_id = row.get("nconst")
            category = row.get("category")
            if category in ("actor", "actress"):
                if person_id not in actors:
                    cursor.execute(
                    "INSERT INTO Actor (actorId, number_of_fans) VALUES (%s, %s)",
                    (person_id, random.randint(0, 3000))
                    )
                    actors.add(person_id)
                cursor.execute(
                    "INSERT IGNORE INTO Acts_In (movieId, actorId) VALUES (%s, %s)",
                    (movie_id, person_id)
                )
            elif category == "director":
                if person_id not in directors:
                    cursor.execute(
                        "INSERT INTO Director (directorId, directing_style, best_known_movieId) "
                        "VALUES (%s, %s, %s)",
                        (person_id, random.choice(DIRECTING_STYLES), movie_id)
                    )
                    directors.add(person_id)
                cursor.execute(
                    "INSERT INTO Directs (movieId, directorId) VALUES (%s, %s)",
                    (movie_id, person_id)
                )
            elif category == "writer":
                if person_id not in writers:
                    cursor.execute(
                        "INSERT INTO Writer (writerId, writing_style, best_known_movieId) "
                        "VALUES (%s, %s, %s)",
                        (person_id, random.choice(WRITING_STYLES), movie_id)
                    )
                    writers.add(person_id)
                cursor.execute(
                    "INSERT INTO Writes_Script_For (movieId, writerId) VALUES (%s, %s)",
                    (movie_id, person_id)
                )
    close_cursor(conn, cursor)


# =========================================
# STEP 5: Insert Genres & Has_Genre
# =========================================
def insert_genres():
    conn, cursor = open_cursor()
    genres = set()
    with open("filtered_data/movies.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        reader: csv.DictReader
        for row in reader:
            genre = None if row.get("genres") == '' else row.get("genres").split(",")[0].strip()
            if genre is None:
                continue
            if genre not in genres:
                cursor.execute(
                    "INSERT INTO Genre (name) "
                    "VALUES (%s)",
                    (genre,)
                )
                genres.add(genre)
            cursor.execute(
                "SELECT genreId FROM Genre WHERE name = %s",
                (genre,)
            )
            result = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO Has_Genre (movieId, genreId) "
                "VALUES (%s, %s)",
                (row.get("tconst"), result)
            )
        close_cursor(conn, cursor)

# =========================================
# STEP 6: Insert Studios (synthetic using STUDIO_LIST)
# =========================================
def insert_studios():
    insert_from_tsv("Studio", "filtered_data/studios.tsv")
    conn, cursor = open_cursor()
    with open("filtered_data/movie_ids.txt", "r", encoding="utf-8") as f:
        movie_ids = [line.strip() for line in f if line.strip()]
    sql = f"INSERT INTO Produced_By (movieId, studioId) VALUES (%s, %s)"
    rows = []
    for mid in movie_ids:
        sid = random.randint(1, 10)
        rows.append((mid, sid))
    cursor.executemany(sql, rows)
    close_cursor(conn, cursor)

# =========================================
# STEP 7: Insert Awards (synthetic using AWARD_LIST)
# =========================================
def insert_awards():
    conn, cursor = open_cursor()
    sql = "INSERT INTO Award (awardName) VALUES (%s)"
    rows = [(name,) for name in AWARD_LIST]
    cursor.executemany(sql, rows)
    conn.commit()
    with open("filtered_data/movies.tsv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        reader: csv.DictReader
        win_awards = []
        for row in reader:
            year = None if row.get("startYear") == '' else int(float(row.get("startYear")))
            if year is None or year > 2025 or random.random() < 0.75:
                continue
            win_awards.append((row.get("tconst"), random.randint(1, len(AWARD_LIST)), random.randint(year, 2025)))
    win_award_sql = "INSERT INTO Wins_Award (movieId, awardId, year) VALUES (%s, %s, %s)"
    cursor.executemany(win_award_sql, win_awards)
    close_cursor(conn, cursor)

def insert_users():
    import csv
    conn, cursor = open_cursor()
    with open("filtered_data/users.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [(row[0],) for row in reader if row]
    cursor.executemany(
        "INSERT INTO User (userName) VALUES (%s)",
        rows
    )
    close_cursor(conn, cursor)


# =========================================
# STEP 8: Insert Favorites (synthetic)
# =========================================
def insert_favorites():
    conn, cursor = open_cursor()
    cursor.execute("SELECT userId FROM User")
    user_ids = [x[0] for x in cursor.fetchall()]
    cursor.execute("SELECT movieId FROM Movies")
    movie_ids = [x[0] for x in cursor.fetchall()]
    sql = """
        INSERT INTO Favorites (userId, movieId)
        VALUES (%s, %s)
    """
    rows = []
    for uid in user_ids:
        fav_count = random.randint(5, 30)
        fav_movies = random.sample(movie_ids, fav_count)
        for mid in fav_movies:
            rows.append((uid, mid))
    cursor.executemany(sql, rows)
    close_cursor(conn, cursor)


# =========================================
# MAIN
# =========================================
if __name__ == "__main__":
    print("Starting data insertion...")

    # ---------- RUN ONLY ONCE ----------
    print("Inserting movies...")
    insert_movies()
    print("Inserting studios...")
    insert_studios()
    print("Inserting people...")
    insert_people()
    print("Inserting roles...")
    insert_roles()
    print("Inserting genres...")
    insert_genres()
    print("Inserting awards...")
    insert_awards()
    print("Inserting users...")
    insert_users()
    print("Inserting reviews...")
    insert_reviews()
    print("Inserting favorites...")
    insert_favorites()
    print("Data insertion completed.")
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


STUDIO_LIST = [
    "Warner Bros", "Universal Pictures", "Paramount Pictures",
    "20th Century Studios", "Columbia Pictures", "Metro-Goldwyn-Mayer",
    "Lionsgate", "A24", "Focus Features", "Sony Pictures Animation"
]

AWARD_LIST = [
    "Academy Award Best Picture", "Academy Award Best Director",
    "Golden Globe Best Drama", "Golden Globe Best Comedy",
    "BAFTA Best Film", "Cannes Palme d'Or",
    "Berlin Golden Bear", "Venice Golden Lion"
]


# =========================================
# STEP 1: Insert Reviews (Kaggle)
# =========================================
def insert_reviews():
    df = pd.read_csv(
        "filtered_data/imdb_reviews.csv",
        encoding="utf-8"
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


# =========================================
# STEP 2: Insert Movies
# =========================================
def insert_movies():
    # TODO: load filtered_data/movies.tsv and insert into Movies table
    pass


# =========================================
# STEP 3: Insert People
# =========================================
def insert_people():
    # TODO: load filtered_data/people.tsv and insert into People table
    pass


# =========================================
# STEP 4: Insert Actor / Director / Writer / Role Relations
# =========================================
def insert_roles():
    # TODO: parse principals.tsv and insert into Actor/Director/Writer + role tables
    pass


# =========================================
# STEP 5: Insert Genres & Has_Genre
# =========================================
def insert_genres():
    # TODO: extract genres from movies.tsv, insert Genre + Has_Genre
    pass


# =========================================
# STEP 6: Insert Studios (synthetic using STUDIO_LIST)
# =========================================
def insert_studios():
    # TODO: iterate STUDIO_LIST and insert into Studio table
    pass


# =========================================
# STEP 7: Insert Awards (synthetic using AWARD_LIST)
# =========================================
def insert_awards():
    # TODO: iterate AWARD_LIST and insert into Award + assign some to movies
    pass


# =========================================
# STEP 8: Insert Favorites (synthetic)
# =========================================
def insert_favorites():
    # TODO: randomly assign userId–movieId pairs into Favorites table
    pass


# =========================================
# MAIN
# =========================================
if __name__ == "__main__":
    print("Starting data insertion...")

    # ---------- RUN ONLY ONCE ----------
    # insert_movies()
    # insert_people()
    # insert_roles()
    # insert_genres()
    # insert_studios()
    # insert_awards()
    # insert_reviews()
    # insert_favorites()

    print("Data insertion completed.")
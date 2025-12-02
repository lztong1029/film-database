import os
import pandas as pd

# =========================
# CONFIG
# =========================
DOWNLOAD_DIR = os.path.expanduser("~/Downloads")

BASICS_PATH = os.path.join(DOWNLOAD_DIR, "title.basics.tsv")
PRINCIPALS_PATH = os.path.join(DOWNLOAD_DIR, "title.principals.tsv")
CREW_PATH = os.path.join(DOWNLOAD_DIR, "title.crew.tsv")
NAME_PATH = os.path.join(DOWNLOAD_DIR, "name.basics.tsv")

OUTPUT_DIR = "filtered_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

MOVIE_LIMIT = 50000
YEAR_THRESHOLD = 2000     # filter movies after year 2000


# =========================
# STEP 1 — Filter Movies (title.basics)
# =========================
def filter_movies():
    print(" Filtering movies (title.basics.tsv)...")

    basics = pd.read_csv(
        BASICS_PATH,
        sep="\t",
        na_values="\\N",
        low_memory=False,
        dtype=str
    )

    # keep only movies or tvSeries maybe; up to you
    basics = basics[basics["titleType"].isin(["movie", "tvSeries", "short", "video"])]

    # keep only recent movies
    basics["startYear"] = pd.to_numeric(basics["startYear"], errors="coerce")
    recent = basics[basics["startYear"] >= YEAR_THRESHOLD]

    sample = recent.head(MOVIE_LIMIT)  # take first N of recent

    movie_ids = sample["tconst"].tolist()

    sample.to_csv(f"{OUTPUT_DIR}/movies.tsv", sep="\t", index=False)
    with open(f"{OUTPUT_DIR}/movie_ids.txt", "w") as f:
        for mid in movie_ids:
            f.write(mid + "\n")

    print(f"✅ Saved {len(sample)} movies to filtered_data/movies.tsv")
    return set(movie_ids)


# =========================
# STEP 2 — Filter Principals (title.principals)
# =========================
def filter_principals(movie_ids):
    print(" Filtering principals (title.principals.tsv)...")

    chunksize = 200000
    output_path = f"{OUTPUT_DIR}/principals.tsv"
    header_written = False

    for chunk in pd.read_csv(PRINCIPALS_PATH, sep="\t", chunksize=chunksize, na_values="\\N", dtype=str):
        filtered = chunk[chunk["tconst"].isin(movie_ids)]

        if not filtered.empty:
            filtered.to_csv(output_path, sep="\t", index=False, mode="a", header=not header_written)
            header_written = True

    print("✅ Saved principals → filtered_data/principals.tsv")


# =========================
# STEP 3 — Filter Crew (title.crew)
# =========================
def filter_crew(movie_ids):
    print(" Filtering crew (title.crew.tsv)...")

    crew = pd.read_csv(CREW_PATH, sep="\t", na_values="\\N", dtype=str)
    filtered = crew[crew["tconst"].isin(movie_ids)]
    filtered.to_csv(f"{OUTPUT_DIR}/crew.tsv", sep="\t", index=False)

    print("✅ Saved crew → filtered_data/crew.tsv")


# =========================
# STEP 4 — Filter People (name.basics) based on nconst
# =========================
def filter_people():
    print(" Extracting people IDs from principals.tsv...")

    principals = pd.read_csv(f"{OUTPUT_DIR}/principals.tsv", sep="\t", dtype=str)
    people_ids = set(principals["nconst"].dropna().unique())

    with open(f"{OUTPUT_DIR}/people_ids.txt", "w") as f:
        for pid in people_ids:
            f.write(pid + "\n")

    print(f"Found {len(people_ids)} unique people")

    print(" Filtering people (name.basics.tsv)...")
    chunksize = 200000
    output_path = f"{OUTPUT_DIR}/people.tsv"
    header_written = False

    for chunk in pd.read_csv(NAME_PATH, sep="\t", chunksize=chunksize, na_values="\\N", dtype=str):
        filtered = chunk[chunk["nconst"].isin(people_ids)]

        if not filtered.empty:
            filtered.to_csv(output_path, sep="\t", index=False, mode="a", header=not header_written)
            header_written = True

    print("✅ Saved people → filtered_data/people.tsv")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("🚀 Starting IMDb Filter Pipeline...")

    movie_ids = filter_movies()
    filter_principals(movie_ids)
    filter_crew(movie_ids)
    filter_ratings(movie_ids)
    filter_people()

    print("\n🎉 Done! All filtered data saved under filtered_data/")
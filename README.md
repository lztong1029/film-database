# film-database

A database-centric project for storing, querying, and interacting with IMDb movie data and synthetic reviews, featuring a Python-powered GUI.

---

## Table of Contents

1. [Project Workflow](#project-workflow)
2. [Team Responsibilities](#team-responsibilities)
3. [Completed Features](#completed)
4. [Next Steps](#next-steps)
5. [Development & Run Order](#development-run-order)

---

## 1. Project Workflow

**Overall flow:**
```
Create DB ("filmdb") → Prepare/filter data → `filtered_data/` → Insert into DB → Write queries → Build GUI → Run `app.py`
```

**Main Phases:**

| Phase      | Key Files                  | Description                                                        |
|------------|----------------------------|--------------------------------------------------------------------|
| Database   | `schema.sql`, `init_db.py` | Create all SQL tables.                                             |
| Data Insert| `insert_data.py`           | Insert IMDb and synthetic data into DB.                            |
| Queries    | `queries.py`               | Python functions wrapping SQL for GUI calls.                       |
| GUI        | `gui.py`, `app.py`         | User interface for searches, inserts, and result display.          |

---

## 2. Team Responsibilities

| Area            | Files/Functions                | Assigned To                                                                                           | Status      | Details/Notes                      |
|-----------------|-------------------------------|-------------------------------------------------------------------------------------------------------|-------------|------------------------------------|
| Database Schema | `schema.sql`, `init_db.py`    | Juno                                                                                                  | Done        |                                    |
| Data Insertion  | `insert_data.py`              | Juno: Reviews Insert + Studio/Awards<br>(others: see below)<br/>Yilin: Completed remaining insertions | Done        | See [Next Steps](#next-steps)      |
| Query Layer     | `queries.py`                  | *Unassigned*                                                                                          | Todo        |                                    |
| GUI             | `gui.py`, `app.py`            | Zhenyan                                                                                               | in Progress |                                    |

**Data Insertion (details):**
  - **Juno:** Reviews insert, studio and award lists (DONE)
  - **Yilin:** Movies insert, People insert, Roles insert, Genres insert, Studios insert, Users insert, Awards insert, Favorites insert(DONE)

---

## 3. Completed

### Data Filtering Pipeline (`filter_data.py`)

- **Purpose:** Process and reduce IMDb raw data into cleaned, subsetted files in `filtered_data/`.
- **Output Files:**
  - `filtered_data/movies.tsv`
  - `filtered_data/people.tsv`
  - `filtered_data/principals.tsv`
  - `filtered_data/crew.tsv`
  - `filtered_data/movie_ids.txt`
  - `filtered_data/people_ids.txt`
- **Logic:**
  1. Select movies from year **≥ 2000** (`title.basics.tsv`)  
  2. Keep the first 50,000 recent titles  
  3. Filter related tables via `tconst`  
  4. Extract and filter all required `nconst`s for consistency

### Review Processing & Insertion

- **Source:** `filtered_data/imdb_reviews.csv` (Kaggle 50k IMDB reviews)
- **Process:**
  - Sample 5,000 reviews for speed
  - Clean all HTML tags (`<br />`)
  - Randomize:
    - `userId`
    - `movieId`
    - `rating` (1–10)
    - `post_time` (2019–2024)
- **Insertion:** Fully implemented in `insert_data.py → insert_reviews()`

### Studio & Award Dictionaries

- Ready-made lists in `insert_data.py`:
  - `STUDIO_LIST`: Popular studios
  - `AWARD_LIST`: Major award names
- **Usage:** Populate `Studio`, `Award`, `Produced_By`, and `Wins_Award` tables directly.

---

## 4. Next Steps

### Data Insertion: Complete Pending Functions

Implement remaining insert functions in `insert_data.py`, including:
- `insert_movies()` (from `movies.tsv`)
- `insert_people()` (from `people.tsv`)
- `insert_roles()` (from `principals.tsv`; link actors, directors, writers)
- `insert_genres()` (extract & insert genres, manage `Has_Genre`)
- `insert_studios()` (use `STUDIO_LIST`)
- `insert_awards()` (use `AWARD_LIST`, assign to movies)
- `insert_favorites()` (random user–movie pairs)

### Query Functions (`queries.py`)
- Each function: Accepts user input, runs SQL, returns rows for GUI.
- Examples to implement:
  - Find movies by year
  - List actors in a movie
  - Get top-rated movies
  - Insert a user or a review

### GUI Implementation

- Display available queries
- Show input fields as necessary
- Link buttons to query functions
- Display results in a table
- Support inserting a new user or review

---

## 5. Development Run Order

To set up and run the project, follow this sequence:

1. **Create DB schema:**  
   `python init_db.py`  
2. **(Already done) Prepare filtered data:**  
   `python filter_data.py`  
3. **Complete all "insert" functions** in `insert_data.py`
4. **Insert all data:**  
   `python insert_data.py`
5. **Write query functions:**  
   Edit `queries.py`
6. **Build GUI:**  
   Edit `gui.py` and `app.py`
7. **Launch the application:**  
   ```
   python app.py
   ```

---

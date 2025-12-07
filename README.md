# Film Database - Global Film Database Explorer

A complete database application for exploring IMDb movie data with user reviews, featuring a Python GUI built with PySimpleGUI and MySQL backend.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation & Setup](#installation--setup)
5. [Usage](#usage)
6. [Database Schema](#database-schema)
7. [Queries](#queries)
8. [Project Structure](#project-structure)

---

## 1. Project Overview

This project implements a comprehensive film database system that allows users to:

- Browse and search movies by various criteria (genre, year, director, runtime, etc.)
- View detailed information about actors, directors, and writers
- Explore studio production data and award-winning films
- Read and write movie reviews
- Manage user favorite movies

The application uses a MySQL database backend with a Python GUI frontend, providing an intuitive interface for complex database queries.

---

## 2. Features

### Query Explorer

- **12 Pre-built Queries** covering common search scenarios:
  - Movies by genre and year
  - Cast and crew information
  - Studio analytics
  - Award-winning films
  - User reviews and favorites
  - Runtime-based searches
  - Birth year actor searches

### Review Management

- **Insert New Reviews** with automatic movie lookup by title
- User-friendly form with validation
- Real-time feedback on insertion success/failure

### Data Visualization

- Table view with sortable columns
- Color-coded status messages
- Clean, modern UI with PySimpleGUI

---

## 3. Technology Stack

- **Database:** MySQL 8.0+
- **Backend:** Python 3.8+
  - `mysql-connector-python` for database connectivity
  - Type hints for better code maintainability
- **Frontend:** PySimpleGUI for cross-platform GUI
- **Data Source:** IMDb datasets (movies from 2000+)

---

## 4. Installation & Setup

### Prerequisites

1. **MySQL Server** installed and running
2. **Python 3.8+** installed

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Database Connection

Edit `backend/db.py` with your MySQL credentials:

```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "filmdb"
```

### Step 3: Create Database and Load Data

```bash
# Initialize database schema
python init_db.py

# Load IMDb data into database
python insert_db.py
```

### Step 4: Test Database Connection

```bash
cd backend
python db.py
```

You should see:

```
✓ Successfully connected to MySQL Server
✓ Database: filmdb
✓ Tables: Movies, People, Actor, Director, ...
```

### Step 5: Test Queries

```bash
# From project root
python -m backend.queries
```

This verifies the module imports. Use the GUI to run the queries themselves.

---

## 5. Usage

### Launch the GUI

```bash
# From project root
python -m frontend.gui
```

### Query Explorer Tab

1. Select a query from the list (e.g., "Q1: Movies in Science Fiction genre after a year")
2. Enter parameters in the input fields
3. Click **Run Query**
4. View results in the table below

### Insert Review Tab

1. Enter **User ID** (valid IDs: 1-10)
2. Enter **Movie Title** (exact title, e.g., "Ten Lives")
3. Select **Rating** (1-10)
4. Write **Review Content**
5. Click **Submit Review**

The application will automatically:

- Look up the movie ID from the title
- Validate all inputs
- Insert the review into the database
- Display success/error messages

---

## 6. Database Schema

### Core Tables

| Table      | Description                             |
| ---------- | --------------------------------------- |
| `Movies`   | Film information (title, year, runtime) |
| `People`   | Actors, directors, writers              |
| `Actor`    | Actor-specific data                     |
| `Director` | Director-specific data                  |
| `Writer`   | Writer-specific data                    |
| `Genre`    | Film genres                             |
| `Studio`   | Production studios                      |
| `Award`    | Film awards                             |
| `User`     | System users                            |
| `Review`   | User movie reviews                      |

### Relationship Tables

| Table               | Relationship     |
| ------------------- | ---------------- |
| `Acts_In`           | Actor ↔ Movie    |
| `Directs`           | Director ↔ Movie |
| `Writes_Script_For` | Writer ↔ Movie   |
| `Has_Genre`         | Movie ↔ Genre    |
| `Produced_By`       | Movie ↔ Studio   |
| `Wins_Award`        | Movie ↔ Award    |
| `Favorites`         | User ↔ Movie     |

---

## 7. Queries

### Q1: Science Fiction Movies After Year

Lists all Sci-Fi movies released after a specified year.

**Parameters:** Year (e.g., 2010)

### Q2: Actors in a Movie

Shows all actors who starred in a specific movie.

**Parameters:** Movie Title (e.g., "Ten Lives")

### Q3: Reviews for a Movie

Displays all user reviews for a specific movie with ratings and timestamps.

**Parameters:** Movie Title (e.g., "Ten Lives")

### Q4: Movies by Director

Lists all movies directed by a specific director.

**Parameters:** Director Name (e.g., "Christopher Nolan")

### Q5: Average Rating by Studio

Calculates average user rating for all movies produced by a studio.

**Parameters:** Studio Name (e.g., "A24")

### Q6: Best Picture Award Winners

Finds all movies that won a "Best Picture" style award.

**Parameters:** Award Keyword (e.g., "Best Picture")

### Q7: Actors in Old Studios

Lists actors associated with studios founded before a given year.

**Parameters:** Cutoff Year (e.g., 1950)

### Q8: Writers for a Director

Shows all writers who wrote scripts for a specific director's movies.

**Parameters:** Director Name (e.g., "Christopher Nolan")

### Q9: User's Favorite Movies

Lists all movies marked as favorites by a specific user.

**Parameters:** Username (e.g., "smomery0")

### Q10: Top 10 Movies by Genre

Ranks the highest-rated movies in a specific genre.

**Parameters:** Genre Name (e.g., "Horror")

### Q11: Long Movies

Finds movies with runtime longer than a specified duration.

**Parameters:** Minimum Runtime in minutes (e.g., 180)

### Q12: Actors Born in Year

Lists all actors born in a specific year.

**Parameters:** Birth Year (e.g., 1980)

---

## 8. Project Structure

```
film-database/
├── backend/
│   ├── db.py                 # MySQL connection management
│   └── queries.py            # SQL query implementations
│
├── frontend/
│   └── gui.py                # PySimpleGUI application
│
├── filtered_data/            # Preprocessed data files
│   ├── movie_ids.txt
│   └── people_ids.txt
│
├── init_db.py                # Database schema creation
├── insert_db.py              # Data loading script
├── filter_data.py            # Data preprocessing script
└── README.md                 # This file
```

### Key Files

**Backend:**

- [backend/db.py](backend/db.py) - Database connection and query execution functions
- [backend/queries.py](backend/queries.py) - All 12 SQL queries + helper functions

**Frontend:**

- [frontend/gui.py](frontend/gui.py) - Complete GUI application with two tabs

**Setup Scripts:**

- [init_db.py](init_db.py) - Creates database schema
- [insert_db.py](insert_db.py) - Loads IMDb data into database
- [filter_data.py](filter_data.py) - Preprocesses raw IMDb data files

---

## Development Notes

### Design Decisions

1. **Two-Step Review Insertion:** Users enter movie titles instead of IDs. The application automatically looks up the movieId behind the scenes for better UX.

2. **Real Database Only:** The application requires a working MySQL connection. It will exit with an error message if the database is unavailable.

3. **Parameterized Queries:** All SQL queries use parameterized statements to prevent SQL injection attacks.

4. **Connection Pooling:** Each query opens and closes its own database connection to avoid connection timeout issues.

### Database Configuration

The database contains:

- **Movies:** Filtered to year 2000+ for relevance
- **Users:** 10 test users (IDs 1-10)
- **Reviews:** Synthetic review data for testing
- **Relationships:** Full relational mapping between all entities

---

## Troubleshooting

### "Failed to import queries module"

- Check that `backend/queries.py` exists
- Run from the project root using module invocation: `python -m frontend.gui` or `python -m backend.queries`
- If running a script directly, set PYTHONPATH to the project root: `PYTHONPATH=. python frontend/gui.py`


### "Error connecting to MySQL"

- Verify MySQL server is running
- Check credentials in `backend/db.py`
- Ensure database "filmdb" exists

### "No movie found with title"

- Check exact spelling of movie title
- Movie must exist in database (year 2000+)
- For multiple matches, try including year in title

### "Foreign key constraint fails"

- For reviews: Use valid User ID (1-10)
- For reviews: Movie must exist in database
- Check database referential integrity

---

## License

Educational project for MPCS 53001 Database Systems.

---

## Contributors

- Zhenyan Li - GUI Development & Queries Development 
- Juno - Database Schema & Data Pipeline
- Xiaoyu Zhang - GUI & DB Queries Development 
- Yilin Long - Database Schema & Data Pipeline
  

---

## Acknowledgments

- IMDb for movie datasets
- PySimpleGUI for the GUI framework
- MySQL for database management

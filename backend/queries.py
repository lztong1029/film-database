#!/usr/bin/env python3
"""
Query functions for the Film Database project.

Each function corresponds to one of the queries described in Step 1/Step 3
and is called from the GUI (frontend/gui.py).

All SELECT helpers return:
    rows, column_names

The GUI then takes (column_names, rows) 来显示表格。
"""

from typing import List, Tuple, Optional
from .db import run_select_query, run_insert_query


# ---------------------------------------------------------------------------
# Q1: Movies in Science Fiction genre after a given year
# ---------------------------------------------------------------------------

def query_Q1_scifi_after_year(min_year: int) -> Tuple[List[Tuple], List[str]]:
    """
    Q1: List all movies in the Science Fiction / Sci-Fi genre released after a given year.

    Args:
        min_year: only return movies with startYear >= min_year

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            m.movieId,
            m.primaryTitle,
            m.startYear,
            m.runtimeMinutes,
            g.name AS genre
        FROM Movies AS m
        JOIN Has_Genre AS hg ON m.movieId = hg.movieId
        JOIN Genre AS g ON hg.genreId = g.genreId
        WHERE
            m.startYear >= %s
            AND g.name IN ('Sci-Fi', 'Science Fiction')
        ORDER BY m.startYear ASC, m.primaryTitle ASC
        LIMIT 200
    """
    return run_select_query(sql, (min_year,))


# ---------------------------------------------------------------------------
# Q2: Actors who starred in a specific movie
# ---------------------------------------------------------------------------

def query_Q2_actors_in_movie(movie_title: str) -> Tuple[List[Tuple], List[str]]:
    """
    Q2: List all actors who starred in a specific movie (by title).

    Args:
        movie_title: the primaryTitle of the movie

    Returns:
        rows, column_names
    """
    sql = """
        SELECT DISTINCT
            p.pId        AS actorId,
            p.primaryName AS actorName
        FROM Movies AS m
        JOIN Acts_In AS ai    ON m.movieId = ai.movieId
        JOIN Actor   AS a     ON ai.actorId = a.actorId
        JOIN People  AS p     ON a.actorId = p.pId
        WHERE m.primaryTitle = %s
        ORDER BY p.primaryName ASC
    """
    return run_select_query(sql, (movie_title,))


# ---------------------------------------------------------------------------
# Q3: All reviews for a specific movie
# ---------------------------------------------------------------------------

def query_Q3_reviews_for_movie(movie_title: str) -> Tuple[List[Tuple], List[str]]:
    """
    Q3: Show all reviews for a specific movie (with username, rating, time, content).

    Args:
        movie_title: primaryTitle of the movie

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            m.primaryTitle AS movieTitle,
            u.userName     AS userName,
            r.rating       AS rating,
            r.post_time    AS postTime,
            r.content      AS reviewContent
        FROM Movies AS m
        JOIN Review AS r ON m.movieId = r.movieId
        JOIN User   AS u ON r.userId = u.userId
        WHERE m.primaryTitle = %s
        ORDER BY r.post_time DESC
    """
    return run_select_query(sql, (movie_title,))


# ---------------------------------------------------------------------------
# Q4: All movies directed by a specific director
# ---------------------------------------------------------------------------

def query_Q4_movies_by_director(director_name: str) -> Tuple[List[Tuple], List[str]]:
    """
    Q4: List all movies directed by a specific director.

    Args:
        director_name: director's primaryName

    Returns:
        rows, column_names
    """
    sql = """
          SELECT m.movieId,
                 m.primaryTitle,
                 m.startYear,
                 m.runtimeMinutes
          FROM People AS p
                   JOIN Director AS d ON p.pId = d.directorId
                   JOIN Directs AS di ON d.directorId = di.directorId
                   JOIN Movies AS m ON di.movieId = m.movieId
          WHERE p.primaryName = %s
          ORDER BY m.startYear, m.primaryTitle
          """
    return run_select_query(sql, (director_name,))


# ---------------------------------------------------------------------------
# Q5: Average rating for movies produced by a specific studio
# ---------------------------------------------------------------------------

def query_Q5_avg_rating_by_studio(studio_name: str) -> Tuple[List[Tuple], List[str]]:
    """
    Q5: Compute the average rating of all movies produced by a given studio.

    Args:
        studio_name: Studio.name (e.g., 'A24')

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            s.name AS studioName,
            AVG(r.rating) AS avgUserRating,
            COUNT(DISTINCT m.movieId) AS numMovies,
            COUNT(r.reviewId) AS numReviews
        FROM Studio      AS s
        JOIN Produced_By AS pb ON s.studioId = pb.studioId
        JOIN Movies      AS m  ON pb.movieId = m.movieId
        JOIN Review      AS r  ON m.movieId = r.movieId
        WHERE s.name = %s
        GROUP BY s.name
    """
    return run_select_query(sql, (studio_name,))


# ---------------------------------------------------------------------------
# Q10: Top 10 highest-rated movies in a genre
# ---------------------------------------------------------------------------

def query_Q10_top10_by_genre(genre_name: str) -> Tuple[List[Tuple], List[str]]:
    """
    Q10: Top 10 highest-rated movies in a genre (using user reviews).

    Args:
        genre_name: e.g., 'Horror', 'Comedy'

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            m.movieId,
            m.primaryTitle,
            m.startYear,
            g.name       AS genre,
            AVG(r.rating) AS avgRating,
            COUNT(r.reviewId) AS numReviews
        FROM Movies  AS m
        JOIN Has_Genre AS hg ON m.movieId = hg.movieId
        JOIN Genre   AS g    ON hg.genreId = g.genreId
        LEFT JOIN Review AS r ON m.movieId = r.movieId
        WHERE g.name = %s
        GROUP BY m.movieId, m.primaryTitle, m.startYear, g.name
        HAVING avgRating IS NOT NULL
        ORDER BY avgRating DESC, numReviews DESC
        LIMIT 10
    """
    return run_select_query(sql, (genre_name,))


# ---------------------------------------------------------------------------
# Q11: Movies with runtime longer than a threshold
# ---------------------------------------------------------------------------

def query_Q11_long_movies(min_runtime: int) -> Tuple[List[Tuple], List[str]]:
    """
    Q11: List all movies with runtime longer than min_runtime minutes.

    Args:
        min_runtime: minimum runtime in minutes (e.g., 180)

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            m.movieId,
            m.primaryTitle,
            m.startYear,
            m.runtimeMinutes
        FROM Movies AS m
        WHERE m.runtimeMinutes >= %s
        ORDER BY m.runtimeMinutes DESC, m.primaryTitle ASC
        LIMIT 200
    """
    return run_select_query(sql, (min_runtime,))


# ---------------------------------------------------------------------------
# Q12: Actors born in a specific year
# ---------------------------------------------------------------------------

def query_Q12_actors_born_in_year(birth_year: int) -> Tuple[List[Tuple], List[str]]:
    """
    Q12: List all actors (people with an Actor entry) who were born in a specific year.

    Args:
        birth_year: e.g., 1980

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            p.pId        AS actorId,
            p.primaryName AS actorName,
            p.birthYear,
            p.primaryProfession
        FROM People AS p
        JOIN Actor  AS a ON p.pId = a.actorId
        WHERE p.birthYear = %s
        ORDER BY p.primaryName ASC
    """
    return run_select_query(sql, (birth_year,))


# ---------------------------------------------------------------------------
# Q6: Movies that won a Best Picture award
# ---------------------------------------------------------------------------

def query_Q6_best_picture_movies(award_keyword: str = "Best Picture") -> Tuple[List[Tuple], List[str]]:
    """
    Q6: Find all movies that won a 'Best Picture' style award.

    Args:
        award_keyword: Keyword to match award name using LIKE (default: "Best Picture")

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            m.movieId,
            m.primaryTitle,
            m.releaseYear,
            a.awardName,
            w.year AS awardYear
        FROM Movies AS m
        JOIN Wins_Award AS w ON m.movieId = w.movieId
        JOIN Award AS a ON w.awardId = a.awardId
        WHERE a.awardName LIKE %s
        ORDER BY w.year DESC, m.primaryTitle ASC
        LIMIT 200
    """
    like_pattern = f"%{award_keyword}%"
    return run_select_query(sql, (like_pattern,))


# ---------------------------------------------------------------------------
# Q7: Actors associated with studios founded before a given year
# ---------------------------------------------------------------------------

def query_Q7_actors_in_pre1950_studios(cutoff_year: int = 1950) -> Tuple[List[Tuple], List[str]]:
    """
    Q7: List all actors who are associated with a studio founded before a given year.

    Args:
        cutoff_year: Only include studios with foundedYear < cutoff_year (default: 1950)

    Returns:
        rows, column_names
    """
    sql = """
        SELECT DISTINCT
            p.pId        AS actorId,
            p.primaryName,
            s.name       AS studioName,
            s.foundedYear
        FROM People AS p
        JOIN Actor  AS a ON p.pId = a.actorId
        JOIN Studio AS s ON p.currentStudioId = s.studioId
        WHERE s.foundedYear < %s
        ORDER BY s.foundedYear ASC, p.primaryName ASC
        LIMIT 500
    """
    return run_select_query(sql, (cutoff_year,))


# ---------------------------------------------------------------------------
# Q8: Writers who wrote for a specific director
# ---------------------------------------------------------------------------

def query_Q8_writers_for_director(director_name: str = "Martin Scorsese") -> Tuple[List[Tuple], List[str]]:
    """
    Q8: Find the names of all writers who wrote a movie directed by a given director.

    Args:
        director_name: Director's primary name (default: "Martin Scorsese")

    Returns:
        rows, column_names
    """
    sql = """
        SELECT DISTINCT
            pw.pId         AS writerId,
            pw.primaryName AS writerName,
            m.primaryTitle AS movieTitle
        FROM People AS pd
        JOIN Directs AS d ON d.directorId = pd.pId
        JOIN Movies AS m ON m.movieId = d.movieId
        JOIN Writes_Script_For AS wsf ON wsf.movieId = m.movieId
        JOIN People AS pw ON pw.pId = wsf.writerId
        WHERE pd.primaryName = %s
        ORDER BY pw.primaryName ASC, m.primaryTitle ASC
    """
    return run_select_query(sql, (director_name,))


# ---------------------------------------------------------------------------
# Q9: Favorite movies for a user
# ---------------------------------------------------------------------------

def query_Q9_favorite_movies_for_user(username: str) -> Tuple[List[Tuple], List[str]]:
    """
    Q9: List all movies that a given user has marked as favorite.

    Args:
        username: User.userName

    Returns:
        rows, column_names
    """
    sql = """
        SELECT
            m.movieId,
            m.primaryTitle,
            m.releaseYear
        FROM User AS u
        JOIN Favorites AS f ON u.userId = f.userId
        JOIN Movies    AS m ON f.movieId = m.movieId
        WHERE u.userName = %s
        ORDER BY m.primaryTitle ASC, m.releaseYear ASC
    """
    return run_select_query(sql, (username,))



# ---------------------------------------------------------------------------
# Helper: Find movieId by title
# ---------------------------------------------------------------------------

def find_movie_id_by_title(movie_title: str) -> Tuple[Optional[str], str]:
    """
    Find the movieId for a given movie title.

    Args:
        movie_title: The primaryTitle of the movie

    Returns:
        tuple: (movieId or None, message)
            - If exactly one match: (movieId, "")
            - If no matches: (None, "No movie found with that title")
            - If multiple matches: (None, "Multiple movies found with that title")
    """
    sql = """
        SELECT movieId, primaryTitle, startYear
        FROM Movies
        WHERE primaryTitle = %s
    """

    rows, headers = run_select_query(sql, (movie_title,))

    if len(rows) == 0:
        return None, f"No movie found with title '{movie_title}'"
    elif len(rows) == 1:
        return rows[0][0], ""  # Return the movieId
    else:
        # Multiple matches - show user which years are available
        years = [str(row[2]) for row in rows if row[2]]
        years_str = ", ".join(years) if years else "various years"
        return None, f"Multiple movies found with title '{movie_title}' ({years_str}). Please be more specific."


# ---------------------------------------------------------------------------
# Insert New Review (used by the "Insert New Review" tab)
# ---------------------------------------------------------------------------

def insert_review(
    user_id: int,
    movie_id: str,
    rating: int,
    content: str,
    post_time: str,
) -> Tuple[bool, str]:
    """
    Insert a new review into the Review table.

    The GUI expects (success: bool, message: str).

    Args:
        user_id: existing User.userId (integer)
        movie_id: existing Movies.movieId (IMDb ID string like 'tt0413354')
        rating: integer rating, typically 1–10
        content: review text
        post_time: a datetime string 'YYYY-MM-DD HH:MM:SS'

    Returns:
        (True, '...') on success
        (False, 'error message') on failure
    """
    # Basic validation (just to avoid totally crazy input)
    if rating < 1 or rating > 10:
        return False, "Rating must be between 1 and 10."

    sql = """
        INSERT INTO Review (userId, movieId, rating, content, post_time)
        VALUES (%s, %s, %s, %s, %s)
    """

    params = (user_id, movie_id, rating, content, post_time)

    try:
        affected = run_insert_query(sql, params)
        if affected == 1:
            return True, "Review inserted successfully."
        elif affected > 1:
            # extremely unlikely, but just in case
            return True, f"Inserted {affected} rows (unexpected)."
        else:
            return False, "No row inserted (check userId/movieId)."
    except Exception as e:
        return False, f"Database error: {e}"

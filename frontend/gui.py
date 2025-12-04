#!/usr/bin/env python3
"""
Global Film Database Explorer - GUI Interface
MPCS 53001 Database Final Project - Step 3

This GUI allows users to:
- Run analytical queries on movies, people, studios, and reviews
- Insert new movie reviews
- Browse query results in a table format
"""

import PySimpleGUI as sg
from datetime import datetime
import sys
import os

# Add backend directory to path for imports
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.append(backend_path)

# Import backend query functions
try:
    import queries as q
    print("✓ Successfully imported queries module")
except ImportError as e:
    print(f"✗ Failed to import queries module: {e}")
    print("  Please check that backend/queries.py exists and database is configured")
    sys.exit(1)


# ============================================================================
# DATABASE QUERY FUNCTIONS
# ============================================================================

def run_query(query_id, params):
    """
    Execute a query based on query_id and parameters using the real MySQL database.

    Args:
        query_id (str): Query identifier (Q1, Q2, etc.)
        params (dict): Query parameters

    Returns:
        tuple: (headers, rows) where headers is a list of column names
               and rows is a list of tuples/lists containing result data
    """
    try:
        if query_id == "Q1":
            # Q1: Science Fiction movies after a year
            min_year = params.get('year', 2010)
            rows, headers = q.query_Q1_scifi_after_year(min_year)
            return headers, rows

        elif query_id == "Q2":
            # Q2: Actors in a specific movie
            movie_title = params.get('movie_title', 'Inception')
            rows, headers = q.query_Q2_actors_in_movie(movie_title)
            return headers, rows

        elif query_id == "Q3":
            # Q3: Reviews for a specific movie
            movie_title = params.get('movie_title', 'Dune')
            rows, headers = q.query_Q3_reviews_for_movie(movie_title)
            return headers, rows

        elif query_id == "Q4":
            # Q4: Movies by a specific director
            director_name = params.get('director_name', 'Christopher Nolan')
            rows, headers = q.query_Q4_movies_by_director(director_name)
            return headers, rows

        elif query_id == "Q5":
            # Q5: Average rating by studio
            studio_name = params.get('studio_name', 'A24')
            rows, headers = q.query_Q5_avg_rating_by_studio(studio_name)
            return headers, rows

        elif query_id == "Q6":
            # Q6: Movies that won a Best Picture award
            award_keyword = params.get('award_keyword', 'Best Picture')
            rows, headers = q.query_Q6_best_picture_movies(award_keyword)
            return headers, rows

        elif query_id == "Q7":
            # Q7: Actors in studios founded before a year
            cutoff_year = params.get('cutoff_year', 1950)
            rows, headers = q.query_Q7_actors_in_pre1950_studios(cutoff_year)
            return headers, rows

        elif query_id == "Q8":
            # Q8: Writers who wrote for a director
            director_name = params.get('director_name', 'Martin Scorsese')
            rows, headers = q.query_Q8_writers_for_director(director_name)
            return headers, rows

        elif query_id == "Q9":
            # Q9: Favorite movies for a user
            username = params.get('username', 'smomery0')
            rows, headers = q.query_Q9_favorite_movies_for_user(username)
            return headers, rows

        elif query_id == "Q10":
            # Q10: Top 10 movies by genre
            genre_name = params.get('genre_name', 'Horror')
            rows, headers = q.query_Q10_top10_by_genre(genre_name)
            return headers, rows

        elif query_id == "Q11":
            # Q11: Long movies
            min_runtime = params.get('min_runtime', 180)
            rows, headers = q.query_Q11_long_movies(min_runtime)
            return headers, rows

        elif query_id == "Q12":
            # Q12: Actors born in a specific year
            birth_year = params.get('birth_year', 1980)
            rows, headers = q.query_Q12_actors_born_in_year(birth_year)
            return headers, rows

        else:
            # Query not implemented
            return ['Message'], [['Query not implemented']]

    except Exception as e:
        # Database error occurred
        error_msg = f"Database error: {str(e)}"
        print(error_msg)
        return ['Error'], [[error_msg]]


def insert_review(review_data):
    """
    Insert a new review into the database using real MySQL connection.
    Automatically looks up movieId from movie title.

    Args:
        review_data (dict): Dictionary containing userId, movieTitle, rating, content, postTime

    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate inputs
    user_id = review_data.get('userId')
    movie_title = review_data.get('movieTitle')
    rating = review_data.get('rating')
    content = review_data.get('content', '').strip()
    post_time = review_data.get('postTime')

    # Validate required fields
    if not user_id:
        return False, "User ID is required."

    if not movie_title:
        return False, "Movie Title is required."

    if not content:
        return False, "Review content cannot be empty."

    # Validate rating
    try:
        rating_int = int(rating)
        if rating_int < 1 or rating_int > 10:
            return False, f"Invalid rating: {rating_int}. Must be between 1 and 10."
    except (ValueError, TypeError):
        return False, f"Invalid rating value: {rating}. Must be an integer between 1 and 10."

    # Convert user_id to integer
    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return False, "User ID must be a valid integer."

    # Step 1: Lookup movieId from movie title (this is hidden from the user)
    movie_title_str = str(movie_title).strip()
    movie_id, lookup_error = q.find_movie_id_by_title(movie_title_str)

    if movie_id is None:
        # Movie not found or multiple matches
        return False, lookup_error

    # Step 2: Insert the review using the found movieId
    try:
        success, message = q.insert_review(
            user_id=user_id_int,
            movie_id=movie_id,  # movieId is already a string from the lookup
            rating=rating_int,
            content=content,
            post_time=post_time
        )
        return success, message

    except Exception as e:
        error_msg = f"Database error: {str(e)}"
        print(error_msg)
        return False, error_msg


# ============================================================================
# QUERY DEFINITIONS
# ============================================================================

QUERIES = {
    'Q1': {
        'label': 'Q1: Movies in Science Fiction genre after a year',
        'params': [
            {'name': 'year', 'type': 'int', 'label': 'Year (release after):', 'default': '2010'}
        ]
    },
    'Q2': {
        'label': 'Q2: Actors who starred in a specific movie',
        'params': [
            {'name': 'movie_title', 'type': 'str', 'label': 'Movie Title:', 'default': 'Ten Lives'}
        ]
    },
    'Q3': {
        'label': 'Q3: All reviews for a specific movie',
        'params': [
            {'name': 'movie_title', 'type': 'str', 'label': 'Movie Title:', 'default': 'Ten Lives'}
        ]
    },
    'Q4': {
        'label': 'Q4: All movies directed by a specific director',
        'params': [
            {'name': 'director_name', 'type': 'str', 'label': 'Director Name:', 'default': 'Christopher Nolan'}
        ]
    },
    'Q5': {
        'label': 'Q5: Average rating for movies by a studio',
        'params': [
            {'name': 'studio_name', 'type': 'str', 'label': 'Studio Name:', 'default': 'A24'}
        ]
    },
    'Q6': {
        'label': 'Q6: Movies that won a Best Picture award',
        'params': [
            {'name': 'award_keyword', 'type': 'str', 'label': 'Award Keyword:', 'default': 'Best Picture'}
        ]
    },
    'Q7': {
        'label': 'Q7: Actors in studios founded before a year',
        'params': [
            {'name': 'cutoff_year', 'type': 'int', 'label': 'Founded Before Year:', 'default': '1950'}
        ]
    },
    'Q8': {
        'label': 'Q8: Writers who wrote for a director',
        'params': [
            {'name': 'director_name', 'type': 'str', 'label': 'Director Name:', 'default': 'Christopher Nolan'}
        ]
    },
    'Q9': {
        'label': 'Q9: Favorite movies for a user',
        'params': [
            {'name': 'username', 'type': 'str', 'label': 'Username:', 'default': 'smomery0'}
        ]
    },
    'Q10': {
        'label': 'Q10: Top 10 highest-rated movies in a genre',
        'params': [
            {'name': 'genre_name', 'type': 'str', 'label': 'Genre Name:', 'default': 'Horror'}
        ]
    },
    'Q11': {
        'label': 'Q11: Movies longer than a given runtime',
        'params': [
            {'name': 'min_runtime', 'type': 'int',
             'label': 'Minimum runtime (minutes):', 'default': '180'}
        ]
    },
    'Q12': {
        'label': 'Q12: Actors born in a specific year',
        'params': [
            {'name': 'birth_year', 'type': 'int', 'label': 'Birth Year:', 'default': '1980'}
        ]
    }
}


# ============================================================================
# GUI LAYOUT
# ============================================================================

def create_query_tab():
    """Create the Query Explorer tab layout."""

    # Header section
    header_section = [
        [sg.Text('Global Film Database Explorer', font=('Helvetica', 20, 'bold'),
                 text_color='#1E88E5', pad=(0, 10))],
        [sg.Text('Browse and search movies, people, studios, genres, and user reviews.',
                 font=('Helvetica', 11))],
        [sg.Text('Select a query below, enter parameters, and click "Run Query" to see results.',
                 font=('Helvetica', 11))],
        [sg.HorizontalSeparator(pad=(0, 15))]
    ]

    # Query selection section
    query_list = [QUERIES[qid]['label'] for qid in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12']]

    query_selection = [
        [sg.Text('Select Query:', font=('Helvetica', 12, 'bold'), pad=(0, 5))],
        [sg.Listbox(values=query_list, size=(60, 12), key='-QUERY_LIST-',
                    enable_events=True, default_values=[query_list[0]],
                    font=('Helvetica', 10))]
    ]

    # Parameters section (dynamic based on selected query)
    params_section = [
        [sg.Text('Query Parameters:', font=('Helvetica', 12, 'bold'), pad=(0, (15, 5)))],
        [sg.Frame('', [
            [sg.Text('Year (release after):', size=(20, 1)),
             sg.Input('2010', key='-PARAM_year-', size=(30, 1))],
        ], key='-PARAMS_FRAME-', relief=sg.RELIEF_SUNKEN, pad=(0, 10))]
    ]

    # Run button
    run_button = [
        [sg.Button('Run Query', size=(15, 1), button_color=('#FFFFFF', '#1E88E5'),
                   font=('Helvetica', 11, 'bold'), key='-RUN_QUERY-'),
         sg.Text('', key='-QUERY_STATUS-', size=(40, 1), text_color='#43A047')]
    ]

    # Results section
    results_section = [
        [sg.Text('Query Results:', font=('Helvetica', 12, 'bold'), pad=(0, (15, 5)))],
        [sg.Table(values=[['', '', '', '']],
                  headings=['Col1', 'Col2', 'Col3', 'Col4'],
                  auto_size_columns=True, display_row_numbers=False,
                  justification='left', num_rows=15, key='-RESULTS_TABLE-',
                  enable_events=False, expand_x=True, expand_y=True,
                  font=('Helvetica', 10), header_font=('Helvetica', 10, 'bold'),
                  alternating_row_color='#E3F2FD')]
    ]

    # Combine all sections
    layout = [
        [sg.Column(header_section + query_selection + params_section + run_button + results_section,
                   scrollable=True, vertical_scroll_only=True, expand_x=True, expand_y=True)]
    ]

    return layout


def create_insert_tab():
    """Create the Insert New Review tab layout."""

    layout = [
        [sg.Text('Insert New Review', font=('Helvetica', 18, 'bold'),
                 text_color='#1E88E5', pad=(0, 10))],
        [sg.Text('Add a new movie review to the database.', font=('Helvetica', 11))],
        [sg.HorizontalSeparator(pad=(0, 15))],

        [sg.Text('Review Details:', font=('Helvetica', 12, 'bold'), pad=(0, (10, 10)))],

        [sg.Frame('', [
            [sg.Text('User ID:', size=(15, 1)),
             sg.Input('', key='-REVIEW_USER_ID-', size=(40, 1))],

            [sg.Text('Movie Title:', size=(15, 1)),
             sg.Input('', key='-REVIEW_MOVIE_TITLE-', size=(40, 1))],

            [sg.Text('Rating (1-10):', size=(15, 1)),
             sg.Spin([i for i in range(1, 11)], initial_value=8,
                     key='-REVIEW_RATING-', size=(10, 1))],

            [sg.Text('Review Content:', size=(15, 1))],
            [sg.Multiline('', key='-REVIEW_CONTENT-', size=(60, 8),
                          font=('Helvetica', 10))],

            [sg.Text('Post Time:', size=(15, 1)),
             sg.Input(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                      key='-REVIEW_POST_TIME-', size=(40, 1))],

        ], relief=sg.RELIEF_SUNKEN, pad=(0, 10))],

        [sg.Button('Submit Review', size=(15, 1), button_color=('#FFFFFF', '#43A047'),
                   font=('Helvetica', 11, 'bold'), key='-SUBMIT_REVIEW-'),
         sg.Button('Clear Form', size=(15, 1), button_color=('#FFFFFF', '#757575'),
                   font=('Helvetica', 11, 'bold'), key='-CLEAR_FORM-')],

        [sg.Text('', key='-INSERT_STATUS-', size=(60, 2), text_color='#43A047',
                 font=('Helvetica', 10))]
    ]

    return layout


def create_main_window():
    """Create the main application window."""

    sg.theme('LightBlue2')

    tab_group = [
        [sg.TabGroup([
            [sg.Tab('Query Explorer', create_query_tab(), key='-TAB_QUERY-'),
             sg.Tab('Insert New Review', create_insert_tab(), key='-TAB_INSERT-')]
        ], expand_x=True, expand_y=True)]
    ]

    layout = [
        [sg.Column(tab_group, expand_x=True, expand_y=True, pad=(10, 10))]
    ]

    window = sg.Window('Global Film Database Explorer', layout,
                       size=(900, 700), resizable=True, finalize=True)

    return window


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _normalize_rows(rows, max_cols=4):
    """
    Normalize rows to have exactly max_cols columns.
    Pads with empty strings or truncates as needed.

    Args:
        rows: List of tuples/lists
        max_cols: Target number of columns (default 4)

    Returns:
        List of lists with exactly max_cols elements each
    """
    normalized = []
    for row in rows:
        row_list = list(row)
        if len(row_list) < max_cols:
            # Pad with empty strings
            row_list += [''] * (max_cols - len(row_list))
        elif len(row_list) > max_cols:
            # Truncate to max_cols
            row_list = row_list[:max_cols]
        normalized.append(row_list)
    return normalized


# ============================================================================
# EVENT HANDLERS
# ============================================================================

def update_params_frame(window, query_id):
    """Update the parameters frame based on selected query."""

    if query_id not in QUERIES:
        return

    params_def = QUERIES[query_id]['params']

    # Clear all old parameter widgets from the frame
    frame = window['-PARAMS_FRAME-']
    for child in frame.Widget.winfo_children():
        child.destroy()

    # Build new parameter inputs
    param_rows = []
    for param in params_def:
        param_rows.append([
            sg.Text(f"{param['label']}", size=(20, 1)),
            sg.Input(param['default'], key=f"-PARAM_{param['name']}-", size=(30, 1))
        ])

    if not param_rows:
        param_rows = [[sg.Text('No parameters needed', font=('Helvetica', 10, 'italic'))]]

    # Add new parameter widgets
    window.extend_layout(frame, param_rows)


def handle_query_selection(window, values):
    """Handle query selection from listbox."""

    if not values['-QUERY_LIST-']:
        return

    selected_label = values['-QUERY_LIST-'][0]

    # Find query ID from label
    query_id = None
    for qid, qdata in QUERIES.items():
        if qdata['label'] == selected_label:
            query_id = qid
            break

    if query_id:
        # Recreate params frame with new parameters
        update_params_frame(window, query_id)


def handle_run_query(window, values):
    """Handle Run Query button click."""

    if not values['-QUERY_LIST-']:
        sg.popup_error('Please select a query first!')
        return

    selected_label = values['-QUERY_LIST-'][0]

    # Find query ID from label
    query_id = None
    for qid, qdata in QUERIES.items():
        if qdata['label'] == selected_label:
            query_id = qid
            break

    if not query_id:
        sg.popup_error('Invalid query selection!')
        return

    # Collect parameters
    params = {}
    for param_def in QUERIES[query_id]['params']:
        param_name = param_def['name']
        param_key = f"-PARAM_{param_name}-"
        if param_key in values:
            param_value = values[param_key]
            # Convert to appropriate type
            if param_def['type'] == 'int':
                try:
                    params[param_name] = int(param_value)
                except ValueError:
                    sg.popup_error(f"Invalid integer value for {param_def['label']}")
                    return
            else:
                params[param_name] = param_value

    # Run the query
    try:
        headers, rows = run_query(query_id, params)

        # Handle empty results
        if not rows or len(rows) == 0:
            window['-RESULTS_TABLE-'].update(values=[['', '', '', '']])
            window['-QUERY_STATUS-'].update('No results found')
            sg.popup('Query completed successfully!\n\nNo results found.',
                     title='Query Success', auto_close=True, auto_close_duration=2)
            return

        # Normalize rows to 4 columns
        normalized_rows = _normalize_rows(rows, max_cols=4)

        # Update the table with normalized data
        window['-RESULTS_TABLE-'].update(values=normalized_rows)

        # Update status text
        window['-QUERY_STATUS-'].update(f"Query {query_id} completed. {len(rows)} row(s) returned.")

        # Update table headings (only first 4 headers)
        try:
            table_widget = window['-RESULTS_TABLE-'].Widget
            for i, header in enumerate(headers[:4]):
                table_widget.heading(i, text=header)
        except Exception:
            pass

        # Show success popup
        sg.popup('Query completed successfully!',
                 title='Query Success', auto_close=True, auto_close_duration=2)

    except Exception as e:
        error_msg = f"Error running query: {str(e)}"
        print(error_msg)
        sg.popup_error(error_msg, title='Query Error')


def handle_submit_review(window, values):
    """Handle Submit Review button click."""

    review_data = {
        'userId': values.get('-REVIEW_USER_ID-'),
        'movieTitle': values.get('-REVIEW_MOVIE_TITLE-'),
        'rating': values.get('-REVIEW_RATING-'),
        'content': values.get('-REVIEW_CONTENT-'),
        'postTime': values.get('-REVIEW_POST_TIME-')
    }

    success, message = insert_review(review_data)

    color = '#43A047' if success else '#D32F2F'
    window['-INSERT_STATUS-'].update(message, text_color=color)

    if success:
        sg.popup('Review inserted successfully!',
                 title='Insert Success', auto_close=True, auto_close_duration=2)
    else:
        sg.popup_error(f'Failed to insert review:\n\n{message}', title='Insert Error')


def handle_clear_form(window):
    """Clear the Insert Review form fields."""

    window['-REVIEW_USER_ID-'].update('')
    window['-REVIEW_MOVIE_TITLE-'].update('')
    window['-REVIEW_RATING-'].update(8)
    window['-REVIEW_CONTENT-'].update('')
    window['-REVIEW_POST_TIME-'].update(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    window['-INSERT_STATUS-'].update('')


# ============================================================================
# MAIN EVENT LOOP
# ============================================================================

def main():
    """Main entry point for the application."""

    window = create_main_window()

    # Initialize default parameters for the first query
    first_query_id = 'Q1'
    update_params_frame(window, first_query_id)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == '-QUERY_LIST-':
            handle_query_selection(window, values)

        elif event == '-RUN_QUERY-':
            handle_run_query(window, values)

        elif event == '-SUBMIT_REVIEW-':
            handle_submit_review(window, values)

        elif event == '-CLEAR_FORM-':
            handle_clear_form(window)

    window.close()


if __name__ == '__main__':
    main()

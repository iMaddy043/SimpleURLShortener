# Simple URL Shortener

This is a simple URL shortening service built using Python and Flask. It allows users to shorten long URLs and track the number of clicks on each shortened link.

## Features

*   **URL Shortening:** Shortens long URLs into shorter, more manageable links.
*   **Custom Display URL:** Uses a custom domain (e.g., `http://prashant.smp/`) for the shortened URLs, making them more recognizable.
*   **Click Tracking:** Tracks the number of clicks each shortened URL receives.
*   **Analytics Dashboard:** Provides a simple analytics page to view the most popular shortened URLs and their click counts.
*   **API Endpoint:** Offers an API endpoint (`/api/analytics`) to retrieve analytics data in JSON format.
*   **Shareable Links:** Generates shareable links that display the custom domain URL but redirect to the actual URL.
*   **Database Persistence:** Uses SQLite to store URL mappings and click data.
* **Error Handling:** Handles cases where a short code is not found.
* **URL Validation:** Adds `http://` prefix if the user does not provide it.

## Technologies Used

*   **Python:** The primary programming language.
*   **Flask:** A micro web framework for building the web application.
*   **SQLite:** A lightweight database for storing URL data.
*   **HTML/CSS:** For the basic front-end interface.
* **Werkzeug:** For handling HTTP exceptions.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/iMaddy043/SimpleURLShortener.git
    cd SimpleURLShortener
    ```

2.  **Create Virtual Environment:**
    python -m venv venv
    venv\Scripts\activate
    

3.  **Install Dependencies:**

    pip install -r requirements.txt
    

4.  **Run the Application:**
    ```bash
    python app.py
    ```

5.  **Access the Application:**
    Open your web browser and go to `http://127.0.0.1:5000/`.

## Usage

1.  **Shorten a URL:**
    *  Enter a long URL in the input field on the homepage.
    *  Click the "Shorten" button.
    *  The application will generate a shortened URL and display it.
    *  The shortened URL will be displayed with the custom domain.
    *  The actual URL that works will also be displayed.

2.  **Access the Shortened URL:**
    *   Click on the displayed shortened URL (or copy and paste it into your browser).
    *   You will be redirected to the original, long URL.

3.  **View Analytics:**
    *   Go to `http://127.0.0.1:5000/analytics` to view the analytics dashboard.
    *   The dashboard shows a list of shortened URLs, their original URLs, creation dates, and click counts, sorted by most clicks.

4. **API Analytics:**
    * Go to `http://127.0.0.1:5000/api/analytics` to get the analytics data in JSON format.

5. **Shareable Links**
    * Go to `http://127.0.0.1:5000/r/<short_code>` to get a shareable link that displays the custom domain but redirects to the actual URL.

## Configuration

*   **`ACTUAL_HOST`:** This variable in `app.py` defines the actual host URL where the application is running (e.g., `http://127.0.0.1:5000/`).
*   **`DISPLAY_HOST`:** This variable defines the custom domain you want to use for the shortened URLs (e.g., `http://prashant.smp/`). You can change this to your own domain.
* **Database:** The database file is `url_shortener.db`.

## File Structure

*   **`app.py`:** The main Python application file.
*   **`url_shortener.db`:** The SQLite database file.
*   **`templates/`:**
    *   `index.html`: The homepage template.
    *   `analytics.html`: The analytics dashboard template.
    * `404.html`: The 404 error page.
    * `redirect.html`: The page for shareable links.


## Usage

1.  **Shorten a URL:**
    *   Enter a long URL in the input field on the homepage.
        *   **Example Input:** `https://www.example.com/a/very/long/url/with/many/parameters?param1=value1&param2=value2`
    *   Click the "Shorten" button.
    *   The application will generate a shortened URL and display it.
        *   **Example Output (Shortened URL with custom domain):** `http://prashant.smp/r/abcde`
        *   **Example Output (Actual URL that works):** `http://127.0.0.1:5000/abcde`
    *   The shortened URL will be displayed with the custom domain.
    *   The actual URL that works will also be displayed.

2.  **Access the Shortened URL:**
    *   Click on the displayed shortened URL (or copy and paste it into your browser).
        *   **Example:** Clicking on `http://127.0.0.1:5000/abcde` or `http://prashant.smp/r/abcde` will redirect you to `https://www.example.com/a/very/long/url/with/many/parameters?param1=value1&param2=value2`.
    *   You will be redirected to the original, long URL.

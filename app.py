import os
import sqlite3
import string
import random
from datetime import datetime
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
from werkzeug.exceptions import NotFound

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
ACTUAL_HOST = "http://127.0.0.1:5000/"  # Your actual host URL
DISPLAY_HOST = "http://prashant.smp/"      # The display URL you want to show (like bit.ly)

# Database setup
def init_db():
    conn = sqlite3.connect('url_shortener.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url TEXT NOT NULL,
        short_code TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        clicks INTEGER DEFAULT 0,
        display_url TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('url_shortener.db')
    conn.row_factory = sqlite3.Row
    return conn

# Generate a random short code
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Create a new short URL
def create_short_url(original_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the URL already exists in the database
    cursor.execute('SELECT short_code, display_url FROM urls WHERE original_url = ?', (original_url,))
    existing_url = cursor.fetchone()
    
    if existing_url:
        short_code = existing_url['short_code']
        display_url = existing_url['display_url']
    else:
        # Generate a new short code
        while True:
            short_code = generate_short_code()
            cursor.execute('SELECT id FROM urls WHERE short_code = ?', (short_code,))
            if not cursor.fetchone():
                break
        
        # Create display URL with custom domain
        display_url = f"{DISPLAY_HOST}{short_code}"
        
        cursor.execute(
            'INSERT INTO urls (original_url, short_code, created_at, display_url) VALUES (?, ?, ?, ?)',
            (original_url, short_code, datetime.now(), display_url)
        )
        conn.commit()
    
    conn.close()
    return short_code, display_url

# Redirect user to original URL and increment click count
def redirect_to_url(short_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    url_data = cursor.fetchone()
    
    if url_data:
        original_url = url_data['original_url']
        
        # Increment click count
        cursor.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?', (short_code,))
        conn.commit()
        conn.close()
        
        return original_url
    
    conn.close()
    return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['url']
    
    if not original_url:
        flash('Please enter a URL')
        return redirect(url_for('index'))
    
    # Add http:// prefix if not present
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'http://' + original_url
    
    short_code, display_url = create_short_url(original_url)
    actual_url = ACTUAL_HOST + short_code  # This is what will actually work
    
    return render_template('index.html', 
                          short_url=display_url,         # What we show to the user
                          actual_url=actual_url,         # The real URL that works
                          original_url=original_url)

@app.route('/<short_code>')
def redirect_short_url(short_code):
    original_url = redirect_to_url(short_code)
    
    if original_url:
        return redirect(original_url)
    else:
        return render_template('404.html'), 404

@app.route('/analytics')
def analytics():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT short_code, original_url, created_at, clicks, display_url FROM urls ORDER BY clicks DESC')
    urls = cursor.fetchall()
    
    conn.close()
    
    return render_template('analytics.html', urls=urls)

@app.route('/api/analytics')
def api_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT short_code, original_url, created_at, clicks, display_url FROM urls ORDER BY clicks DESC')
    urls = cursor.fetchall()
    
    conn.close()
    
    url_list = [dict(url) for url in urls]
    return jsonify(url_list)

# For generating shareable links to copy display URL but navigate to actual URL
@app.route('/r/<short_code>')
def get_redirect_html(short_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT original_url, display_url FROM urls WHERE short_code = ?', (short_code,))
    url_data = cursor.fetchone()
    
    if url_data:
        return render_template('redirect.html', 
                              display_url=url_data['display_url'],
                              original_url=url_data['original_url'])
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
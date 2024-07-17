from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/videos'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv'}  # Define allowed file extensions
MOVIE_DIRECTORY = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])
DATABASE = 'gazedata.db'

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database and create the table
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS GazeData (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                docX REAL,
                docY REAL,
                time REAL,
                state INTEGER,
                headX REAL,
                headY REAL,
                headZ REAL,
                headYaw REAL,
                headPitch REAL,
                headRoll REAL,
                header TEXT
            )
        ''')
        conn.commit()

init_db()

@app.route('/store_gaze_data', methods=['POST'])
def store_gaze_data():
    data = request.json
    with get_db_connection() as conn:
        conn.execute('''
            INSERT INTO GazeData (docX, docY, time, state, headX, headY, headZ, headYaw, headPitch, headRoll, header)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['docX'], data['docY'], data['time'], data['state'],
              data.get('headX'), data.get('headY'), data.get('headZ'),
              data.get('headYaw'), data.get('headPitch'), data.get('headRoll'),
              data.get('header')))
        conn.commit()
    return jsonify({'message': 'Data stored successfully'}), 201


@app.route('/visualize', methods=['GET'])
def visualize():
    header = request.args.get('header')
    with get_db_connection() as conn:
        gaze_data = conn.execute('SELECT * FROM GazeData WHERE header = ?', (header,)).fetchall()
    return render_template('visualization.html', gaze_data=gaze_data, header=header)


# Home page with upload form and dropdown
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        
        # If file is allowed and valid, save it to the upload folder
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))  # Redirect to home page after upload
    
    # List all movie files in the movies directory
    #movie_files = [f for f in os.listdir(MOVIE_DIRECTORY) if f.endswith({'mp4', 'avi', 'mov', 'mkv'})]
    movie_files = [f for f in os.listdir(MOVIE_DIRECTORY) if f.endswith(tuple(app.config['ALLOWED_EXTENSIONS']))]

    # Sort movie files by modification time in descending order
    movie_files.sort(key=lambda x: os.path.getmtime(os.path.join(MOVIE_DIRECTORY, x)), reverse=True)

    # Fetch headers for visualization
    with get_db_connection() as conn:
        headers = conn.execute('SELECT DISTINCT header FROM GazeData').fetchall()

    return render_template('index.html', movies=movie_files, headers=headers)

if __name__ == '__main__':
    app.run(debug=True)


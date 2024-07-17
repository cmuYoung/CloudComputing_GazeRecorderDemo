from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/videos'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv'}  # Define allowed file extensions
MOVIE_DIRECTORY = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'])

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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

    return render_template('index.html', movies=movie_files)

if __name__ == '__main__':
    app.run(debug=True)


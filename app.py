from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "shared"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    # return "LANSHARE is running!"
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    print("Upload route reached!")
    uploaded_file = request.files["file"]
    safe_filename = secure_filename(uploaded_file.filename)
    if not safe_filename:
        return "Invalid filename!"
    
    name, extension = os.path.splitext(safe_filename)
    counter = 1
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)

    while os.path.exists(file_path):
        safe_filename = f"{name}_{counter}{extension}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)
        counter += 1


    uploaded_file.save(file_path)
    return "File uploaded successfully!"

if (__name__ == "__main__"):
    app.run(debug=True)

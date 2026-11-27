from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import qrcode
import io

app = Flask(__name__)

UPLOAD_FOLDER = "shared"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def format_size(size):
    file_sizes = ["KB", "MB", "GB", "TB"]
    i = -1

    while size >= 1000 and i < len(file_sizes) - 1:
        size = size / 1000
        i += 1

    if i == -1:
        return f"{size} bytes"

    return f"{size:.2f} {file_sizes[i]}"

@app.route("/")
def home():

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    file_details = []
    for file in files:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)
        if not os.path.isfile(file_path):
            continue
        size = os.path.getsize(file_path)

        file_details.append({
            "name": file,
            "size": format_size(size),
        })
    return render_template("index.html", file_details=file_details)

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"],
                        filename,
                        as_attachment=True)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    safe_filename = secure_filename(filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)

    if os.path.isfile(file_path):
        os.remove(file_path)

    return jsonify({
    "success": True,
    "filename": safe_filename
})

@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_files = request.files.getlist("files")

    for uploaded_file in uploaded_files:
        if not uploaded_file.filename:
            continue

        safe_filename = secure_filename(uploaded_file.filename)

        if not safe_filename:
            continue
    
        name, extension = os.path.splitext(safe_filename)
        counter = 1

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)

        while os.path.exists(file_path):
            safe_filename = f"{name}_{counter}{extension}"
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_filename)
            counter += 1

        uploaded_file.save(file_path)

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    file_details = []

    for file in files:
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)

        if not os.path.isfile(file_path):
            continue

        size = os.path.getsize(file_path)

        file_details.append({
            "name": file,
            "size": format_size(size)
        })

    return jsonify({
        "success": True,
        "message": "Files uploaded successfully!",
        "files": file_details
    })

@app.route("/qr-code")
def generate_qr():
    qr = qrcode.make(request.host_url)

    image = io.BytesIO()
    qr.save(image, format="PNG")
    image.seek(0)

    return send_file(image, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
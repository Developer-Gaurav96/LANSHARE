from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "shared"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    # return "LANSHARE is running!"
    return render_template("index.html")

if (__name__ == "__main__"):
    app.run(debug=True)

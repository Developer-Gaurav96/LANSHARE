from flask import Flask, render_template, request
import _osx_support

app = Flask(__name__)

UPLOAD_FOLDER = "shared"
app.config["UPLOAD_"]

@app.route("/")
def home():
    # return "LANSHARE is running!"
    return render_template("index.html")

if (__name__ == "__main__"):
    app.run(debug=True)

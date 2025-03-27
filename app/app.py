from flask import Flask, request, render_template, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from FileAnalyzer import FileAnalyzer  # ✅ Make sure this import is valid

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "static/out"

app = Flask(__name__, static_url_path="/static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_folder():
    folder_path = request.form.get("folderPath")

    if not os.path.exists(folder_path):
        return jsonify({"status": "error", "message": "Path does not exist."})

    try:
        print(f"Analyzing: {folder_path}")
        fileAnalyzer = FileAnalyzer()
        fileAnalyzer.analyze(folder_path, None)  # ✅ Your actual analyzer call
        return jsonify({"status": "ok"})
    except Exception as e:
        print(f"Error during analysis: {e}")
        return jsonify({"status": "error", "message": str(e)})


@app.route("/out/data.json")
def data():
    return send_from_directory(RESULT_FOLDER, "data.json")


@app.route("/upload-files", methods=["POST"])
def upload_files():
    files = request.files.getlist("files")
    temp_folder = os.path.join(app.config["UPLOAD_FOLDER"], "session")
    os.makedirs(temp_folder, exist_ok=True)

    for file in files:
        rel_path = secure_filename(file.filename)
        file_path = os.path.join(temp_folder, rel_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)

    try:
        fileAnalyzer = FileAnalyzer()
        fileAnalyzer.analyze(temp_folder, None)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)

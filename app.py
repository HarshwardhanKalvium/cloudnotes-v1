import os

from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory

from api.routes import api_bp
from utils.helpers import init_db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")


def create_app():
    load_dotenv()

    database_url = os.environ.get("DATABASE_URL")
    secret_key = os.environ.get("SECRET_KEY")
    if not database_url:
        raise RuntimeError("DATABASE_URL must be set")
    if not secret_key:
        raise RuntimeError("SECRET_KEY must be set")

    application = Flask(__name__)
    application.config["UPLOAD_FOLDER"] = os.environ.get(
        "UPLOAD_FOLDER", UPLOAD_FOLDER
    )
    application.config["DATABASE_URL"] = database_url
    application.config["SECRET_KEY"] = secret_key
    application.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    init_db(database_url)
    os.makedirs(application.config["UPLOAD_FOLDER"], exist_ok=True)
    application.register_blueprint(api_bp, url_prefix="/api")

    @application.route("/")
    def home():
        return render_template("index.html")

    @application.route("/notes")
    def notes_page():
        return render_template("notes.html")

    @application.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(application.config["UPLOAD_FOLDER"], filename)

    return application


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

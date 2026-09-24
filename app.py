import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for


def create_app(db_path=None):
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path or os.environ.get("DB_PATH", "feedback.db")
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    def get_db():
        conn = sqlite3.connect(app.config["DB_PATH"])
        conn.row_factory = sqlite3.Row
        return conn

    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                feedback TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            course = request.form.get("course", "").strip()
            text = request.form.get("feedback", "").strip()
            if not (name and course and text):
                flash("All fields are required.", "error")
            else:
                with get_db() as conn:
                    conn.execute(
                        "INSERT INTO feedback (name, course, feedback) VALUES (?, ?, ?)",
                        (name, course, text),
                    )
                flash("Thank you! Your feedback was submitted.", "success")
                return redirect(url_for("index"))
        with get_db() as conn:
            rows = conn.execute(
                "SELECT * FROM feedback ORDER BY id DESC"
            ).fetchall()
        return render_template("index.html", entries=rows)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

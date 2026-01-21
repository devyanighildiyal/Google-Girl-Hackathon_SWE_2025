import re
import sqlite3
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for


auth = Blueprint("auth", __name__)

DB_PATH = "helperms.db"


def _get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = _get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS login_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            success INTEGER NOT NULL,
            ip TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def _norm(s: str) -> str:
    return (s or "").strip().lower()


def _valid_email(email: str) -> bool:
    # Simple validation good enough for a prototype.
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email or ""))


@auth.before_app_request
def _ensure_db():
    init_db()


@auth.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = (request.form.get("first_name") or "").strip()
        last_name = (request.form.get("last_name") or "").strip()
        age_raw = (request.form.get("age") or "").strip()
        gender = (request.form.get("gender") or "").strip()
        email = (request.form.get("email") or "").strip()

        if not first_name or not last_name:
            flash("Please enter your first and last name.", "error")
            return render_template("signup.html")

        try:
            age = int(age_raw)
            if age <= 0 or age > 120:
                raise ValueError
        except Exception:
            flash("Please enter a valid age.", "error")
            return render_template("signup.html")

        if gender not in {"Female", "Male", "Other", "Prefer not to say"}:
            flash("Please select a gender.", "error")
            return render_template("signup.html")

        if not _valid_email(email):
            flash("Please enter a valid organization email.", "error")
            return render_template("signup.html")

        conn = _get_db()
        try:
            conn.execute(
                """
                INSERT INTO users (first_name, last_name, age, gender, email, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (first_name, last_name, age, gender, email, datetime.utcnow().isoformat()),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("That email is already registered. Please log in.", "error")
            return redirect(url_for("auth.login"))
        finally:
            conn.close()

        session["user_email"] = email
        session["user_name"] = first_name
        flash("Signup successful! Welcome to HelperMS.", "success")
        return redirect(url_for("dashboard"))

    return render_template("signup.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()

        if not username:
            flash("Please enter your username.", "error")
            return render_template("login.html")
        if not _valid_email(email):
            flash("Please enter a valid organization email.", "error")
            return render_template("login.html")

        conn = _get_db()
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        ).fetchone()

        success = 0
        if row:
            # Accept either first name or full name as "username"
            full_name = f"{row['first_name']} {row['last_name']}"
            if _norm(username) in {_norm(row["first_name"]), _norm(full_name)}:
                success = 1

        conn.execute(
            """
            INSERT INTO login_events (username, email, success, ip, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                username,
                email,
                success,
                request.headers.get("X-Forwarded-For", request.remote_addr),
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

        if success:
            session["user_email"] = email
            session["user_name"] = row["first_name"]
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))

        flash("Login failed. Please check your username and email.", "error")
        return render_template("login.html")

    return render_template("login.html")

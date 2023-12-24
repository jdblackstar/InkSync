from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from scrape import scrape_kindle_highlights

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/scrape")
def scrape():
    scrape_kindle_highlights()
    return jsonify({"message": "Scrape completed!"})

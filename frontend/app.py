from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
API_URL = "http://backend:8000"


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/listar")
def listing():
    return render_template("listing.html")

@app.route("/cadastro")
def create():
    return render_template("create.html")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")

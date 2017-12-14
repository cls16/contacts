from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello():
    username = request.args.get("name", "World")
    return render_template("hello.html", username=username)

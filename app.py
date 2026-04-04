from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, world!"


if __name__ == "__main__":
    # Bandit fail demo (B201 flask_debug_true) — remove debug=True after CI fails as expected
    app.run(debug=True)

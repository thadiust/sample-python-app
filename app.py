from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, world!"


if __name__ == "__main__":
    # Intentional Bandit finding (B201: Flask debug mode). Remove debug=True for a clean scan.
    app.run(debug=True)

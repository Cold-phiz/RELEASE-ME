import funcs as dl
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

dl.download_playlist("")

if __name__ == "__main__":
    app.run(debug=True)
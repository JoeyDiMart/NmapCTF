# the server file to make a tiny web server
from flask import Flask  # Python web framework

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>flag{joeygoat}</p>"


@app.route("/robots.txt")
def robots():
    return "flag{robotflag}\n", 200, {"Contend-Type": "text/plain"}


# bind docker to 0.0.0.0 so anything outside the docker container can reach this server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)  # listen on port 80

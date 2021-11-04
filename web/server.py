import flask

app = flask.Flask(__name__)

@app.route("/<path:filename>", methods=["GET"])
def file_reader(filename):
    if not "." in filename:
        filename += ".html"
    return flask.send_from_directory("../", filename)


@app.route("/", methods=["GET"])
def home():
    return flask.send_from_directory("../", "index.html")

app.run(host="0.0.0.0", port="80", threaded=True)
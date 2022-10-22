import flask

app = flask.Flask(__name__)

OUTPUT_DIRECTORY = "../dist"

@app.route("/<path:filename>", methods=["GET"])
def file_reader(filename):
    if not "." in filename:
        filename += ".html"
    return flask.send_from_directory(OUTPUT_DIRECTORY, filename)


@app.route("/", methods=["GET"])
def home():
    return flask.send_from_directory(OUTPUT_DIRECTORY, "index.html")

app.run(host="0.0.0.0", port="80", threaded=True)
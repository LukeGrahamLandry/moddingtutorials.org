import flask, os

app = flask.Flask(__name__)

OUTPUT_DIRECTORY = os.getcwd() + "/dist"


@app.route("/<path:filename>", methods=["GET"])
def file_reader(filename):
    original = filename
    if not "." in filename:
        filename += ".html"

    if not os.path.exists(OUTPUT_DIRECTORY + "/" + filename):
        filename = original + "/index.html"
    
    return flask.send_from_directory(OUTPUT_DIRECTORY, filename)


@app.route("/", methods=["GET"])
def home():
    return flask.send_from_directory(OUTPUT_DIRECTORY, "index.html")

app.run(host="0.0.0.0", port="80", threaded=True)
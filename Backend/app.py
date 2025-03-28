from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

frontend_folder=os.path.join(os.getcwd(),"..","Frontend")
dist_folder=os.path.join(frontend_folder,"dist")

@app.route("/",defaults={"filename":""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename="index.html"
    return send_from_directory(dist_folder,filename)

#Add test data


@app.route("/api/testdata")
def testdata():
    return jsonify({"data":[{"name":"John","score":25},{"name":"Jane","score":24}]})





if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/files"
from routes import *

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
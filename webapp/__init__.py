import os

from flask import Flask, request, render_template, redirect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
        host="0.0.0.0",
        UPLOAD_FOLDER="uploads/",
    )
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024 * 1204  # 8 GB

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.config["UPLOAD_FOLDER"])
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def hello():
        return """
        <html>
            <body>
                <form enctype = "multipart/form-data" action = "/upload" method = "post">
    
                    <p>Upload File: <input type = "file" name = "filename" /></p>
 
    
                    <p><input type = "submit" value = "Upload" /></p>
 
                </form>
            </body>
        </html>
        """

    @app.route("/upload", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            if "filename" not in request.files:
                print("No file attached in request")
                return "Error"
            file = request.files["filename"]
            print(file)
            if file.filename == "":
                print("No file selected")
                return redirect(request.url)
            if file:
                filename = file.filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return "success"
            return "Something got Wrong"
        elif request.method == "GET":
            return "Go to homepage"

    return app

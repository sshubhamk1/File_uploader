import os

from flask import (
    Flask,
    jsonify,
    render_template_string,
    request,
    render_template,
    redirect,
    send_from_directory,
)

HELPER_LINKS = """
    <br/>
    <ul>
    <li><a href="/">Upload </a></li>
    <li><a href="/files">Show files </a></li>
    <li><a href="/delete">Delete all updated files</a></li>
    </ul>
    <br />
"""


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
        return f"""
        <html>
            <body>
                <form enctype = "multipart/form-data" action = "/upload" method = "post">
    
                    <p>Upload File: <input type = "file" name = "filename" /></p>
 
    
                    <p><input type = "submit" value = "Upload" /></p>
 
                </form>
                {HELPER_LINKS}
            </body>
        </html>
        """

    @app.route("/upload", methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            if "filename" not in request.files:
                print("No file attached in request")
                return "Error" + HELPER_LINKS
            file = request.files["filename"]
            print(file)
            if file.filename == "":
                print("No file selected" + HELPER_LINKS)
                return redirect(request.url)
            if file:
                filename = file.filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return "success" + HELPER_LINKS
            return "Something got Wrong" + HELPER_LINKS
        elif request.method == "GET":
            return HELPER_LINKS

    @app.route("/files")
    def list_files():
        files = os.listdir(app.config["UPLOAD_FOLDER"])
        return render_template_string(
            """
        <h1>Files</h1>
        <ul>
            {% for file in files %}
            <li><a href="/download/{{ file }}">{{ file }}</a></li>
            {% endfor %}
        </ul>
        """
            + HELPER_LINKS,
            files=files,
        )

    # Route to download a file
    @app.route("/download/<filename>")
    def download_file(filename):
        print(os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"], filename)))
        return send_from_directory(
            os.path.abspath(app.config["UPLOAD_FOLDER"]), filename, as_attachment=True
        )

    # Route to delete all files in the uploads directory

    @app.route("/delete", methods=["GET"])
    def delete_all_files():
        try:
            # List all files in the upload folder
            files = os.listdir(app.config["UPLOAD_FOLDER"])
            for file in files:
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return jsonify({"message": "All files deleted successfully."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

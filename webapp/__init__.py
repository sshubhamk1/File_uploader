import os

from flask import Flask,request, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        host='0.0.0.0',
        UPLOAD_FOLDER="instance/"
    )
    app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024 * 1204

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/upload')
    def upload():
        fileitem = form['filename']
        # check if the file has been uploaded
        if fileitem.filename:
            # strip the leading path from the file name
            fn = os.path.basename(fileitem.filename)
            # open read and write the file into the server
            open(fn, 'wb').write(fileitem.file.read())
        return False
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return '''<html>
<body>
   <form enctype = "multipart/form-data" action = "/" method = "post">
    
<p>Upload File: <input type = "file" name = "filename" /></p>
 
    
<p><input type = "submit" value = "Upload" /></p>
 
</form>
</body>
</html> '''

    @app.route('/', methods=['GET', 'POST'])
    def index():
        #if request.method == 'POST':
        if 'filename' not in request.files:
            print('No file attached in request')
            return "Error"
        file = request.files['filename']
        print(file)
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file :
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return "success"
        return render_template('index.html')

    return app
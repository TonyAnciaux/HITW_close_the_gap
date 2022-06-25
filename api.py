"""
A File that manage to FLASK API opearation which is gather the excel file from user
"""
import os
import pandas as pd


from flask import Flask, request, send_from_directory, redirect, flash, render_template
from werkzeug.utils import secure_filename

from utils.preprocessing import DfFormating


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'kivanc'

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("welcome.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print('not file')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            print('empty file name')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            os.mkdir('uploads')
            filename = secure_filename(file.filename)
            dname = request.form['dname']
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # data_xls = pd.read_excel(f, sheet_name=None)
            # df = pd.DataFrame([data_xls])
            dfFormater = DfFormating(file_path)
            # @ToDo: Test it and change to redirect upload.html
            return "Uploaded successfuly" # df.to_html()
    return render_template('index.html')

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


if __name__ == '__main__':
    port = os.environ.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=False)

import os
import sys
from flask import Flask, flash, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
sys.path.insert(0, "../ETL/")   # used to import files from other folder dir in project
sys.path.insert(0, "../DataTransfer/")   # used to import files from other folder dir in project
from ETLProcess import main as ETL
from kafka_manager import *


UPLOAD_FOLDER = '../../res/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'])

app = Flask(__name__, static_url_path = "/res", static_folder = "res")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #limit file size to 16 mb

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/analysisResults', methods=['GET', 'POST'])
def displayAnalysisResults():
    if request.method == 'GET':
        resultsString = ""
        json_data_list = Consumer.pull_jsons("target")   # pull jsons from target (for now until whole project is done) kafka topic
        framesWithTargetFound = []
        for i in range(len(json_data_list)):
            json_data_parsed = json.loads(json_data_list[i])   # loads json data into a parsed string (back to dict)
            if json_data_parsed.get('foundTargetWithConfidence') != None:
                framesWithTargetFound.append(json_data_list[i])   # if specific frame json contains the key for having found the target object confidently, append that json to a list for display on the results page.
                resultsString = resultsString + "\n\n" + str(json_data_parsed.get('frameNum')) + ": " + str(json_data_parsed.get('foundTargetWithConfidence'))
    return resultsString
                
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):   # if file's type is allowed, then secure filename and save it to the project res folder.
            filename = secure_filename(file.filename)
            videoFilePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)   # make videos filePath for saving it and then sending it to ETL
            file.save(videoFilePath)      # save uploaded video to the project's res folder for ETL to extract
            ETL(videoFromUI=videoFilePath)   # send uploaded video's file path to ETL to begin processing.
            return redirect(url_for('displayAnalysisResults'))
    return render_template("index.html")

if __name__ == "__main__":
    app.run()

import os
import sys
from flask import Flask, flash, session, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
sys.path.insert(0, "../ETL/")   # used to import files from other folder dir in project
sys.path.insert(0, "../DataTransfer/")   # used to import files from other folder dir in project
from ETLProcess import main as ETL
from kafka_consumer import *


UPLOAD_FOLDER = '../'
ALLOWED_EXTENSIONS = set(['avi', 'flv', 'wmv', 'mov', 'mp4'])

app = Flask(__name__, static_url_path = "/static", static_folder = "static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #limit file size to 16 mb

def allowed_file(filename):
    """ Checks to ensure file chose is a correct type """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/analysisResults/', methods=['GET', 'POST'])
def displayAnalysisResults():
    """ Displays the analysis results """
    if request.method == 'GET':
        
        messages = session['messages']  # pull messages from session!
        messages_json = json.loads(messages) # convert str back to json
        messages_json['data'] = [] # blank array for storing jsons
        
        #==================================================================
        stri = ""
        # Consuming messages from general
        consumer = Consumer.initialize("general")
        for m in consumer:
            json_data = m.value
            # Running object detection model against the frames
            #json_data_parsed = json.loads(json_data)
            messages_json['data'].append(json.loads(json_data))
            #return json_data
            '''frame = Utilities.decodeFrameForObjectDetection(json_data_parsed)   # this utility method will not only decode the b64 string, but also prepare the image to be compatible with opencv
            self.image = frame
            self.run_object_detection(json_data_parsed)
            json_data = json.dumps(json_data_parsed)  # writes json_data_parsed to the JSON file
            Utilities.exportJson(json_data, "general")   # exports JSON file with the list of labels for the identified objects'''

        '''json_data_list = Consumer.pull_jsons("target")   # pull jsons from target (for now until whole project is done) kafka topic
        framesWithTargetFound = []
        for i in range(len(json_data_list)):
            json_data_parsed = json.loads(json_data_list[i])   # loads json data into a parsed string (back to dict)
            if json_data_parsed.get('foundTargetWithConfidence') != None:
                framesWithTargetFound.append(json_data_list[i])   # if specific frame json contains the key for having found the target object confidently, append that json to a list for display on the results page.
                resultsString = resultsString + "<br />" + str(json_data_parsed.get('frameNum')) + ": " + str(json_data_parsed.get('foundTargetWithConfidence'))
        '''
        #return stri
        #================================================================
       
        #messages_json['data'].append
        
    return render_template("analyze.html", messages=messages_json)
    '''return resultsString'''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """ Returns the file that has been uploaded """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Home page for app """
    # Upload file button selected
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
            videoFilePath = os.path.join("static", filename)   # make videos filePath for saving it and then sending it to ETL
            file.save(videoFilePath)      # save uploaded video to the project's res folder for ETL to extract
            #ETL(videoFromUI=videoFilePath)   # send uploaded video's file path to ETL to begin processing.
            
            os.system('cd ../../bin/ && ./launch.sh &')
            
            
            messages = json.dumps({"filename":file.filename}) #messages is string of json
            session['messages'] = messages #store messages in session

            return redirect(url_for('displayAnalysisResults'))
    return render_template("upload.html")


if __name__ == "__main__":
    app.secret_key = 'the goose is in the hen house'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(threaded=True)

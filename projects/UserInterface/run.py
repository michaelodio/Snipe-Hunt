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
        messages_json['topics'] = [] # blank array for storing topics
        all_jsons = []

        '''
        # Consuming all messages from general
        consumer = Consumer.initialize("general")
        for m in consumer:
            json_data = m.value
            all_jsons.append(json.loads(json_data))
        '''
        
        for l in read_file(messages_json['filename']):
            all_jsons.append(json.loads(l))

        for j in get_targeted_jsons(all_jsons):
            messages_json['data'].append(j)
            
        for t in get_topics(all_jsons):
            messages_json['topics'].append(t)
            
        messages_json['topicframeconfidence'] = get_topic_frame_confidence(all_jsons)
        
    return render_template("analyze.html", messages=messages_json)


def read_file(fname):
    """ json.dump str of json """
    filename = "static/%s_Metadata.txt" % fname
    fh = open(filename)
    text = fh.read()
    lines = text.split("\n")
    lines = lines[0:len(lines)-1]   #cut off blank tail element in array
    print lines
    return lines


def get_topic_frame_confidence(all_jsons):
    """ Returns a json list of each frame and confidence by topic """
    tfc = {}
    for j in all_jsons:
        if 'GeneralObjectsDetected' in j:
            for obj in j['GeneralObjectsDetected']:
                topic = obj.split(':')[0]
                confidence = obj.split(' ')[1]
                if topic in tfc:
                    tfc[topic].append({'frame': j['frameNum'], 'confidence': confidence})
                else:
                    tfc[topic] = [{'frame': j['frameNum'], 'confidence': confidence}]
    return tfc


def get_targeted_jsons(all_jsons):
    """ Returns a json list of all frames where the target has been found """
    found_jsons = []
    for j in all_jsons:
        if 'foundTargetWithConfidence' in j:
            found_jsons.append(j)
    return found_jsons


def get_topics(all_jsons):
    """ Returns a json list of all the topics found non repeating """
    topics = []
    for j in all_jsons:
        if 'GeneralObjectsDetected' in j:
            for obj in j['GeneralObjectsDetected']:
                topics.append(obj.split(':')[0])
    return list(set(topics))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """ Returns the file that has been uploaded """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/analysisResults/home', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
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
            
            #os.system('cd ../../bin/ && ./launch.sh | tee launch_output.txt &')   # run launch command and save results to text file
            
            
            messages = json.dumps({"filename":file.filename}) #messages is string of json
            session['messages'] = messages #store messages in session

            return redirect(url_for('displayAnalysisResults'))
    return render_template("home.html")


if __name__ == "__main__":
    app.secret_key = 'the goose is in the hen house'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(threaded=True)

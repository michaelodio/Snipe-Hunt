from ..Utility.utilities import *


class videoAnalysis(object):

    def __init__(self):
        """ Constructor """
        self.logger = Utilities.setup_logger("videoanalysis", '../../logs/videoAnalysis.log')
        self.count = 0
        self.confidenceThresh = 60.0
        self.totalFrames = None
        self.averageTargetConfidence = 0.0
        self.conn = None
        self.targetConfidenceHi = 0.0
        self.targetConfidenceLo = 100.0
        self.targetConfidenceHiFrame = None
        self.targetConfidenceLoFrame = None
        self.targetFrameList = []
        self.targetTimesPresent = {'startTime': [],
                                   "endTime": []}  # dictionary of start and end times for the targeted object
        self.targetScreenTime = 0.0  # amount of time the target object is on screen in seconds
        self.targetPercentage = 0.0  # percentage of time target object is on screen
        self.generalObjectsFoundAnalysisData = {}
        self.generalObjectsMetadata = {}
        self.finalJson = {}

    def readyForAnalysis(self, table):
        """ Preps table for analysis """
        self.logger.info("Checking if a video is ready for analysis...")
        self.logger.info("Attempting to connect to Accumulo...")
        try:
            self.conn = Accumulo(host="localhost", port=50096, user="root", password="RoadRally4321")
        except:
            self.logger.info("Failed to connect to Accumulo")
            raise ValueError("Failed to make connection to accumulo!\n")
        self.logger.info("established connection successfully")
        try:
            for entry in self.conn.scan(table, scanrange=Range(srow='row_0'), cols=[
                ["cf1"]]):  # starting at row 0 (the first row) only scan col 1 which contains the metadata for analysis
                if self.count == 0:
                    self.totalFrames = json.loads(entry.val)['videoMetadata']['totalFrames']
                self.count = self.count + 1
        except:
            self.logger.info("Failed to scan table in Accumulo! Shutting down conn")
            self.conn.close()
            raise ValueError("Failed to scan table in Accumulo! Shutting down conn")
        self.logger.info("number of entries = " + str(self.count))
        self.logger.info("Total frames = " + str(self.totalFrames))
        if self.count == self.totalFrames:
            self.logger.info("Video is ready for analysis!")
            return True
        self.logger.info("Video is not ready for analysis!")
        return False

    def calculateTargetScreenTime(self, json_data_parsed):
        """ Determines the on screen time for a target """
        previously_present = False
        for x in range(len(self.targetFrameList)):
            if x == len(self.targetFrameList) - 1:
                if not previously_present:
                    self.targetTimesPresent['startTime'].append(
                        self.targetFrameList[x] * (1 / json_data_parsed['videoMetadata']['FPS']))
                    self.targetTimesPresent['endTime'].append(
                        self.targetFrameList[x] * (1 / json_data_parsed['videoMetadata']['FPS']))
                    break
                if previously_present:
                    self.targetTimesPresent['endTime'].append(
                        self.targetFrameList[x] * (1 / json_data_parsed['videoMetadata']['FPS']))
                    break
            if not previously_present:
                self.targetTimesPresent['startTime'].append(
                    self.targetFrameList[x] * (1 / json_data_parsed['videoMetadata']['FPS']))
            if self.targetFrameList[x] + 1 == self.targetFrameList[x + 1]:
                previously_present = True
                continue
            if self.targetFrameList[x] + 1 != self.targetFrameList[x + 1]:
                self.targetTimesPresent['endTime'].append(
                    self.targetFrameList[x] * (1 / json_data_parsed['videoMetadata']['FPS']))
                previously_present = False

    def calculateObjScreenTime(self, json_data_parsed):
        """ Determines the on screen time for general objects """
        previously_present = False
        for label in self.generalObjectsFoundAnalysisData.keys():
            self.generalObjectsFoundAnalysisData[label]['timeRange'] = {'startTime': [],
                                                                        'endTime': []}  # dictionary of lists for the start and end times for the time ranges where obj is present
            for x in range(len(self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'])):
                if x == len(self.generalObjectsFoundAnalysisData[label]['framesAboveThresh']) - 1:
                    if not previously_present:
                        self.generalObjectsFoundAnalysisData[label]['timeRange']['startTime'].append(
                            self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x] * (
                                    1 / json_data_parsed['videoMetadata']['FPS']))
                        self.generalObjectsFoundAnalysisData[label]['timeRange']['endTime'].append(
                            self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x] * (
                                    1 / json_data_parsed['videoMetadata']['FPS']))
                        break
                    if previously_present:
                        self.generalObjectsFoundAnalysisData[label]['timeRange']['endTime'].append(
                            self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x] * (
                                    1 / json_data_parsed['videoMetadata']['FPS']))
                        break
                if not previously_present:
                    self.generalObjectsFoundAnalysisData[label]['timeRange']['startTime'].append(
                        self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x] * (
                                1 / json_data_parsed['videoMetadata']['FPS']))
                if self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x] + 1 == \
                        self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x + 1]:
                    previously_present = True
                    continue
                if self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x] + 1 != \
                        self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x + 1]:
                    self.generalObjectsFoundAnalysisData[label]['timeRange']['endTime'].append(
                        self.generalObjectsFoundAnalysisData[label]['framesAboveThresh'][x] * (
                                1 / json_data_parsed['videoMetadata']['FPS']))
                    previously_present = False

    def calculateAverageTargetConfidence(self, table):
        """ Calculates average target confidence and finds the highest/lowest target confidence with their specific frame number """
        self.logger.info("Calculating the average target confidence across the whole video...")
        try:
            for entry in self.conn.scan(table, scanrange=Range(srow='row_0'), cols=[["cf1"]]):
                json_data_parsed = json.loads(entry.val)
                if 'foundTargetWithConfidence' in json_data_parsed['frameMetadata']:
                    percent = float(json_data_parsed['frameMetadata']['foundTargetWithConfidence'])
                    self.averageTargetConfidence = self.averageTargetConfidence + percent
                    if percent >= self.confidenceThresh:
                        self.targetFrameList.append(json_data_parsed['frameMetadata']['frameNum'])
                    if percent < self.targetConfidenceLo:
                        self.targetConfidenceLo = percent
                        self.targetConfidenceLoFrame = int(json_data_parsed['frameMetadata']['frameNum'])
                    if percent > self.targetConfidenceHi:
                        self.targetConfidenceHi = percent
                        self.targetConfidenceHiFrame = int(json_data_parsed['frameMetadata']['frameNum'])
        except Exception as e:
            self.logger.info("Exception error occurred: " + str(e))
            print(str(e))
        except:
            self.logger.info("Failed to scan table in Accumulo! Shutting down conn")
            self.conn.close()
            raise ValueError("Failed to scan table in Accumulo! Shutting down conn")

        self.averageTargetConfidence = self.averageTargetConfidence / self.totalFrames  # divides by total frames to calculate avg target confidence across whole video
        self.targetPercentage = (len(self.targetFrameList) / self.totalFrames) * 100
        self.targetScreenTime = (len(self.targetFrameList) / json_data_parsed['videoMetadata']['FPS'])
        self.targetFrameList.sort()  # sort the frame numbers in the target frames list
        self.calculateTargetScreenTime(json_data_parsed)
        self.logger.info("The average target confidence across the whole video = " + str(self.averageTargetConfidence))
        self.logger.info("The highest target confidence across the whole video = " + str(self.targetConfidenceHi))
        self.logger.info("The highest target confidence frame num = " + str(self.targetConfidenceHiFrame))
        self.logger.info("The lowest target confidence across the whole video = " + str(self.targetConfidenceLo))
        self.logger.info("The lowest target confidence frame num = " + str(self.targetConfidenceLoFrame))
        self.logger.info("The target is on screen for " + str(self.targetPercentage) + "% of the video")
        self.logger.info("The target has " + str(self.targetScreenTime) + " seconds of screen time")
        self.logger.info(
            "List of frames that target was found in with confidence above threshold = " + str(self.targetFrameList))
        self.logger.info("List of time ranges where the target found:")
        for x in range(len(self.targetTimesPresent['startTime'])):
            self.logger.info("Start time: " + str(self.targetTimesPresent['startTime'][x]) + " End time: " + str(
                self.targetTimesPresent['endTime'][x]))

    def calculateAverageGenObjectConfidence(self, table):
        """ Calculates average gen objs confidence and finds the highest/lowest gen objs confidence with their specific frame number """

    self.logger.info("Calculating the average gen obj confidence across the whole video...")
    try:
        for entry in self.conn.scan(table, scanrange=Range(srow='row_0'), cols=[["cf1"]]):
            json_data_parsed = json.loads(entry.val)
            if 'GeneralObjectsDetected' in json_data_parsed['frameMetadata']:
                for x in json_data_parsed['frameMetadata']['GeneralObjectsDetected']:
                    obj = x.split(":")[0]  # splits the string to only collect the label
                    objConf = float(x.split(":")[1].strip(' %'))  # strips the float confidence value out of the string
                    if obj not in self.generalObjectsFoundAnalysisData.keys():  # if the label is in the analysis dict
                        self.generalObjectsFoundAnalysisData[obj] = {}
                        self.generalObjectsFoundAnalysisData[obj]['lowestConf'] = 100.0
                        self.generalObjectsFoundAnalysisData[obj]['highestConf'] = 0.0
                        self.generalObjectsFoundAnalysisData[obj]['averageConf'] = 0.0
                        self.generalObjectsFoundAnalysisData[obj][
                            'framesAboveThresh'] = []  # a list of the frames that had a confidence above the threshold
                        self.generalObjectsFoundAnalysisData[obj][
                            'screenTime'] = 0.0  # total amount of time where obj is present
                        self.generalObjectsFoundAnalysisData[obj][
                            'percentage'] = 0.0  # percentage of the video where obj is present
                    self.generalObjectsFoundAnalysisData[obj]['averageConf'] = \
                        self.generalObjectsFoundAnalysisData[obj][
                            'averageConf'] + objConf  # add confidence across whole video to later calculate the average
                    if objConf >= self.confidenceThresh:
                        (self.generalObjectsFoundAnalysisData[obj]['framesAboveThresh']).append(int(
                            json_data_parsed['frameMetadata'][
                                'frameNum']))  # if the conf is above the thresh, add it to the frame list for that object
                    if objConf > self.generalObjectsFoundAnalysisData[obj][
                        'highestConf']:  # if the new found label confidence is higher than current highest conf
                        self.generalObjectsFoundAnalysisData[obj][
                            'highestConf'] = objConf  # update the new highest confidence
                        self.generalObjectsFoundAnalysisData[obj]['highestConfFrame'] = int(
                            json_data_parsed['frameMetadata']['frameNum'])  # update the frameNum the conf was found in
                    if objConf < self.generalObjectsFoundAnalysisData[obj][
                        'lowestConf']:  # if the new found label confidence is lower than current lowest conf
                        self.generalObjectsFoundAnalysisData[obj][
                            'lowestConf'] = objConf  # update the new lowest confidence
                        self.generalObjectsFoundAnalysisData[obj]['lowestConfFrame'] = int(
                            json_data_parsed['frameMetadata']['frameNum'])  # update the frameNum the conf was found in
    except:
        self.logger.info("Failed to scan table in Accumulo! Shutting down conn")
        self.conn.close()
        raise ValueError("Failed to scan table in Accumulo! Shutting down conn")
    for label in self.generalObjectsFoundAnalysisData.keys():
        self.generalObjectsFoundAnalysisData[label]['averageConf'] = self.generalObjectsFoundAnalysisData[label][
                                                                         'averageConf'] / self.totalFrames  # divide by the total frames to calculate average confidence for each gen obj across whole video
        self.generalObjectsFoundAnalysisData[label]['percentage'] = str(
            (len(self.generalObjectsFoundAnalysisData[label]['framesAboveThresh']) / self.totalFrames) * 100) + "%"
        self.generalObjectsFoundAnalysisData[label]['screenTime'] = str(
            len(self.generalObjectsFoundAnalysisData[label]['framesAboveThresh']) / json_data_parsed['videoMetadata'][
                'FPS']) + " seconds"
        (self.generalObjectsFoundAnalysisData[label]['framesAboveThresh']).sort()
    self.calculateObjScreenTime(json_data_parsed)
    self.logger.info("Analysis data on general objects = " + str(self.generalObjectsFoundAnalysisData))
    self.conn.close()


def makeFinalJson(self):
    """ Prepares the final json with the collected analysis data """


self.finalJson['avgTargetConfidence'] = self.averageTargetConfidence
self.finalJson['highestTargetConfidence'] = self.targetConfidenceHi
self.finalJson['lowestTargetConfidence'] = self.targetConfidenceLo
self.finalJson['highestTargetConfidenceFrame'] = self.targetConfidenceHiFrame
self.finalJson['lowestTargetConfidenceFrame'] = self.targetConfidenceLoFrame
self.finalJson['targetFrameList'] = self.targetFrameList
self.finalJson['genObjsAnalysis'] = self.generalObjectsFoundAnalysisData


def pushResultsToDB(self, table):
    """ Pushes final json to accumulo under 'videoname_analysis' """


self.logger.info("Pushing analysis results to Accumulo under table name " + table + "_analysis")
try:
    self.conn = Accumulo(host="localhost", port=50096, user="root", password="RoadRally4321")
except:
    self.logger.info("Failed to connect to Accumulo")
    raise ValueError("Failed to make connection to accumulo!\n")
table = table + "_analysis"
if not self.conn.table_exists(table):
    self.conn.create_table(table)
m = Mutation("row_1")  # one row that contains the full analysis json
self.finalJson = json.dumps(self.finalJson)
m.put(cf="cf1", cq="cq1", val=self.finalJson)
self.conn.write(table, m)
self.conn.close()
self.logger.info("Pushed analysis results to Accumulo")


def performAnalysis(self, table):
    """ Runs analysis """


self.logger.info("Performing video analysis...")
self.calculateAverageTargetConfidence(table)
self.calculateAverageGenObjectConfidence(table)
self.makeFinalJson()
self.pushResultsToDB(table)


def run(self, table):
    """ Launches the analysis """


if self.readyForAnalysis(table):
    self.performAnalysis(table)


def main():
    """ Auto run main method """


vidanalysis = videoAnalysis()
vidanalysis.run("vid_mp4")

if __name__ == "__main__":
    main()

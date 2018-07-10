import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


class Analysis(object):

    def __init__(self):
        self.all_jsons = []
        self.filtered_jsons = []
    
    def pull_jsons(self):
        # Consuming all messages from accumulo topic, will change for database
        consumer = Consumer.initialize("accumulo")
        for m in consumer:
            json_data = m.value
            self.all_jsons.append(json.loads(json_data))
    
    def filter_jsons(self):
        for j in self.all_jsons:
            if 'foundTargetWithConfidence' in j:
                self.filtered_jsons.append(j)
    
    def printj(self):
        for j in self.filtered_jsons:
            print json.dumps(j, indent=4, sort_keys=True)
    


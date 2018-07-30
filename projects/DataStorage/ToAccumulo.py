# import the necessary packages
import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *

class shipToAccumulo(object):

    def __init__(self): 
        """ Constructor """
        self.logger = Utilities.setup_logger("ToAccumulo", "../../logs/shipToAccumulo.log")
        self.validate_arg_parse()
        
    def validate_arg_parse(self):
        """ Validates arg parser """
        # Parser to parse arguments passed
        parser = argparse.ArgumentParser()
        
        parser.add_argument('--topic_name_in',
        help = "topic that it is pulling from",
        type = str,
        required = False,
        default = "Accumulo")
        
        args = parser.parse_args()
        
        if args.topic_name_in:
            self.topic_name_in = args.topic_name_in
        
    def run(self):
        self.logger.info("Shipping to accumulo...")
        consumer = Consumer.initialize(self.topic_name_in)
        for m in consumer:
            conn = Accumulo(host="localhost", port=50096, user="root", password="RoadRally4321")
            json_data_parsed = json.loads(json_data) #put json data back into dictionary
            frameNum = json_data_parsed['frameMetadata']['frameNum']
            table = json_data_parsed['videoMetadata']['videoName'] #get the video name and set that as the table name
            table = table.replace('.', '_')
            table = table.encode('ascii', 'ignore')
            if not conn.table_exists(table):
                conn.create_table(table)
            m = Mutation("row_%d"%frameNum)  #table row number is the frame number
            m.put(cf="cf2", cq="cq2", val = json_data_parsed['imageBase64'])   #saves the frame image separately from the metadata
            if 'LabeledImage' in json_data_parsed.keys():
                m.put(cf="cf3", cq="cq3", val = json_data_parsed['LabeledImage'])  #saves the labeled image separately from the metadata
                json_data_parsed.pop('LabeledImage', None) #delete the base64 representation of the labeled frame
            json_data_parsed.pop('imageBase64', None)  #delete the base64 representation of the frame
            json_data = json.dumps(json_data_parsed)
            m.put(cf="cf1", cq="cq1", val=json_data)   #set the first column to now only the metadata.
            conn.write(table, m)
            conn.close()
        consumer.close()
        self.logger.info("Accumulo consumer closed")





def main():
    """ Auto run main method """
    accumuloOut = shipToAccumulo()
    accumuloOut.run()
    


if __name__=="__main__":
        main()

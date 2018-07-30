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
            self.logger.info("sending to accum...")
        consumer.close()
        self.logger.info("Frame labeling consumer closed")





def main():
    """ Auto run main method """
    accumuloOut = shipToAccumulo()
    accumuloOut.run()
    


if __name__=="__main__":
        main()

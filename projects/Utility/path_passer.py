from utilities import *

class PathPasser(object):

    def __init__(self):
        """ Constructor """
        self.validate_arg_parse()
 
 
    def validate_arg_parse(self):
        """ Validates arg parser """
        parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    
        parser.add_argument('--video_path', 
            help = 'Path to video for processing',
            type = str, 
            required = True)

        parser.add_argument('--topic_name_out', 
            help = 'Topic pushed on',
            type = str, 
            required = False,
            default = "pathfinder")
    
        args = parser.parse_args()
    
        self.video_path = args.video_path
        self.topic_name_out = args.topic_name_out


    def run(self):
        """ Runs paths """
        json_data = json.dumps(self.video_path)
        Utilities.exportJson(json_data, self.topic_name_out)    # export updated Json files to kafka topic 'pathfinder'


def main():
    """ Auto run main method """
    p = PathPasser()
    p.run()


if __name__ == "__main__":
    main()


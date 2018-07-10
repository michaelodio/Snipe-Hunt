from kafka_manager import *


def main():
        """ Auto run main method """
        topic_name = 'FrameFeeder'
        data = [{"frameNum": 1, "timeStamp": 10, "imageBase64": "234gr83hen"},
                {"frameNum": 2, "timeStamp": 20, "imageBase64": "43hfhuf6b3"},
                {"frameNum": 3, "timeStamp": 30, "imageBase64": "9fbufbh434"}]
        
        #Manager.start_server()
        
        # Manager.clear_topic('TutorialTopic')
        Manager.list_topics()
        
        Producer.push_jsons(topic_name, data)
        Consumer.pull_jsons(topic_name)


if __name__ == '__main__':
    main()

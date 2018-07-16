import logging

class Logger(object):

    @staticmethod
    def initilaize(fname):
        logging.basicConfig(
            filename = fname, 
            level = logging.DEBUG,
            format = '%(asctime)s    %(levelname)s: %(message)s',
            datefmt = '%Y.%m.%d    %I:%M:%S %p')

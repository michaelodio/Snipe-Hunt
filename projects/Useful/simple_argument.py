# import necessary packages
import argparse

# construct the arg parse and parse args
ap = argparse.ArgumentParser()

# add name parameter, expreesed as -n or -name and required means that the parameter must be passed
ap.add_argument("-n", "--name", required=True,
                help="name of user")

ap.add_argument("-m", "--model", required=True,
                help="model name")

# parse command line arguments
args = vars(ap.parse_args())

# diplay message
print "Hi there {}, its nice to meet you!".format(args["name"])
print "You are a model {}!".format(args["model"])


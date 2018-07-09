import subprocess


def bash(bash_command, *positional_parameters, **keyword_parameters):
    """ Launches bash scripts """
    new_directory = None
    
    if('directory'  in keyword_parameters):
        new_directory = keyword_parameters['directory']
    
    process = subprocess.Popen(bash_command.split(), shell=False, stdout=subprocess.PIPE, cwd=new_directory)
    output, error = process.communicate()    
    if error != None:
        print "Error: " + error
    print "Output: " + output


def main():
    bash("ls -a", directory="../")


if __name__=="__main__":
    main()

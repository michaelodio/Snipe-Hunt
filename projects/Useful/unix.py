import os
os.system('ls')


os.system('/home/bt-intern5/Apps/kafka/bin/kafka-topics.sh --zookeeper localhost:200 --delete ')


import subprocess
time = subprocess.check_output('date')
print 'It is ', time
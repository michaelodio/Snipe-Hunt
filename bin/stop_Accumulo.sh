cd ../res/Apps/accumulo-1.9.1/
./bin/stop-all.sh 

cd ../hadoop-2.6.5/
sbin/stop-dfs.sh 

cd ../kafka/
sudo bin/zookeeper-server-stop.sh config/zookeeper.properties > bin/zookeeper-log.txt &
echo Zookeeper stopped




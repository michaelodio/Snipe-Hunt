cd ../res/Apps/kafka/
sudo bin/zookeeper-server-start.sh config/zookeeper.properties > bin/zookeeper-log.txt &
echo Zookeeper started

cd ../hadoop-2.6.5/
bin/hdfs namenode -format
bin/hdfs datanode -format 
sbin/start-dfs.sh 

cd ../accumulo-1.9.1/
./bin/accumulo init 
./bin/start-all.sh 
./bin/accumulo proxy -p proxy/proxy.properties 

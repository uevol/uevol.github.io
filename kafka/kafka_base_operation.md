# KAFKA

## 1. 创建kafka

./bin/kafka-topics.sh --create --zookeeper zk.service.consul:2181/common_kafka --replication-factor 1 --partitions 1 --topic logMonitor

## 2. 查看topic

./bin/kafka-topics.sh --list --zookeeper zk.service.consul:2181/common_kafka

## 3. 删除topic

./bin/kafka-topics.sh --delete --zookeeper zk.service.consul:2181/common_kafka --topic logMonitor

## 4. 消费

./bin/kafka-console-consumer.sh --zookeeper=zk.service.consul:2181/common_kafka --topic logMonitor --from-beginning

## 5. 查看topic详情

kafka-topics --describe --zookeeper=zk.service.consul:2181/common_kafka --topic mydemo5

## 6. 查看正在运行的消费组

kafka-consumer-groups.sh --bootstrap-server master:9092 --list --new-consumer

## 7. 计算消息的消息堆积情况

kafka-consumer-groups.sh --bootstrap-server master:9092 --describe --group  group_id

    ####详细说明
    LogEndOffset：下一条将要被加入到日志的消息的位移
    CurrentOffset： 当前消费的位移
    LAG： 消息堆积量
    消息堆积量：消息中间件服务端中所留存的消息与消费掉的消息之间的差值即为消息堆积量也称之为消费滞后量

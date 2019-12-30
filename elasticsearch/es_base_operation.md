# elasticsearch

## 1. docker 安装

+ 拉取镜像

```shell
docker pull elasticsearch:5.4
```

+ 启动es镜像

```shell
docker run -d --name es -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:.5.4
```

## 2. 通过_cat API查看es集群和节点状态

+ 集群是否健康

```shell
curl http://localhost:9200/_cat/health\?v
```

+ 获取集群的节点列表

```shell
curl http://localhost:9200/_cat/nodes\?v
```

## 3. 索引管理

+ 查看索引

```shell
curl http://localhost:9200/_cat/indices\?v
```

+ 创建索引

```shell
curl -XPUT http://localhost:9200/myindex -d '{
    "mappings" : {
        "mylog" : {
        "_all" : {
            "enabled" : true
        },
        "dynamic_templates" : [
            {
            "strings_as_keywords" : {
                "match_mapping_type" : "string",
                "mapping" : {
                "norms" : "false",
                "type" : "keyword"
                }
            }
            }
        ],
        "properties" : {
            "log" : {
            "type" : "keyword",
            "include_in_all" : false
            }
        }
        }
    }
}'
```

+ 删除索引

```shell
curl -XDELETE http://localhost:9200/myindex
```

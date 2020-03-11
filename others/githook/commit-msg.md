# git commit msg格式规范校验

## 1. commit规范

代码提交规范为: commit分类 + 提交描述，commit分类如下：

+ bugfix - 线上功能 bug
+ sprintfix - 功能模块未上线部分 bug
+ minor - 不重要的修改（换行，拼写错误等）
+ feature - 新功能说明
+ docs - 文档
+ refactor - 重构（即不是新增功能，也不是修改bug的代码变动）

## git hooks校验

在.git/hooks目录下有很多钩子，我们可以根据需要自定义不同的内容，修改commit-msg配置git commit msg校验

+ 首先将commit-msg.sample 改为 commit-msg
+ 将里面的内容修改为下面内容

```shell
#!/bin/sh
MSG=`awk '{printf("%s",$0)}' $1`
if [[ $MSG =~ ^(feature|bugfix|sprintfix|refactor|docs|minor):.*$ ]]
then
    echo "\033[32m commit success! \033[0m"
else
    echo "\033[31m Error: the commit message is irregular \033[m"
    echo "\033[31m Error: type must be one of [feature,bugfix,sprintfix,docs,minor,refactor] \033[m"
    echo "\033[31m eg: feature: add commit-msg function \033[m"
    exit 1
fi
```

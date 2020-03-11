# 运维开发人员通用规范

此规范目前仅适用于SAAS开发人员，包括前端和后端开发人员，其他非saas开发可参考

## 1. 开发规范说明

### 1.1 目录结构规范

#### 1.1.1 后端

+ home_application应用仅用于首页加载，禁止在其中写入业务逻辑
+ 业务逻辑放入自行创建的模块

#### 1.1.2 前端

+ frontend为前端工程目录，所有前端文件统一存放该目录，前端文件禁止放入该目录之外的目录

#### 1.1.3 公共

+ 要求做好工程结构规范化，开发人员根据实际开发需求在各自根目录下创建模块目录
+ 模块目录命名要求见名知意，使用下划线，如：home_application
+ 如需编写说明文档，必须使用[markdown](http://xianbai.me/learn-md/index.html)编写，放置合适位置

## 2. 编码规范

编码规范可以使新开发人员快速掌握代码，然后编写出其他开发人员可以快速轻松理解的代码！

### 2.1 后端编码规范

+ 后端编码规范参考[Google 开源项目风格指南 - Python 风格指南](https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/contents/)
+ [配置pre-commit](../githook/pre-commit.md)，使用flake8进行静态检查，包括逻辑错误、复杂度和编码风格检查

### 2.2 前端编码规范

前端编码规范建议参考以下规范一种，前端人员讨论决定，希望前端人员可以在本次项目后，结合实际，选择其中一种规范作为后续上海开发人员前端开发编码规范，强制严格准守

+ 参考规范

  + [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
  + [Google JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html)
  + [Idiomatic JavaScript Style Guide](https://github.com/rwaldron/idiomatic.js)
  + [JavaScript Standard Style Guide](https://github.com/standard/standard)

+ [配置pre-commit](../githook/pre-commit.md)
  使用pre-commit进行自动检查，可直接在pre-commit-config.yaml文件添加hook。
  默认配置了jshint，如需使用，取消注释即可

  + [jshit hook](github.com/pre-commit/mirrors-jshint)

## 3. 提交规范

### 3.1 分支管理

+ 主分支（master）保持随时可用，禁止向master分支推送或发起合并请求，当然也会通过权限配置禁止
+ 开发分支（dev）用于提交代码合并请求，所有人员均可发起合并请求
+ 个人分支，所有开发人员在自己的本地个人分支进行开发，开发完成后推送到远程仓库的个人分支，最后向dev分支发起合并请求

### 3.2 提交规范

+ 代码提交规范为: `<type>: <subject>`

  **commit分类如下:**

  + bugfix - 线上功能 bug
  + sprintfix - 功能模块未上线部分 bug
  + minor - 不重要的修改（换行，拼写错误等）
  + feature - 新功能说明
  + docs - 文档
  + refactor - 重构（即不是新增功能，也不是修改bug的代码变动）
  + test - 增加测试

  **subject规范入下:**
  + 以动词开头，使用第一人称现在时，比如change，而不是changed或changes
  + 第一个字母小写
  + 结尾不加句号（.）

+ [配置commit-msg](../githook/commit-msg.md)
  使用 git hook commit-msg 规范 git commit message

+ 上班拉取dev分支最新代码
  **禁止长时间不拉取更新代码，导致本地开发分支与master分支偏离越来越远，合并代码冲突解决困难**
+ 下班提交代码，防止代码丢失
  **禁止长时间不提交代码，导致本地开发分支与master分支偏离越来越远，合并代码冲突解决困难**

## 4. Code Review

+ 根据开发进度，不定期进行不定规模的code review，希望各开发人员按以上规范编码
+ 规范方面，针对**较强个性编码人员**，会有**较强定制化奖励**

## 5. 其他说明

+ 个人本地配置如数据库连接信息等，请新建配置文件conf/local.py，该文件已做ignore
+ 公共配置，根据环境放入对应模块

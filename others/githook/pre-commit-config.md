# pre-commit 安装配置

[pre-commit官方文档]()

## 1. 快速安装配置pre-commit

### 1.1 安装

```shell
# 安装
pip install pre-commit

# 检查是否安装成功
pre-commit --version
```

### 1.2 添加pre-commit配置文件

```shell
# 在仓库根目录添加
pre-commit sample-config > pre-commit-config.yaml
```

默认生成如下配置文件：

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
```

### 1.3 安装git hook脚本

```shell
# 项目仓库根目录执行安装命令
# 脚本安装在 `.git/hooks` 目录，之后每次commit代码时，会自动按配置文件中配置的规则检查，检查失败则提交失败
pre-commit install
```

## 2. pre-commit-config.yaml

*配置文件说明如下：*

![yaml配置文件说明](./pre-commit1.png)

## 3. 蓝鲸SAAS开发配置git-commit

*所有开发人员均须配置git-commit，使用统一的配配置文件。如果有特殊需求，提出后，评估可行统一修改，统一应用。*

[统一pre-commit配置文件](./pre-commit-config.yaml)，可直接把配置文件放入仓库，直接使用。

```yaml
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
default_language_version:
    python: python3

# 蓝鲸框架自带模块不检查
exclude: |
    (?x)(
        blueapps/|
        config/|
        blueking|
        settings.py
    )

repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v2.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
    -   id: requirements-txt-fixer

# flake8检查: 代码逻辑、pep8风格、复杂度
-   repo: https://gitlab.com/PyCQA/flake8
    rev: 3.7.1
    hooks:
    -   id: flake8
        args: [--max-complexity=12] # flake8官方推荐不超过12

# python第三方库安全漏洞检查
-   repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.1.0
    hooks:
    -   id: python-safety-dependencies-check

# python库导入检查
-   repo: https://github.com/pre-commit/mirrors-isort
    rev: 'v4.3.21'  # Use the revision sha / tag you want to point at
    hooks:
    -   id: isort
```

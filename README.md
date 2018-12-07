<div align="center">
  <img src="http://47.94.172.250:33334/static/frontend/head_portrait/logo@2x.png?t=1542252961.100895" width="150px">
  <br>
  <strong>问卷调查系统</strong>
</div>

# 开发环境

* Python (3.6.2)
* Django (2.1.3)
* Drf (3.9.0)

# 配置开发环境

## 使用虚拟环境(virturalenv)

```
pip3 install virtualenv

切换到项目目录下, 执行下面的命令
source venv/bin/activate

pip install -r requirements.txt

```

## 生成表结构

```
python manage.py makemigrations

python manage.py migrate
```

## 导入虚拟数据

```

```

## 启动项目

```
python manage.py runserver 0.0.0.0:9527
```

## 访问首页示例

## 常见问题

### 第一次执行这条语句报No changes detected

* 问题

```
python manage.py makemigrations
```

* 解决

在`APP`创建目录 migrations 并在里面创建__init__.py
```
mkdir APP_NAME/migrations
touch APP_NAME/migrations/__init__.py
```

### 模板渲染冲突

* 问题

```
django模板与vue.js冲突问题

django模板与vue.js的变量都是使用“{{”和“}}”包裹起来的，在渲染django模板时会先替代掉所有的“{{”和“}}”及被包裹在其中的内容，使得vue.js没有使用”{{“、”}}”来绑定变量。

```

* 解决

```
1、修改vue.js的默认的绑定符号
    Vue.config.delimiters = ["[[", "]]"];
    
2、使用模板的标签来输出`{{`、`}}`
    详情参见: https://docs.djangoproject.com/en/2.1/ref/templates/builtins/
    
3、禁用django模板渲染
    django标签 verbatim可以使包裹其中的代码不进行渲染保持原样输出
    {% verbatim %}
        {{ vue }}
    {% endverbatim %}
```

## 学习资料

```
# 我所认为的RESTful API最佳实践
http://www.scienjus.com/my-restful-api-best-practices/
```


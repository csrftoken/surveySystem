# surveySystem

Thank you to all the people who already contributed to this project！

---

## Introduction

后端使用 `django` & `DRF` 实现的 `restfulApi`  

前端使用 `vue` & `element-ui` 

## 开发环境

- Python 3.6.8  
- Django 2.1.5
- Drf 3.9.4 

## Quick Tutorial

### 使用虚拟环境(virturalenv)

```
pip3 install virtualenv

切换到项目目录下, 执行下面的命令
source venv/bin/activate

pip install -r requirements.txt

```

### 生成表结构

> 默认使用 `sqlite` 数据库

如果您想使用 `mysql` 数据库，请移步至常见问题（配置完成后，继续如下操作）。

```
python manage.py makemigrations

python manage.py migrate
```

### 导入虚拟数据

```
python manage.py loaddata init.json
```

### 启动项目

```
python manage.py runserver 0.0.0.0:8023

后台地址：

127.0.0.1:8023/admin/

账号密码 root root123456
```

### 效果图及代码结构图

![image](https://csrftoken.oss-cn-beijing.aliyuncs.com/github/6DBA4BE6-8EA5-4AA7-A673-457D30FE906A.png)

![image](https://csrftoken.oss-cn-beijing.aliyuncs.com/github/59A544B3-AE40-48DF-BA8A-2D58CB8CE9F2%2011.00.13.png)

## 常见问题

### mysql 数据库使用 

* 配置

```
# 在 settings.py 文件下找到 DATABASES 配置，修改为 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '数据库名称',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': '',  # 默认 127.0.0.1
        'PORT': '',  # 默认 3306
    }
}
```

然后连接至您的数据库终端

```
$ mysql -u 用户名 -p 密码
创建数据库，记得指定编码
>>> create database 数据库名称 default charset utf8;

```

### 第一次执行这条语句报No changes detected

* 问题

```
python manage.py makemigrations
```

* 解决

在 `web` 下面创建目录 migrations 并在里面创建__init__.py
```
mkdir web/migrations
touch web/migrations/__init__.py
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

### 文件下载

* 问题

```
 `response` 实现文件流下载, 且点击下载显示文件名称的问题
```

* 解决

```
response['Content-Type'] = 'application/octet-stream'
response['Content-Disposition'] = 'attachment; {}'.format(
    "filename*=utf-8''{}".format(quote(self.file_name))
)
```

## 学习资料

```
# 我所认为的RESTful API最佳实践
http://www.scienjus.com/my-restful-api-best-practices/

# `xlwt` 简单使用

import xlwt

xls = xlwt.Workbook(encoding="utf-8", style_compression=2)
sheet = xls.add_sheet("唯一码", cell_overwrite_ok=True)
sheet.write(0, 0, '号码')

for index, code in enumerate(queryset.iterator(), 1):
    sheet.write(index, 0, code.unique_code)

xls.save(`file_name`)

```

## Donate

如果本仓库对你有帮助，可以请作者喝杯白开水或Star。

Thanks ~

![image](https://csrftoken.oss-cn-beijing.aliyuncs.com/github/F83BF8B1-998B-4818-BDA9-1FAADEEFD16F.png?x-oss-process=image/resize,w_200)

## Support

```
2020 By Liuzhichao.
```

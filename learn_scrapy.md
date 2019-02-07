# scrapy  
1. 创建项目  
命令 *scrapy startproject projectname* 创建名为Projectname的项目,项目结构如下
```
.  # 项目根目录
│  scrapy.cfg  # scrapy部署时的配置文件
│
└─tutorial  # 项目模块，需要从这里引入
    │  items.py  # Items的定义，定义爬去的数据结构
    │  middlewares.py #  Middlewares的定义，定义爬取时的中间件
    │  pipelines.py #  Pipeline的定义，定义数据管道
    │  settings.py #  配置文件
    │  __init__.py   
    │
    ├─spiders # 放置Spiders的文件夹
    │  │  __init__.py
    │  │
    │  └─__pycache__
    └─__pycache__
```
2. 创建item  
修改items.py  
自定义的item需要继承scrapy.Item类,并定义类型为scrapy.Field的字段,使用与dict类似
3. 创建spider  
在spiders文件夹下创建新的spider *scrapy genspider spidername web-address*创建名为spidername,目标网址为web-address的spider  
spider需完成以下工作:
* 解析response
* 使用item保存数据
* 继续后续请求
4. 运行spider
*scrapy runspider spiderfile* 运行名为spider file文件的spider
5. 运行项目
6. 命令行模式
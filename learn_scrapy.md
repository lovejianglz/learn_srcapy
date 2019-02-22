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

在spiders文件夹下创建新的spider *scrapy genspider spidername web-domain*创建名为spidername,目标域为web-domain的spider  

spider需完成以下工作:  
* 解析response  
* 使用item保存数据  
* 产生继续后续请求  

自定义spider类需继承自scrapy.Spider。  
提供默认start_requests()方法请求start_urls，根据返回结果调用parse()方法解析结果，当spider关闭时调用closed()方法。  

4. 运行spider  

*scrapy runspider spiderfile* 运行名为spider file文件的spider  

5. 运行项目  

*scrapy crawl spidername* 运行名为spidername的爬虫  

6. 保存到文件  

*scrapy crawl spidername -o file*把spidername爬取到的内容输出保存到file文件中

7. 命令行模式  

*scrapy shell web_address*  以命令行的方式获得web_address网页的响应  

8. selector 选择器  

响应response，可用*response.css*或者“response.xpath”提取内容,并跟*.re*正则匹配。  

9. Downloader Middleware  
 
有以下作用：  
* 在scheduler调度出队列的request发送给downloader下载之前，经过download middleware
* 在下载后生成的Response发送给spider之前，也就是我们可以在生成response被spider解析之前对其进行修改  

需定义以下方法：
* process_request(request, spider)  
Request被Scrapy引擎调度给Downloader之前，process_request()方法就会被调用，也就是在Request从队列里调度出来到Downloader下载执行之前，我们都可以用process_request()方法对Request进行处理。
必须返回一下类型：
	* None ：继续调用优先级低的middleware，直到downloader把Request执行后得到response对象
	* Response对象 ：依次调用middleware的process_response()方法
	* Request对象 ： 把Request对象放回schedule中，等待重新调度
	* 抛出IgnoreRequest异常 ： 依次调用middleware的process_exceptiono()方法。
* process_response(request, response, spider)  
在downloader完成下载之后，会通过download middlware把Response发回给scrapy解析，此时调用process_response()方法处理Response。  
必须返回以下类型：
	* Request对象： 把Request对象放回schedule中，等待重新调度
	* Response对象： 调用更低优先级的downloader middleware中的process_response
	* 抛出IgnoreRequest异常: 回调Request的errback()方法，如果异常没有被处理，则会被忽略。 
* process_exception(request, response, spider)  
当downloader抛出异常时，调用该方法，必须返回以下类型：
	* None: 更低优先级的Downloader Middleware的process_exception()方法被依次调用，直到所有方法被调用完毕
	* Response对象：依次调用Downloader Middleware的process_response()方法
	* Request对象: 把Resquest对象重新放回schedule队列中，等待调度

10. 日志输出  
spider.loggger.debug("log message")  

11. Spider Middleware  
当Downloader生成Response之后，Response会被发送到Spider，在发送之前，Response会首先经过Spider Middleware处理，当Spider处理生成Item和Request之后，Item和Resquest还会经过Spider Middleware的处理。  
有如下作用：
* 在Response发送给Spider之前，对Response进行处理
* 在Spider生成Request发送给Schedule之前，对Reques进行处理
* 在Spider生成Item发送给Item Pipeline之前，对Item进行处理  

需实现下列任意方法：  
* process_spider_input(response, spider): 当Response被Spider Middleware处理时，调用本方法，返回以下内容：  
	* None: 调用其它Spider Middleware的process_spider_input()方法，直到Spider处理该Response  
	*  ***抛出异常***，Scrapy会调用Request的errback方法，errback的输出将会被重新输入到中间件中，使用Process_spider_output()方法处理。当其抛出异常时，则调用process_spider_exception()来处理。 
* process_spider_output(response, result, spider)：当Spider处理Response并返回结果后，调用本方法。必须返回Item或Request对象的 **可迭代对象** 
* process_spider_excption(response, exception, spider)：
当Spider或Spider Middleware的process_spider_input()方法抛出异常时，调用process_spider_exception()方法。 
	* None: 调用其它Spider Middleware的process_spider_exceptino()方法，直到所有的process_spider_exception都被调用。  
	* 可迭代对象: 调用其它middleware的 process_spider_output方法
* process_start_requests(start_requests, spider):  

12. Item Pipeline  

Item Pipeline主要有以下作用：
* 清洗数据
* 验证爬取数据，检查爬取字段
* 查重并丢弃重复内容
* 数据保存到数据库  

自定义类需实现以下方法: 
* process_item(item, spider) **必须实现** :对数据进行处理，须返回Item或者DropItem。
	* 返回Item对象: Item被传到优先级低的Pipeline处理，直到所有方法被调用完毕
	* 抛出DropItem异常: Item被丢弃
* open_spider(spider): Spider开启时自动调用。
* close_spider(spider): Spider关闭时自动调用，用于清理现场，关闭数据库等。
* from_crawler(cls, crawler) @classmethod: 利用crawler对象获得全局配置信息，然后创建一个Pipeline实例。  

在settings.py中配置使用pipline  
```
ITEM_PIPELINES = {
    "tutorial.pipelines.TextPipeline":100,
    'tutorial.pipelines.TutorialPipeline': 300,
}
```  
数值越小，越先被调用  

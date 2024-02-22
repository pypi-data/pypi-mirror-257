# 来自
> https://github.com/shengchenyang/AyugeSpiderTools/blob/master/docs//docs/intro/install.md
> 
> 增加个人使用的模板

## 安装

> `python 3.8+` 可以直接输入以下命令：

```shell
pip install gzspidertools
```

> 可选安装1，安装数据库相关的所有依赖：

```shell
pip install gzspidertools[database]
```

> 可选安装2，通过以下命令安装所有依赖：

```shell
pip install gzspidertools[all]
```

*注：详细的安装介绍请查看[安装指南](https://ayugespidertools.readthedocs.io/en/latest/intro/install.html)。*

## 用法
```shell
# 查看库版本
ayuge version

# 创建项目
ayuge startproject <project_name>

# 进入项目根目录
cd <project_name>

# 替换(覆盖)为真实的配置 .conf 文件：
# 这里是为了演示方便，正常情况是直接在 VIT 中的 .conf 文件填上你需要的配置即可
cp /root/mytemp/.conf DemoSpider/VIT/.conf

# 生成爬虫脚本
ayuge genspider <spider_name> <example.com>

# 运行脚本
scrapy crawl <spider_name>
# 注：也可以使用 ayuge crawl <spider_name>
```


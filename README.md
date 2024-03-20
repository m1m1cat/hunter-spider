# Hunter API 爬虫

这个脚本使用 Hunter API 来爬取指定单位的网站信息。Hunter API 提供了网络资产搜索功能，可以帮助您收集有关网站的各种信息，如IP地址、域名、状态码等。

## 使用方法

### 1. 准备工作

- 在 [Hunter 官网](https://hunter.qianxin.com/) 注册账号并获取 API Key。
- 准备一个包含单位名称的文本文件（例如 `units.txt`），每行一个单位名称。
- 如需更改查询语句请修改源码文件如下部分：
```
rule = f'icp.web_name="{unit.strip()}"' #设置查询语句
```

### 2. 运行脚本

在命令行中执行以下命令：

```bash
python hunter-spider.py --apikey YOUR_API_KEY --txt units.txt
```

确保将 `YOUR_API_KEY` 替换为您的 Hunter API Key，并将 `units.txt` 替换为您准备的单位名称文件路径。

## 参数说明

- `--apikey`: 您的 Hunter API Key。
- `--txt`: 包含单位名称的文本文件路径。
- `--start_page`: 爬取开始页数，默认为 1。
- `--end_page`: 爬取结束页数，默认为爬取全部数据。
- `--page_size`: 每页爬取数量，最大为 100，默认为 100。
- `--interval`: 每次请求 API 之间的时间间隔，默认为 3.0 秒。

## 注意事项

- 请确保单位名称文件中每行只包含一个单位名称。
- 请合理使用 Hunter API，遵守服务条款和使用政策。
- 遇到网络问题或异常时，脚本会记录错误日志并继续执行。
- 在使用本工具进行检测时，你应确保该行为符合当地的法律法规，并且已经取得了足够的授权。
- 如你在使用本工具的过程中存在任何非法行为，你需自行承担相应后果，我将不承担任何法律及连带责任。

# 捐赠支持
 如果这个项目对你有帮助，你可以给作者发烟 [点我](image/thanku.png)

# 参考链接
https://github.com/akkuman/HunterApi


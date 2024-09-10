# LeetCode刷题提醒脚本

## 简介

这是一个自动化脚本，用于检查指定用户的LeetCode（力扣）刷题数量，并发送桌面通知提醒用户继续刷题。该脚本使用Selenium WebDriver来爬取LeetCode个人主页上的题目解答数量，然后使用系统的通知功能发送一条"激励"消息。

## 功能

- 自动访问指定用户的LeetCode（力扣）个人主页
- 提取用户已解答的题目数量
- 发送包含刷题数量的桌面通知
- 如果无法获取题目数量，发送错误通知

## 依赖

- Python 3.6+
- Selenium WebDriver
- Chrome浏览器
- ChromeDriver
- notify-send

## 安装

1. 确保您的系统上安装了Python 3.6或更高版本。
2. 安装所需的Python包：
   ```
   pip install selenium
   ```
3. 安装Chrome浏览器（如果尚未安装）。
4. 下载与您的Chrome版本相匹配的ChromeDriver，并将其放置在`/usr/bin/`目录下（或更新脚本中的路径）。

## 配置

在脚本中，您可以修改以下变量来自定义行为：

- `username`: 您要查看的LeetCode用户名
- `notify_title`: 通知的标题
- `notify_icon`: 通知图标的路径(可以没有)
- `notify_timeout`: 通知显示的时间（毫秒）
- `notify_head`: 通知的应用名称

## 使用

运行脚本：

```
python leetcode_notify.py
```

脚本将自动执行以下操作：
1. 访问指定用户的LeetCode主页
2. 提取已解答的题目数量
3. 发送包含这个数量的桌面通知

如果无法获取题目数量（例如，由于网络问题），脚本将发送一个错误通知。

你可以将其与定时任务结合，或特定事件触发。

## 注意事项

- 该脚本使用了系统的`notify-send`命令来发送通知，确保您的系统支持此命令。

# 说明

- 该程序用于自动化刷阴阳师的妖气副本，主程序为: yysgo.py
- 使用前对阴阳师窗口左上角的用户名部分进行截图，并保存在 usr 目录下，要求使用 png 格式
- order.py 内的常量部分有关于窗口尺寸位置的设置，使用前请依照自己电脑的情况设置好

# 使用方法

```
python yysgo.py user_name what_to_do times code
```

- user_name: 用户名，即保存在 usr 目录下的截图文件名，不要加后缀
- what_to_do: 需要刷的副本，使用拼音首字母，如：鬼使黑-gsh。（order.py 提供鬼使黑和二口女两个副本的代码，用户可根据需要添加）
- times: 刷副本的次数
- code: 模式代码，3位2进制（使用10进制写）
    1. 第一位：刷副本的过程中是否接受好友的邀请
    2. 第二位：如果原房主退出，是否以房主身份继续
    3. 第三位：是否有特殊活动（某些鬼王活动会导致妖气封印按钮下移一位）

## eg.

```
python yysgo.py smm ekn 100 5
```
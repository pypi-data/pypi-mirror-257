## 用户指南

```python
pip3 install PyPoeApi==0.2.2
```

设置账户文件，使用PyPoeApi
```python
from PyPoeApi.poe_client import PoeClient, Chat

PoeClient.ACCOUNT_FILE = "设置文件位置"

async with await PoeClient.create() as poe_client:
    chat = Chat()

    image_url = await poe_client.ask(bot_name="Playground-v2",
                                  question="白天，下雨，沙滩，美女，长发，跳舞",
                                  chat=chat)
    print(image_url)

```
ACCOUNT_FILE格式如下
```yaml
accounts:
- Claude-instant-100k: false
  formkey: ""
  p_b: ""
  limit: true
date: 2024-02-08
hour: 9
```
文件格式为yaml  
accounts是数组  
- p_b和formkey是登录的cookie，通过浏览器或者抓包都可以获取到，为固定值 
- limit表示账户是否限制，目前POE采用计算点，免费的用户具有3000个计算点，每个模型的每个消息计算点都不一样，一旦达到了总计算点，会使limit为true    

date用于标志是什么时候，由于计算点数每天会自动重置，当日期超过date的话，会重置上面每个账户的limit为false  
hour指出从每天的什么时候开始更新

## 借鉴
https://github.com/canxin121/Async-Poe-Client
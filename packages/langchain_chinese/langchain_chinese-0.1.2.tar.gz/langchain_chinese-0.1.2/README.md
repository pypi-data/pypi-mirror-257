**langchain_chinese** 的目标是提供中文大语言模型和中文友好的`langchain`工具。

## 安装

你可以使用 pip 安装：
```
pip install -U langchain_chinese
```

或者使用 poetry 安装：
```
poetry add langchain_chinese
```

## 使用

### invoke
```python
from langchain_chinese import ZhipuAIChat
llm = ZhipuAIChat()
llm.invoke("讲个笑话来听吧")
```

```
AIMessage(content='好的，我来给您讲一个幽默的笑话：\n\n有一天，小明迟到了，老师问他：“你为什么迟到？”\n小明回答说：“老师，我今天看到一块牌子上写着‘学校慢行’，所以我就慢慢地走来了。”')
```

### stream
```python
llm.invoke("讲个笑话来听吧")
```

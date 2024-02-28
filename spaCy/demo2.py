import spacy

nlp = spacy.load("zh_core_web_sm")
text = "这是第一句。这是第二句。"
doc = nlp(text)

# 查找句子的开始和结束索引
start_index = doc[0].i
end_index = doc[-1].i

# 创建一个包含两个句子的Span对象
span = doc[start_index:end_index+1]

print(type(span))  # 输出 "<class 'spacy.tokens.span.Span'>"
print(span.text)  # 输出 "这是第一句。这是第二句。"

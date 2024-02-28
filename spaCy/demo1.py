import spacy

# 加载中文模型
nlp = spacy.load("zh_core_web_sm")

# 示例文本
with open("spaCy/demo1.txt", "r", encoding="utf-8") as f:
    text = f.read()
# 清理换行符
text = text.replace("\n", " ").strip()

# 使用spaCy进行处理
doc = nlp(text)

# 创建词汇表
speechVerbs = ["说", "道", "告诉", "问", "回答"]

# 提取句子
sentences = [sent for sent in doc.sents]

# TODO：
# 句子合并，有些说话内容是多句话，所以将多句话合并成一句话，用引号来判断
# 句子打断，有些说话旁白和说话内容在同一句话中，需要打断成旁白和说话内容两句话
# 说话内容找主人，找不到主人的就先当做旁白处理

# 检查每个句子
for i, sent in enumerate(sentences):
    print(f">>>> {i + 1}: {sent.text}")
    if "“" in sent.text and "”" in sent.text:
        print(f"说话内容：{sent.text}")
        # 检查前一个句子
        if i > 0:
            for speechVerb in speechVerbs:
                if speechVerb in sentences[i - 1].text:
                    print(f"说话动作（前）：{sentences[i - 1].text}")
        
        # 检查后一个句子
        if i < len(sentences) - 1:
            for speechVerb in speechVerbs:
                if speechVerb in sentences[i + 1].text:
                    print(f"说话动作（后）：{sentences[i + 1].text}")

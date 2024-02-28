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
# 提取句子
sentences = [sent for sent in doc.sents]

for i, sent in enumerate(sentences):
    print(f">>>> {i}: {sent.text}")

print("------------------")

# 句子打断，有些说话旁白和说话内容在同一句话中，需要打断成旁白和说话内容两句话
def break_sentences(sentences, speech_verbs):
    broken_sentences = []

    for sent in sentences:
        tokens = list(sent)
        break_points = []

        # 如果句子的开头和结尾是引号，不进行拆分
        if sent.text.startswith("“") and sent.text.endswith("”") and sent.text.count("“") == 1 and sent.text.count("”") == 1:
            broken_sentences.append(sent)
            continue

        # 查找说话动词后面的标点符号位置
        for i, token in enumerate(tokens):
            if token.text in speech_verbs:
                for j in range(i + 1, len(tokens)):
                    if tokens[j].text == "“":
                        break_points.append(j-1) 
                        break

        # 如果找到了打断点，将句子拆分为多个部分
        if break_points:
            start = 0
            for point in break_points:
                broken_text = (sent[start:point+1].text)
                start = point + 1
                doc = nlp(broken_text)
                span = doc[:]
                broken_sentences.append(span)
            broken_text = (sent[start:].text)
            doc = nlp(broken_text)
            span = doc[:]
            broken_sentences.append(span)
        else:
            broken_sentences.append(sent)

    return broken_sentences

# 创建词汇表
speechVerbs = ["说", "道", "告诉", "问", "回答"]

sentencesBroken = break_sentences(sentences, speechVerbs)
for i, sent in enumerate(sentencesBroken):
    print(f">>>> {i}: {sent}")


# 句子合并，有些说话内容是多句话，所以将多句话合并成一句话，用引号来判断
def merge_sentences(sentences, max_merge_count=3):
    sentences_merged = []
    i = 0

    while i < len(sentences):
        sent = sentences[i]

        # 如果句子包含“但没有”，则尝试合并
        if "“" in sent.text and "”" not in sent.text:
            merge_count = 0
            merged_text = sent.text
            temp_i = i  # 临时存储当前索引

            # 查找后续句子，直到找到”为止，或达到最大合并数量
            while temp_i < len(sentences) - 1 and merge_count < max_merge_count:
                temp_i += 1
                merge_count += 1
                merged_text += sentences[temp_i].text
                if "”" in sentences[temp_i].text:
                    break

            # 如果在范围内找到”，则进行合并
            if "”" in sentences[temp_i].text:
                sentences_merged.append(merged_text)
                i = temp_i
            else:
                # 如果在范围内没有找到”，则取消合并
                for j in range(i, temp_i + 1):
                    sentences_merged.append(sentences[j].text)
                i = temp_i
        else:
            sentences_merged.append(sent.text)

        i += 1
    
    return sentences_merged

# sentencesMerged = merge_sentences(sentencesBroken, 5)

# # 输出合并后的句子
# for i, sent in enumerate(sentencesMerged):
#     print(f">>>> {i}: {sent}")


# TODO：


# 说话内容找主人，找不到主人的就先当做旁白处理


# # 检查每个句子
# for i, sent in enumerate(sentences):
#     print(f">>>> {i + 1}: {sent.text}")
#     if "“" in sent.text and "”" in sent.text:
#         print(f"说话内容：{sent.text}")
#         # 检查前一个句子
#         if i > 0:
#             for speechVerb in speechVerbs:
#                 if speechVerb in sentences[i - 1].text:
#                     print(f"说话动作（前）：{sentences[i - 1].text}")
        
#         # 检查后一个句子
#         if i < len(sentences) - 1:
#             for speechVerb in speechVerbs:
#                 if speechVerb in sentences[i + 1].text:
#                     print(f"说话动作（后）：{sentences[i + 1].text}")

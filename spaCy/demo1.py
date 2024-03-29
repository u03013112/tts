import spacy

# 句子打断，有些说话旁白和说话内容在同一句话中，需要打断成旁白和说话内容两句话
def break_sentences(nlp,sentences, speech_verbs):
    broken_sentences = []

    for sent in sentences:
        tokens = list(sent)
        break_points = []

        # 如果句子的开头和结尾是引号，不进行拆分
        if sent.text.startswith("“") and sent.text.endswith("”") and sent.text.count("“") == 1 and sent.text.count("”") == 1:
            broken_sentences.append(sent)
            continue

        
        for i, token in enumerate(tokens):
            if token.text in speech_verbs:
                # 查找说话动词前面的”号位置
                for j in range(i - 1, -1, -1):
                    if tokens[j].text == "”":
                        break_points.append(j)
                        break

                # 查找说话动词后面的“号位置
                for j in range(i + 1, len(tokens)):
                    if tokens[j].text == "“":
                        break_points.append(j-1) 
                        break

        # 如果找到了打断点，将句子拆分为多个部分
        if break_points:
            # print(f"sentence: {sent.text}, break_points: {break_points}")
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

# 句子合并，有些说话内容是多句话，所以将多句话合并成一句话，用引号来判断
def merge_sentences(nlp,sentences, max_merge_count=3):
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
                doc = nlp(merged_text)
                span = doc[:]
                sentences_merged.append(span)
                i = temp_i
            else:
                # 如果在范围内没有找到”，则取消合并
                for j in range(i, temp_i + 1):
                    sentences_merged.append(sentences[j])
                i = temp_i
        else:
            sentences_merged.append(sent)

        i += 1
    
    return sentences_merged

# TODO：
# 说话内容找主人，找不到主人的就先当做旁白处理
# 找到真正的主人需要nlp，这里只是区分说话内容和旁白
def markSpeaker(sentences):
    retList = []
    for i, sent in enumerate(sentences):
        # 如果句子被引号包裹，则认为是说话内容
        if sent.text.startswith("“") and sent.text.endswith("”"):
            ret = {
                "type": "对话",
                "content": sent.text
            }
        else:
            ret = {
                "type": "旁白",
                "content": sent.text
            }

        retList.append(ret)
    return retList

def printSentences(sentences):
    for i, sent in enumerate(sentences):
        print(f">>>> {i}: {sent}")

def getDemoSentences(nlp):
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "demo1.txt")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    text = text.replace("\n", " ").strip()
    doc = nlp(text)
    sentences = [sent for sent in doc.sents]

    return sentences

def main():
    # 加载中文模型
    nlp = spacy.load("zh_core_web_sm")

    sentences = getDemoSentences(nlp)

    # 说话词汇表，不断的补充
    speechVerbs = ["说", "道", "便道", "告诉", "问", "回答"]
    sentencesBroken = break_sentences(nlp,sentences, speechVerbs)

    sentencesMerged = merge_sentences(nlp,sentencesBroken, 5)

    # printSentences(sentencesMerged)
    retList = markSpeaker(sentencesMerged)

    # print(retList)
    return retList


if __name__ == "__main__":
    main()

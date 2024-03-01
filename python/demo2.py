import torch
from TTS.api import TTS
from io import BytesIO

import sys
sys.path.append('../')

from spaCy.demo1 import main as main1

from pydub import AudioSegment


def demo2():
    # Get device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    speakers = ['Claribel Dervla', 'Daisy Studious', 'Gracie Wise', 'Tammie Ema', 'Alison Dietlinde', 'Ana Florence', 'Annmarie Nele', 'Asya Anara', 'Brenda Stern', 'Gitta Nikolina', 'Henriette Usha', 'Sofia Hellen', 'Tammy Grit', 'Tanja Adelina', 'Vjollca Johnnie', 'Andrew Chipper', 'Badr Odhiambo', 'Dionisio Schuyler', 'Royston Min', 'Viktor Eka', 'Abrahan Mack', 'Adde Michal', 'Baldur Sanjin', 'Craig Gutsy', 'Damien Black', 'Gilberto Mathias', 'Ilkin Urbano', 'Kazuhiko Atallah', 'Ludvig Milivoj', 'Suad Qasim', 'Torcull Diarmuid', 'Viktor Menelaos', 'Zacharie Aimilios', 'Nova Hogarth', 'Maja Ruoho', 'Uta Obando', 'Lidiya Szekeres', 'Chandra MacFarland', 'Szofi Granger', 'Camilla Holmström', 'Lilya Stainthorpe', 'Zofija Kendrick', 'Narelle Moon', 'Barbora MacLean', 'Alexandra Hisakawa', 'Alma María', 'Rosemary Okafor', 'Ige Behringer', 'Filip Traverse', 'Damjan Chapman', 'Wulf Carlevaro', 'Aaron Dreschner', 'Kumar Dahl', 'Eugenio Mataracı', 'Ferran Simen', 'Xavier Hayasaka', 'Luis Moray', 'Marcos Rudaski']

    retList = main1()
    # main1 返回类似{"type": "对话","content": ""}或{"type": "旁白","content": ""}的列表
    # 对话用speaker1，旁白用speaker2
    speaker1 = speakers[0]
    speaker2 = speakers[1]

    final_audio = AudioSegment.empty()

    for ret in retList:
        # print(ret["content"])
        tmpFilename = "../out/demo2Tmp.wav"
        if ret["type"] == "对话":
            tts.tts_to_file(text=ret["content"], speaker=speaker1, language="zh-cn", file_path=tmpFilename)
        else:
            tts.tts_to_file(text=ret["content"], speaker=speaker2, language="zh-cn", file_path=tmpFilename)

        audio_segment = AudioSegment.from_wav(tmpFilename)

        # 将当前音频片段拼接到最终音频中
        final_audio += audio_segment

    # 保存最终音频到文件
    final_audio.export("../out/demo2.wav", format="wav")    

if __name__ == "__main__":
    demo2()
    

from pyannote.audio import Pipeline
import pandas as pd


class SpeakerDiarization():
    def __init__(self,audio_path):
        self.audio_path = audio_path
        self.pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token="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")

      
    def connect_speakers(self,data):
        a=1
        i=0
        try:
            while i < len(data['start']) - a:
                if(data['speaker'][i] == data['speaker'][i+1]):
                    data['end'][i]=data['end'][i+1]
                    print(i)

                    #data=data.drop(axis="index",index=data.index[i+1])
                    data.drop(data.index[i+1],inplace=True)
                    data.reset_index(drop=True, inplace=True)
                    a=a+1
                
                else:
                    i=i+1
        except:
            print(data)
            print(data[i])
        finally:
            return data

    def return_speaker(self):
        
        diarization = self.pipeline(self.audio_path)
        data = pd.DataFrame(columns=['start','end','speaker'])  
        
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            data=data._append({'start': turn.start, 'end': turn.end, 'speaker': speaker}, ignore_index=True)
        if(len(data.index)>1):
            data=self.connect_speakers(data)
        return  data
  
 









'''
f = open(audio_path+"speakers"+".txt",mode='w',encoding = "utf-8")
for i in lista:
    f.write(i + '\n')
f.close()
'''

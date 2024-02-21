#import audio_transcription
from audiotranscription import audio_transcription
from audiotranscription import text_processing
import pandas as pd
#import text_processing

class ReturnTranscription():
    def __init__(self,model,audio_path,transcryption_model="Whisper"):
        if(transcryption_model == "Whisper"):
            self.model = model
            self.audio_path = audio_path
            self.audio_model = audio_transcription.WhisperAIToText(audio_path,model)
            self.text_processing = text_processing.TextProcessing()

    def return_transcription_without_punctuation(self):
        return self.audio_model.get_text_from_audio()['text']
    
    def return_transcription_with_punctuation(self):
        text = self.audio_model.get_text_from_audio()['text']
                
        #return self.text_processing.restore_punctuation(text)
    
    def return_trascription_with_timestamps(self):
        text=""
        result=self.audio_model.get_text_from_audio()
        for i in range(0,len(result['segments']),1):
            text = text + str("{:.2f}".format(result["segments"][i]["start"])) + "   " + str("{:.2f}".format(result["segments"][i]["end"])) + "   " + str(result["segments"][i]["text"])+"\n"
        return text
    def return_transcription_with_speakers(self):
        pass

if __name__ == "__main__":
    pass

#from google.cloud.speech_v2 import SpeechClient
#from google.cloud.speech_v2.types import cloud_speech
from abc import ABC, abstractmethod
import whisper


project_id = 0 # not used by now
timeout_time = 1000

class AudioToTextAbstract(ABC):
    @abstractmethod
    def get_text_from_audio(self, audio_path):
        pass
'''
class GoogleSpeechToText(AudioToTextAbstract):    
    def __init__(self, audio_time, audio_path , language = "en-GB",model="latest_long"):
        self.language = language
        self.model = model
        self.audio_time =  audio_time
        self.audio_path = audio_path

    #long video
    def get_text_from_audio(
        self,
        
        ) -> cloud_speech.BatchRecognizeResults:

        # Instantiates a client
        client = SpeechClient()
        config = cloud_speech.RecognitionConfig(
                auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
                language_codes=[self.language],
                model = self.model,
            )

        if(self.audio_time == "long"):
            

            file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=self.audio_path)

            request = cloud_speech.BatchRecognizeRequest(
                recognizer=f"projects/{project_id}/locations/global/recognizers/_",
                config=config,
                files=[file_metadata],
                recognition_output_config=cloud_speech.RecognitionOutputConfig(
                    inline_response_config=cloud_speech.InlineOutputConfig(),
                ),
            )

            # Transcribes the audio into text
            try:
                operation = client.batch_recognize(request=request)

                print("Waiting for operation to complete...")
                response = operation.result(timeout=timeout_time)
                text = ""
                for result in response.results[self.audio_path].transcript.results:
                    #print(f"Transcript: {result.alternatives[0].transcript}")
                    text = text + " " + str(result.alternatives[0].transcript)

                return text
                
            
            except ValueError: 
                return "Nie udało się zrozumieć mowy"
            
            except:
                return "Błąd"
        
        
        elif(self.audio_time == "short"):
            
            with open(self.audio_path, "rb") as f:
                content = f.read()

            request = cloud_speech.RecognizeRequest(
                recognizer=f"projects/{project_id}/locations/global/recognizers/_",
                config=config,
                content=content,
            )

            # Transcribes the audio into text
            try:
                response = client.recognize(request=request)

                #for result in response.results:
                #   print(f"Transcript: {result.alternatives[0].transcript}")
                text = ""
                for result in response.results:
                    text  = text + " " + result.alternatives[0].transcript
            
                return text
            
            except ValueError:
                return "Nie udało się zrozumieć mowy"
            
            except:
                return "Błąd"

        
        else:
            return "Bad audio_time argument"
'''
class WhisperAIToText(AudioToTextAbstract): 
    def __init__(self,audio_path,model="large"):
        self.audio_path=audio_path
        self.model=model

    def get_text_from_audio(self):
        try:
            model = whisper.load_model(self.model)
            result = model.transcribe(self.audio_path)
            return result
        except:
            return "Błąd w transkrypcji"

if __name__ == "__main__":
    pass

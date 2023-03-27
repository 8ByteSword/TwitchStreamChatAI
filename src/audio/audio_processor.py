from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech

from utils.audit_decorators import AuditBase

class AudioProcessor(AuditBase):
    def __init__(self, google_credentials_file):
        self.client = speech.SpeechClient.from_service_account_json(google_credentials_file)

    def process_audio(self, audio_file_path):
        audio_data = self._read_audio_file(audio_file_path)
        transcript = self._convert_speech_to_text(audio_data)
        return transcript

    def _read_audio_file(self, audio_file_path):
        audio = AudioSegment.from_file(audio_file_path, format="mp3")
        audio = audio.set_frame_rate(16000).set_channels(1)
        return audio.raw_data

    def _convert_speech_to_text(self, audio_data):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        response = self.client.recognize(config=config, audio=speech.RecognitionAudio(content=audio_data))
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        return transcript

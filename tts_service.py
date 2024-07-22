import hashlib
import os
from gtts import gTTS
from slugify import slugify

class TTSService:
    def __init__(self, audio_dir='audio_cache'):
        self.audio_dir = audio_dir
        os.makedirs(audio_dir, exist_ok=True)

    def create_slugified_filename(self, text):
        # Create a slugified filename with the first 10 and last 10 characters of the text
        slug = slugify(text[:10] + text[-10:])
        return slug[:255]  # Ensure the filename doesn't exceed filesystem limitations

    def get_audio(self, text, lang='en'):
        # Generate a unique hash for the text and language
        text_hash = hashlib.md5(f"{text}_{lang}".encode()).hexdigest()
        slugified_filename = self.create_slugified_filename(text)
        audio_filename = f"{text_hash}_{slugified_filename}.mp3"
        audio_path = os.path.join(self.audio_dir, audio_filename)

        # If audio file doesn't exist, generate it
        if not os.path.exists(audio_path):
            try:
                tts = gTTS(text=text, lang=lang)
                tts.save(audio_path)
            except ValueError:
                # Handle unsupported language
                print(f"Unsupported language: {lang}. Falling back to English.")
                tts = gTTS(text=text, lang='en')
                tts.save(audio_path)
            except Exception as e:
                print(f"Error generating audio: {str(e)}")
                return None

        return audio_path

tts_service = TTSService()
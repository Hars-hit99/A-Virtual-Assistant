import os
from gtts import gTTS
import pygame
import tempfile

pygame.mixer.init()

def speak(text: str) -> str:
    print(f"jarvis: {text}")
    try:
        tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            temp_path = f.name
        
        tts.save(temp_path)
        
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(20)
        
        pygame.mixer.music.unload()
        os.remove(temp_path)  
        
    except Exception as e:
        print(f"Speech error: {e}")
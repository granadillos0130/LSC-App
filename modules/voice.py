import pyttsx3
import speech_recognition as sr
import threading

class VoiceModule:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.set_spanish_voice()

    def set_spanish_voice(self):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        self.voice_id = None
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                self.voice_id = voice.id
                break
        engine.stop()

    def speak(self, text):
        if text.strip():
            def run():
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 1.0)
                if self.voice_id:
                    engine.setProperty('voice', self.voice_id)
                engine.say(text)
                engine.runAndWait()
                engine.stop()
            thread = threading.Thread(target=run)
            thread.daemon = True
            thread.start()

    def listen(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Escuchando...")
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language='es-CO')
                print(f"Escuché: {text}")
                return text
            except sr.WaitTimeoutError:
                print("No se detectó audio")
                return None
            except sr.UnknownValueError:
                print("No se entendió el audio")
                return None
            except sr.RequestError:
                print("Error de conexión con el servicio de voz")
                return None
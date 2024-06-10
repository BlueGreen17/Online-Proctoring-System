import speech_recognition as sr
import pyttsx3
import tkinter as tk
from threading import Thread
from datetime import datetime

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Exam Proctoring System")
        self.geometry("800x600")

        self.label_status = tk.Label(self, text="Listening for speech...", font=("Helvetica", 18, "bold"))
        self.label_status.pack(pady=20)

        self.text_output = tk.Text(self, height=20, width=100, wrap=tk.WORD, font=("Helvetica", 14))
        self.text_output.pack(pady=20)

        self.btn_clear = tk.Button(self, text="Clear", command=self.clear_output, font=("Helvetica", 12))
        self.btn_clear.pack(pady=10)

        # Start the listening thread
        self.start_listening_thread()

    def recognize_speech_from_mic(self, recognizer, microphone):
        """Transcribe speech from recorded from `microphone`."""
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        try:
            # Try recognize_google
            response["transcription"] = recognizer.recognize_google(audio)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            try:
                # Fallback to recognize_sphinx
                response["transcription"] = recognizer.recognize_sphinx(audio)
            except sr.RequestError:
                response["success"] = False
                response["error"] = "Sphinx API unavailable"
            except sr.UnknownValueError:
                response["error"] = "Unable to recognize speech"

        return response

    def listen_continuously(self):
        mic = sr.Microphone()

        while True:
            result = self.recognize_speech_from_mic(recognizer, mic)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if result["transcription"]:
                self.update_output(f"[{timestamp}] Speech detected: {result['transcription']}\n")
                print("Suspicious act detected")
                engine.say("Suspicious activity detected!")
                engine.runAndWait()
            elif result["error"]:
                self.update_output(f"[{timestamp}] Error: {result['error']}\n")
                print(f"ERROR: {result['error']}")
            else:
                self.update_output(f"[{timestamp}] No speech detected\n")

    def start_listening_thread(self):
        thread = Thread(target=self.listen_continuously)
        thread.daemon = True
        thread.start()

    def update_output(self, message):
        self.text_output.insert(tk.END, message)
        self.text_output.see(tk.END)  # Scroll to the bottom

    def clear_output(self):
        self.text_output.delete(1.0, tk.END)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()

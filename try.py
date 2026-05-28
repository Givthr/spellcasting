import random
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

engine.setProperty("rate", 160)


def speak(text):
    print(f"AI: {text}")
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening... (Speak now)")

        try:

            audio = r.listen(source, timeout=5)
      
            text = r.recognize_google(audio).lower()
        
            return text.replace(" ", "")
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""


def play_voice_spelling():
    words = ["python", "giraffe", "computer", "inventory", "django"]
    speak("Welcome to the voice spelling bee.")

    while True:
        word = random.choice(words)
        speak(f"Your word is... {word}")
        print(f"Target word: {word}")

        
        guess = get_audio()
        print(f"I heard: {guess}")

        if guess == word:
            speak("That is correct!")
        elif guess == "":
            speak("I didn't catch that.")
        else:
            speak(f"Not quite. I heard {guess}, but the correct spelling is {word}")

     
        speak("Would you like to play again? Say yes or no.")
        answer = get_audio()
        if "no" in answer:
            speak("Systems powering down. Goodbye.")
            break


if __name__ == "__main__":
    play_voice_spelling()

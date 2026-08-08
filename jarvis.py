import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import datetime
import os
import sys

# -----------------------------
# JARVIS SETTINGS
# -----------------------------

engine = pyttsx3.init()

# Change speaking speed
engine.setProperty("rate", 175)

# Voice selection
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)


# -----------------------------
# SPEAK FUNCTION
# -----------------------------

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()


# -----------------------------
# LISTEN FUNCTION
# -----------------------------

def take_command():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language="en-IN")
        print("YOU:", command)
        return command.lower()

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""

    except sr.RequestError:
        speak("I'm having trouble connecting to the speech service.")
        return ""


# -----------------------------
# GREETING
# -----------------------------

def wish_user():
    hour = datetime.datetime.now().hour

    if hour < 12:
        speak("Good morning.")
    elif hour < 18:
        speak("Good afternoon.")
    else:
        speak("Good evening.")

    speak("I am JARVIS. How can I help you?")


# -----------------------------
# COMMAND PROCESSING
# -----------------------------

def process_command(command):

    # Stop JARVIS
    if command in ["exit", "quit", "stop", "shutdown jarvis"]:
        speak("Shutting down. Goodbye.")
        sys.exit()

    # Time
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    # Date
    elif "date" in command:
        today = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {today}.")

    # Open YouTube
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    # Open Google
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    # Open GitHub
    elif "open github" in command:
        speak("Opening GitHub.")
        webbrowser.open("https://github.com")

    # Search Google
    elif command.startswith("search for"):
        search_text = command.replace("search for", "", 1).strip()

        if search_text:
            speak(f"Searching for {search_text}.")
            url = "https://www.google.com/search?q=" + search_text.replace(" ", "+")
            webbrowser.open(url)
        else:
            speak("What should I search for?")

    # Wikipedia
    elif command.startswith("wikipedia"):
        topic = command.replace("wikipedia", "", 1).strip()

        if topic:
            speak(f"Searching Wikipedia for {topic}.")
            try:
                result = wikipedia.summary(topic, sentences=2)
                speak(result)
            except Exception:
                speak("I couldn't find information about that topic.")
        else:
            speak("Please tell me what you want to know.")

    # Open VS Code
    elif "open vs code" in command or "open visual studio code" in command:
        speak("Opening Visual Studio Code.")

        try:
            os.system("code")
        except Exception:
            speak("I couldn't open Visual Studio Code.")

    # Open calculator
    elif "open calculator" in command:
        speak("Opening calculator.")

        if sys.platform == "win32":
            os.system("start calc")

    # Open Notepad
    elif "open notepad" in command:
        speak("Opening Notepad.")

        if sys.platform == "win32":
            os.system("start notepad")

    # Tell what it can do
    elif "what can you do" in command or "help" in command:
        speak(
            "I can tell you the time and date, "
            "open websites, search Google, search Wikipedia, "
            "open VS Code, open calculator, and open Notepad."
        )

    # Unknown command
    else:
        speak(
            "I don't know that command yet. "
            "You can teach me new commands by adding them to my program."
        )


# -----------------------------
# MAIN PROGRAM
# -----------------------------

if __name__ == "__main__":

    wish_user()

    while True:
        command = take_command()

        if command:
            process_command(command)

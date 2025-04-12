import tkinter as tk
import time
import webbrowser
import speech_recognition as sr
import datetime
import pyjokes
import pyttsx3
import requests  # Import requests to make API calls
import re

# GUI for voice command history
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("400x400")
history_label = tk.Label(root, text="Voice Command History:")
history_label.pack(pady=20)
history_text = tk.Text(root, width=40, height=10)
history_text.pack()

# Initialize the speech recognizer
r = sr.Recognizer()

def process_command(command):
    """Process the recognized command."""
    if command.lower() == "quit":
        return False
    elif "what time is it" in command.lower():
        current_time = datetime.datetime.now().strftime("%H:%M")
        print(current_time)
        engine = pyttsx3.init()
        engine.say(current_time)
        engine.runAndWait()
    elif "set timer" in command.lower():
        set_timer(command)  # Set timer based on the command
    elif "search" in command.lower():
        search_query = command.split(" ")[1:]
        webbrowser.open(f"https://www.google.com/search?q={' '.join(search_query)}")
    elif "tell a joke" in command.lower():
        joke = pyjokes.get_joke()  # Get a joke from pyjokes
        print(joke)
        engine = pyttsx3.init()
        engine.say(joke)  # Use text-to-speech to tell the joke
        engine.runAndWait()
    elif "weather" in command.lower():
        get_weather("Lewiston, Maine")  # Get weather for Lewiston, Maine
    elif "text to speech" in command.lower():
        text_to_speak = input("Enter text to speak: ")
        engine = pyttsx3.init()
        engine.say(text_to_speak)
        engine.runAndWait()
    else:
        history_text.insert(tk.END, f"{command}\n")
        history_text.see(tk.END)
    return True

def get_weather(city):
    """Fetch and announce the weather for the specified city."""
    api_key = "8512cfab5a846c22ac03704ee1c61f9e"  # Replace with your OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"  # Use imperial for Fahrenheit
    response = requests.get(url)
    data = response.json()
    
    if data["cod"] == 200:
        main = data["main"]
        weather = data["weather"][0]["description"]
        temp = main["temp"]
        weather_report = f"The current temperature in {city} is {temp:.1f}°F with {weather}."
        print(weather_report)

def set_timer(command):
    """Set a timer based on the recognized command."""
    # Use regex to find the number of minutes in the command
    match = re.search(r'(\d+)\s*minutes?|one minute|two minutes|three minutes|four minutes|five minutes|six minutes|seven minutes|eight minutes|nine minutes|ten minutes', command.lower())
    
    if match:
        # Check if the match is a number or a word
        if match.group(1):
            minutes = int(match.group(1))
        else:
            # Map word to number
            word_to_number = {
                "one minute": 1,
                "two minutes": 2,
                "three minutes": 3,
                "four minutes": 4,
                "five minutes": 5,
                "six minutes": 6,
                "seven minutes": 7,
                "eight minutes": 8,
                "nine minutes": 9,
                "ten minutes": 10
            }
            minutes = word_to_number[match.group(0)]
        
        print(f"Timer set for {minutes} minutes.")
        engine = pyttsx3.init()
        engine.say(f"Timer set for {minutes} minutes.")
        engine.runAndWait()
        
        # Countdown loop
        for remaining in range(minutes * 60, 0, -1):
            print(f"Time remaining: {remaining // 60} minutes and {remaining % 60} seconds")
            time.sleep(1)  # Wait for 1 second
        
        print("Timer complete!")
        engine.say("Timer complete!")
        engine.runAndWait()
    else:
        print("I couldn't understand the timer duration.")
        engine = pyttsx3.init()
        engine.say("I couldn't understand the timer duration.")
        engine.runAndWait()

# Continuous listening without rerunning script
with sr.Microphone() as source:
    print("Listening...")
    while True:
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print(f"Recognized: {text}")

            # Check for the activation phrase
            if "hey assistant" in text.lower():
                print("Activation phrase detected.")
                engine = pyttsx3.init()
                engine.say("Yes, my liege.")  # Respond with "Yes, my liege"
                engine.runAndWait()
                # Listen for the command after activation phrase
                audio = r.listen(source)
                command = r.recognize_google(audio)
                print(f"Command: {command}")
                if not process_command(command):
                    break  # Exit if the command is "quit"
            else:
                print("Activation phrase not detected.")
                
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

root.mainloop()

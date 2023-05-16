import socket
import speech_recognition as sr
import pyttsx3

# Function to get voice input from the user
def get_voice_input():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Speak now...")
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            speak_text(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            error_message = "Sorry, I could not understand your voice. Please try again."
            print(error_message)
            speak_text(error_message)
        except sr.RequestError:
            error_message = "Sorry, I'm having trouble accessing the speech recognition service."
            print(error_message)
            speak_text(error_message)

# Function to speak the given text
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to play the game
def play_game():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    speak_text("I salute Ovidiu !Welcome to Guess the Number! I'm thinking of a number between 1 and 100. Try to guess it.")

    while True:
        guess = get_voice_input()
        client_socket.send(guess.encode())

        response = client_socket.recv(1024).decode().strip()
        print(response)
        speak_text(response)

        if response.startswith("Correct"):
            speak_text("Congratulations! You guessed the number correctly.")
            break

    client_socket.close()

# Start the game
play_game()

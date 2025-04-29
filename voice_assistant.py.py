import speech_recognition as sr
import pywhatkit
import time
import winsound
import pyttsx3
import re
import json

should_exit = False  # Flag to exit the assistant

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    print("🔈", text)
    engine.say(text)
    engine.runAndWait()

# Sample recipes with nutritional information
recipes = {
    "maggi": {
        "steps": [
            "Boil 1 and a half cups of water in a pan.",
            "Add Maggi noodles and tastemaker.",
            "Cook for 2 minutes while stirring.",
            "Let it simmer for another minute.",
            "Your Maggi is ready to serve."
        ],
        "ingredients": [
            "1 and a half cups of water",
            "1 pack of Maggi noodles",
            "Maggi tastemaker"
        ],
        "nutrition": {
            "calories": "320 kcal",
            "protein": "6g",
            "carbs": "45g",
            "fat": "14g"
        }
    },
    "pasta": {
        "steps": [
            "Boil 1 liter of water in a pan.",
            "Add pasta and cook for 10 minutes.",
            "Drain water and add pasta sauce.",
            "Mix well and serve hot."
        ],
        "ingredients": [
            "1 liter of water",
            "1 pack of pasta",
            "Pasta sauce"
        ],
        "nutrition": {
            "calories": "400 kcal",
            "protein": "10g",
            "carbs": "60g",
            "fat": "15g"
        }
    }
}

# Globals to track recipe
current_recipe = {}
step_index = 0

# User Profile
user_profile = {
    "name": "User",
    "favorite_recipes": ["maggi", "pasta"],
    "allergies": ["peanut"],
    "preferences": {
        "spiciness": "mild",  # Could be 'mild', 'medium', 'spicy'
        "cuisine": "Indian"
    }
}

# Save and load user profile
def save_profile():
    with open('user_profile.json', 'w') as file:
        json.dump(user_profile, file)

def load_profile():
    global user_profile
    try:
        with open('user_profile.json', 'r') as file:
            user_profile = json.load(file)
    except FileNotFoundError:
        print("No existing profile found, creating a new one.")
        save_profile()

def update_user_preference(key, value):
    user_profile['preferences'][key] = value
    save_profile()
    speak(f"Your {key} preference has been updated to {value}.")

def suggest_recipe():
    if "spicy" in user_profile['preferences']['spiciness']:
        speak("I suggest trying Spicy Maggi or Spicy Pasta.")
    else:
        speak("How about trying a simple and mild Maggi or some Pasta?")

# Recipe commands
def listen_command():
    global should_exit
    global step_index
    global current_recipe

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("🗣️ You said:", command)

            if 'play' in command.lower():
                song_or_video = command.lower().replace('play', '').strip()
                print(f"🎬 Playing '{song_or_video}' on YouTube...")
                pywhatkit.playonyt(song_or_video)
                time.sleep(5)

            elif 'set a timer for' in command.lower():
                match = re.search(r"(\d+)\s*(minute|second)s?", command.lower())
                if match:
                    value = int(match.group(1))
                    unit = match.group(2)

                    seconds = value * 60 if 'minute' in unit else value
                    print(f"⏱️ Timer set for {value} {unit}(s)...")
                    time.sleep(seconds)
                    print("🔔 Time's up!")
                    winsound.PlaySound("timer_done.wav", winsound.SND_FILENAME)
                else:
                    print("⏱️ Could not understand timer duration.")

            elif 'start' in command.lower() and 'recipe' in command.lower():
                recipe_name = command.lower().split('start ')[-1].split(' recipe')[0]
                if recipe_name in recipes:
                    current_recipe = recipes[recipe_name]
                    step_index = 0
                    speak(f"Starting {recipe_name} recipe. Step 1: {current_recipe['steps'][0]}")
                else:
                    speak(f"Sorry, I don't have a recipe for {recipe_name}.")

            elif 'next step' in command.lower():
                if current_recipe and step_index + 1 < len(current_recipe['steps']):
                    step_index += 1
                    speak(f"Step {step_index + 1}: {current_recipe['steps'][step_index]}")
                else:
                    speak("No more steps remaining.")

            elif 'repeat step' in command.lower():
                if current_recipe:
                    speak(f"Repeating step {step_index + 1}: {current_recipe['steps'][step_index]}")
                else:
                    speak("No recipe in progress.")

            elif 'start over' in command.lower():
                if current_recipe:
                    step_index = 0
                    speak(f"Starting over. Step 1: {current_recipe['steps'][0]}")
                else:
                    speak("No recipe in progress.")

            elif 'nutritional information' in command.lower():
                if current_recipe:
                    nutrition_info = current_recipe['nutrition']
                    speak(f"The nutritional information for this recipe is: "
                          f"Calories: {nutrition_info['calories']}, "
                          f"Protein: {nutrition_info['protein']}, "
                          f"Carbs: {nutrition_info['carbs']}, "
                          f"Fat: {nutrition_info['fat']}.")
                else:
                    speak("No recipe in progress.")

            elif 'ingredients' in command.lower():
                if current_recipe:
                    ingredients = ", ".join(current_recipe['ingredients'])
                    speak(f"The ingredients for this recipe are: {ingredients}.")
                else:
                    speak("No recipe in progress.")

            elif 'suggest a recipe' in command.lower():
                suggest_recipe()

            # Updated command for spice level change
            elif 'change spice level' in command.lower():
                if 'spicy' in command.lower():
                    update_user_preference('spiciness', 'spicy')
                    speak(f"Spice level updated to spicy.")
                elif 'mild' in command.lower():
                    update_user_preference('spiciness', 'mild')
                    speak(f"Spice level updated to mild.")
                else:
                    speak("I could not understand your spice level preference.")

            elif 'exit' in command.lower() or 'stop' in command.lower():
                print("👋 Exiting the assistant. Happy cooking!")
                speak("Okay, exiting. Happy cooking!")
                should_exit = True  # Set the flag to True to exit the loop

            else:
                print("🤔 No valid command detected.")

        except sr.UnknownValueError:
            print("😕 Sorry, I couldn't understand.")
        except sr.RequestError:
            print("⚠️ Network issue with the recognition service.")


if __name__ == "__main__":
    load_profile()
    while not should_exit:
        listen_command()  # Keep listening until 'exit' or 'stop' is said

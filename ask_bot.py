import json
import subprocess
import sys
import speech_recognition as sr  # The new audio library

sys.stdout.reconfigure(encoding='utf-8')

def load_locations():
    try:
        with open('locations.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("❌ Error: Could not find locations.json!")
        sys.exit(1)

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Calibrating microphone... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("🟢 Listening! (Say a location like 'kitchen' or 'bedroom')")
        try:
            # Listen for up to 5 seconds
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            # Send the audio to Google's AI to translate it to text
            print("🔄 Processing speech...")
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ I heard: '{command}'")
            return command
            
        except sr.WaitTimeoutError:
            print("⏳ I didn't hear anything.")
            return None
        except sr.UnknownValueError:
            print("🤔 Sorry, the audio was garbled. I couldn't understand that.")
            return None
        except sr.RequestError:
            print("❌ Network error. I need an internet connection to process speech.")
            return None

def main():
    locations = load_locations()

    print("========================================")
    print(" 🤖 SmartBot Voice Interface (LIVE AUDIO)")
    print("========================================")
    print(f"Saved Locations: {', '.join(locations.keys())}\n")

    # Wake up the microphone instead of asking for keyboard input
    command = listen_for_command()

    # If the microphone failed or timed out, gracefully exit
    if not command:
        print("Shutting down voice interface.")
        return

    # Check if any part of the spoken sentence contains a saved location
    # (e.g., if you say "Take me to the bedroom", it will find "bedroom")
    target_location = None
    for loc in locations:
        if loc in command:
            target_location = loc
            break

    if target_location:
        coords = locations[target_location]
        target_x = str(coords[0])
        target_y = str(coords[1])
        
        print(f"\n✅ Understood! Engaging Navigation Stack for '{target_location}'.")
        print("⚙️ Waking up the C Engine...\n")
        
        try:
            subprocess.run([".\\pathfinder.exe", target_x, target_y])
        except FileNotFoundError:
            print("\n❌ Error: pathfinder.exe not found! Did you compile it?")
    else:
        print(f"\n❌ I'm sorry, I don't recognize a destination in what you said.")
        print("Please add the room to locations.json first.")

if __name__ == "__main__":
    main()
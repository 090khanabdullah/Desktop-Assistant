import google.generativeai as ai
from google.generativeai.types.generation_types import StopCandidateException
import json
import AppOpener
# from main1 as 

API_KEY = 'AIzaSyBrG3q6aHVMvmN-liNyOT-weTADMlouhmo'

# List of predefined commands
commands_list = [
    "go to <website name>",
    "search on google <query>",
    "open <app/system tool>",
    "close <app/system tool>",
    "ip address of my device",
    "search on wikipedia <topic>",
    "send message",
    "current temperature <city_name>",
    "play video on youtube <video_name>",
    "current time",
    "ai mode <query>",
    "shutdown",
    "restart",
    "sleep",
    "minimise window",
    "maximise window",
    "close window",
    "help"
    "exit"
]

# Configure the API once globally to avoid redundant setup
ai.configure(api_key=API_KEY)

# Create a new model and chat object once
model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

def scanapp():
    app_keys=AppOpener.give_appnames()
    return app_keys

def processcmd(command):
    
    app_keys=scanapp()
    
        
    # Refined prompt that asks the AI to match input with the correct command from the list
    prompt = (
    f"You are a command assistant designed to help users, including those who may be illiterate or make mistakes in their input. "
    f"Your task is to interpret the user's intent and correct any spelling mistakes, command structure errors, or word choice issues. "
    f"Consider the following possibilities for mistakes:\n"
    f"- The user might confuse 'go to' for websites and apps. If they say 'go to' followed by a website name, change it to 'open <website>' and append '.com' if not specified. For apps, return 'open <app>' or 'close <app>' as needed, but only if the app name exists in the user's installed apps, which are listed in {app_keys}.\n"
    f"- If the user says 'open' or 'close' followed by a website name, change it to 'go to <website>.com'.\n"
    f"- Ensure the command returns the exact app name required by the AppOpener library from this list: {app_keys}. If the user provides an app name not listed in {app_keys}, inform the user that the app is not available.\n"
    f"- Match user input to the correct app name supported by the AppOpener library from {app_keys}. This includes handling common variations, abbreviations, and misspellings.\n"
    f"- Handle spelling errors or typos in app names and correct them automatically.\n\n"
    f"- If the user only types 'AI' instead of 'AI mode', assume they meant 'AI mode'.\n"
    f"- The user might give incomplete commands. For example, 'go to google' should be interpreted as a web search, while 'search on google' should include a query if missing.\n"
    f"- If the user says anything resembling 'help', such as 'run help function', 'show help', 'assist', or 'guide', return the 'help' command.\n\n"
    f"- If the user says anything resembling 'exit', 'no thanks', 'close', or any phrase indicating the intent to stop or exit the software, return 'exit'.\n\n"
    f"Commands List:\n"
    f"{commands_list}\n\n"
    f"Here is the app name mapping from the user's system (available apps):\n"
    f"{app_keys}\n\n"
    f"User Input: {command}\n\n"
    f"Response (return 'open <app_name>' or 'close <app_name>' only if the app exists in the app_keys list, or inform the user that the app is not available if it's not in app_keys):"
)





    try:
        # Send the refined prompt to the AI
        response = chat.send_message(prompt)
        matched_command = response.text.strip()

        # Debug print the raw response from AI
        print(f"Raw AI Response: {matched_command}")

        # Return the processed response from AI
        return matched_command

    except StopCandidateException as e:
        print("AI Error: That question seems to be causing an issue. Please try rephrasing.")
        print(f"Error Details: {e}")
        return "Command not recognized. Please try again."
    except Exception as e:
        print("AI Error: Sorry, something went wrong.")
        print(f"Error: {e}")
        return "Command not recognized. Please try again."
    
# print(processcmd("open chatgtp"))
# print(app_name)

"""
 Copyright 2024 Wesley Kimeli

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

import sys
from configparser import ConfigParser
from chatbot import Chatbot

def main():
    """
    Entry point of the Gemini AI_Chatbot CLI application.
    Reads API key from 'credentials.ini' file, initializes the Chatbot,
    and starts the conversation loop until the user types 'quit'.
    """
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']

    chatbot = Chatbot(api_key=api_key)
    chatbot.start_conversation()

    print("Welcome to Gemini AI_Chatbot CLI. To exit type 'quit'.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            sys.exit('Exiting AI_Chatbot CLI....')

        try:
            response = chatbot.send_prompt(user_input)
            print(f"{chatbot.CHATBOT_NAME}:{response}")
        except Exception as e:
            print(f"Error: {e}")

main()
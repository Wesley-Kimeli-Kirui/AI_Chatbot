import sys
from configparser import ConfigParser
from chatbot import Chatbot

def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']

    chatbot = Chatbot(api_key=api_key)
    chatbot.start_conversation()
    # chatbot.clear_conversation()

    print("Welcome to Gemini AI_Chatbot CLI. To exit type 'quit'.")
    
    # print('{0}: {1}'.format(chatbot.CHATBOT_NAME, chatbot.history[-1]['text']))
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            #print('Exiting AI_Chatbot CLI....')
            sys.exit('Exiting AI_Chatbot CLI....')

        try:
            response = chatbot.send_prompt(user_input)
            print(f"{chatbot.CHATBOT_NAME}:{response}")
        except Exception as e:
            print(f"Error: {e}")    

main()
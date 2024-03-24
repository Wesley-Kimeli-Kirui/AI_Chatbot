import google.generativeai as genai

class GenAIExeption(Exception):
    # Exception base class for all exceptions raised by the GenAI module


class Chatbot:
    # Can only have one candidate response at a time.
    CHATBOT_NAME = 'AI Assistant'

    def __init__(self, api_key):
        self.genai = genai
        self.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []
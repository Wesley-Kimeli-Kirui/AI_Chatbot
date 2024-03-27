import google.generativeai as genai

class GenAIExeption(Exception):
    """Exception base class for all exceptions raised by the GenAI module"""


class Chatbot:
    CHATBOT_NAME = 'AI Assistant'

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []

        self.preload_conversation()
    
    def send_prompt(self, prompt, temperature = 0.1):
        if temperature < 0  or temperature > 1:
            raise GenAIExeption('Temperature must be between 0 and 1')
        if not prompt:
            raise GenAIExeption('Promt cannot be empty')
        try:
            response = self.conversation.send_message(
                content = prompt,
                generation_config=self._generate_config(temperature),

            )
            response.resolve()
            return f'{response.text}\n' + '---' * 20
        except Exception as e:
            raise GenAIExeption(e.message)
    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history = [])

    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)
    
    def _generate_config(self, temperature):                 
        return genai.types.GenerationConfig (
            temperature=temperature 
        )                 
            
    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }
    
    def preload_conversation(self, conversation_history = None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._constract_message('From now on, return the output as JSON object that can be loaded in Python with the key as \'text\'. For example, {"text": "<output goes here>"}'),
                self._constract_message('{"text": "Sure ,I can return the output as JSON object that can be loaded in Python with the key as `text`. Here is an example: {"text": "Your Output"}.', 'model')
            ]
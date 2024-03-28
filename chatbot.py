import google.generativeai as genai

class GenAIExeption(Exception):
    """Exception base class for all exceptions raised by the GenAI module"""


class Chatbot:
    """
    A class representing a chatbot.

    Attributes:
        CHATBOT_NAME (str): The name of the chatbot.
    """

    CHATBOT_NAME = 'AI Assistant'

    def __init__(self, api_key):
        """
        Initializes a new instance of the Chatbot class.

        Args:
            api_key (str): The API key for the chatbot.
        """
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []

        self.preload_conversation()
    
    def send_prompt(self, prompt, temperature = 0.1):
        """
        Sends a prompt to the chatbot and returns the response.

        Args:
            prompt (str): The prompt to send to the chatbot.
            temperature (float, optional): The temperature for generating the response. Must be between 0 and 1. Defaults to 0.1.

        Returns:
            str: The response from the chatbot.
        """
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
        """
        Gets the conversation history.

        Returns:
            list: The conversation history.
        """
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history

    def clear_conversation(self):
        """
        Clears the conversation history.
        """
        self.conversation = self.model.start_chat(history = [])

    def start_conversation(self):
        """
        Starts a new conversation with the chatbot.
        """
        self.conversation = self.model.start_chat(history=self._conversation_history)
    
    def _generate_config(self, temperature):                 
        """
        Generates the configuration for generating the response.

        Args:
            temperature (float): The temperature for generating the response.

        Returns:
            genai.types.GenerationConfig: The generation configuration.
        """                 
        return genai.types.GenerationConfig (
            temperature=temperature 
        )                 
            
    def _construct_message(self, text, role='user'):
        """
        Constructs a message object.

        Args:
            text (str): The text of the message.
            role (str, optional): The role of the message. Defaults to 'user'.

        Returns:
            dict: The message object.
        """
        return {
            'role': role,
            'parts': [text]
        }
    
    def preload_conversation(self, conversation_history = None):
        """
        Preloads the conversation history.

        Args:
            conversation_history (list, optional): The conversation history to preload. Defaults to None.
        """
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message('From now on, return the output as JSON object that can be loaded in Python with the key as \'text\'. For example, {"text": "<output goes here>"}'),
                self._construct_message('{"text": "Sure ,I can return the output as JSON object that can be loaded in Python with the key as `text`. Here is an example: {"text": "Your Output"}.', 'model')
            ]
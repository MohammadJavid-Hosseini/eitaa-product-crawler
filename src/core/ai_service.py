import logging
from duckduckgo_search import DDGS


class CoreAIService:
    def __init__(self, model: str = 'gpt-4o-mini'):
        self.model = model
        logging.info("CoreAIService initialized with model: %s", model)

    def ask(self, prompt: str) -> str:
        "Send a prompt to the AI model and return response"
        try:
            response = DDGS().chat(prompt, model=self.model)
            return response
        except Exception as e:
            logging.error(f"AI service failed: {e}")
            return ""

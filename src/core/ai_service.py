import logging
import os
from openai import OpenAI


class CoreAIService:
    def __init__(self, model: str = 'gpt-4o-mini'):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=self.api_key)

        logging.info("CoreAIService initialized with model: %s", model)

    def ask(self, prompt: str) -> str:
        "Send a prompt to the AI model and return response"
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
            )
            result = response.choices[0].message.content.strip()
            logging.info(f"The keys: {result}")
            return result

        except Exception as e:
            logging.error("AI service failed: %s", e)
            return ""


        # # HACK: simulated AI aoutput for keyword generation
        # simulated_keywords = [
        #     "خرید آنلاین",
        #     "فروش ویژه",
        #     "ارسال رایگان",
        #     "قیمت مناسب",
        #     "سفارش اینترنتی",
        #     "فروشگاه آنلاین",
        #     "تخفیف ویژه"
        # ]
        # return ", ".join(simulated_keywords)

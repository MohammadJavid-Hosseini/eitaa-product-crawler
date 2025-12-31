import logging
import os
import time
from openai import OpenAI


class CoreAIService:
    def __init__(
        self,
        model: str = 'gpt-4o-mini',
        max_tokens: int = 120,
        timeout: int = 10,
        max_retries: int = 2
    ):
        self.model = model
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries

        # fetch API key
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        # set the AI client
        self.client = OpenAI(api_key=self.api_key)

        logging.info(
            "CoreAIService initialized (model: %s, max_tokens=%s",
            model,
            self.max_tokens
        )

    def ask(self, prompt: str) -> str:
        "Send a prompt to the AI model and return response"

        for attempt in range(1, self.max_retries + 2):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout

                )
                result = response.choices[0].message.content.strip()
                return result

            except Exception as e:
                logging.error(
                    "AI request failed: (attempt %s/%s): %s",
                    attempt, self.max_retries + 1, e
                    )

                if attempt <= self.max_retries:
                    time.sleep(2 ** attempt)
                logging.error("AI service unavailable after retires")

        return ""

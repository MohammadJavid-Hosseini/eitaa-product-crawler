import logging
# from ddgs import DDGS


class CoreAIService:
    def __init__(self, model: str = 'gpt-4o-mini'):
        self.model = model
        logging.info("CoreAIService initialized with model: %s", model)

    def ask(self, prompt: str) -> str:
        "Send a prompt to the AI model and return response"
        # FIX: deal with a working stable LLM later
        # try:
        #     response = DDGS().chat(prompt, model=self.model)
        #     return response
        # except Exception as e:
        #     logging.error(f"AI service failed: {e}")
        #     return ""
        logging.debug("AI prompt: %s", prompt)

        # HACK: simulated AI aoutput for keyword generation
        simulated_keywords = [
            "خرید آنلاین",
            "فروش ویژه",
            "ارسال رایگان",
            "قیمت مناسب",
            "سفارش اینترنتی",
            "فروشگاه آنلاین",
            "تخفیف ویژه"
        ]
        return ", ".join(simulated_keywords)

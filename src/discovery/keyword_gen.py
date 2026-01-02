import logging
from typing import List
from core.ai_service import CoreAIService


class KeywordGenerator:
    def __init__(self, ai_service: CoreAIService):
        self.ai = ai_service

    def generate_buying_keywords(self, category: str) -> List[str]:
        prompt = (
            f"""
            Generate 10 Persian search keywords to find '{category}' shops on a messenger.
            Focus on commercial intent like 'ارسال رایگان' or 'خرید آنلاین'.
            Return ONLY the keywords separated by commas.
            """
        )

        raw_output = self.ai.ask(prompt)
        if not raw_output:
            return self._fallback_keywords(category)

        keywords = [
            kw.strip()
            for kw in raw_output.replace('\n', ',').split(',')
            if len(kw.strip()) > 2
        ]
        if keywords:
            logging.info(f"Generated keywords by AI: {keywords[:10]}")
            return keywords[:10]
        return self._fallback_keywords(category)

    def _fallback_keywords(self, category: str) -> List[str]:
        logging.warning("Using fallback keywords for category: %s", category)
        return [
            category,
            "خرید",
            "فروش",
            "آنلاین"
        ]

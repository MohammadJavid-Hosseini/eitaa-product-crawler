import logging
from typing import Dict
from core.ai_service import CoreAIService


class ChannelValidator:
    def __init__(self, ai_service: CoreAIService, use_ai: bool = True):
        self.ai = ai_service
        self.use_ai = use_ai

    def validate(self, channel: Dict) -> bool:
        "Return True if channel is considered a shop channel"

        if self.ai.disabled:
            logging.warning(
                "AI unavailable, switching to rule-based validation")
            self.use_ai = False

        # fast rule-based rejection
        if self._rule_based_reject(channel):
            return False

        # AI-based validation
        if self.use_ai:
            return self._ai_validate(channel)

        return True

    def _rule_based_reject(self, channel):
        "Checks simply to avoid overusing AI validation"

        username = channel.get("username", "").lower()
        # this list or this mechanism can improve later
        blacklist = ["اخبار", "آموزش", "فان", "جوک"]
        return any(word in username for word in blacklist)

    def _ai_validate(self, channel: Dict) -> bool:
        prompt = self._build_prompt(channel)
        response = self.ai.ask(prompt)

        if not response:
            logging.warning("AI validation failed for channel")
            return False

        return response.strip().upper() == "YES"

    def _build_prompt(self, channel: Dict) -> str:
        posts_text = "\n".join(
            post.get("text", "") for post in channel.get("recent_posts", [])[:10]
        )

        return f"""
You are given information about a messenger channel.
Username:
{channel.get("username", "")}
Bio:
{channel.get("bio", "")}
Last posts:
{posts_text}

Question:
Is this channel primarily a product-selling or commercial channel?

Rules:
- Answer only with "YES" or "NO"
- Do not explain
""".strip()

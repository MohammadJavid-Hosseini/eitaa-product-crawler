from typing import List, Dict
from core.ai_service import CoreAIService


def is_shop_channel_rule_based(channel: Dict) -> bool:
    "Determine if the given channel is a shop channel"
    # HACK: role-based validation for now checking only username and bio;
    # later use AI and check the last posts as well

    SHOP_KEYWODS = ["ارسال", "سفارش", "قیمت", "خرید", "فروش"]
    text = " ".join([
        channel.get("username", ""),
        channel.get("bio", "")
    ])

    return any(keyword in text for keyword in SHOP_KEYWODS)


def is_shop_channel_ai(channel: Dict, ai: CoreAIService) -> bool:
    "AI-based validation of shop channels using username, bio, and recent posts."

    recent_posts = channel.get("recent_posts", [])

    posts_text = "\n".join(
        f"- {post.get('text', '')}"
        for post in recent_posts[:10]
    )

    prompt = f"""
        You are classifying messaging channels.
        Determine whether the following channel is a SHOP / SELLER channel.

        Use these signals:
        - commercial intent
        - selling products
        - prices, ordering, delivery, promotions

        Channel information:
        Username: {channel.get("username", "")}
        Bio: {channel.get("bio", "")}

        Last posts:
        {posts_text}

        Answer ONLY with:
        yes
        or
        no
        """

    response = ai.ask(prompt).strip().lower()
    return response == "yes"


def is_shop_channel(channel: Dict, ai: CoreAIService | None = None) -> bool:
    if is_shop_channel_rule_based(channel):
        return True

    if ai:
        return is_shop_channel_ai(channel, ai)

    return False


def validate_channels(channels: List[Dict], ai=None) -> List[Dict]:
    "Filter and return only shop channels"

    return [ch for ch in channels if is_shop_channel(ch, ai)]

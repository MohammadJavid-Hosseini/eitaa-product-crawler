from typing import Dict
from .parser import clean_text


def is_product_post(text: str) -> bool:
    "Determine if a given post is a product one"
    # HACK: very simple; later it must use AI
    keywords = ["قیمت", "تومان", "فروش", "تخفیف", "ریال"]
    for keyword in keywords:
        if keyword in text:
            return True

    return False


def extract_product(message: Dict, ) -> Dict | None:
    "Extract the data from a product post"

    text = clean_text(message.get("text", ""))
    if not is_product_post(text):
        return None

    return {
        "message_id": message.get("id", ""),
        "text": text,
        "images": message.get("images", []),
        "has_price": True
    }

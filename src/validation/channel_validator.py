from typing import List, Dict


def is_shop_channel(channel: Dict) -> bool:
    "Determine if the given channel is a shop channel"
    # HACK: role-based validation for now checking only username and bio;
    # later use AI and check the last posts as well

    SHOP_KEYWODS = ["ارسال", "سفارش", "قیمت", "خرید", "فروش"]
    text = " ".join([
        channel.get("username", ""),
        channel.get("bio", "")
    ])

    return any(keyword in text for keyword in SHOP_KEYWODS)


def validate_channels(channels: List[Dict]) -> List[Dict]:
    "Filter and return only shop channels"

    validated = []
    for channel in channels:
        if is_shop_channel(channel):
            validated.append(channel)

    return validated

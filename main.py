from fastapi import FastAPI, Query
import requests
import random

app = FastAPI()

# Simplified odds mapping for pull chances
odds_mapping = {
    "common": "10 per booster (~66%)",
    "uncommon": "3 per booster (~20%)",
    "rare": "1 per booster (~12.5%)",
    "mythic": "1 per 8 boosters (~1.5%)"
}

@app.get("/card")
def get_card(name: str = Query(..., description="Name of the MTG card, e.g. Lightning Bolt")):
    """
    Fetch card info and calculate estimated pull odds
    """
    url = f"https://api.scryfall.com/cards/named?exact={name}"
    response = requests.get(url)
   
    if response.status_code != 200:
        return {"error": "Card not found"}
   
    data = response.json()
   
    rarity = data.get("rarity")
    odds = odds_mapping.get(rarity, "Unknown")
   
    card_info = {
        "name": data.get("name"),
        "mana_cost": data.get("mana_cost"),
        "type": data.get("type_line"),
        "text": data.get("oracle_text"),
        "rarity": rarity,
        "set": data.get("set_name"),
        "estimated_pull_odds": odds
    }
   
    return card_info


@app.get("/booster")
def get_booster(set_code: str = Query(..., description="MTG set code, e.g. jou")):
    """
    Generate a random booster pack from a specified set
    """
    url = f"https://api.scryfall.com/cards/search?order=set&q=e:{set_code}&unique=prints"
    response = requests.get(url)
   
    if response.status_code != 200:
        return {"error": "Set not found or invalid set code"}
   
    data = response.json()
    cards = data.get("data", [])
   
    if not cards:
        return {"error": "No cards found in set"}
   
    # Separate cards by rarity
    commons = [c for c in cards if c.get("rarity") == "common"]
    uncommons = [c for c in cards if c.get("rarity") == "uncommon"]
    rares = [c for c in cards if c.get("rarity") == "rare"]
    mythics = [c for c in cards if c.get("rarity") == "mythic"]
   
    booster_pack = []

    # Pick 10 commons
    booster_pack.extend(random.sample(commons, min(10, len(commons))))
   
    # Pick 3 uncommons
    booster_pack.extend(random.sample(uncommons, min(3, len(uncommons))))
   
    # Pick 1 rare or mythic
    if mythics and random.random() < 0.125:  # ~1/8 boosters have a mythic
        booster_pack.append(random.choice(mythics))
    else:
        booster_pack.append(random.choice(rares))
   
    # Format output with estimated pull odds
    formatted_pack = [
        {
            "name": c.get("name"),
            "rarity": c.get("rarity"),
            "set": c.get("set_name"),
            "estimated_pull_odds": odds_mapping.get(c.get("rarity"), "Unknown")
        }
        for c in booster_pack
    ]
   
    return {"booster_pack": formatted_pack}
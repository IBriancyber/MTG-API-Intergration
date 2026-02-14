# MTG-API-Intergration
MTG card API- A Python FastAPI project intergrting with the Scryfall API to fetch Magic The Gathering card data and generate random booster packs. This Demostates API intergration, JSON data handling, query parameter usage, randomization, and probability calculations.


Features
/card endpoint

    Fetch detailed card information and estimated pull odds.

    Query parameter: name (card name)

    Example:

GET /card?name=Lightning+Bolt

Sample response:

{
  "name": "Lightning Bolt",
  "mana_cost": "{R}",
  "type": "Instant",
  "text": "Lightning Bolt deals 3 damage to any target.",
  "rarity": "common",
  "set": "Magic 2010",
  "estimated_pull_odds": "10 per booster (~66%)"
}

/booster endpoint

    Generate a random booster pack from a specified set, with pull odds included.

    Query parameter: set_code (e.g., jou for Journey Into Nyx)

    Example:

GET /booster?set_code=jou

Sample response:

{
  "booster_pack": [
    {
      "name": "Lightning Bolt",
      "rarity": "common",
      "set": "Magic 2010",
      "estimated_pull_odds": "10 per booster (~66%)"
    },
    {
      "name": "Goblin Guide",
      "rarity": "rare",
      "set": "Zendikar",
      "estimated_pull_odds": "1 per booster (~12.5%)"
    }
    ...
  ]
}

Setup Instructions



mkdir mtg_api_project
cd mtg_api_project

    Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

    Install dependencies:

pip install fastapi uvicorn requests

    Run the API:

uvicorn main:app --reload

    Open your browser or Postman:

http://127.0.0.1:8000/card?name=Shivan+Dragon
http://127.0.0.1:8000/booster?set_code=jou

Notes / Known Issues

    Pull odds are simplified estimates based on card rarity.

    /booster generates a random pack each call; results differ every time.

    Query parameters are required (Query(...)) to prevent 422 errors.

Future Improvements

    

    Calculate odds based on actual set composition.

    Add filtering (e.g., creatures, spells).

    Create a front-end interface for live interaction.

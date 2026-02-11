"""Service for interacting with Google Gemini API."""
import os
import json
from typing import Dict, List, Any
import google.generativeai as genai


def get_api_key() -> str:
    """Get API key from environment."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    return api_key


GAME_SCHEMA = {
    "type": "object",
    "properties": {
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "steamAppId": {"type": "string", "description": "The numeric Steam App ID."},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "genres": {"type": "array", "items": {"type": "string"}},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "mainStoryTime": {"type": "number"},
                    "completionistTime": {"type": "number"},
                    "suitabilityScore": {"type": "number"},
                    "imageUrl": {"type": "string"},
                    "developer": {"type": "string"},
                    "reasonForPick": {"type": "string"}
                },
                "required": ["id", "steamAppId", "title", "description", "mainStoryTime", 
                           "completionistTime", "suitabilityScore", "imageUrl", "reasonForPick"]
            }
        },
        "accuracy": {
            "type": "object",
            "properties": {
                "percentage": {"type": "number"},
                "reasoning": {"type": "string"}
            },
            "required": ["percentage", "reasoning"]
        }
    },
    "required": ["recommendations", "accuracy"]
}


async def get_game_recommendations(
    preferred_genres: List[str],
    playstyle: str,
    time_availability: str,
    specific_keywords: str
) -> Dict[str, Any]:
    """Get game recommendations from Gemini based on quiz answers."""
    try:
        api_key = get_api_key()
        genai.configure(api_key=api_key)
        
        prompt = f"""Act as a world-class Steam curator. Suggest 6 real video games available on Steam.
Genres: {', '.join(preferred_genres)}, Playstyle: {playstyle}, Time: {time_availability}, Keywords: {specific_keywords}.
Identify correct Steam App IDs. Estimate playtimes for main story and completionist. Calculate suitabilityScore (0-100)."""

        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = await model.generate_content_async(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=GAME_SCHEMA
            )
        )
        
        parsed = json.loads(response.text)
        return {
            "recommendations": parsed.get("recommendations", []),
            "accuracy": parsed.get("accuracy", {"percentage": 0, "reasoning": "Unknown"})
        }
    except Exception as e:
        print(f"Gemini Error: {e}")
        raise


async def search_specific_game(query: str) -> Dict[str, Any]:
    """Search for a specific game by name."""
    try:
        api_key = get_api_key()
        genai.configure(api_key=api_key)
        
        prompt = f'Search for the video game "{query}". Provide its numeric steamAppId and full metadata including playtimes and description.'
        
        single_game_schema = {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "steamAppId": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "mainStoryTime": {"type": "number"},
                "completionistTime": {"type": "number"},
                "suitabilityScore": {"type": "number"},
                "imageUrl": {"type": "string"},
                "reasonForPick": {"type": "string"}
            },
            "required": ["id", "steamAppId", "title", "description", "mainStoryTime", 
                        "completionistTime", "imageUrl", "reasonForPick"]
        }
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = await model.generate_content_async(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=single_game_schema
            )
        )
        
        return json.loads(response.text)
    except Exception as e:
        print(f"Search Error: {e}")
        raise

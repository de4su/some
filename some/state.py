"""State management for the Steam Quest app."""
import reflex as rx
from typing import List, Dict, Any, Optional
from some.services.gemini import get_game_recommendations, search_specific_game


class QuizState(rx.State):
    """State management for quiz and recommendations."""
    
    # View management
    view: str = "welcome"  # 'welcome', 'quiz', 'loading', 'results'
    
    # Quiz state
    quiz_step: int = 0
    preferred_genres: List[str] = []
    playstyle: str = "balanced"
    time_availability: str = "medium"
    specific_keywords: str = ""
    
    # Results state
    recommendations: List[Dict[str, Any]] = []
    accuracy_percentage: int = 0
    accuracy_reasoning: str = ""
    
    # Search state
    search_query: str = ""
    is_searching: bool = False
    
    # Error state
    error_message: str = ""
    
    # Available genres
    GENRES: List[str] = [
        "Action", "RPG", "Strategy", "Indie", "Adventure", 
        "Simulation", "Horror", "Puzzle", "Sports", "Racing"
    ]
    
    def set_view(self, new_view: str):
        """Change the current view."""
        self.view = new_view
        if new_view == "quiz":
            self.reset_quiz()
    
    def reset_quiz(self):
        """Reset quiz to initial state."""
        self.quiz_step = 0
        self.preferred_genres = []
        self.playstyle = "balanced"
        self.time_availability = "medium"
        self.specific_keywords = ""
    
    def toggle_genre(self, genre: str):
        """Toggle genre selection."""
        if genre in self.preferred_genres:
            self.preferred_genres = [g for g in self.preferred_genres if g != genre]
        else:
            self.preferred_genres = self.preferred_genres + [genre]
    
    def set_playstyle(self, style: str):
        """Set playstyle preference."""
        self.playstyle = style
    
    def set_time_availability(self, time: str):
        """Set time availability."""
        self.time_availability = time
    
    def set_specific_keywords(self, keywords: str):
        """Set specific keywords."""
        self.specific_keywords = keywords
    
    def next_step(self):
        """Move to next quiz step."""
        if self.quiz_step < 3:
            self.quiz_step += 1
    
    def prev_step(self):
        """Move to previous quiz step."""
        if self.quiz_step > 0:
            self.quiz_step -= 1
    
    def set_search_query(self, query: str):
        """Update search query."""
        self.search_query = query
    
    async def submit_quiz(self):
        """Submit quiz and get recommendations."""
        self.view = "loading"
        self.error_message = ""
        
        try:
            result = await get_game_recommendations(
                preferred_genres=self.preferred_genres,
                playstyle=self.playstyle,
                time_availability=self.time_availability,
                specific_keywords=self.specific_keywords
            )
            
            self.recommendations = result.get("recommendations", [])
            accuracy = result.get("accuracy", {})
            self.accuracy_percentage = accuracy.get("percentage", 0)
            self.accuracy_reasoning = accuracy.get("reasoning", "Unknown")
            self.view = "results"
        except Exception as e:
            self.error_message = str(e) or "Error loading recommendations. Please ensure your API key is set."
            self.view = "welcome"
    
    async def search_game(self):
        """Search for a specific game."""
        if not self.search_query.strip():
            return
        
        self.is_searching = True
        self.view = "loading"
        self.error_message = ""
        
        try:
            game = await search_specific_game(self.search_query)
            self.recommendations = [game]
            self.accuracy_percentage = 100
            self.accuracy_reasoning = "Direct search match."
            self.view = "results"
            self.search_query = ""
        except Exception as e:
            self.error_message = "Game not found or API error."
            self.view = "welcome"
        finally:
            self.is_searching = False
    
    @property
    def progress_percentage(self) -> int:
        """Calculate quiz progress percentage."""
        return int(((self.quiz_step + 1) / 4) * 100)
    
    @property
    def can_advance(self) -> bool:
        """Check if user can advance from current step."""
        if self.quiz_step == 0:
            return len(self.preferred_genres) > 0
        return True

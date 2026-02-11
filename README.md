# Steam Quest - Python Edition

A Steam game recommendation app built with Python and [Reflex](https://reflex.dev), featuring AI-powered game suggestions based on your preferences.

## Features

- 🎮 **4-Phase Quiz System**: Genre selection, playstyle, time availability, and specific keywords
- 🤖 **AI-Powered Recommendations**: Uses Google Gemini AI to suggest games
- ⏱️ **HowLongToBeat Integration**: Shows main story and completionist playtimes
- 🎨 **Steam-like Dark Theme**: Authentic gaming aesthetic with smooth animations
- 🔍 **Manual Search**: Search for specific games directly
- 📊 **Match Accuracy Score**: See how well recommendations match your preferences

## Setup

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/de4su/some.git
cd some
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API key:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

4. Initialize Reflex:
```bash
reflex init
```

### Running the App

```bash
reflex run
```

The app will be available at `http://localhost:3000`

## Project Structure

```
some/
├── rxconfig.py              # Reflex configuration
├── requirements.txt         # Python dependencies
├── some/
│   ├── __init__.py
│   ├── some.py             # Main UI and routing
│   ├── state.py            # State management and quiz logic
│   ├── components.py       # Reusable UI components
│   └── services/
│       ├── __init__.py
│       └── gemini.py       # Google Gemini API integration
```

## Technology Stack

- **[Reflex](https://reflex.dev)**: Python web framework for full-stack apps
- **[Google Gemini AI](https://ai.google.dev/)**: AI model for game recommendations
- **Python**: Backend and frontend logic
- **Tailwind CSS**: Styling (via Reflex)

## How It Works

1. **Quiz Phase**: Answer 4 phases of questions about your gaming preferences
2. **AI Processing**: Your answers are sent to Google Gemini AI
3. **Recommendations**: Receive 6 personalized game suggestions with:
   - Steam App ID and store link
   - Main story and completionist playtimes
   - Suitability score (0-100%)
   - Curator notes explaining why each game was picked

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

MIT License - feel free to use this project for learning or personal use.
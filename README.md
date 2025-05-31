# Tamil Anagram Game

A web-based anagram game for Tamil words with a modern, mobile-friendly interface. Players need to rearrange scrambled Tamil letters to form the correct word.

## Features

- Mobile-friendly design with touch support
- Intuitive drag-and-drop interface
- Immediate feedback with animated modals
- Proper handling of Tamil Unicode characters
- Retry or start new game options
- Responsive layout that works on all devices

## Technologies Used

- Python/Flask for the backend
- Vanilla JavaScript for frontend interactions
- GraphemeSplitter for proper Tamil character handling
- Modern CSS with animations and responsive design

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd tamil-anagram-game
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit `http://localhost:5000`

## Development

The project structure is organized as follows:

```
.
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── templates/         
│   └── index.html     # Main game interface
└── README.md          # This file
```

## Contributing

Feel free to open issues or submit pull requests for any improvements you'd like to suggest.

## License

MIT License - feel free to use this project however you'd like. 
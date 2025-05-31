# Tamil Anagram Game

A web-based anagram game for Tamil words with a modern, mobile-friendly interface. Players need to rearrange scrambled Tamil letters to form the correct word.

## Features

- Mobile-friendly design with touch support
- Intuitive drag-and-drop interface
- Immediate feedback with animated modals
- Proper handling of Tamil Unicode characters
- Retry or start new game options
- Responsive layout that works on all devices
- Customizable word list via words.txt file

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

3. (Optional) Customize the word list:
   - Edit `words.txt` to add or remove Tamil words
   - Each word should be on a new line
   - The file should be saved with UTF-8 encoding

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit `http://localhost:5000`

## Development

The project structure is organized as follows:

```
.
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── words.txt          # List of Tamil words for the game
├── templates/         
│   └── index.html     # Main game interface
└── README.md          # This file
```

### Customizing Words

The game reads words from `words.txt`. To add your own words:
1. Open `words.txt` in a text editor that supports UTF-8
2. Add one Tamil word per line
3. Save the file with UTF-8 encoding
4. Restart the application if it's running

If `words.txt` is not found or is empty, the game will use a default set of words.

## Contributing

Feel free to open issues or submit pull requests for any improvements you'd like to suggest.

## License

MIT License - feel free to use this project however you'd like. 
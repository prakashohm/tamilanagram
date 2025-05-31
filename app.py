from flask import Flask, render_template, request, redirect
import random
import regex
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_words():
    """Load and categorize words from words.txt file"""
    try:
        with open('words.txt', 'r', encoding='utf-8') as file:
            # Read lines and remove empty lines and whitespace
            words = [line.strip() for line in file if line.strip()]
        
        if not words:
            # Fallback words in case file is empty
            return {
                'basic': ["தமிழ்", "நாடு"],
                'advanced': ["கணினி", "புத்தகம்"]
            }

        # Categorize words based on length (using graphemes)
        basic_words = []
        advanced_words = []
        
        for word in words:
            graphemes = split_graphemes(word)
            if len(graphemes) <= 4:
                basic_words.append(word)
            else:
                advanced_words.append(word)

        # Ensure each level has at least one word
        if not basic_words:
            basic_words = ["தமிழ்", "நாடு"]
        if not advanced_words:
            advanced_words = ["கணினி", "புத்தகம்"]

        return {
            'basic': basic_words,
            'advanced': advanced_words
        }
    except Exception as e:
        print(f"Error loading words: {e}")
        return {
            'basic': ["தமிழ்", "நாடு"],
            'advanced': ["கணினி", "புத்தகம்"]
        }

def split_graphemes(word):
    return regex.findall(r'\X', word)

def shuffle_tamil_word(word):
    chars = split_graphemes(word)
    random.shuffle(chars)
    return ''.join(chars)

def get_scrambled_word(word):
    """Scramble the characters of a word"""
    while True:
        scrambled = shuffle_tamil_word(word)
        if scrambled != word:
            return scrambled

@app.route('/')
def index():
    return render_template('level_select.html')

@app.route('/play/<level>')
def play(level):
    if level not in ['basic', 'advanced']:
        return redirect('/')
    
    words = load_words()
    level_words = words[level]
    word = random.choice(level_words)
    scrambled = get_scrambled_word(word)
    return render_template('game.html', 
                         scrambled=scrambled, 
                         original_word=word, 
                         level=level,
                         word_length=len(split_graphemes(word)))

if __name__ == '__main__':
    app.run(debug=True)


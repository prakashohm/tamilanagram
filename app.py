from flask import Flask, render_template, request, redirect, jsonify
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

        # Categorize words based on length
        basic_words = []
        advanced_words = []
        
        for word in words:
            if len(word) <= 4:
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

def shuffle_tamil_word(word):
    """Shuffle Tamil word while preserving proper character boundaries"""
    try:
        # Simplified pattern for better performance
        chars = regex.findall(r'[\u0B80-\u0BFF][\u0BBE-\u0BCD\u0BD7]?', word)
        if not chars:
            # Fallback to simple character list if pattern doesn't match
            chars = list(word)
        random.shuffle(chars)
        return ''.join(chars)
    except Exception as e:
        print(f"Error shuffling word: {e}")
        # Fallback to simple character list
        chars = list(word)
        random.shuffle(chars)
        return ''.join(chars)

def get_scrambled_word(word):
    """Scramble the characters of a word"""
    try:
        max_attempts = 5  # Limit the number of attempts to prevent infinite loop
        for _ in range(max_attempts):
            scrambled = shuffle_tamil_word(word)
            if scrambled != word:
                return scrambled
        # If we couldn't get a different scramble, just reverse the word
        return word[::-1]
    except Exception as e:
        print(f"Error scrambling word: {e}")
        return word[::-1]  # Fallback to simple reverse

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
                         word_length=len(word))

@app.route('/play/<level>', methods=['POST'])
def check_answer(level):
    answer = request.form.get('answer', '')
    original_word = request.form.get('original_word', '')
    is_correct = answer == original_word
    return jsonify({'correct': is_correct})

if __name__ == '__main__':
    app.run(debug=True)


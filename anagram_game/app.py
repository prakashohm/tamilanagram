from flask import Flask, render_template
import random
import regex

app = Flask(__name__)
app.secret_key = 'supersecretkey'

WORD_LIST = [
    "அறிமுகம்", "பொழுதுபோக்கு", "இலக்கணம்"
]

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
    word = random.choice(WORD_LIST)
    scrambled = get_scrambled_word(word)
    return render_template('index.html', scrambled=scrambled, original_word=word)

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, jsonify, session
import random
import regex
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def load_words():
    """Load words from file and categorize them by length for basic and advanced levels"""
    try:
        with open('words.txt', 'r', encoding='utf-8') as file:
            words = [line.strip() for line in file if line.strip()]
            
        # Split words into basic (≤5 chars) and advanced (>5 chars) levels
        basic_words = [word for word in words if len(word) <= 5]
        advanced_words = [word for word in words if len(word) > 5]
        
        # Further categorize words by difficulty levels within basic and advanced
        words_by_level = {
            'basic': {
                'level1': [w for w in basic_words if len(w) <= 3],
                'level2': [w for w in basic_words if len(w) >= 4 and len(w) <= 5],
            },
            'advanced': {
                'level1': [w for w in advanced_words if len(w) >= 6 and len(w) <= 9],
                'level2': [w for w in advanced_words if len(w) >= 10],
            }
        }
        
        print("Words loaded successfully:")
        for mode, levels in words_by_level.items():
            print(f"\n{mode.upper()} MODE:")
            for level, words in levels.items():
                print(f"{level}: {len(words)} words")
        
        return words_by_level
    except Exception as e:
        print(f"Error loading words: {e}")
        return {
            'basic': {'level1': [], 'level2': []},
            'advanced': {'level1': [], 'level2': []}
        }

def split_tamil_word(word):
    """Split Tamil word into proper graphemes"""
    try:
        # Pattern matches Tamil characters in this order:
        # 1. ஸ்ரீ special character
        # 2. Vowels (அ-ஔ)
        # 3. Consonants (க-ன) with:
        #    - Optional vowel marks (ா-ூ)
        #    - Optional mei marker (்)
        #    - Optional secondary vowel marks (ெ-ௌ)
        pattern = (
            r'ஸ்ரீ|'  # Special character ஸ்ரீ
            r'[அ-ஔ]|'  # Vowels
            # Consonants with various combinations
            r'[க-ன]'  # Base consonant
            r'(?:[ா-ூ])?'  # Optional vowel marks
            r'(?:[்])?'  # Optional mei marker
            r'(?:[ெ-ௌ])?'  # Optional secondary vowel marks
        )
        
        chars = regex.findall(pattern, word, regex.V1)
        
        # Verify the split was correct by joining
        if ''.join(chars) != word:
            print(f"Warning: Pattern matching failed for word: {word}")
            print(f"Split result: {chars}")
            # Try with grapheme splitter as backup
            try:
                from grapheme import graphemes
                chars = list(graphemes(word))
                if ''.join(chars) == word:
                    return chars
            except ImportError:
                pass
            # If all else fails, return character by character
            return list(word)
            
        return chars
    except Exception as e:
        print(f"Error splitting Tamil word: {e}")
        return list(word)  # Fallback to character by character split

def shuffle_tamil_word(word):
    """Shuffle Tamil word while preserving proper character boundaries"""
    try:
        chars = split_tamil_word(word)
        if len(chars) <= 1:
            return word
            
        # Try multiple times to get a different arrangement
        max_attempts = 10
        original_chars = chars.copy()
        
        for _ in range(max_attempts):
            random.shuffle(chars)
            if chars != original_chars:
                shuffled = ''.join(chars)
                if shuffled != word:  # Double check we actually changed the word
                    return shuffled
        
        # If we couldn't get a different arrangement, reverse the characters
        return word[::-1]
    except Exception as e:
        print(f"Error shuffling word: {e}")
        # Fallback to simple reverse
        return word[::-1]

def get_scrambled_word(word):
    """Scramble the characters of a word"""
    try:
        # Don't scramble single-character words
        if len(word) <= 1:
            return word
            
        scrambled = shuffle_tamil_word(word)
        
        # Verify that we haven't lost any characters
        if len(scrambled) != len(word):
            print(f"Warning: Scrambled word length mismatch. Original: {len(word)}, Scrambled: {len(scrambled)}")
            return word[::-1]
            
        return scrambled
    except Exception as e:
        print(f"Error scrambling word: {e}")
        return word[::-1]  # Fallback to simple reverse

def get_current_level(points, game_mode):
    """Determine the current level based on points and game mode"""
    if game_mode == 'basic':
        if points < 15:
            return 'level1'  # ≤3 characters
        else:
            return 'level2'  # 5 characters
    else:  # advanced mode
        if points < 100:
            return 'level1'  # 6 characters
        else:
            return 'level2'  # ≥10 characters

def get_next_word(words, current_points, game_mode='basic'):
    """Get next word ensuring no repetition until all words are used"""
    try:
        # Initialize used words in session if not present
        if 'used_words' not in session:
            session['used_words'] = {'basic': {}, 'advanced': {}}
        
        current_level = get_current_level(current_points, game_mode)
        print(f"Current level: {current_level}, Points: {current_points}, Mode: {game_mode}")
        
        # Initialize used words for current level if not present
        if current_level not in session['used_words'][game_mode]:
            session['used_words'][game_mode][current_level] = []
        
        level_words = words[game_mode][current_level]
        print(f"Available words for {game_mode} mode, {current_level}: {len(level_words)} words")
        
        used_words = session['used_words'][game_mode][current_level]
        
        # If all words have been used, reset the used words list for this level
        if len(used_words) >= len(level_words):
            session['used_words'][game_mode][current_level] = []
            used_words = []
            session['new_round'] = True
        else:
            session['new_round'] = False
        
        # Get available words
        available_words = [w for w in level_words if w not in used_words]
        print(f"Available words: {len(available_words)} words")
        
        if not available_words:
            # If somehow we have no available words, reset and try again
            session['used_words'][game_mode][current_level] = []
            available_words = level_words
        
        # Select a random word from available words
        word = random.choice(available_words) if available_words else "வணக்கம்"
        print(f"Selected word length: {len(word)}")
        
        # Add to used words
        session['used_words'][game_mode][current_level].append(word)
        
        # Check if we should level up
        points_for_next_level = (current_points // 50 + 1) * 50
        session['level_up'] = current_points > 0 and current_points % 50 == 0
        session['next_level_points'] = points_for_next_level
        
        return word
    except Exception as e:
        print(f"Error in get_next_word: {e}")
        return "வணக்கம்"  # Fallback word

@app.route('/')
def index():
    # Initialize points in session if not present
    if 'points' not in session:
        session['points'] = 0
    return render_template('start.html')

@app.route('/play/<level>')
def play(level):
    try:
        if level not in ['basic', 'advanced']:
            return redirect('/play/basic')
        
        # Get current points from session or initialize to 0
        current_points = session.get('points', 0)
        
        words = load_words()
        word = get_next_word(words, current_points, level)
        scrambled = get_scrambled_word(word)
        
        # Get various state flags
        new_round = session.pop('new_round', False)
        level_up = session.pop('level_up', False)
        next_level_points = session.get('next_level_points', 50)
        
        # Store current level in session
        session['current_level'] = level
        
        return render_template('game.html', 
                             scrambled=scrambled, 
                             original_word=word, 
                             level=level,
                             word_length=len(word),
                             new_round=new_round,
                             level_up=level_up,
                             next_level_points=next_level_points,
                             current_points=current_points)
    except Exception as e:
        print(f"Error in play route: {e}")
        session['points'] = 0  # Reset points on error
        return redirect('/')  # Redirect to home on error

@app.route('/play/<level>', methods=['POST'])
def check_answer(level):
    action = request.form.get('action', '')
    original_word = request.form.get('original_word', '')
    current_points = session.get('points', 0)
    current_level = session.get('current_level', 'basic')
    
    # Handle hint action
    if action == 'hint':
        hint_cost = 2  # Fixed hint cost of 2 points
        current_points = max(0, current_points - hint_cost)  # Don't go below 0
        session['points'] = current_points
        return jsonify({
            'success': True,
            'current_points': current_points
        })
    
    # Handle regular answer submission
    answer = request.form.get('answer', '')
    is_correct = answer == original_word
    show_downgrade = False
    
    if is_correct:
        # Award different points based on level
        points_to_add = 15 if level == 'advanced' else 10
        current_points += points_to_add
        session['points'] = current_points
        
        # Check if we hit a 50-point milestone and are in basic level
        show_upgrade_choice = (
            current_points >= 50 and  # Has enough points
            level == 'basic'  # Current route is basic
        )
        
    else:
        # Deduct points for wrong answer
        points_to_deduct = 3  # Changed from 5 to 3 points for wrong answers
        current_points = max(0, current_points - points_to_deduct)  # Don't go below 0
        session['points'] = current_points        
        show_upgrade_choice = False
        
    # Check if we need to downgrade to basic level
    if level == 'advanced' and current_points < 50:
        show_downgrade = True
        session['current_level'] = 'basic'  # Set level back to basic

    return jsonify({
        'correct': is_correct,
        'new_round': session.get('new_round', False),
        'level_up': session.get('level_up', False),
        'next_level_points': session.get('next_level_points', 50),
        'current_points': current_points,
        'show_upgrade_choice': show_upgrade_choice,
        'show_downgrade': show_downgrade,
        'current_level': session.get('current_level', 'basic'),
        'points_earned': points_to_add if is_correct else -points_to_deduct
    })

@app.route('/upgrade_level', methods=['POST'])
def upgrade_level():
    """Handle level upgrade choice"""
    choice = request.form.get('choice', 'no')
    if choice.lower() == 'yes':
        return jsonify({
            'success': True,
            'redirect': '/play/advanced'
        })
    return jsonify({
        'success': True,
        'redirect': '/play/basic'
    })

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Clear all session data"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Session cleared successfully'
    })

if __name__ == '__main__':
    app.run(debug=True)


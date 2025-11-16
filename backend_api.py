from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from apikey import APIKEY
import random
import uuid
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

genai.configure(api_key=APIKEY)

stories = {}  # session_id: {'data': {...}, 'episode': 1, 'xp': 0, 'previous_choice': None}
users_file = 'instance/users.json'

def load_users():
    if not os.path.exists('instance'):
        os.makedirs('instance')
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    if not os.path.exists('instance'):
        os.makedirs('instance')
    with open(users_file, 'w') as f:
        json.dump(users, f)

def generate_story(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_episode(emotion, inattentiveness, hyperactivity, impulsiveness, episode_num, previous_choice=None):
    episode_titles = {
        1: "Introduction",
        2: "Small Challenge",
        3: "Turning Point",
        4: "Triumph Using Their Strength",
        5: "Conclusion"
    }
    title = episode_titles.get(episode_num, f"Episode {episode_num}")
    prompt = f"""
Generate a progressive, connected story episode for a child with ADHD. Emotion: {emotion}. Traits: Inattentiveness {inattentiveness} (distracted), Hyperactivity {hyperactivity} (fidgety), Impulsiveness {impulsiveness} (rash). Episode {episode_num}/5: {title}. Use simple English for kids 8-12. Make the story build on previous events.
"""
    if episode_num == 1:
        prompt += " Introduction: Set the scene, mood, the realm, and introduce the guide character."
    elif episode_num == 2:
        prompt += " Small Challenge: Based on game metrics (focus, impulse, energy)."
    elif episode_num == 3:
        prompt += " Turning Point: Child faces difficulty, guide character supports them."
    elif episode_num == 4:
        prompt += " Triumph Using Their Strength: Use their highest metric to create empowerment."
    elif episode_num == 5:
        prompt += " Conclusion: Child learns insight, realm shifts, guide praises strength, receives emotional skill/power."
    if previous_choice and episode_num > 1:
        prompt += f" Previous choice: {previous_choice}. Continue the story progressively from there."
    prompt += """
Story: Short paragraph (20 words max) advancing the plot.
Choices:
1. Good: Helpful action that progresses positively.
2. Neutral: Okay action that continues the story.
3. Bad: Troublesome action that creates challenges.
Format: Story: [text]
Choice 1 (Good): [text]
Choice 2 (Neutral): [text]
Choice 3 (Bad): [text]
"""
    return generate_story(prompt)

def parse_scenario(response):
    lines = response.split('\n')
    story = ""
    choices = []
    for line in lines:
        if line.startswith("Story:"):
            story = line.replace("Story:", "").strip()
        elif line.startswith("Choice 1 (Good):"):
            choices.append(("good", line.replace("Choice 1 (Good):", "").strip()))
        elif line.startswith("Choice 2 (Neutral):"):
            choices.append(("neutral", line.replace("Choice 2 (Neutral):", "").strip()))
        elif line.startswith("Choice 3 (Bad):"):
            choices.append(("bad", line.replace("Choice 3 (Bad):", "").strip()))
    # Shuffle the choices to randomize their order
    random.shuffle(choices)
    return story, choices

def generate_full_story(childName, emotion, inattentiveness, hyperactivity, impulsiveness):
    full_story = f"Once upon a time, there was a brave adventurer named {childName}. "
    previous_choice = None
    for episode in range(1, 6):
        episode_titles = {
            1: "Introduction",
            2: "Small Challenge",
            3: "Turning Point",
            4: "Triumph Using Their Strength",
            5: "Conclusion"
        }
        title = episode_titles.get(episode, f"Episode {episode}")
        prompt = f"""
Generate a progressive, connected story episode for a child with ADHD. Emotion: {emotion}. Traits: Inattentiveness {inattentiveness} (distracted), Hyperactivity {hyperactivity} (fidgety), Impulsiveness {impulsiveness} (rash). Episode {episode}/5: {title}. Use simple English for kids 8-12. Make the story build on previous events.
"""
        if episode == 1:
            prompt += " Introduction: Set the scene, mood, the realm, and introduce the guide character."
        elif episode == 2:
            prompt += " Small Challenge: Based on game metrics (focus, impulse, energy)."
        elif episode == 3:
            prompt += " Turning Point: Child faces difficulty, guide character supports them."
        elif episode == 4:
            prompt += " Triumph Using Their Strength: Use their highest metric to create empowerment."
        elif episode == 5:
            prompt += " Conclusion: Child learns insight, realm shifts, guide praises strength, receives emotional skill/power."
        if previous_choice and episode > 1:
            prompt += f" Previous choice: {previous_choice}. Continue the story progressively from there."
    prompt += """
Story: Short paragraph (20 words max) advancing the plot.
Choices:
1. Good: Helpful action that progresses positively.
2. Neutral: Okay action that continues the story.
3. Bad: Troublesome action that creates challenges.
Format: Story: [text]
Choice 1 (Good): [text]
Choice 2 (Neutral): [text]
Choice 3 (Bad): [text]
"""
        response = generate_story(prompt)
        lines = response.split('\n')
        story = ""
        choices = []
        for line in lines:
            if line.startswith("Story:"):
                story = line.replace("Story:", "").strip()
            elif line.startswith("Choice 1 (Good):"):
                choices.append(("good", line.replace("Choice 1 (Good):", "").strip()))
            elif line.startswith("Choice 2 (Neutral):"):
                choices.append(("neutral", line.replace("Choice 2 (Neutral):", "").strip()))
            elif line.startswith("Choice 3 (Bad):"):
                choices.append(("bad", line.replace("Choice 3 (Bad):", "").strip()))
        # Randomly select a choice to continue the story
        if choices:
            selected_choice = random.choice(choices)
            previous_choice = selected_choice[1]
        full_story += story + " "
    # Add conclusion based on traits
    if inattentiveness == "low" and hyperactivity == "low" and impulsiveness == "low":
        full_story += f"Nimbus smiled softly. 'You didn’t just travel through the realms,' he said. 'You discovered something powerful about yourself — your Focus Magic grows every time you pause and breathe. Remember this skill. It will follow you wherever you go.'"
    elif inattentiveness == "high" or hyperactivity == "high" or impulsiveness == "high":
        full_story += f"Hoppity hopped beside you and said, 'You know what I learned today? You’re brave. Even when some jumps were fast or bumpy, you kept trying. And guess what — trying again is a superpower.'"
    else:
        full_story += f"Zapberry tilted its little head. 'Energy can be wild sometimes,' it said kindly. 'But today you learned that when things feel too fast inside you, slowing down your hands helps slow down your thoughts too. That’s real magic.'"
    full_story += " Remember, every realm you visit teaches you something small but powerful — and every small change makes a big difference in your world."
    return full_story

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '').strip()
    age = data.get('age')
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    try:
        age = int(age)
        if age >= 18:
            return jsonify({'error': 'Age must be under 18'}), 400
        if age < 3:
            return jsonify({'error': 'Age must be at least 3'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid age'}), 400
    
    users = load_users()
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    users[username] = {'age': age}
    save_users(users)
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'error': 'Username is required'}), 400
    
    users = load_users()
    if username not in users:
        return jsonify({'error': 'Username not found'}), 400
    
    return jsonify({'success': True, 'username': username, 'age': users[username]['age']})

@app.route('/generate_story', methods=['POST'])
def generate_story_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    childName = data.get('childName', 'Child')
    emotion = data.get('emotion', 'Happy')
    inattentiveness = data.get('inattentiveness', 'low')
    hyperactivity = data.get('hyperactivity', 'low')
    impulsiveness = data.get('impulsiveness', 'low')
    try:
        story = generate_full_story(childName, emotion, inattentiveness, hyperactivity, impulsiveness)
        return jsonify({"story": story})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/start_story', methods=['POST'])
def start_story():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    session_id = str(uuid.uuid4())
    stories[session_id] = {
        'data': data,
        'episode': 1,
        'xp': 0,
        'previous_choice': None
    }
    return jsonify({'session_id': session_id})

@app.route('/get_episode', methods=['GET'])
def get_episode():
    session_id = request.args.get('session_id')
    if not session_id or session_id not in stories:
        return jsonify({'error': 'Invalid session'}), 400
    story_data = stories[session_id]
    if story_data['episode'] > 5:
        # Conclusion
        if story_data['xp'] >= 8:
            conclusion = "Nimbus smiled softly. ‘You didn’t just travel through CloudWhisper Cove,’ he said. ‘You discovered something powerful about yourself — your Focus Magic grows every time you pause and breathe. Remember this skill. It will follow you wherever you go.’"
        elif story_data['xp'] >= 5:
            conclusion = "Hoppity hopped beside you and said, ‘You know what I learned today? You’re brave. Even when some jumps were fast or bumpy, you kept trying. And guess what — trying again is a superpower.’"
        else:
            conclusion = "Zapberry tilted its little head. ‘Energy can be wild sometimes,’ it said kindly. ‘But today you learned that when things feel too fast inside you, slowing down your hands helps slow down your thoughts too. That’s real magic.’"
        conclusion += " Remember, every realm you visit teaches you something small but powerful — and every small change makes a big difference in your world."
        return jsonify({'conclusion': conclusion, 'xp': story_data['xp']})
    # Generate episode
    data = story_data['data']
    episode_num = story_data['episode']
    previous_choice = story_data['previous_choice']
    scenario_response = generate_episode(data['emotion'], data['inattentiveness'], data['hyperactivity'], data['impulsiveness'], episode_num, previous_choice)
    story, choices = parse_scenario(scenario_response)
    episode_titles = {
        1: "Introduction",
        2: "Small Challenge",
        3: "Turning Point",
        4: "Triumph Using Their Strength",
        5: "Conclusion"
    }
    title = episode_titles.get(episode_num, f"Episode {episode_num}")
    return jsonify({
        'episode': episode_num,
        'title': title,
        'story': story,
        'choices': [choice[1] for choice in choices],  # list of choice texts
        'xp': story_data['xp']
    })

@app.route('/make_choice', methods=['POST'])
def make_choice():
    data = request.get_json()
    session_id = data.get('session_id')
    choice_index = data.get('choice_index')  # 0,1,2
    if not session_id or session_id not in stories:
        return jsonify({'error': 'Invalid session'}), 400
    story_data = stories[session_id]
    if story_data['episode'] > 5:
        return jsonify({'error': 'Story completed'}), 400
    # Regenerate to get choices (since not stored)
    data = story_data['data']
    episode_num = story_data['episode']
    previous_choice = story_data['previous_choice']
    scenario_response = generate_episode(data['emotion'], data['inattentiveness'], data['hyperactivity'], data['impulsiveness'], episode_num, previous_choice)
    story, choices = parse_scenario(scenario_response)
    if choice_index < 0 or choice_index >= len(choices):
        return jsonify({'error': 'Invalid choice'}), 400
    selected_choice = choices[choice_index]
    choice_type = selected_choice[0]
    choice_text = selected_choice[1]
    if choice_type == "good":
        story_data['xp'] += 2
    elif choice_type == "neutral":
        story_data['xp'] += 1
    # bad: +0
    story_data['previous_choice'] = choice_text
    story_data['episode'] += 1
    return jsonify({'success': True, 'xp': story_data['xp']})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

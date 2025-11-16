import google.generativeai as genai
from apikey import APIKEY
import pyttsx3
import random
import os

genai.configure(api_key=APIKEY)

def generate_story(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

def get_user_data():
    emotion = input("Enter an emotion: ")
    inattentiveness = input("Inattentiveness level (high/low): ").lower()
    hyperactivity = input("Hyperactivity level (high/low): ").lower()
    impulsiveness = input("Impulsiveness level (high/low): ").lower()
    return emotion, inattentiveness, hyperactivity, impulsiveness

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





def main():
    emotion, inattentiveness, hyperactivity, impulsiveness = get_user_data()
    xp = 0
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
        print(f"\n--- Episode {episode} — {title} ---")
        try:
            scenario_response = generate_episode(emotion, inattentiveness, hyperactivity, impulsiveness, episode, previous_choice)
            story, choices = parse_scenario(scenario_response)
            print(story)
            if story:
                engine = pyttsx3.init()
                engine.say(story)
                engine.runAndWait()
            for i, (choice_type, choice_text) in enumerate(choices, 1):
                print(f"{i}. {choice_text}")
            choice = int(input("Choose 1, 2, or 3: "))
            selected_choice = choices[choice - 1]
            if selected_choice[0] == "good":
                xp += 2
                print("Good choice! +2 XP")
            elif selected_choice[0] == "neutral":
                xp += 1
                print("Neutral choice! +1 XP")
            elif selected_choice[0] == "bad":
                xp += 0
                print("Bad choice! +0 XP")
            if selected_choice[1]:
                engine = pyttsx3.init()
                engine.say(selected_choice[1])
                engine.runAndWait()
                
            previous_choice = selected_choice[1]
        except Exception as e:
            print(f"Error generating scenario: {e}")
            continue
    # Generate therapeutic conclusion based on XP
    if xp >= 8:
        conclusion_type = "Strength Reflection"
        conclusion = f"Nimbus smiled softly. ‘You didn’t just travel through CloudWhisper Cove,’ he said. ‘You discovered something powerful about yourself — your Focus Magic grows every time you pause and breathe. Remember this skill. It will follow you wherever you go.’"
    elif xp >= 5:
        conclusion_type = "Courage + Imperfect Progress"
        conclusion = f"Hoppity hopped beside you and said, ‘You know what I learned today? You’re brave. Even when some jumps were fast or bumpy, you kept trying. And guess what — trying again is a superpower.’"
    else:
        conclusion_type = "Gentle Guidance"
        conclusion = f"Zapberry tilted its little head. ‘Energy can be wild sometimes,’ it said kindly. ‘But today you learned that when things feel too fast inside you, slowing down your hands helps slow down your thoughts too. That’s real magic.’"
    print(f"\n{conclusion}")
    print("Remember, every realm you visit teaches you something small but powerful — and every small change makes a big difference in your world.")
    print(f"Total XP: {xp}")

if __name__ == "__main__":
    main()

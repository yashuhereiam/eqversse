import google.generativeai as genai
from apikey import APIKEY

genai.configure(api_key=APIKEY)

def generate_story(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text.strip()
if __name__ == "__main__":
     user_input = input("Enter an emotion: ")
     prompt = f"Write a short story based on the emotion: {user_input}"
     print(prompt)
     response = generate_story(prompt)
     print("Generated Story: ", response)

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv ()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

responses = {
    "who are you": "I am the chatbot of Butt Karahi. I will help you choose the best meal according to your requirements.",
    "introduction": "Butt Karahi Canada is a renowned Pakistani restaurant known for authentic Punjabi flavors and quality.",
    "what is special in you": "Experience Punjabi cuisine at Butt Karahi. Enjoy dishes celebrating tradition and rich flavors.",
    "location": "Mississauga: 3015 Winston Churchill Blvd, ON L5L 2V8, Canada\nPickering: 820 Kingston Rd, ON L1V 1A8, Canada",
    "featured dishes": "Chicken Karahi\nVeal Karahi\nGoat Karahi\nPaneer Karahi\nDaal",
    "menu": """Authentic Punjabi dishes crafted with fresh ingredients.

  Appetizers:
   - Lahori Fried Fish  Spiced, crispy fried fish.
   - Channa Chaat  Chickpeas, potatoes, tomatoes, green chilies.
   - Fresh Vegetable Salad  Cucumber, tomato, onion, lettuce.
   - Onion Salad  Diced onions, green chilies, lemon.

  Karahi Specials:
  - Chicken Karahi Charsi-style, salt & black pepper. (CAD 45.99)
  - Veal Karahi  Specially flavored veal. (CAD 52.99)
  - Goat Karahi  Charsi-style goat meat. (CAD 75.99)
  - Lamb Karahi  Lamb with unique spices. (CAD 69.99)
  - Paneer Karahi  Paneer in aromatic Karahi Masala. (CAD 24.99)
  - Daal Channa  Chickpeas & lentils with butter. (CAD 11.99)
    """,
    "tray & ramadan menu": "Special party trays and Ramadan-specific dishes available. Details not provided.",
    "about us": "Established in 1979 in Lahore, Butt Karahi is known for authentic taste, 100% halal meat, and hand-picked spices.",
    "contact us": "Mississauga Branch:\n\ud83d\udccd 3015 Winston Churchill Blvd, Mississauga, ON\n\ud83d\udcde +1 416-494-5477",
    "timing": "Mon: 3 PM-11 PM | Tue-Thu: 12 PM-11 PM | Fri-Sat: 12 PM-12 AM | Sun: 12 PM-11 PM",
    "pickering branch": "\ud83d\udccd 820 Kingston Rd, Pickering, ON\n\ud83d\udcde +1 905-839-0002\n\ud83d\udd52 Same hours as Mississauga branch",
    "social media": """Facebook: Butt Karahi Canada
 Instagram: @buttkarahicanada
 TikTok: @buttkarahicanada
 Yelp: Butt Karahi Reviews
 For more details, visit their website.""",
}

def GenerateResponse(input_text):
    input_text = input_text.lower()

    # Check if any predefined key exists in user input
    for key in responses:
        if key in input_text:
            return responses[key]  # Return predefined response

    # Provide context to the AI model
    prompt = f"""You are a chatbot for Butt Karahi, a Pakistani restaurant. Answer user queries based on the restaurant's information.
    User: {input_text}
    Chatbot:"""

    response = model.generate_content(prompt)
    
    # If AI model gives an irrelevant response, handle it
    if "I don't know" in response.text.lower():
        return "Working on model training"
    
    return response.text

#while True:
    #user_input = input("Enter your prompt:  ")
    #print(GenerateResponse(user_input))

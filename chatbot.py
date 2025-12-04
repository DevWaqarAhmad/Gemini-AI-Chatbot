import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# -------------------------------------------------
# LOAD API KEY
# -------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("ERROR: GEMINI_API_KEY not found in .env file!")
    st.stop()

genai.configure(api_key=API_KEY)

# -------------------------------------------------
# MODEL CONFIG
# -------------------------------------------------
@st.cache_resource
def load_model():
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }
    
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
    )

model = load_model()

# -------------------------------------------------
# EXPANDED RESTAURANT DATA
# -------------------------------------------------
restaurant_data = """
BUTT KARAHI CANADA - COMPLETE RESTAURANT INFORMATION

=== ABOUT US ===
Butt Karahi Canada has been serving authentic Pakistani and Punjabi cuisine since 1979. 
We are renowned for our traditional karahi dishes, made with 100% halal meat, fresh ingredients, 
and premium spices imported directly from Pakistan. Our chefs follow generations-old recipes 
to bring you the true taste of Lahore.

=== LOCATIONS ===

📍 MISSISSAUGA BRANCH:
Address: 3015 Winston Churchill Blvd, Mississauga, ON L5L 1C1
Phone: +1 416-494-5477
Email: info@buttkarahi.ca
Parking: Free parking available

📍 PICKERING BRANCH:
Address: 820 Kingston Rd, Pickering, ON L1V 1A7
Phone: +1 905-839-0002
Email: pickering@buttkarahi.ca
Parking: Street parking and nearby lot

=== OPENING HOURS ===
Monday: 3:00 PM – 11:00 PM
Tuesday–Thursday: 12:00 PM – 11:00 PM
Friday–Saturday: 12:00 PM – 12:00 AM
Sunday: 12:00 PM – 11:00 PM

=== COMPLETE MENU ===

--- APPETIZERS ---
• Lahori Fried Fish - $15.99 CAD
• Channa Chaat - $8.99 CAD
• Samosa (2 pcs) - $4.99 CAD
• Pakora Plate - $9.99 CAD
• Seekh Kebab (2 pcs) - $12.99 CAD
• Chicken Tikka (4 pcs) - $13.99 CAD

--- KARAHI SPECIALTIES ---
• Chicken Karahi (Small) - $45.99 CAD
• Chicken Karahi (Large) - $65.99 CAD
• Veal Karahi - $52.99 CAD
• Goat Karahi - $75.99 CAD
• Lamb Karahi - $69.99 CAD
• Paneer Karahi - $24.99 CAD
• Mixed Karahi (Chicken + Veal + Lamb) - $79.99 CAD

--- CURRY DISHES ---
• Chicken Curry - $35.99 CAD
• Beef Nihari - $42.99 CAD
• Paya - $38.99 CAD
• Haleem - $18.99 CAD
• Aloo Gosht - $39.99 CAD
• Dal Makhani - $14.99 CAD

--- RICE & BREAD ---
• Plain Rice - $6.99 CAD
• Pulao Rice - $12.99 CAD
• Biryani (Chicken) - $18.99 CAD
• Biryani (Goat) - $24.99 CAD
• Naan (Plain) - $2.50 CAD
• Naan (Garlic) - $3.50 CAD
• Naan (Butter) - $3.00 CAD
• Tandoori Roti - $2.00 CAD
• Paratha - $4.00 CAD

--- VEGETABLES ---
• Daal Channa - $11.99 CAD
• Palak Paneer - $14.99 CAD
• Mix Vegetables - $12.99 CAD
• Aloo Gobi - $11.99 CAD
• Bhindi Masala - $13.99 CAD

--- DRINKS ---
• Lassi (Sweet/Salt) - $5.99 CAD
• Mango Lassi - $6.99 CAD
• Soft Drinks - $2.99 CAD
• Bottled Water - $1.99 CAD
• Chai - $2.50 CAD
• Rooh Afza - $3.99 CAD

--- DESSERTS ---
• Kheer - $5.99 CAD
• Gulab Jamun (2 pcs) - $4.99 CAD
• Gajar Halwa - $6.99 CAD
• Ras Malai (2 pcs) - $6.99 CAD

=== KIDS MENU ===
• Kids Chicken Biryani - $9.99 CAD  
• Kids Boneless Chicken Karahi (Mild) - $12.99 CAD  
• Chicken Nuggets & Fries - $8.99 CAD  
• Kids Paratha Roll (Boneless) - $7.99 CAD  
• Kids Mango Juice - $2.99 CAD  
• Kids Chocolate Milkshake - $3.99 CAD

=== BREAKFAST MENU (WEEKENDS ONLY) ===
• Halwa Puri Plate - $11.99 CAD  
• Nihari with Naan - $16.99 CAD  
• Channa Puri - $9.99 CAD  
• Omelette + Paratha - $7.99 CAD  
• Aloo Paratha - $6.99 CAD  
• French Toast - $5.99 CAD

=== COMBOS & DEALS ===
• Family Deal: 2 Large Karahis + 4 Naans + 2 Drinks = $120 CAD  
• Student Deal: Chicken Biryani + Drink = $14.99 CAD  
• Weekend Breakfast Deal: Halwa Puri + Chai = $12.99 CAD  
• Kids Meal Combo: Nuggets + Fries + Juice = $11.99 CAD  
• Party Pack (Serves 6): 3 Large Karahis + 6 Naans + 6 Drinks = $220 CAD

=== SEASONAL & CHEF SPECIALS ===
• Butter Chicken Karahi - $55.99 CAD  
• Karahi Prawns - $59.99 CAD  
• Chef's Surprise Curry - Market Price (ask the staff)

=== SERVICES ===
Dine-in, Takeout, Delivery (Uber Eats, DoorDash), Catering, Private Parties, Halal Certified.

=== FAQ ===
Q: Is your food halal?  
A: Yes, 100% halal.

Q: Do you have kids meals?  
A: Yes, we have a full kids menu.

Q: Do you offer breakfast?  
A: Breakfast is served Saturday–Sunday only.

Q: Do you do catering for large events?  
A: Yes, we cater weddings, corporate events, and parties.

Q: Can I customize my dish?  
A: Yes, ask our staff or chatbot for customization options.

=== CHATBOT TIP ===
You can ask our AI assistant to:
- Recommend dishes for first-time visitors
- Suggest a kids meal or combo
- Provide nutritional info for selected dishes
- Tell you today's chef specials
- Guide you on allergen information
"""

# -------------------------------------------------
# INITIALIZE CUSTOM MEMORY
# -------------------------------------------------
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# -------------------------------------------------
# RESPONSE GENERATOR WITH MEMORY
# -------------------------------------------------
def generate_response(user_input):
    text = user_input.lower().strip()
    
    # Extract user information
    if "my name is" in text or "i am" in text or "i'm" in text:
        words = text.split()
        if "name is" in text:
            idx = text.index("name is") + len("name is")
            name = text[idx:].strip().split()[0].title()
            st.session_state.user_info["name"] = name
            return f"Nice to meet you, {name}! How can I help you today with our menu or services?"
        elif "i am" in text or "i'm" in text:
            for word in words:
                if len(word) > 2 and word.isalpha() and word not in ["am", "i'm", "my", "name", "is"]:
                    st.session_state.user_info["name"] = word.title()
                    return f"Hello {word.title()}! Welcome to Butt Karahi. What would you like to know?"
    
    # Build context with user info and chat history
    context = f"""
You are the official Butt Karahi Restaurant AI assistant.

RESTAURANT INFORMATION:
{restaurant_data}

"""
    
    # Add user info if available
    if st.session_state.user_info.get("name"):
        context += f"Current customer name: {st.session_state.user_info['name']}\n"
    
    # Add conversation history
    if st.session_state.messages:
        context += "\nCONVERSATION HISTORY:\n"
        for msg in st.session_state.messages[-6:]:
            role = "Customer" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
    
    context += f"\nCurrent Customer Question: {user_input}\n\n"
    context += """
INSTRUCTIONS:
- Answer using ONLY the restaurant information provided above
- Be friendly, helpful, and conversational
- Remember the customer's name if they shared it
- If asked about contact details, timing, menu, or services - provide complete information
- If information is not available in the data, say: "I don't have that information right now, but you can call us at +1 416-494-5477 for more details."
- Keep responses natural and not too long unless providing menu/pricing details

Response:"""
    
    try:
        ai_response = model.generate_content(context)
        reply = ai_response.text.strip()
        
        if not reply or "i don't know" in reply.lower():
            return "I'd be happy to help! You can reach us at +1 416-494-5477 (Mississauga) or +1 905-839-0002 (Pickering) for more information."
        
        return reply
        
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# -------------------------------------------------
# STREAMLIT PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Butt Karahi Chatbot",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# CUSTOM CSS FOR BETTER DESIGN
# -------------------------------------------------
st.markdown("""
<style>
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e1e 0%, #2d2d2d 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
        font-size: 14px;
    }
    
    /* Main Header */
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5em;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        color: #f0f0f0;
        font-size: 1.1em;
        margin: 10px 0 0 0;
    }
    
    /* Button Styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Chat Input */
    .stChatInput {
        border-radius: 25px;
    }
    
    /* Sidebar Image */
    [data-testid="stSidebar"] img {
        border-radius: 10px;
        margin: 10px auto;
        display: block;
    }
    
    /* Chat Messages */
    .stChatMessage {
        border-radius: 15px;
        margin: 10px 0;
        padding: 15px;
    }
    
    /* Sidebar Button */
    [data-testid="stSidebar"] .stButton > button {
        background: #ff4b4b;
        color: white;
        width: 100%;
        margin-top: 20px;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: #ff3333;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR WITH BETTER LAYOUT
# -------------------------------------------------
with st.sidebar:
    st.image("https://i.ytimg.com/vi/jNrBUIm-rIA/hqdefault.jpg", width=180)
    
    st.markdown("### 📞 Quick Contact")
    st.markdown("**Mississauga**  \n+1 416-494-5477")
    st.markdown("**Pickering**  \n+1 905-839-0002")
    
    st.markdown("---")
    
    st.markdown("### 🕐 Hours")
    st.markdown("**Mon:** 3 PM–11 PM")
    st.markdown("**Tue-Thu:** 12 PM–11 PM")
    st.markdown("**Fri-Sat:** 12 PM–12 AM")
    st.markdown("**Sun:** 12 PM–11 PM")
    
    st.markdown("---")
    
    # Show remembered user info
    if st.session_state.user_info.get("name"):
        st.success(f"👤 **{st.session_state.user_info['name']}**")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.user_info = {}
        st.session_state.conversation_history = []
        st.rerun()

# -------------------------------------------------
# MAIN HEADER
# -------------------------------------------------
st.markdown("""
    <div class="main-header">
        <h1>Butt Karahi Chatbot</h1>
        <p>Ask about menu, prices, locations, hours & more!</p>
    </div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# QUICK ACTION BUTTONS
# -------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 Show Menu", use_container_width=True):
        st.session_state.quick_query = "show me the complete menu with prices"
with col2:
    if st.button("📍 Locations", use_container_width=True):
        st.session_state.quick_query = "what are your locations and contact details"
with col3:
    if st.button("⏰ Hours", use_container_width=True):
        st.session_state.quick_query = "what are your opening hours"

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# INITIALIZE CHAT HISTORY
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------------------------
# HANDLE QUICK QUERY BUTTONS
# -------------------------------------------------
if "quick_query" in st.session_state:
    prompt = st.session_state.quick_query
    del st.session_state.quick_query
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# -------------------------------------------------
# STREAMING RESPONSE FUNCTION
# -------------------------------------------------
def stream_response(response_text):
    for word in response_text.split():
        yield word + " "
        time.sleep(0.02)

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
if prompt := st.chat_input("Ask me anything about Butt Karahi..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate bot response
    with st.chat_message("assistant"):
        response = generate_response(prompt)
        full_response = st.write_stream(stream_response(response))
    
    # Add bot response to chat
    st.session_state.messages.append({"role": "assistant", "content": full_response})

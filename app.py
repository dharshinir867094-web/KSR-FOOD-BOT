import streamlit as st
import re

# --- PAGE SETUP ---
st.set_page_config(page_title="KSR Food Bot", layout="wide")

# --- LOGIN PAGE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("KSR Food Bot - Login 🔐")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "ksr" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong Username or Password!")
    st.stop()

# --- SIDEBAR CONTROLS (Idhu than side la varum) ---
with st.sidebar:
    st.header("⚙️ Controls")

    # Max Budget Slider
    budget = st.slider("Max Budget: ₹", 50, 500, 100)

    st.write(f"**Max Budget: ₹{budget}**")

    # Preference Dropdown
    st.write("Preference:")
    preference = st.selectbox("Preference:", ["Vegetarian", "Non-Vegetarian"], label_visibility="collapsed")

    # Location
    st.write("**Location:** College Campus • Coimbatore")

    # Project info box
    st.info("KSR Food Bot v1.0 College Project Built with Streamlit")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- MAIN CHAT PAGE ---
st.title("🍔 KSR Food Bot")
st.subheader(f"Chat • Online | Budget: ₹{budget}")

# Menu Data
veg_menu = {
    "Gobi Manchurian": 80,
    "Veg Fried Rice": 90,
    "Paneer Roll": 100,
    "Veg Noodles": 90,
    "Mushroom Fry": 95
}
non_veg_menu = {
    "Chicken Biryani": 120,
    "Chicken Fried Rice": 110,
    "Egg Noodles": 90,
    "Chicken 65": 100
}

# Auto translate Tanglish to English
def to_english(text):
    low = text.lower()
    if "enakku" in low and "venum" in low:
        nums = re.findall(r'\d+', low)
        b = nums[0] if nums else str(budget)
        return f"I need veg food under {b} rupees"
    return text

# Welcome message - FULL ENGLISH
st.write(f"👋 Hello! I'm KSR Food Bot I can help you find vegetarian food within your budget. Just tell me what you're craving and your budget!")

# Input box
user_input = st.text_input("Type your message...", placeholder="I need veg food under 100 rupees")

if st.button("Send 📤"):
    english_text = to_english(user_input)
    st.write(f"**You (in English):** {english_text}")

    # Find budget from text
    found = re.findall(r'\d+', english_text)
    final_budget = int(found[0]) if found else budget

    # Choose menu based on Preference
    current_menu = veg_menu if preference == "Vegetarian" else {**veg_menu, **non_veg_menu}

    st.write(f"**Bot Reply (English):** Foods under ₹{final_budget}:")
    for food, price in current_menu.items():
        if price <= final_budget:
            st.success(f"{food} - Rs.{price}")
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import pyperclip
import base64
import random

# Load environment variables
load_dotenv()

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
except Exception as e:
    st.error("Error configuring Gemini API. Please check your API key in the .env file.")
    st.stop()

# Set page config
st.set_page_config(
    page_title="Wisdom - Quotes in Every Language",
    page_icon="💭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Define available languages
LANGUAGES = {
    "English": "English",
    "Urdu": "Urdu",
    "Spanish": "Spanish",
    "French": "French",
    "German": "German",
    "Italian": "Italian",
    "Portuguese": "Portuguese",
    "Russian": "Russian",
    "Japanese": "Japanese",
    "Korean": "Korean",
    "Chinese": "Chinese",
    "Arabic": "Arabic",
    "Hindi": "Hindi",
    "Bengali": "Bengali",
    "Turkish": "Turkish",
    "Dutch": "Dutch",
    "Swedish": "Swedish",
    "Greek": "Greek",
    "Hebrew": "Hebrew",
    "Thai": "Thai",
    "Vietnamese": "Vietnamese",
    "Indonesian": "Indonesian",
    "Polish": "Polish",
    "Romanian": "Romanian",
    "Hungarian": "Hungarian",
    "Czech": "Czech",
    "Danish": "Danish",
    "Finnish": "Finnish",
    "Norwegian": "Norwegian",
    "Persian": "Persian",
    "Malay": "Malay",
    "Tagalog": "Tagalog",
    "Ukrainian": "Ukrainian"
}

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
        min-height: 100vh;
        animation: gradientBG 15s ease infinite;
        background-size: 400% 400%;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .stButton>button {
        background-color: #ff6b6b;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    .stButton>button:hover {
        background-color: #ff5252;
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        cursor: pointer;
        color: white;
    }
    .stButton>button:hover::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, rgba(255,255,255,0.1), rgba(255,255,255,0.2));
        animation: shine 1.5s infinite;
        z-index: 0;
    }
    @keyframes shine {
        0% { transform: translateX(-100%) skewX(-15deg); }
        100% { transform: translateX(100%) skewX(-15deg); }
    }
    .stButton>button:active {
        transform: translateY(0) scale(0.98);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .stButton>button span {
        position: relative;
        z-index: 1;
        color: white;
    }
    .stButton>button:hover span {
        color: white;
    }
    .quote-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .quote-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5);
    }
    .title {
        color: white;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 0.5em;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        animation: titleGlow 2s ease-in-out infinite alternate;
    }
    @keyframes titleGlow {
        from { text-shadow: 0 0 10px rgba(255,255,255,0.5); }
        to { text-shadow: 0 0 20px rgba(255,255,255,0.8); }
    }
    .subtitle {
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 2em;
        animation: subtitleFloat 3s ease-in-out infinite;
    }
    @keyframes subtitleFloat {
        0% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0); }
    }
    .quote-text {
        font-size: 1.5em;
        line-height: 1.6;
        color: white;
        text-align: center;
        font-style: italic;
        transition: all 0.3s ease;
    }
    .quote-text:hover {
        transform: scale(1.02);
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    .author {
        text-align: right;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1em;
        margin-top: 1em;
        transition: all 0.3s ease;
    }
    .author:hover {
        color: white;
        transform: translateX(-5px);
    }
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 2em;
        font-size: 0.9em;
        animation: footerPulse 2s ease-in-out infinite;
    }
    @keyframes footerPulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }
    [data-testid="stSelectbox"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        padding: 5px;
        color: white;
        transition: all 0.3s ease;
    }
    [data-testid="stSelectbox"]:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    .stSelectbox > div {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    .stSelectbox > div:hover {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    .stSelectbox > div > div {
        color: white !important;
    }
    .stSelectbox > div > div > div {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_quote' not in st.session_state:
    st.session_state.current_quote = None
if 'last_generated' not in st.session_state:
    st.session_state.last_generated = 0
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"
if 'emotion' not in st.session_state:
    st.session_state.emotion = "Motivational"
if 'language' not in st.session_state:
    st.session_state.language = "English"

def get_random_choice(options):
    """Get a random choice from the given options"""
    return random.choice(options)

def generate_quote(emotion, language):
    """Generate a quote based on selected emotion and language using Gemini AI"""
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Define available options
    languages = list(LANGUAGES.keys())
    emotions = ["Motivational", "Love", "Sad", "Happy", "Wisdom"]
    
    # Handle random selections
    if language == "Random":
        language = get_random_choice(languages)
    if emotion == "Random":
        emotion = get_random_choice(emotions)
    
    # Get the actual language name
    actual_language = LANGUAGES.get(language, "English")
    
    prompt = f"""Generate a detailed, powerful, and original {emotion.lower()} quote in {actual_language}. 
    The quote should be inspiring and meaningful. Make it at least 2-3 sentences long. 
    Format: 'Quote' - Author"""
    
    try:
        response = model.generate_content(prompt)
        if response.text:
            return response.text.strip()
        else:
            return "Error: No response from AI"
    except Exception as e:
        return f"Error generating quote: {str(e)}"

def copy_to_clipboard(text):
    """Copy text to clipboard"""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        st.error(f"Error copying to clipboard: {str(e)}")
        return False

def get_download_link(text, filename="motivational_quote.txt"):
    """Generate a download link for the text file"""
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="text-decoration: none; color: white;">Download Quote</a>'

def main():
    # Header
    st.markdown('<h1 class="title">💭 Wisdom</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Quotes in Every Language</p>', unsafe_allow_html=True)
    
    # Create two columns for settings
    col1, col2 = st.columns(2)
    
    with col1:
        # Language selector
        language_options = ["Random"] + list(LANGUAGES.keys())
        current_language_index = language_options.index(st.session_state.language) if st.session_state.language in language_options else 0
        language = st.selectbox(
            "🌐 Select Language",
            language_options,
            index=current_language_index
        )
    
    with col2:
        # Emotion selector
        emotion_options = ["Random", "Motivational", "Love", "Sad", "Happy", "Wisdom"]
        current_emotion_index = emotion_options.index(st.session_state.emotion)
        emotion = st.selectbox(
            "🎭 Select Emotion",
            emotion_options,
            index=current_emotion_index
        )
    
    if language != st.session_state.language or emotion != st.session_state.emotion:
        st.session_state.language = language
        st.session_state.emotion = emotion
        st.session_state.current_quote = None
    
    # Generate button
    if st.button(f"✨ Generate {'Random' if language == 'Random' or emotion == 'Random' else f'{emotion}'} Quote {'in Random Language' if language == 'Random' else f'in {language}'}", use_container_width=True):
        with st.spinner(f"Generating your {'random' if language == 'Random' or emotion == 'Random' else f'{emotion.lower()}'} quote {'in random language' if language == 'Random' else f'in {language}'}..."):
            st.session_state.current_quote = generate_quote(emotion, language)
            st.session_state.last_generated = time.time()
    
    # Display quote
    if st.session_state.current_quote:
        st.markdown('<div class="quote-box">', unsafe_allow_html=True)
        st.markdown(f'<p class="quote-text">{st.session_state.current_quote}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Create two columns for action buttons
        col3, col4 = st.columns(2)
        
        with col3:
            if st.button("📋 Copy Quote", use_container_width=True):
                if copy_to_clipboard(st.session_state.current_quote):
                    st.success("Quote copied to clipboard!")
        
        with col4:
            st.markdown(f'<div style="text-align: center;">{get_download_link(st.session_state.current_quote)}</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">Made with ❤️ by Muhammad Sami using Gemini AI and Streamlit</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
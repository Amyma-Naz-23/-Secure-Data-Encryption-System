

import streamlit as st
from cryptography.fernet import Fernet

# Set page config
st.set_page_config(page_title="Secure Encryptor", page_icon="🔐", layout="centered")

# Custom CSS for UI
st.markdown("""
    <style>
        .main {
            background-color: #f4f6f8;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #1f77b4;
        }
        .stTextInput > div > div > input {
            font-size: 16px;
            padding: 10px;
        }
        .stButton > button {
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 8px;
            background-color: #1f77b4;
            color: white;
            border: none;
        }
        .stButton > button:hover {
            background-color: #125d96;
        }
    </style>
""", unsafe_allow_html=True)

# Encryption Key (Store securely in production)
@st.cache_resource
def get_cipher():
    key = Fernet.generate_key()
    return Fernet(key)

cipher = get_cipher()

# UI
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("Secure Encryptor App")

mode = st.radio("Choose Operation:", ["Encrypt Text", "Decrypt Text"], horizontal=True)

if mode == "Encrypt Text":
    plain_text = st.text_area("Enter text to encrypt:", height=150)
    if st.button("Encrypt"):
        if plain_text:
            encrypted_text = cipher.encrypt(plain_text.encode()).decode()
            st.success("Encrypted Text:")
            st.code(encrypted_text, language="text")
        else:
            st.warning("Please enter some text to encrypt.")

elif mode == "Decrypt Text":
    encrypted_input = st.text_area("Enter encrypted text:", height=150)
    if st.button("Decrypt"):
        try:
            decrypted_text = cipher.decrypt(encrypted_input.encode()).decode()
            st.success("Decrypted Text:")
            st.code(decrypted_text, language="text")
        except Exception as e:
            st.error("Decryption failed. Please check your input.")

st.markdown("</div>", unsafe_allow_html=True)
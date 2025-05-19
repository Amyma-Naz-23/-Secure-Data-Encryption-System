import streamlit as st
from cryptography.fernet import Fernet

# Page configuration
st.set_page_config(page_title="Secure Encryptor", page_icon="🔐", layout="centered")

# Custom UI CSS
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

# Start UI
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("🔐 Secure Encryptor App")

# Choose operation
mode = st.radio("Choose Operation:", ["Encrypt Text", "Decrypt Text"], horizontal=True)

# Key input or generation
st.subheader("Encryption Key")
key_input = st.text_input("Enter encryption key (leave blank to auto-generate):")

# Validate key or generate new
def get_cipher(key_input):
    try:
        if key_input:
            key = key_input.encode()
        else:
            key = Fernet.generate_key()
        cipher = Fernet(key)
        return cipher, key.decode()
    except Exception:
        return None, None

cipher, used_key = get_cipher(key_input)

if cipher is None:
    st.error("Invalid encryption key provided.")
else:
    if mode == "Encrypt Text":
        plain_text = st.text_area("Enter text to encrypt:", height=150)
        if st.button("Encrypt"):
            if plain_text:
                encrypted_text = cipher.encrypt(plain_text.encode()).decode()
                st.success("Encryption Successful!")
                st.text("Encryption Key (Save this to decrypt later):")
                st.code(used_key)
                st.text("Encrypted Text:")
                st.code(encrypted_text)
            else:
                st.warning("Please enter some text to encrypt.")

    elif mode == "Decrypt Text":
        encrypted_input = st.text_area("Enter encrypted text:", height=150)
        if st.button("Decrypt"):
            if encrypted_input:
                try:
                    decrypted_text = cipher.decrypt(encrypted_input.encode()).decode()
                    st.success("Decrypted Text:")
                    st.code(decrypted_text)
                except Exception:
                    st.error("Decryption failed. Please check the input and the key.")
            else:
                st.warning("Please enter some encrypted text to decrypt.")

st.markdown("</div>", unsafe_allow_html=True)

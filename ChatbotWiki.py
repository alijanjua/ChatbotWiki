import wikipedia
import streamlit as st
import pyrebase
from firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

st.set_page_config(page_title="Chatbot-Wiki", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

def login_form():
    st.title("🔐 Login to Chatbot-Wiki")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.user = user
            st.success("✅ Logged in!")
        except:
            st.error("❌ Invalid credentials")

def main_app():
    st.sidebar.success(f"Logged in as {st.session_state.user['email']}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.experimental_rerun()


    if "queries" not in st.session_state:
        st.session_state["queries"] = []

    # Page config
    st.set_page_config(page_title="Chatbot-Wiki", page_icon="📚", layout="centered")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Go to", ["Home", "About", "Contact Us"])

    if menu == "Home":
        st.title("📚 Chatbot-Wiki")
        st.subheader("Ask me anything, and I'll try to get the answer from Wikipedia!")

        # Show latest queries if available
        if st.session_state["queries"]:
            st.markdown("""
                <div style="border: 1px solid #ddd; padding: 1rem; border-radius: 10px; background-color: #f9f9f9;">
                    <h4 style="margin-top: 0;">🕘 Recent Queries</h4>
            """, unsafe_allow_html=True)

            for idx, q in enumerate(st.session_state["queries"], 1):
                st.markdown(
                    f"<div style='padding: 4px 0;'><strong>{idx}.</strong> {q}</div>",
                    unsafe_allow_html=True
                )

            st.markdown("</div><br>", unsafe_allow_html=True)

        # Always show input field
        user_input = st.text_input("🔍 Enter your query:")

        # Get answer
        if st.button("Get Answer"):
            if user_input:
                try:
                    summary = wikipedia.summary(user_input, sentences=3)
                    st.success("✅ Answer:")
                    st.write(summary)

                    # Save query
                    if user_input not in st.session_state["queries"]:
                        st.session_state["queries"].insert(0, user_input)
                        st.session_state["queries"] = st.session_state["queries"][:5]

                except wikipedia.exceptions.DisambiguationError as e:
                    st.warning("⚠️ Your query is ambiguous. Please be more specific.")
                    st.write(e.options[:5])
                except wikipedia.exceptions.PageError:
                    st.error("❌ No page found for your query.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.info("Please enter a query to get started.")
    # --- About Section ---
    elif menu == "About":
        st.title("ℹ️ About Chatbot-Wiki")
        st.markdown("""
        **Chatbot-Wiki** is a simple Streamlit application that acts as a friendly Wikipedia-powered assistant.
        
        - Built with ❤️ using [Streamlit](https://streamlit.io/)
        - Uses the [Wikipedia Python API](https://pypi.org/project/wikipedia/)
        """)

    # --- Contact Us Section ---
    elif menu == "Contact Us":
        st.title("📬 Contact Us")
        st.markdown("""
        We'd love to hear from you!

        - 📧 Email: support@chatbotwiki.com
        - 🌐 Website: [chatbotwiki.com](https://chatbotwiki.com)
        - 🐦 Twitter: [@chatbotwiki](https://twitter.com/chatbotwiki)
        """)
# Show login or app
if st.session_state.user:
    main_app()
else:
    login_form()

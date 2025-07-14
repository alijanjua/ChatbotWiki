import streamlit as st
import wikipedia

# Initialize session state for recent queries
if "queries" not in st.session_state:
    st.session_state.queries = []

# Page config
st.set_page_config(page_title="Chatbot-Wiki", page_icon="📚", layout="centered")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "About", "Contact Us"])

# --- Home Section ---
if menu == "Home":
    st.title("📚 Chatbot-Wiki")
    st.subheader("Ask me anything, and I'll try to get the answer from Wikipedia!")

    user_input = st.text_input("🔍 Enter your query:")

    if st.button("Get Answer"):
        if user_input:
            try:
                summary = wikipedia.summary(user_input, sentences=3)
                st.success("✅ Answer:")
                st.write(summary)

                # Save query in session state
                if user_input not in st.session_state.queries:
                    st.session_state.queries.insert(0, user_input)
                    # Keep only last 5 queries
                    st.session_state.queries = st.session_state.queries[:5]

            except wikipedia.exceptions.DisambiguationError as e:
                st.warning("⚠️ Your query is ambiguous. Please be more specific.")
                st.write(e.options[:5])
            except wikipedia.exceptions.PageError:
                st.error("❌ No page found for your query.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.info("Please enter a query to get started.")

    # --- Show latest queries below result ---
    if st.session_state.queries:
        st.markdown("---")
        st.subheader("🕘 Latest Queries")
        for idx, q in enumerate(st.session_state.queries, 1):
            st.markdown(f"{idx}. **{q}**")

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

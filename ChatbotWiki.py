import streamlit as st
import wikipedia

# Initialize session state
if "queries" not in st.session_state:
    st.session_state["queries"] = []

# Page config
st.set_page_config(page_title="Chatbot-Wiki", page_icon="📚", layout="centered")

# Sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "About", "Contact Us"])

# --- Home Section ---
# Show latest queries on load with bordered card layout
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

    user_input = st.text_input("🔍 Enter your query:")
    if "queries" not in st.session_state:
       st.session_state["queries"] = []
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

    # Show latest queries
    if st.session_state["queries"]:
        st.markdown("---")
        st.subheader("🕘 Latest Queries")
        for idx, q in enumerate(st.session_state["queries"], 1):
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

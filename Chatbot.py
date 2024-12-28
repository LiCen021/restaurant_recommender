import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI

# Navigation State
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Home Page
if st.session_state["page"] == "home":
    st.title("Welcome to My Streamlit App")
    st.write("Press the button below to start the chatbot.")
    
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        google_map_api_key = st.text_input("Google Map API Key", key="google_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    # Embed Google Maps with iframe
# Check if API key is entered
if google_map_api_key:
    st.title("Google Maps Places Searchbox Integration")
    st.write("Type an address or place name in the search box to find its location.")

    # HTML + JavaScript for Google Maps Searchbox
    google_maps_html = f"""
    <html>
        <head>
            <title>Places Search Box</title>

            <link rel="stylesheet" type="text/css" href="./style.css" />
            <script type="module" src="./index.js"></script>
        </head>
        <body>
            <input
            id="pac-input"
            class="controls"
            type="text"
            placeholder="Search Box"
            />
            <div id="map"></div>

            <!-- 
            The `defer` attribute causes the script to execute after the full HTML
            document has been parsed. For non-blocking uses, avoiding race conditions,
            and consistent behavior across browsers, consider loading using Promises. See
            https://developers.google.com/maps/documentation/javascript/load-maps-js-api
            for more information.
            -->
            <script
            src="https://maps.googleapis.com/maps/api/js?key="+"&callback=initAutocomplete&libraries=places&v=weekly"
            defer
            ></script>
        </body>
    </html>
    """

    # Embed the Google Maps HTML code in Streamlit
    components.html(google_maps_html, height=600, scrolling=False)

else:
    st.warning("Please enter your Google Maps API Key in the sidebar to load the map.")

    if st.button("Go to Chatbot"):
        st.session_state["page"] = "chatbot"
        st.rerun()

# Chatbot Page
if st.session_state["page"] == "chatbot":


    st.title("💬 Chatbot")
    st.caption("🚀 A Streamlit chatbot powered by OpenAI")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    if st.button("Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()
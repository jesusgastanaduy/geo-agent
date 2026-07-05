import streamlit as st
from streamlit_folium import st_folium
from agent import agent
from tools import get_session_data, clear_session_data
import uuid

def generate_response(input_text, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    response = agent.invoke(
        {"messages": [{"role": "user",
                       "content": input_text}]},
        config=config
    )
    return response


st.title("Peru Wildfire Analysis Chat")

# Initialize chat history and thread_id
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # If this message has an associated map, display it
        if "map" in message:
            st_folium(message["map"], width=700, height=500, returned_objects=[])

# Accept user input
if prompt := st.chat_input("Ask about Peru wildfires..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = generate_response(prompt, st.session_state.thread_id)
        content = response["messages"][-1].content

        # Handle both string and content blocks format
        if isinstance(content, str):
            response_text = content
        else:
            response_text = content[0]['text']

        st.markdown(response_text)

        # Check if there's a pending map to display
        session_data = get_session_data()
        pending_map = session_data.pop("pending_map", None)
        map_title = session_data.pop("map_title", None)

        if pending_map is not None:
            if map_title:
                st.subheader(map_title)
            st_folium(pending_map, width=700, height=500, returned_objects=[])
            # Store the message with the map for history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "map": pending_map
            })
        else:
            # Add assistant response to chat history (no map)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

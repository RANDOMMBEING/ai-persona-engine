# app.py
import warnings
warnings.filterwarnings("ignore") # Hide scary warnings for beginners

import streamlit as st
from conversation import PersonaConversation
from personas import PERSONAS

st.set_page_config(page_title="AI Persona Engine", page_icon="🤖")

# Make a list of options for the dropdown
display_names = []
for key in PERSONAS:
    display_names.append(PERSONAS[key]["name"])

display_names.append("✨ Create Custom Persona...")

# Sidebar setup
st.sidebar.title("Persona Settings")

# Default persona if none is selected yet
if "selected_persona_key" not in st.session_state:
    st.session_state.selected_persona_key = "lawyer" # just pick the first one

# Find what index to select in the dropdown
current_index = 0
for i in range(len(display_names)):
    name = display_names[i]
    if st.session_state.selected_persona_key == "custom":
        if name == "✨ Create Custom Persona...":
            current_index = i
    else:
        if name == PERSONAS.get(st.session_state.selected_persona_key, {}).get("name"):
            current_index = i

selected_name = st.sidebar.selectbox(
    "Choose a persona or make a custom one",
    options=display_names,
    index=current_index
)

# Find the key for the name the user picked
selected_key = "custom"
for key in PERSONAS:
    if PERSONAS[key]["name"] == selected_name:
        selected_key = key

# Helper function to get the right persona dictionary
def get_persona_dict(key):
    if key == "custom":
        custom_name = st.session_state.get("custom_name", "My Custom AI")
        custom_desc = st.session_state.get("custom_desc", "A custom persona.")
        custom_prompt = st.session_state.get("custom_prompt", "You are a helpful assistant.")
        return {
            "name": custom_name,
            "description": custom_desc,
            "system_prompt": custom_prompt
        }
    else:
        return PERSONAS[key]

# Check if the user changed the persona in the dropdown
if selected_key != st.session_state.selected_persona_key:
    st.session_state.selected_persona_key = selected_key
    # start fresh conversation
    st.session_state.conversation = PersonaConversation(get_persona_dict(selected_key))
    st.rerun() # Refresh the app instantly to lock in the new selection

# First time setup
if "conversation" not in st.session_state:
    st.session_state.conversation = PersonaConversation(get_persona_dict(st.session_state.selected_persona_key))

# Show custom builder if they want to make one
if selected_key == "custom":
    st.sidebar.subheader("Custom Persona Builder")
    tab_wizard, tab_advanced = st.sidebar.tabs(["🧙‍♂️ Wizard", "⚙️ Advanced"])
    
    with tab_wizard:
        with st.form("wizard_form"):
            st.markdown("**Build a Persona step by step!**")
            custom_name_w = st.text_input("Name", value=st.session_state.get("custom_name", "My Custom AI"))
            custom_desc_w = st.text_input("Description", value=st.session_state.get("custom_desc", "A custom persona."))
            
            role_w = st.text_input("1. Who are you?", placeholder="A supportive mother...")
            tone_w = st.text_input("2. What is your tone?", placeholder="Warm, worrying, always calls me sweetie...")
            boundaries_w = st.text_input("3. Boundaries", placeholder="Never give medical advice...")
            examples_w = st.text_area("4. Dialogue Examples (Crucial!)", placeholder="User: I'm tired.\nYou: Oh sweetie, did you eat?", height=100)
            
            # When user clicks Save & Chat
            if st.form_submit_button("Save & Chat"):
                st.session_state.custom_name = custom_name_w
                st.session_state.custom_desc = custom_desc_w
                
                # Stitch the prompt together
                stitched_prompt = f"ROLE:\nYou are {role_w}\n\nTONE:\n{tone_w}\n\nBOUNDARIES:\n{boundaries_w}\n\nEXAMPLES:\n{examples_w}"
                st.session_state.custom_prompt = stitched_prompt
                
                st.session_state.conversation = PersonaConversation(get_persona_dict("custom"))
                st.rerun()

    with tab_advanced:
        with st.form("advanced_form"):
            st.markdown("**Paste your raw System Prompt here.**")
            custom_name_a = st.text_input("Name", value=st.session_state.get("custom_name", "My Custom AI"))
            custom_desc_a = st.text_input("Description", value=st.session_state.get("custom_desc", "A custom persona."))
            custom_prompt_a = st.text_area("System Prompt", value=st.session_state.get("custom_prompt", "You are a helpful assistant."), height=300)
            
            # When user clicks Save & Chat
            if st.form_submit_button("Save & Chat"):
                st.session_state.custom_name = custom_name_a
                st.session_state.custom_desc = custom_desc_a
                st.session_state.custom_prompt = custom_prompt_a
                
                st.session_state.conversation = PersonaConversation(get_persona_dict("custom"))
                st.rerun()

# Show details of current persona
st.sidebar.markdown("---")
custom_box = f"""
<div style="
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.15), rgba(26, 26, 26, 0.9));
    border-left: 4px solid #7C3AED;
    border-radius: 8px;
    padding: 16px;
    color: #e0e0e0;
    font-size: 14px;
    line-height: 1.6;
">
    <strong style="color: #A78BFA; font-size: 15px;">📖 Persona Description</strong><br><br>
    {st.session_state.conversation.persona['description']}
</div>
"""
st.sidebar.markdown(custom_box, unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Turn Count:** {st.session_state.conversation.get_turn_count()}")

# Clear Chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.conversation.reset()
    st.rerun()

# --- Main Page ---
st.title("AI Persona Engine")
st.subheader(f"Chatting with: {st.session_state.conversation.persona['name']}")

# Show old messages from memory
for msg in st.session_state.conversation.memory.chat_memory.messages:
    if msg.type == "human":
        with st.chat_message("user"):
            st.markdown(msg.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(msg.content)
            # Show latency if we saved it
            if "latency" in msg.additional_kwargs:
                latency = msg.additional_kwargs["latency"]
                st.caption(f"Response time: {latency:.0f} ms")

# Check turn limit before accepting input
MAX_TURNS = 21
turn_count = st.session_state.conversation.get_turn_count()

if turn_count >= MAX_TURNS:
    st.warning("🛑 You have reached the maximum limit of 21 turns for this session. Please click **Clear Chat** in the sidebar to start over.")
    st.chat_input("Conversation limit reached (21 turns).", disabled=True)
else:
    # Get user input
    user_input = st.chat_input("Type your message here...")
    if user_input:
        # show user message instantly
        with st.chat_message("user"):
            st.markdown(user_input)

        # get reply from AI
        with st.chat_message("assistant"):
            st_container = st.empty()
            reply, latency_ms = st.session_state.conversation.chat(user_input, st_container)
            
            # show final reply and latency
            st_container.markdown(reply)
            st.caption(f"Response time: {latency_ms:.0f} ms")

        # restart app to refresh memory display
        st.rerun()

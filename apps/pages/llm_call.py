import streamlit as st
import openai
from pydantic import BaseModel
from typing import Optional

st.markdown("# 💬 Basic LLM Call")
st.markdown("---")

st.markdown("""
### 🎯 Basic LLM Interaction
Send a message to AI, get a response. Simple as that.
""")

# Check for API key from session state
api_key = st.session_state.get("openai_api_key")

if api_key:
    client = openai.Client(api_key=api_key)
    
    # Simple example
    st.markdown("### 💬 Try a Simple Conversation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_prompt = st.text_area(
            "What would you like to ask the AI?", 
            value="Write a short poem about coding",
            height=100
        )
    
    with col2:
        model = st.selectbox("Choose Model:", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"])
        temperature = st.slider("Creativity (Temperature):", 0.0, 1.0, 0.7, 0.1)
    
    if st.button("🚀 Send to AI", type="primary"):
        try:
            with st.spinner("🤔 AI is thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=temperature
                )
            
            st.markdown("### 🎉 AI Response:")
            st.markdown(f"**{response.choices[0].message.content}**")
            
            # Show some stats
            st.markdown("### 📊 Usage Stats:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Input Tokens", response.usage.prompt_tokens)
            with col2:
                st.metric("Output Tokens", response.usage.completion_tokens)
            with col3:
                st.metric("Total Tokens", response.usage.total_tokens)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Code example section
    st.markdown("---")
    st.markdown("### 👨‍💻 Want to see the code?")
    
    with st.expander("Click to show/hide the Python code"):
        st.code("""
import openai

# Initialize the client
client = openai.Client(api_key="your-api-key-here")

# Make a simple request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Write a short poem about coding"}
    ],
    temperature=0.7
)

# Get the response
print(response.choices[0].message.content)
        """, language="python")
    
    # Structured output example
    st.markdown("---")
    st.markdown("### 🏗️ Structured Output")
    st.markdown("Get JSON instead of just text for better integration.")
    
    # Define a Pydantic model for structured output
    class EmailStructure(BaseModel):
        subject: str
        body: str
        tone: str
        urgency: Optional[str] = None
    
    email_prompt = st.text_area(
        "Email Request:", 
        value="Write a professional email asking for a day off",
        height=80
    )
    
    if st.button("📧 Generate Structured Email", type="secondary"):
        try:
            with st.spinner("✨ Creating structured response..."):
                response = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional email assistant."},
                        {"role": "user", "content": email_prompt}
                    ],
                    response_format=EmailStructure
                )
            
            email_data = response.choices[0].message.parsed
            
            st.markdown("### 📧 Structured Email Output:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Subject:**")
                st.info(email_data.subject)
                st.markdown("**Tone:**")
                st.info(email_data.tone)
                if email_data.urgency:
                    st.markdown("**Urgency:**")
                    st.info(email_data.urgency)
            
            with col2:
                st.markdown("**Email Body:**")
                st.text_area("", value=email_data.body, height=200, disabled=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with st.expander("Show structured output code"):
        st.code("""
from pydantic import BaseModel
from typing import Optional

# Define the structure we want
class EmailStructure(BaseModel):
    subject: str
    body: str
    tone: str
    urgency: Optional[str] = None

# Request structured output
response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a professional email assistant."},
        {"role": "user", "content": "Write a professional email asking for a day off"}
    ],
    response_format=EmailStructure
)

# Get structured data
email_data = response.choices[0].message.parsed
print(f"Subject: {email_data.subject}")
print(f"Body: {email_data.body}")
        """, language="python")

else:
    st.info("👆 Please enter your OpenAI API key in the sidebar to try the examples!")

# Summary section
st.markdown("---")
st.markdown("### 🧠 Summary")
st.markdown("""
- **Basic LLM**: Send prompt → get response
- **Temperature**: Controls creativity (0 = focused, 1 = creative)
- **Structured Output**: Get JSON for better integration
- **Tokens**: AI processes text in chunks (~3/4 of a word)

**Next**: Add tools to make AI more powerful 🔧
""")

st.markdown("---")
st.markdown("### 🎯 Key Takeaways")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **✅ Pros:**
    - Simple and straightforward
    - Great for text generation
    - Fast responses
    """)
with col2:
    st.markdown("""
    **❌ Limitations:**
    - No access to real-time data
    - Can't perform actions
    - Limited to training knowledge
    """) 
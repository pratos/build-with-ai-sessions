import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get default API keys from environment variables
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_EXA_API_KEY = os.getenv("EXA_API_KEY")

# Check if defaults are available
DEFAULTS_AVAILABLE = bool(DEFAULT_OPENAI_API_KEY and DEFAULT_EXA_API_KEY)

# Page configuration
st.set_page_config(
    page_title="MCPs + Agents Demo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .page-description {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.1rem;
    }
    /* Hide any default Streamlit navigation elements */
    .css-1d391kg {
        display: none;
    }
    /* Clean sidebar styling */
    .css-1lcbmhc {
        padding-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🤖 MCPs + Agents Demo</h1>', unsafe_allow_html=True)

# Centralized API Key Management
st.sidebar.markdown("### 🔑 API Keys")

# API Key mode selection
if DEFAULTS_AVAILABLE:
    key_mode = st.sidebar.selectbox(
        "API Key Mode:",
        ["Use Default Keys", "Enter Manually"],
        help="Choose to use provided demo keys or enter your own"
    )
else:
    key_mode = "Enter Manually"
    st.sidebar.info("💡 Default keys not available - enter manually")

if key_mode == "Use Default Keys" and DEFAULTS_AVAILABLE:
    # Use default keys
    api_key = DEFAULT_OPENAI_API_KEY
    exa_api_key = DEFAULT_EXA_API_KEY
    
    st.sidebar.success("🎯 Using Default Demo Keys")
    st.sidebar.info("✅ OpenAI API Key: Loaded from defaults")
    st.sidebar.info("✅ EXA API Key: Loaded from defaults")
    
else:
    # Manual key entry
    st.sidebar.markdown("**Manual Key Entry:**")
    
    # OpenAI API Key
    api_key = st.sidebar.text_input(
        "OpenAI API Key:", 
        type="password", 
        help="Get your API key from https://platform.openai.com/api-keys",
        key="global_api_key"
    )

    # EXA API Key
    exa_api_key = st.sidebar.text_input(
        "EXA API Key:", 
        type="password", 
        help="Get your API key from https://exa.ai/",
        key="global_exa_key"
    )

# Store API keys in session state for global access
if api_key:
    st.session_state.openai_api_key = api_key
else:
    st.session_state.openai_api_key = None

if exa_api_key:
    st.session_state.exa_api_key = exa_api_key
else:
    st.session_state.exa_api_key = None

# Status indicators for manual entry mode
if key_mode == "Enter Manually":
    if api_key and exa_api_key:
        st.sidebar.success("✅ All API Keys Set!")
    elif api_key:
        st.sidebar.success("✅ OpenAI Key Set!")
        st.sidebar.info("💡 Add EXA key for enhanced multi-agent features")
    elif exa_api_key:
        st.sidebar.success("✅ EXA Key Set!")
        st.sidebar.info("💡 Add OpenAI key to use interactive features")
    else:
        st.sidebar.info("👆 Enter API keys to use interactive features")

st.sidebar.markdown("---")

# Navigation Pages
pages = {
    "🏠 Home": "home",
    "💬 Basic LLM Call": "llm_call",
    "🔧 LLM + Tool Call": "tool_call", 
    "🔄 ReAct Agent": "react_agent",
    "🤝 Multi-Agent Workflow": "multi_agent",
    "⚖️ ReAct vs Multi-Agent": "comparison"
}

# Get the selected page from query params or default to home
if "page" not in st.session_state:
    st.session_state.page = "home"

# Sidebar navigation buttons
for page_name, page_key in pages.items():
    if st.sidebar.button(page_name, key=f"nav_{page_key}"):
        st.session_state.page = page_key



# Route to the appropriate page
if st.session_state.page == "home":
    st.markdown("## 🎯 Explore AI Agents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Demo Flow")
        st.markdown("""
        1. **Basic LLM Call** - Simple AI conversations
        2. **LLM + Tool Call** - AI with external tools
        3. **ReAct Agent** - AI that thinks and acts
        4. **Multi-Agent** - Multiple AIs collaborating
        """)
        
    with col2:
        st.markdown("### 🧠 Concepts")
        st.markdown("""
        **MCP**: Connect AI to external tools and data
        
        **Agents**: AI that can plan and take actions
        
        **ReAct**: Reasoning + Acting in loops
        
        **Multi-Agent**: Specialized AIs working together
        """)
    
    st.markdown("---")
    
    # Quick start info
    if DEFAULTS_AVAILABLE:
        st.markdown("### 🚀 Quick Start")
        st.info("💡 **Ready to go!** API keys loaded from `.env` file. Just select 'Use Default Keys' in the sidebar and start exploring!")
    else:
        st.markdown("### 🔑 Setup Required")
        st.warning("⚠️ No API keys found in `.env` file. Select 'Enter Manually' in the sidebar to add your keys.")
    
    st.markdown("### 👈 Pick a demo from the sidebar")

elif st.session_state.page == "llm_call":
    exec(open("apps/pages/llm_call.py").read())
elif st.session_state.page == "tool_call":
    exec(open("apps/pages/tool_call.py").read())
elif st.session_state.page == "react_agent":
    exec(open("apps/pages/react_agent.py").read())
elif st.session_state.page == "multi_agent":
    exec(open("apps/pages/multi_agent.py").read())
elif st.session_state.page == "comparison":
    exec(open("apps/pages/comparison.py").read()) 
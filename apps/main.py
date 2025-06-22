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
    
    # Weather API Key (OpenWeatherMap)
    weather_api_key = st.sidebar.text_input(
        "Weather API Key (Optional):", 
        type="password", 
        help="Get your free API key from https://openweathermap.org/api",
        key="global_weather_key"
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

if weather_api_key:
    st.session_state.weather_api_key = weather_api_key
else:
    st.session_state.weather_api_key = None

# Status indicators for manual entry mode
if key_mode == "Enter Manually":
    if api_key and exa_api_key:
        st.sidebar.success("✅ Core API Keys Set!")
        if weather_api_key:
            st.sidebar.success("✅ Weather API Key Set!")
        else:
            st.sidebar.info("💡 Add Weather key for real weather data")
    elif api_key:
        st.sidebar.success("✅ OpenAI Key Set!")
        st.sidebar.info("💡 Add EXA key for enhanced multi-agent features")
        if weather_api_key:
            st.sidebar.info("✅ Weather API Key Set!")
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
    "🔧 LLM + Tool Calling": "tool_call", 
    "🔄 ReAct Agent": "react_agent",
    "🤝 Multi-Agent": "multi_agent",
    "⚖️ Architecture Comparison": "comparison",
    "🔌 MCP Introduction": "mcp_intro",
    "🛠️ MCP Examples": "mcp_example",
    "⚡ API vs MCP": "exa_comparison",
    "🌐 MCP Deployment": "remote_mcp_comparison"
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
    st.markdown("## 🎯 Master AI Agents & Model Context Protocol")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Learning Path")
        st.markdown("""
        **🔰 Fundamentals:**
        1. **💬 Basic LLM Call** - OpenAI API basics & structured output
        2. **🔧 LLM + Tool Calling** - Connect AI to real APIs
        3. **🔄 ReAct Agent** - AI reasoning loops with live debugging
        4. **🤝 Multi-Agent** - Specialized AI teams (OpenAI Agents SDK)
        
        **🔌 Model Context Protocol (MCP):**
        5. **MCP Introduction** - Universal AI-tool connection standard
        6. **MCP Examples** - Build real servers (file, weather, analytics)
        7. **API vs MCP** - Why MCPs beat traditional integrations
        8. **MCP Deployment** - Local vs remote server options
        """)
        
    with col2:
        st.markdown("### 🧠 What You'll Build")
        st.markdown("""
        **🔧 Real Integrations:**
        - OpenWeatherMap API integration
        - Mathematical expression evaluator
        - File system operations via MCP
        - Real-time web search with Exa AI
        
        **🤖 Agent Systems:**
        - Autonomous ReAct reasoning loops
        - Multi-agent workflows with handoffs
        - Cost tracking and debugging tools
        - Production-ready MCP servers
        """)
    
    st.markdown("---")
    
    # Feature highlights
    st.markdown("### ✨ Interactive Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🔍 Live Debugging**
        
        See LLM inputs, outputs, and tool calls in real-time.
        """)
    
    with col2:
        st.info("""
        **🌐 Real API Integration**
        
        Connect to OpenWeatherMap and Exa AI with your API keys.
        """)
    
    with col3:
        st.info("""
        **📋 Copy-Paste Code**
        
        Production-ready code for your projects.
        """)
    
    # Quick start info
    if DEFAULTS_AVAILABLE:
        st.markdown("### 🚀 Quick Start")
        st.success("💡 **Ready to go!** API keys loaded from `.env` file. Just select 'Use Default Keys' in the sidebar and start exploring!")
    else:
        st.markdown("### 🔑 Setup Required")
        st.warning("⚠️ No API keys found in `.env` file. Select 'Enter Manually' in the sidebar to add your keys.")
    
    st.markdown("### 👈 Pick a demo from the sidebar to get started")

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
elif st.session_state.page == "mcp_intro":
    from pages import mcp_intro
    mcp_intro.show()
elif st.session_state.page == "mcp_example":
    from pages import mcp_example
    mcp_example.show()
elif st.session_state.page == "exa_comparison":
    from pages import exa_comparison
    exa_comparison.show()
elif st.session_state.page == "remote_mcp_comparison":
    from pages import remote_mcp_comparison
    remote_mcp_comparison.show() 
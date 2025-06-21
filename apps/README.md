# MCPs + Agents Demo Application

A comprehensive Streamlit application that introduces non-technical users to Model Context Protocol (MCPs) and AI Agents through interactive examples.

## 🎯 What This App Teaches

This application takes users through a progressive journey:

1. **💬 Basic LLM Call** - Simple AI conversations and structured outputs
2. **🔧 LLM + Tool Call** - Giving AI superpowers with external tools
3. **🔄 ReAct Agent** - AI that thinks, acts, and reasons in loops
4. **🤝 Multi-Agent Workflow** - Multiple specialized AI agents collaborating

## 🚀 How to Run

### Prerequisites

Make sure you have the required dependencies installed:

```bash
# Install dependencies (already in pyproject.toml)
pip install streamlit openai openai-agents pydantic python-dotenv
```

### Running the Application

From the project root directory:

```bash
# Run the Streamlit app
streamlit run apps/main.py
```

The application will open in your browser at `http://localhost:8501`

### API Key Setup

#### 🚀 Quick Start (Recommended)
The app comes with **default demo keys** in the `.env` file! Just:
1. Select **"Use Default Keys"** in the sidebar dropdown
2. Start exploring immediately - no setup required!

The app automatically loads API keys from the `.env` file in the project root.

#### 🔑 Use Your Own Keys
If you prefer to use your own API keys:

1. Select **"Enter Manually"** in the sidebar dropdown
2. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
3. **EXA API Key** (optional): Get from [EXA.ai](https://exa.ai/) for enhanced web search in multi-agent workflows
4. Enter keys **once** in the sidebar - they'll be used across all pages
5. Keys are only stored in your browser session and not saved anywhere

#### 📁 Environment Variables (Alternative)
You can also modify the `.env` file or set system environment variables:

**Option 1: Edit `.env` file**
```bash
# Edit the .env file in the project root
OPENAI_API_KEY=your-openai-key
EXA_API_KEY=your-exa-key
```

**Option 2: System environment variables**
```bash
export OPENAI_API_KEY="your-openai-key"
export EXA_API_KEY="your-exa-key"
```

## 📁 Application Structure

```
apps/
├── main.py              # Main Streamlit application entry point
├── pages/
│   ├── llm_call.py      # Basic LLM interactions
│   ├── tool_call.py     # Tool calling examples
│   ├── react_agent.py   # ReAct agent implementation
│   └── multi_agent.py   # Multi-agent workflows
└── README.md           # This file
```

## 🎮 Interactive Features

- **Centralized API Key**: Enter your OpenAI key once in the sidebar, use everywhere
- **Live Examples**: Try real AI interactions with your own prompts
- **Code Visibility**: Collapsible code sections to see how everything works
- **Progressive Learning**: Each page builds on the previous concepts
- **Example Scenarios**: Pre-built examples to demonstrate capabilities
- **Visual Feedback**: See AI thinking processes and tool usage in real-time

## 🛠️ Technologies Used

- **Streamlit**: Interactive web application framework
- **OpenAI SDK**: Direct API access for basic LLM and tool calling
- **OpenAI Agents SDK**: Advanced multi-agent workflows
- **Pydantic**: Structured data validation and parsing

## 🎯 Target Audience

Perfect for:
- Non-technical "vibe coders" who want to understand AI agents
- Developers new to LLM applications
- Anyone curious about how AI tools and agents work
- Teams exploring AI integration possibilities

## 🔧 Customization

You can easily customize the examples by:

1. **Adding New Tools**: Create new functions in the tool calling pages
2. **New Agent Types**: Add specialized agents in the multi-agent section  
3. **Different Examples**: Modify the example prompts and scenarios
4. **Styling**: Update the CSS in `main.py` for different themes

## 🚨 Notes

- **Default Keys Included**: Demo keys are provided for immediate use
- **EXA Integration**: Real-time web search, academic papers (arXiv), social media (Twitter), and code repositories (Papers with Code)
- **Mock Data Fallback**: Some tools use mock data when EXA is not available
- **Multi-Agent Requirements**: The multi-agent page requires the `openai-agents` package
- **API Costs**: All API calls are made directly to OpenAI and EXA (costs apply when using your own keys)
- **Real-Time Data**: With EXA enabled, get current information instead of training data cutoffs

## 🎊 Have Fun!

This app is designed to make AI agents approachable and fun. Experiment with different prompts, see how agents think, and discover the power of multi-agent collaboration!

**The future is multi-agent!** 🤖🤝🤖 
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def show():
    st.title("⚡ Exa API vs Exa MCP")
    st.markdown("*Why MCPs are superior for LLM integration*")
    
    # Overview
    st.markdown("---")
    st.markdown("## 🎯 The Integration Challenge")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("""
        **Traditional API Approach**
        
        • Custom integration for each LLM provider
        • Manual function calling setup
        • Complex error handling
        • Vendor lock-in
        • Repetitive code across projects
        """)
    
    with col2:
        st.success("""
        **MCP Approach**
        
        • Universal standard across all LLMs
        • Automatic tool discovery
        • Built-in error handling
        • Vendor agnostic
        • Reusable across projects
        """)
    
    # Step-by-step comparison
    st.markdown("---")
    st.markdown("## 📋 Step-by-Step Comparison")
    
    comparison_step = st.selectbox(
        "Choose a comparison step:",
        [
            "1️⃣ Setup & Authentication",
            "2️⃣ Function Definition", 
            "3️⃣ LLM Integration",
            "4️⃣ Error Handling",
            "5️⃣ Maintenance & Updates"
        ]
    )
    
    if comparison_step == "1️⃣ Setup & Authentication":
        show_setup_comparison()
    elif comparison_step == "2️⃣ Function Definition":
        show_function_definition_comparison()
    elif comparison_step == "3️⃣ LLM Integration":
        show_llm_integration_comparison()
    elif comparison_step == "4️⃣ Error Handling":
        show_error_handling_comparison()
    elif comparison_step == "5️⃣ Maintenance & Updates":
        show_maintenance_comparison()

def show_setup_comparison():
    st.markdown("### 1️⃣ Setup & Authentication")
    
    tab1, tab2 = st.tabs(["🔴 Traditional API", "🟢 MCP Approach"])
    
    with tab1:
        st.markdown("**Traditional Exa API Setup:**")
        st.code("""
# Multiple files needed for different LLM providers
from openai import OpenAI
from exa_py import Exa
import anthropic

openai_client = OpenAI(api_key="sk-...")
exa_client = Exa(api_key="exa-key...")
claude_client = anthropic.Anthropic(api_key="claude-key...")

# Separate Exa integration for each provider
def exa_search_openai(query):
    # Custom OpenAI function calling setup
    pass

def exa_search_claude(query):
    # Custom Claude tool setup  
    pass
        """, language="python")
        
        st.error("**Problems:** Separate setup for each LLM provider, multiple API clients, code duplication")
    
    with tab2:
        st.markdown("**MCP Approach:**")
        st.code("""
# Single MCP server works with ALL LLM providers
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from exa_py import Exa

# Single server setup
server = Server("exa-search")
exa_client = Exa(api_key=os.getenv("EXA_API_KEY"))

@server.list_tools()
async def list_tools():
    return ListToolsResult(tools=[
        Tool(name="web_search", description="Search the web", ...),
        Tool(name="company_research", description="Research companies", ...)
    ])

# Works with OpenAI, Claude, Gemini, or any MCP-compatible LLM
if __name__ == "__main__":
    asyncio.run(stdio_server(server))
        """, language="python")
        
        st.success("**Benefits:** Single server for all LLM providers, one authentication setup, no code duplication")

def show_function_definition_comparison():
    st.markdown("### 2️⃣ Function Definition")
    
    tab1, tab2 = st.tabs(["🔴 Traditional API", "🟢 MCP Approach"])
    
    with tab1:
        st.code("""
# OpenAI Function Calling
openai_tools = [{
    "type": "function",
    "function": {
        "name": "exa_web_search",
        "description": "Search the web using Exa",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "num_results": {"type": "integer"}
            }
        }
    }
}]

# Claude Tools (different format)
claude_tools = [{
    "name": "exa_web_search",
    "description": "Search the web using Exa",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "num_results": {"type": "integer"}
        }
    }
}]
        """, language="python")
        
        st.error("**Problems:** Different schema formats, manual repetition, separate implementations")
    
    with tab2:
        st.code("""
# Single tool definition works everywhere
@server.list_tools()
async def list_tools() -> ListToolsResult:
    return ListToolsResult(tools=[
        Tool(
            name="exa_web_search",
            description="Search the web using Exa AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        )
    ])

# This SAME code works with OpenAI, Claude, Gemini, etc.
        """, language="python")
        
        st.success("**Benefits:** Single definition, automatic schema conversion, consistent behavior")

def show_llm_integration_comparison():
    st.markdown("### 3️⃣ LLM Integration")
    
    tab1, tab2 = st.tabs(["🔴 Traditional API", "🟢 MCP Approach"])
    
    with tab1:
        st.code("""
# OpenAI Integration
def chat_with_openai(query):
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        tools=openai_tools
    )
    # Handle tool calls manually for OpenAI...

# Claude Integration  
def chat_with_claude(query):
    response = claude_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": query}],
        tools=claude_tools
    )
    # Different tool handling for Claude...
        """, language="python")
        
        st.error("**Problems:** Different integration code, different tool mechanisms, high maintenance")
    
    with tab2:
        st.code("""
# Universal MCP client works with ANY LLM provider
class UniversalMCPAgent:
    async def connect_mcp_server(self):
        server_params = StdioServerParameters(
            command="python", 
            args=["exa_mcp_server.py"]
        )
        
        self.mcp_session = await ClientSession(read, write).__aenter__()
        await self.mcp_session.initialize()
        
        # Auto-discover tools (works with any MCP server)
        tools_result = await self.mcp_session.list_tools()
        self.available_tools = tools_result.tools
    
    async def chat(self, query):
        # Same interface for all providers!
        return await self.process_with_mcp_tools(query)

# Usage - Same interface for all providers!
agent = UniversalMCPAgent()
        """, language="python")
        
        st.success("**Benefits:** Universal integration, automatic tool discovery, provider-agnostic")

def show_error_handling_comparison():
    st.markdown("### 4️⃣ Error Handling")
    
    tab1, tab2 = st.tabs(["🔴 Traditional API", "🟢 MCP Approach"])
    
    with tab1:
        st.code("""
# Separate error handling for each provider
def handle_openai_exa_search(args):
    try:
        results = exa_client.search(args["query"])
        return {"status": "success", "data": results}
    except ExaAPIError as e:
        return {"status": "error", "message": str(e)}

def handle_claude_exa_search(args):
    # Duplicate error handling with different format
    try:
        results = exa_client.search(args["query"])
        return claude_format_success(results)
    except ExaAPIError as e:
        return claude_format_error(str(e))
        """, language="python")
        
        st.error("**Problems:** Duplicate error handling, inconsistent formats, manual routing")
    
    with tab2:
        st.code("""
# Single error handling in MCP server works for all providers
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "exa_web_search":
        try:
            results = exa_client.search(
                query=arguments["query"],
                num_results=arguments.get("num_results", 5)
            )
            
            return CallToolResult(
                content=[TextContent(type="text", text=format_results(results))]
            )
            
        except ExaAPIError as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Search error: {str(e)}")],
                isError=True
            )

# MCP automatically handles error propagation to all LLM providers
        """, language="python")
        
        st.success("**Benefits:** Single error handling, consistent messages, automatic propagation")

def show_maintenance_comparison():
    st.markdown("### 5️⃣ Maintenance & Updates")
    
    tab1, tab2 = st.tabs(["🔴 Traditional API", "🟢 MCP Approach"])
    
    with tab1:
        st.code("""
# When Exa API updates, update EVERY integration

# Update OpenAI integration
openai_tools[0]["function"]["parameters"]["properties"]["search_type"] = {
    "type": "string", "enum": ["neural", "keyword"]
}

# Update Claude integration  
claude_tools[0]["input_schema"]["properties"]["search_type"] = {
    "type": "string", "enum": ["neural", "keyword"]
}

# Update all handler functions
def handle_openai_exa_search(args):
    results = exa_client.search(args["query"], search_type=args.get("search_type"))

def handle_claude_exa_search(args):
    results = exa_client.search(args["query"], search_type=args.get("search_type"))
        """, language="python")
        
        st.error("**Problems:** Update multiple files, risk of inconsistencies, time-consuming testing")
    
    with tab2:
        st.code("""
# When Exa API updates, update ONLY the MCP server

# Single update in MCP server
@server.list_tools()
async def list_tools() -> ListToolsResult:
    return ListToolsResult(tools=[
        Tool(
            name="exa_web_search",
            inputSchema={
                "properties": {
                    "query": {"type": "string"},
                    "search_type": {  # NEW PARAMETER - added once
                        "type": "string",
                        "enum": ["neural", "keyword"],
                        "default": "neural"
                    }
                }
            }
        )
    ])

# ALL LLM providers automatically get the update!
        """, language="python")
        
        st.success("**Benefits:** Single point of update, automatic propagation, reduced risk of bugs")

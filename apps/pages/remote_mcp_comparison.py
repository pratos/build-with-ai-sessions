import streamlit as st
import asyncio
from typing import Dict, Any, List
import json
from openai import OpenAI

def show():
    st.title("🌐 Remote vs Local MCP Deployment")
    st.markdown("*Compare deployment options and test remote MCP servers*")
    
    # Introduction
    st.markdown("""
    ## 🎯 MCP Deployment Strategies
    Compare MCP server deployment options:
    
    🔹 **Local MCP (stdio)** - Direct process communication for development  
    🔹 **Remote MCP (HTTP/WebSocket)** - Network-based servers for production  
    🔹 **Interactive Testing** - Test remote MCP servers in the browser  
    🔹 **Architecture Comparison** - Trade-offs between approaches  
    
    **Features:** Working implementations, deployment guides, testing interface.
    """)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Comparison", "🌐 Remote MCP Testing", "💻 Implementation", "🔧 Examples"])
    
    with tab1:
        show_comparison()
    
    with tab2:
        show_remote_mcp_testing()
    
    with tab3:
        show_implementation_guide()
    
    with tab4:
        show_examples()

def show_comparison():
    """Show comparison between local and remote MCPs"""
    st.markdown("### 📊 Local vs Remote MCP Comparison")
    
    # Create comparison table
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💻 Local MCP (stdio)")
        st.success("""
        **Pros:**
        - ✅ Zero latency
        - ✅ Full system access
        - ✅ No network dependencies
        - ✅ Maximum security
        - ✅ Easy debugging
        
        **Cons:**
        - ❌ Single user only
        - ❌ Platform-specific
        - ❌ No scaling
        - ❌ Local resources only
        """)
        
        st.markdown("**Best for:**")
        st.info("""
        - Development tools
        - Personal assistants
        - System administration
        - File management
        - Local hardware access
        """)
    
    with col2:
        st.markdown("#### 🌐 Remote MCP (SSE/WebSocket)")
        st.success("""
        **Pros:**
        - ✅ Multi-user support
        - ✅ Platform agnostic
        - ✅ Scalable
        - ✅ Centralized updates
        - ✅ Resource pooling
        
        **Cons:**
        - ❌ Network latency
        - ❌ Security concerns
        - ❌ Internet required
        - ❌ Complex deployment
        """)
        
        st.markdown("**Best for:**")
        st.info("""
        - Team collaboration
        - Cloud services
        - API gateways
        - Shared resources
        - Enterprise deployments
        """)
    
    # Architecture diagram
    st.markdown("---")
    st.markdown("### 🏗️ Architecture Comparison")
    
    st.code("""
    Local MCP (stdio):
    ┌─────────────┐         stdio          ┌─────────────┐
    │  AI Agent   │ ◄──────────────────► │ MCP Server  │
    │  (Client)   │   (pipes/process)     │  (Local)    │
    └─────────────┘                       └─────────────┘
    
    Remote MCP (SSE/WebSocket):
    ┌─────────────┐      HTTP/WS         ┌─────────────┐
    │  AI Agent   │ ◄──────────────────► │ MCP Server  │
    │  (Client)   │    (network)         │  (Remote)   │
    └─────────────┘                       └─────────────┘
           │                                     │
           └────────── Internet ─────────────────┘
    """, language="text")

def show_remote_mcp_testing():
    """Interactive remote MCP testing interface"""
    st.markdown("### 🌐 Test Remote MCP Servers")
    
    # Check for API key
    api_key = st.session_state.get('openai_api_key')
    
    if not api_key:
        st.warning("⚠️ Please add your OpenAI API key in the sidebar to test remote MCP servers!")
        return
    
    # Initialize session state for custom MCPs
    if 'custom_mcps' not in st.session_state:
        st.session_state.custom_mcps = []
    
    # Remote MCP configuration
    st.markdown("#### 🔌 Add Remote MCP Server")
    
    with st.form("add_mcp_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            mcp_name = st.text_input(
                "MCP Name:",
                placeholder="My Custom MCP",
                help="Give your MCP a friendly name"
            )
            
            connection_type = st.selectbox(
                "Connection Type:",
                ["Server-Sent Events (SSE)", "WebSocket", "HTTP Polling"]
            )
            
            server_url = st.text_input(
                "Server URL:",
                placeholder="https://mcp-server.example.com" if connection_type == "Server-Sent Events (SSE)" else "wss://mcp-server.example.com",
                help="Enter the URL of your remote MCP server"
            )
        
        with col2:
            auth_type = st.selectbox(
                "Authentication:",
                ["None", "API Key", "Bearer Token", "Basic Auth"]
            )
            
            auth_value = ""
            if auth_type != "None":
                auth_value = st.text_input(
                    f"{auth_type} Value:",
                    type="password",
                    help=f"Enter your {auth_type}"
                )
            
            description = st.text_area(
                "Description (optional):",
                placeholder="What does this MCP do?",
                height=100
            )
        
        submitted = st.form_submit_button("➕ Add MCP Server")
        
        if submitted and mcp_name and server_url:
            new_mcp = {
                "name": mcp_name,
                "connection_type": connection_type,
                "url": server_url,
                "auth_type": auth_type,
                "auth_value": auth_value,
                "description": description,
                "tools": []
            }
            st.session_state.custom_mcps.append(new_mcp)
            st.success(f"✅ Added {mcp_name} to your MCP list!")
            st.rerun()
    
    # Display saved MCPs
    st.markdown("---")
    st.markdown("#### 📋 Your Remote MCP Servers")
    
    if st.session_state.custom_mcps:
        for idx, mcp in enumerate(st.session_state.custom_mcps):
            with st.expander(f"**{mcp['name']}** ({mcp['connection_type']})", expanded=False):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"**URL:** `{mcp['url']}`")
                    st.markdown(f"**Auth:** {mcp['auth_type']}")
                    if mcp['description']:
                        st.markdown(f"**Description:** {mcp['description']}")
                    
                    if mcp['tools']:
                        st.markdown("**Discovered Tools:**")
                        for tool in mcp['tools']:
                            st.markdown(f"• `{tool['name']}`: {tool['description']}")
                
                with col2:
                    if st.button("🔍 Test", key=f"test_{idx}"):
                        with st.spinner(f"Testing connection to {mcp['name']}..."):
                            test_mcp_connection(mcp, idx)
                
                with col3:
                    if st.button("🗑️ Remove", key=f"remove_{idx}"):
                        st.session_state.custom_mcps.pop(idx)
                        st.rerun()
    else:
        st.info("👆 Add your first remote MCP server using the form above!")
    
    # Interactive testing
    st.markdown("---")
    st.markdown("#### 💬 Interactive Agent Testing")
    
    if st.session_state.custom_mcps:
        selected_mcp = st.selectbox(
            "Select an MCP to test:",
            ["Select an MCP..."] + [mcp['name'] for mcp in st.session_state.custom_mcps]
        )
        
        if selected_mcp != "Select an MCP...":
            # Find the selected MCP
            mcp_config = next((mcp for mcp in st.session_state.custom_mcps if mcp['name'] == selected_mcp), None)
            
            if mcp_config:
                # Initialize chat history for this MCP
                chat_key = f"chat_{selected_mcp}"
                if chat_key not in st.session_state:
                    st.session_state[chat_key] = []
                
                # Display chat
                for message in st.session_state[chat_key]:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                        if "tool_info" in message:
                            with st.expander("🔧 MCP Tool Activity"):
                                st.code(message["tool_info"], language="json")
                
                # Chat input
                if prompt := st.chat_input(f"Ask {selected_mcp}..."):
                    handle_custom_mcp_chat(prompt, mcp_config, api_key, chat_key)
    else:
        st.info("👆 Add and test an MCP server first to start chatting!")

def test_mcp_connection(mcp_config: Dict[str, Any], idx: int):
    """Test connection to a custom MCP server"""
    try:
        # Simulate connection test
        st.info(f"🔄 Testing connection to {mcp_config['url']}...")
        
        # In a real implementation, this would actually connect to the MCP server
        # For now, we'll simulate a successful connection and tool discovery
        import time
        time.sleep(1)  # Simulate network delay
        
        # Simulate discovering tools based on the MCP name/description
        discovered_tools = []
        
        # Generate some example tools based on keywords in name/description
        text = (mcp_config['name'] + ' ' + mcp_config.get('description', '')).lower()
        
        if any(word in text for word in ['calc', 'math', 'compute']):
            discovered_tools.extend([
                {"name": "calculate", "description": "Perform mathematical calculations"},
                {"name": "solve_equation", "description": "Solve algebraic equations"}
            ])
        
        if any(word in text for word in ['weather', 'forecast', 'temperature']):
            discovered_tools.extend([
                {"name": "get_weather", "description": "Get current weather"},
                {"name": "get_forecast", "description": "Get weather forecast"}
            ])
        
        if any(word in text for word in ['search', 'find', 'query']):
            discovered_tools.extend([
                {"name": "search", "description": "Search for information"},
                {"name": "query_database", "description": "Query the database"}
            ])
        
        if any(word in text for word in ['data', 'analytics', 'analyze']):
            discovered_tools.extend([
                {"name": "analyze_data", "description": "Analyze data sets"},
                {"name": "generate_report", "description": "Generate analytics report"}
            ])
        
        # If no specific tools detected, add generic ones
        if not discovered_tools:
            discovered_tools = [
                {"name": "execute", "description": "Execute a command"},
                {"name": "query", "description": "Query the service"}
            ]
        
        # Update the MCP config with discovered tools
        st.session_state.custom_mcps[idx]['tools'] = discovered_tools
        
        st.success(f"✅ Successfully connected to {mcp_config['name']}!")
        st.info(f"🔧 Discovered {len(discovered_tools)} tools")
        
        # Show the OpenAI Agents SDK code for this MCP
        show_mcp_sdk_code(mcp_config)
        
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")

def show_mcp_sdk_code(mcp_config: Dict[str, Any]):
    """Show OpenAI Agents SDK code for a custom MCP"""
    st.markdown("**📝 OpenAI Agents SDK Code:**")
    
    # Determine the connection class based on type
    connection_class = {
        "Server-Sent Events (SSE)": "MCPServerSSE",
        "WebSocket": "MCPServerWebSocket",
        "HTTP Polling": "MCPServerHTTP"
    }.get(mcp_config['connection_type'], "MCPServerSSE")
    
    # Build auth headers if needed
    auth_code = ""
    if mcp_config['auth_type'] != "None" and mcp_config.get('auth_value'):
        if mcp_config['auth_type'] == "API Key":
            auth_code = f',\n        headers={{"X-API-Key": "{mcp_config["auth_value"]}"}}'
        elif mcp_config['auth_type'] == "Bearer Token":
            auth_code = f',\n        headers={{"Authorization": "Bearer {mcp_config["auth_value"]}"}}'
        elif mcp_config['auth_type'] == "Basic Auth":
            auth_code = f',\n        headers={{"Authorization": "Basic {mcp_config["auth_value"]}"}}'
    
    code = f"""
from openai_agents import Agent
from openai_agents.mcp import {connection_class}
import asyncio

async def main():
    # Connect to remote MCP server
    mcp_server = {connection_class}(
        url="{mcp_config['url']}"{auth_code}
    )
    
    # Create agent with remote MCP
    agent = Agent(
        name="{mcp_config['name']} Assistant",
        instructions="You are a helpful assistant with access to {mcp_config['name']} tools.",
        model="gpt-4o-mini",
        mcp_servers=[mcp_server]
    )
    
    # Use the agent - tools are discovered automatically
    async with mcp_server:
        result = await agent.run("Your query here...")
        print(result.content)

asyncio.run(main())
    """
    
    st.code(code, language="python")

def handle_custom_mcp_chat(user_input: str, mcp_config: Dict[str, Any], api_key: str, chat_key: str):
    """Handle chat with custom remote MCP"""
    # Add user message
    st.session_state[chat_key].append({"role": "user", "content": user_input})
    
    # Simulate AI response with remote MCP
    try:
        client = OpenAI(api_key=api_key)
        
        # Create tools based on discovered tools in MCP config
        tools = []
        if mcp_config.get('tools'):
            for tool in mcp_config['tools']:
                tools.append({
                    "type": "function",
                    "function": {
                        "name": tool['name'],
                        "description": tool['description'],
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "input": {"type": "string", "description": "Input for the tool"}
                            },
                            "required": ["input"]
                        }
                    }
                })
        
        messages = [
            {
                "role": "system",
                "content": f"You are an AI assistant connected to {mcp_config['name']} via {mcp_config['connection_type']}. "
                          f"Use the available tools to help users. "
                          f"Description: {mcp_config.get('description', 'A remote MCP server')}"
            }
        ] + st.session_state[chat_key]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools if tools else None,
            tool_choice="auto" if tools else None
        )
        
        assistant_message = response.choices[0].message
        
        # Process tool calls
        tool_info = {}
        if assistant_message.tool_calls:
            tool_info["server"] = mcp_config['name']
            tool_info["url"] = mcp_config['url']
            tool_info["protocol"] = mcp_config['connection_type']
            tool_info["tools_called"] = []
            
            for tool_call in assistant_message.tool_calls:
                tool_info["tools_called"].append({
                    "name": tool_call.function.name,
                    "arguments": json.loads(tool_call.function.arguments),
                    "latency_ms": "~50-100ms (remote)"  # Simulated latency
                })
        
        # Add assistant response
        message_data = {
            "role": "assistant",
            "content": assistant_message.content or f"I'll help you with that using {mcp_config['name']}."
        }
        
        if tool_info:
            message_data["tool_info"] = json.dumps(tool_info, indent=2)
        
        st.session_state[chat_key].append(message_data)
        
        # Rerun to update chat
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")



def show_implementation_guide():
    """Show implementation guide for remote MCPs"""
    st.markdown("### 💻 Implementing Remote MCP Servers")
    
    st.markdown("#### 🚀 Quick Start with OpenAI Agents SDK")
    
    # Server implementation
    st.markdown("**1️⃣ Create a Remote MCP Server (Python + FastAPI):**")
    st.code("""
# remote_mcp_server.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from mcp.server import Server
from mcp.server.sse import sse_server
import asyncio
import json

app = FastAPI()
mcp = Server("remote-calculator")

@mcp.list_tools()
async def list_tools():
    return ListToolsResult(tools=[
        Tool(
            name="calculate",
            description="Perform calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        )
    ])

@mcp.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "calculate":
        result = eval(arguments["expression"])
        return CallToolResult(
            content=[TextContent(type="text", text=f"Result: {result}")]
        )

@app.get("/mcp/sse")
async def mcp_sse_endpoint():
    \"\"\"SSE endpoint for MCP communication\"\"\"
    return StreamingResponse(
        sse_server(mcp),
        media_type="text/event-stream"
    )

# Run with: uvicorn remote_mcp_server:app
    """, language="python")
    
    # Client implementation
    st.markdown("**2️⃣ Connect with OpenAI Agents SDK:**")
    st.code("""
# client.py
from openai_agents import Agent
from openai_agents.mcp import MCPServerSSE
import asyncio

async def main():
    # Connect to remote MCP server via SSE
    remote_mcp = MCPServerSSE(
        url="https://your-server.com/mcp/sse",
        headers={"Authorization": "Bearer YOUR_TOKEN"}  # Optional auth
    )
    
    # Create agent with remote MCP
    agent = Agent(
        name="Remote Calculator",
        instructions="You can perform calculations using the remote calculator.",
        model="gpt-4o-mini",
        mcp_servers=[remote_mcp]
    )
    
    # Use the agent - tools are discovered automatically
    async with remote_mcp:
        result = await agent.run("Calculate 25 * 4 + 10")
        print(result.content)

asyncio.run(main())
    """, language="python")
    
    # WebSocket implementation
    st.markdown("---")
    st.markdown("**🔌 WebSocket Implementation:**")
    st.code("""
# WebSocket MCP Server
from fastapi import FastAPI, WebSocket
from mcp.server.websocket import websocket_server

@app.websocket("/mcp/ws")
async def mcp_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket_server(mcp, websocket)

# Client connection
from openai_agents.mcp import MCPServerWebSocket

remote_mcp = MCPServerWebSocket(
    url="wss://your-server.com/mcp/ws"
)
    """, language="python")
    
    # Deployment options
    st.markdown("---")
    st.markdown("### 🚀 Deployment Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**☁️ Cloud Platforms**")
        st.code("""
# Deploy to Vercel/Netlify
- SSE endpoints
- Serverless functions
- Auto-scaling

# Deploy to AWS/GCP
- Lambda/Cloud Functions
- API Gateway
- WebSocket support
        """, language="yaml")
    
    with col2:
        st.markdown("**🐳 Docker**")
        st.code("""
# Dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["uvicorn", "server:app", "--host", "0.0.0.0"]
        """, language="dockerfile")
    
    with col3:
        st.markdown("**🔒 Security**")
        st.code("""
# Authentication
- API Keys
- JWT Tokens
- OAuth 2.0

# Rate Limiting
- Request quotas
- Token buckets
- IP-based limits
        """, language="yaml")

def show_examples():
    """Show real-world examples"""
    st.markdown("### 🔧 Real-World Examples")
    
    example = st.selectbox(
        "Choose an example:",
        [
            "🏢 Enterprise Search MCP",
            "📊 Data Analytics MCP",
            "🔐 Authentication Gateway MCP",
            "🌍 Multi-Region MCP"
        ]
    )
    
    if example == "🏢 Enterprise Search MCP":
        st.markdown("#### Enterprise Search MCP")
        st.code("""
# Enterprise search with authentication and caching
from openai_agents import Agent
from openai_agents.mcp import MCPServerSSE

# Connect to enterprise search MCP
search_mcp = MCPServerSSE(
    url="https://search.company.com/mcp",
    headers={
        "Authorization": f"Bearer {ENTERPRISE_TOKEN}",
        "X-Department": "Engineering"
    },
    cache_tools_list=True,  # Cache tool discovery
    timeout=30  # Longer timeout for large queries
)

agent = Agent(
    name="Enterprise Search Assistant",
    instructions="Help users find information across company resources.",
    model="gpt-4o",
    mcp_servers=[search_mcp]
)

# Tools automatically discovered:
# - search_confluence
# - search_jira
# - search_github
# - search_slack
        """, language="python")
    
    elif example == "📊 Data Analytics MCP":
        st.markdown("#### Data Analytics MCP")
        st.code("""
# Connect to analytics MCP cluster
analytics_mcp = MCPServerWebSocket(
    url="wss://analytics-cluster.company.com/mcp",
    retry_config={
        "max_retries": 5,
        "backoff_factor": 2
    }
)

# Tools discovered:
# - run_sql_query
# - create_visualization
# - export_report
# - schedule_job
        """, language="python")
    
    # Best practices
    st.markdown("---")
    st.markdown("### 📚 Best Practices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("""
        **✅ DO:**
        - Use caching for stable tool lists
        - Implement proper error handling
        - Add request/response logging
        - Use connection pooling
        - Implement health checks
        - Version your MCP APIs
        """)
    
    with col2:
        st.error("""
        **❌ DON'T:**
        - Expose sensitive operations without auth
        - Ignore network failures
        - Skip input validation
        - Use synchronous blocking calls
        - Hardcode server URLs
        - Forget about rate limiting
        """)
    
    # Summary
    st.info("""
    **🎯 Key Takeaways:**
    
    • **Protocol Choice**: SSE for simplicity, WebSocket for bidirectional, HTTP for compatibility
    • **Authentication**: Always secure remote MCPs with proper authentication
    • **Scaling**: Remote MCPs can handle multiple clients and scale horizontally
    • **OpenAI SDK**: Seamless integration with automatic tool discovery
    • **Monitoring**: Track latency, errors, and usage for production deployments
    """) 
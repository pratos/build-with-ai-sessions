import streamlit as st
import os
import asyncio
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def show():
    st.title("🛠️ Hands-on MCP Examples")
    st.markdown("*Build and test real MCP servers with interactive examples*")
    
    # Introduction
    st.markdown("""
    ### 🎯 Learn MCP by Building
    Hands-on MCP server examples:
    
    🔹 **Interactive Testing** - Test MCP tools directly in the browser  
    🔹 **Real MCP Servers** - Complete implementations you can run  
    🔹 **Multiple Examples** - File operations, calculations, weather, analytics  
    🔹 **OpenAI Agents SDK** - Integration examples  
    
    **Features:** Copy-paste ready code, interactive demos, production examples.
    """)
    
    # Example selection
    st.markdown("---")
    st.markdown("## 📋 Choose Your MCP Example")
    
    example_choice = st.selectbox(
        "Select an MCP example to explore:",
        [
            "🧪 Interactive Testing",
            "📝 Simple File Server",
            "🧮 Calculator Server", 
            "🌤️ Weather Server",
            "📊 Data Analytics Server"
        ]
    )
    
    if example_choice == "🧪 Interactive Testing":
        # Check if API key is available
        api_key = st.session_state.get('openai_api_key')
        
        if not api_key:
            st.warning("⚠️ Please add your OpenAI API key in the sidebar to test MCP tools interactively!")
        else:
            show_interactive_mcp_test()
    elif example_choice == "📝 Simple File Server":
        show_file_server_example()
    elif example_choice == "🧮 Calculator Server":
        show_calculator_server_example()
    elif example_choice == "🌤️ Weather Server":
        show_weather_server_example()
    elif example_choice == "📊 Data Analytics Server":
        show_analytics_server_example()

def show_file_server_example():
    st.markdown("### 📝 Simple File Server MCP")
    st.markdown("This example shows how to create an MCP server that can read and write files using the OpenAI Agents SDK.")
    
    tab1, tab2, tab3 = st.tabs(["📄 MCP Server Code", "🤖 OpenAI Agent Code", "🚀 Usage Example"])
    
    with tab1:
        st.markdown("**MCP Server Implementation:**")
        st.code("""
# file_server.py
import asyncio
import json
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, TextContent, 
    CallToolResult, ListResourcesResult, ListToolsResult, ReadResourceResult
)
import os
from pathlib import Path

# Create MCP server
server = Server("file-server")

@server.list_resources()
async def list_resources() -> ListResourcesResult:
    \"\"\"List available files in the current directory\"\"\"
    resources = []
    for file_path in Path(".").glob("*.txt"):
        resources.append(
            Resource(
                uri=f"file://{file_path.absolute()}",
                name=file_path.name,
                description=f"Text file: {file_path.name}",
                mimeType="text/plain"
            )
        )
    return ListResourcesResult(resources=resources)

@server.read_resource()
async def read_resource(uri: str) -> ReadResourceResult:
    \"\"\"Read a file resource\"\"\"
    if not uri.startswith("file://"):
        raise ValueError("Only file:// URIs are supported")
    
    file_path = uri[7:]  # Remove "file://"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return ReadResourceResult(
            contents=[TextContent(type="text", text=content)]
        )
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    \"\"\"List available tools\"\"\"
    return ListToolsResult(
        tools=[
            Tool(
                name="write_file",
                description="Write content to a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Name of the file"},
                        "content": {"type": "string", "description": "Content to write"}
                    },
                    "required": ["filename", "content"]
                }
            ),
            Tool(
                name="read_file",
                description="Read content from a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Name of the file to read"}
                    },
                    "required": ["filename"]
                }
            )
        ]
    )

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    \"\"\"Handle tool calls\"\"\"
    if name == "write_file":
        filename = arguments["filename"]
        content = arguments["content"]
        
        try:
            with open(filename, 'w') as f:
                f.write(content)
            return CallToolResult(
                content=[TextContent(type="text", text=f"Successfully wrote to {filename}")]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error writing file: {str(e)}")],
                isError=True
            )
    
    elif name == "read_file":
        filename = arguments["filename"]
        
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return CallToolResult(
                content=[TextContent(type="text", text=f"File content:\\n{content}")]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error reading file: {str(e)}")],
                isError=True
            )
    
    else:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Unknown tool: {name}")],
            isError=True
        )

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
        """, language="python")
    
    with tab2:
        st.markdown("**OpenAI Agent with MCP Integration using Official SDK:**")
        st.code("""
# agent_with_mcp.py
import asyncio
from openai_agents import Agent
from openai_agents.mcp import MCPServerStdio

async def main():
    # Create MCP server connection (stdio)
    mcp_server = MCPServerStdio(
        params={
            "command": "python",
            "args": ["file_server.py"],
        }
    )
    
    # Create agent with MCP server
    agent = Agent(
        name="File Assistant",
        instructions="You are a helpful assistant that can read and write files. Use the available tools to help users manage their files.",
        model="gpt-4o-mini",
        mcp_servers=[mcp_server]
    )
    
    # Run the agent
    async with mcp_server:
        # The agent will automatically discover tools from the MCP server
        result = await agent.run("Create a file called 'hello.txt' with the content 'Hello, MCP World!'")
        print(result.content)
        
        # Read the file back
        result = await agent.run("Read the contents of hello.txt")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
        """, language="python")
        
        st.info("💡 **Key Features of OpenAI Agents SDK MCP Integration:**")
        st.markdown("""
        • **Automatic Tool Discovery**: The agent automatically calls `list_tools()` on MCP servers
        • **Seamless Integration**: MCP tools appear as regular function calls to the LLM
        • **Multiple Server Support**: Add multiple MCP servers to a single agent
        • **Caching**: Use `cache_tools_list=True` for better performance with stable tool lists
        • **Tracing**: Automatic tracing of MCP operations for debugging
        """)
    
    with tab3:
        st.markdown("**Usage Example:**")
        st.code("""
# Run the MCP server
python file_server.py

# In another terminal, run the agent
python agent_with_mcp.py

# Output:
# Successfully wrote to hello.txt
# File content:
# Hello, MCP World!
        """, language="bash")
        
        st.markdown("**🎯 Benefits of This Approach:**")
        st.markdown("""
        • **Standardized**: Uses the official MCP protocol
        • **Scalable**: Easy to add more tools and capabilities
        • **Maintainable**: Clean separation between tools and AI logic
        • **Reusable**: MCP servers can be used by any MCP-compatible client
        • **Future-proof**: Built on open standards
        """)

def show_calculator_server_example():
    st.markdown("### 🧮 Calculator Server MCP")
    st.markdown("An MCP server that provides mathematical calculation tools using the OpenAI Agents SDK.")
    
    tab1, tab2, tab3 = st.tabs(["📄 MCP Server Code", "🤖 OpenAI Agent Code", "🚀 Usage Example"])
    
    with tab1:
        st.markdown("**Calculator MCP Server:**")
        st.code("""
# calculator_server.py
import asyncio
import math
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult, ListToolsResult

server = Server("calculator-server")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    return ListToolsResult(
        tools=[
            Tool(
                name="calculate",
                description="Perform mathematical calculations",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string", 
                            "description": "Mathematical expression to evaluate"
                        }
                    },
                    "required": ["expression"]
                }
            ),
            Tool(
                name="advanced_math",
                description="Advanced mathematical functions",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "function": {
                            "type": "string",
                            "enum": ["sin", "cos", "tan", "log", "sqrt", "factorial"],
                            "description": "Mathematical function to apply"
                        },
                        "value": {"type": "number", "description": "Input value"}
                    },
                    "required": ["function", "value"]
                }
            )
        ]
    )

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "calculate":
        expression = arguments["expression"]
        try:
            # Safe evaluation (be careful in production!)
            result = eval(expression, {"__builtins__": {}, "math": math})
            return CallToolResult(
                content=[TextContent(type="text", text=f"Result: {result}")]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )
    
    elif name == "advanced_math":
        func_name = arguments["function"]
        value = arguments["value"]
        
        try:
            if func_name == "sin":
                result = math.sin(value)
            elif func_name == "cos":
                result = math.cos(value)
            elif func_name == "tan":
                result = math.tan(value)
            elif func_name == "log":
                result = math.log(value)
            elif func_name == "sqrt":
                result = math.sqrt(value)
            elif func_name == "factorial":
                result = math.factorial(int(value))
            
            return CallToolResult(
                content=[TextContent(type="text", text=f"{func_name}({value}) = {result}")]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True
            )

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
        """, language="python")
    
    with tab2:
        st.markdown("**OpenAI Agent with Calculator MCP:**")
        st.code("""
# math_agent.py
import asyncio
from openai_agents import Agent
from openai_agents.mcp import MCPServerStdio

async def main():
    # Create MCP server connection
    calculator_server = MCPServerStdio(
        params={
            "command": "python",
            "args": ["calculator_server.py"],
        }
    )
    
    # Create math agent with MCP server
    agent = Agent(
        name="Math Assistant",
        instructions="You are a helpful math assistant. Use the calculator tools to help users with mathematical calculations and advanced math functions.",
        model="gpt-4o-mini",
        mcp_servers=[calculator_server]
    )
    
    # Run the agent
    async with calculator_server:
        # Basic calculation
        result = await agent.run("Calculate 15 * 7 + 23")
        print(result.content)
        
        # Advanced math
        result = await agent.run("What's the sine of π/4 radians?")
        print(result.content)
        
        # Complex calculation
        result = await agent.run("Calculate the factorial of 8 and then find its square root")
        print(result.content)

if __name__ == "__main__":
    asyncio.run(main())
        """, language="python")
        
        st.info("💡 **MCP Benefits for Math Operations:**")
        st.markdown("""
        • **Safe Execution**: Math operations run in isolated MCP server
        • **Extensible**: Easy to add new mathematical functions
        • **Reliable**: Proper error handling for invalid operations
        • **Reusable**: Same MCP server can be used by multiple agents
        """)
    
    with tab3:
        st.markdown("**Usage Example:**")
        st.code("""
# Run the calculator MCP server
python calculator_server.py

# In another terminal, run the math agent
python math_agent.py

# Example outputs:
# Calculate 15 * 7 + 23
# Result: 128

# What's the sine of π/4 radians?
# sin(0.7853981633974483) = 0.7071067811865476

# Calculate the factorial of 8 and then find its square root
# factorial(8) = 40320
# sqrt(40320) = 200.79840636817816
        """, language="bash")
        
        st.markdown("**🎯 Key Features:**")
        st.markdown("""
        • **Basic Arithmetic**: Addition, subtraction, multiplication, division
        • **Advanced Functions**: Trigonometric, logarithmic, square root, factorial
        • **Safe Evaluation**: Controlled execution environment
        • **Error Handling**: Graceful handling of invalid expressions
        • **Extensible**: Easy to add more mathematical functions
        """)

def show_weather_server_example():
    st.markdown("### 🌤️ Weather Server MCP")
    st.markdown("An MCP server that provides weather information (mock data for demo).")
    
    with st.expander("📄 View Weather MCP Server Code"):
        st.code("""
# weather_server.py
import asyncio
import random
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult, ListToolsResult

server = Server("weather-server")

# Mock weather data
WEATHER_DATA = {
    "new york": {"temp": 22, "condition": "Sunny", "humidity": 65},
    "london": {"temp": 15, "condition": "Cloudy", "humidity": 80},
    "tokyo": {"temp": 28, "condition": "Rainy", "humidity": 90},
    "paris": {"temp": 18, "condition": "Partly Cloudy", "humidity": 70}
}

@server.list_tools()
async def list_tools() -> ListToolsResult:
    return ListToolsResult(
        tools=[
            Tool(
                name="get_weather",
                description="Get current weather for a city",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name to get weather for"
                        }
                    },
                    "required": ["city"]
                }
            ),
            Tool(
                name="get_forecast",
                description="Get 5-day weather forecast",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name"},
                        "days": {"type": "integer", "description": "Number of days (1-5)", "default": 5}
                    },
                    "required": ["city"]
                }
            )
        ]
    )

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "get_weather":
        city = arguments["city"].lower()
        
        if city in WEATHER_DATA:
            weather = WEATHER_DATA[city]
            result = f"Weather in {city.title()}:\\n"
            result += f"Temperature: {weather['temp']}°C\\n"
            result += f"Condition: {weather['condition']}\\n"
            result += f"Humidity: {weather['humidity']}%"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Weather data not available for {city}")],
                isError=True
            )
    
    elif name == "get_forecast":
        city = arguments["city"].lower()
        days = arguments.get("days", 5)
        
        if city in WEATHER_DATA:
            base_weather = WEATHER_DATA[city]
            forecast = f"5-day forecast for {city.title()}:\\n"
            
            for i in range(min(days, 5)):
                temp_variation = random.randint(-5, 5)
                temp = base_weather['temp'] + temp_variation
                conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
                condition = random.choice(conditions)
                
                forecast += f"Day {i+1}: {temp}°C, {condition}\\n"
            
            return CallToolResult(
                content=[TextContent(type="text", text=forecast)]
            )
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Forecast not available for {city}")],
                isError=True
            )

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
        """, language="python")

def show_analytics_server_example():
    st.markdown("### 📊 Data Analytics Server MCP")
    st.markdown("An MCP server that provides data analysis capabilities.")
    
    with st.expander("📄 View Analytics MCP Server Code"):
        st.code("""
# analytics_server.py
import asyncio
import json
import statistics
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, CallToolResult, ListToolsResult

server = Server("analytics-server")

@server.list_tools()
async def list_tools() -> ListToolsResult:
    return ListToolsResult(
        tools=[
            Tool(
                name="analyze_data",
                description="Analyze a list of numbers",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "List of numbers to analyze"
                        }
                    },
                    "required": ["data"]
                }
            ),
            Tool(
                name="correlation",
                description="Calculate correlation between two datasets",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "x": {"type": "array", "items": {"type": "number"}},
                        "y": {"type": "array", "items": {"type": "number"}}
                    },
                    "required": ["x", "y"]
                }
            )
        ]
    )

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> CallToolResult:
    if name == "analyze_data":
        data = arguments["data"]
        
        if not data:
            return CallToolResult(
                content=[TextContent(type="text", text="No data provided")],
                isError=True
            )
        
        try:
            analysis = {
                "count": len(data),
                "mean": statistics.mean(data),
                "median": statistics.median(data),
                "std_dev": statistics.stdev(data) if len(data) > 1 else 0,
                "min": min(data),
                "max": max(data)
            }
            
            result = "Data Analysis Results:\\n"
            result += f"Count: {analysis['count']}\\n"
            result += f"Mean: {analysis['mean']:.2f}\\n"
            result += f"Median: {analysis['median']:.2f}\\n"
            result += f"Std Dev: {analysis['std_dev']:.2f}\\n"
            result += f"Min: {analysis['min']}\\n"
            result += f"Max: {analysis['max']}"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Analysis error: {str(e)}")],
                isError=True
            )
    
    elif name == "correlation":
        x = arguments["x"]
        y = arguments["y"]
        
        if len(x) != len(y):
            return CallToolResult(
                content=[TextContent(type="text", text="Datasets must have same length")],
                isError=True
            )
        
        if len(x) < 2:
            return CallToolResult(
                content=[TextContent(type="text", text="Need at least 2 data points")],
                isError=True
            )
        
        try:
            correlation = statistics.correlation(x, y)
            
            result = f"Correlation Analysis:\\n"
            result += f"Correlation coefficient: {correlation:.4f}\\n"
            
            if abs(correlation) > 0.8:
                strength = "Strong"
            elif abs(correlation) > 0.5:
                strength = "Moderate"
            else:
                strength = "Weak"
            
            direction = "positive" if correlation > 0 else "negative"
            result += f"Relationship: {strength} {direction} correlation"
            
            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Correlation error: {str(e)}")],
                isError=True
            )

if __name__ == "__main__":
    asyncio.run(stdio_server(server))
        """, language="python")
    
    # Summary section
    st.markdown("---")
    st.markdown("## 🎯 Key Takeaways")
    
    st.success("""
    **What makes MCP powerful:**
    
    • **Standardized Interface**: All servers follow the same protocol
    • **Easy Integration**: Works seamlessly with OpenAI Agents SDK
    • **Modular Design**: Each server handles specific functionality
    • **Extensible**: Easy to add new tools and capabilities
    • **Language Agnostic**: Can be implemented in any language
    """)
    
    st.info("""
    **Next Steps:**
    
    1. **Try an Example**: Copy one of the examples above and run it locally
    2. **Explore MCP vs API**: Check out the comparison page to understand the benefits
    3. **Build Your Own**: Create MCP servers for your specific use cases
    4. **Join the Community**: Contribute to the growing MCP ecosystem
    """)

def show_interactive_mcp_test():
    """Interactive MCP testing interface with LLM"""
    st.markdown("### 🎮 Interactive MCP Tool Testing with AI")
    st.markdown("*Chat with an AI agent that has access to MCP tools - see real MCP integration in action!*")
    
    # Initialize session state for chat
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'demo_files' not in st.session_state:
        st.session_state.demo_files = {
            'hello.txt': 'Hello, World!',
            'notes.txt': 'My meeting notes\n- Discuss MCP integration\n- Review code examples',
            'data.csv': 'name,age,city\nAlice,25,New York\nBob,30,London\nCharlie,35,Tokyo'
        }
    
    # Available MCP tools
    available_tools = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read content from a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Name of the file to read"}
                    },
                    "required": ["filename"]
                }
            }
        },
        {
            "type": "function", 
            "function": {
                "name": "write_file",
                "description": "Write content to a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Name of the file"},
                        "content": {"type": "string", "description": "Content to write"}
                    },
                    "required": ["filename", "content"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate",
                "description": "Perform mathematical calculations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "Mathematical expression to evaluate"}
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather information for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "City name"}
                    },
                    "required": ["city"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "analyze_data",
                "description": "Analyze numerical data and provide statistics",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "array", "items": {"type": "number"}, "description": "List of numbers to analyze"}
                    },
                    "required": ["data"]
                }
            }
        }
    ]
    
    # Chat interface
    st.markdown("#### 💬 Chat with MCP-Enabled AI Agent")
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "tool_calls" in message:
                with st.expander("🔧 Tool Calls Made"):
                    for tool_call in message["tool_calls"]:
                        st.code(f"Tool: {tool_call['name']}\nArguments: {tool_call['arguments']}", language="json")
            if "tool_responses" in message:
                with st.expander("📋 Tool Responses"):
                    for response in message["tool_responses"]:
                        st.code(response, language="json")
    
    # Suggested prompts
    st.markdown("**💡 Try these example prompts:**")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📁 What files are available?", key="files_btn"):
            handle_user_input("What files are available to read?", available_tools)
        if st.button("🧮 Calculate 15% tip on $45.50", key="calc_btn"):
            handle_user_input("Calculate 15% tip on $45.50", available_tools)
    
    with col2:
        if st.button("🌤️ Weather in Tokyo", key="weather_btn"):
            handle_user_input("What's the weather like in Tokyo?", available_tools)
        if st.button("📊 Analyze: 10,20,30,40,50", key="analyze_btn"):
            handle_user_input("Analyze this data: 10, 20, 30, 40, 50", available_tools)
    
    # Chat input
    if prompt := st.chat_input("Ask the AI agent to use MCP tools..."):
        handle_user_input(prompt, available_tools)
    
    st.info("""
    **💡 What you're seeing:**
    
    • **Real LLM Integration**: The AI agent uses OpenAI's function calling to access MCP tools
    • **Tool Discovery**: The agent knows what tools are available and when to use them
    • **Standardized Protocol**: All tools follow the same MCP response format
    • **Conversational Interface**: Natural language requests get converted to tool calls
    • **Transparent Process**: See exactly which tools are called and their responses
    """)

def handle_user_input(user_input, available_tools):
    """Handle user input and LLM response with MCP tools"""
    import json
    from openai import OpenAI
    
    # Add user message
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get API key
    api_key = st.session_state.get('openai_api_key')
    if not api_key:
        st.error("OpenAI API key not found!")
        return
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Prepare messages for OpenAI
        messages = [
            {
                "role": "system", 
                "content": """You are an AI assistant with access to MCP (Model Context Protocol) tools. 
                You can read/write files, perform calculations, get weather info, and analyze data.
                When users ask questions, use the appropriate tools to help them.
                Be conversational and explain what tools you're using and why."""
            }
        ]
        
        # Add recent chat history (last 10 messages)
        for msg in st.session_state.chat_messages[-10:]:
            if msg["role"] in ["user", "assistant"]:
                messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=available_tools,
            tool_choice="auto",
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message
        
        # Handle tool calls
        tool_calls_made = []
        tool_responses = []
        
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                tool_calls_made.append({
                    "name": tool_name,
                    "arguments": tool_args
                })
                
                # Execute the tool
                tool_result = execute_mcp_tool(tool_name, tool_args)
                tool_responses.append(tool_result)
        
        # Display assistant response
        with st.chat_message("assistant"):
            if assistant_message.content:
                st.markdown(assistant_message.content)
            
            if tool_calls_made:
                with st.expander("🔧 MCP Tools Used"):
                    for i, tool_call in enumerate(tool_calls_made):
                        st.markdown(f"**{tool_call['name']}**")
                        st.code(json.dumps(tool_call['arguments'], indent=2), language="json")
                        if i < len(tool_responses):
                            st.markdown("**Response:**")
                            st.code(tool_responses[i], language="json")
            
            # If there were tool calls, get final response
            if tool_calls_made:
                # Add tool results to conversation and get final response
                final_messages = messages + [
                    {"role": "assistant", "content": assistant_message.content or "I'll use these tools to help you."},
                    {"role": "user", "content": f"Tool results: {'; '.join(tool_responses)}. Please provide a summary."}
                ]
                
                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=final_messages,
                    temperature=0.7
                )
                
                final_content = final_response.choices[0].message.content
                st.markdown("**Summary:** " + final_content)
                
                # Save message with tool info
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": (assistant_message.content or "") + "\n\n**Summary:** " + final_content,
                    "tool_calls": tool_calls_made,
                    "tool_responses": tool_responses
                })
            else:
                # Save regular message
                st.session_state.chat_messages.append({
                    "role": "assistant", 
                    "content": assistant_message.content
                })
        
        # Rerun to update chat display
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def execute_mcp_tool(tool_name, arguments):
    """Execute MCP tool and return response"""
    try:
        if tool_name == "read_file":
            filename = arguments["filename"]
            if filename in st.session_state.demo_files:
                content = st.session_state.demo_files[filename]
                return f"File content of {filename}: {content}"
            else:
                available = ", ".join(st.session_state.demo_files.keys())
                return f"File {filename} not found. Available files: {available}"
        
        elif tool_name == "write_file":
            filename = arguments["filename"]
            content = arguments["content"]
            st.session_state.demo_files[filename] = content
            return f"Successfully wrote to {filename}"
        
        elif tool_name == "calculate":
            expression = arguments["expression"]
            import math
            result = eval(expression, {"__builtins__": {}, "math": math})
            return f"Calculation result: {expression} = {result}"
        
        elif tool_name == "get_weather":
            city = arguments["city"].lower()
            weather_data = {
                "new york": {"temp": 22, "condition": "Sunny", "humidity": 65},
                "london": {"temp": 15, "condition": "Cloudy", "humidity": 80},
                "tokyo": {"temp": 28, "condition": "Rainy", "humidity": 90},
                "paris": {"temp": 18, "condition": "Partly Cloudy", "humidity": 70},
                "san francisco": {"temp": 20, "condition": "Foggy", "humidity": 75}
            }
            
            if city in weather_data:
                weather = weather_data[city]
                return f"Weather in {city.title()}: {weather['temp']}°C, {weather['condition']}, {weather['humidity']}% humidity"
            else:
                return f"Weather data not available for {city}"
        
        elif tool_name == "analyze_data":
            data = arguments["data"]
            import statistics
            
            if len(data) == 0:
                return "No data provided"
            
            analysis = {
                "count": len(data),
                "mean": statistics.mean(data),
                "median": statistics.median(data),
                "std_dev": statistics.stdev(data) if len(data) > 1 else 0,
                "min": min(data),
                "max": max(data)
            }
            
            return f"Data analysis: Count={analysis['count']}, Mean={analysis['mean']:.2f}, Median={analysis['median']:.2f}, StdDev={analysis['std_dev']:.2f}, Min={analysis['min']}, Max={analysis['max']}"
        
        else:
            return f"Unknown tool: {tool_name}"
            
    except Exception as e:
        return f"Tool error: {str(e)}"

 
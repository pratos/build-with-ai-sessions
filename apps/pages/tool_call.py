import streamlit as st
import openai
import json
import requests
from datetime import datetime
import random
from pydantic import BaseModel
from typing import List, Optional

st.markdown("# 🔧 LLM + Tool Call")
st.markdown("---")

st.markdown("""
### 🎯 Tool Calls = AI Superpowers
AI can now use external tools:
- Get weather data 🌤️
- Perform calculations 🧮
- Search the web 🔍
- Send emails 📧
- And much more!
""")

# Check for API key from session state
api_key = st.session_state.get("openai_api_key")

class ToolCallSummary(BaseModel):
    tools_used: List[str]
    summary: str
    key_findings: List[str]

if api_key:
    client = openai.Client(api_key=api_key)
    
    # Define some example tools
    def get_weather(city: str) -> str:
        """Get current weather for a city (mock function)"""
        weather_options = ["sunny ☀️", "cloudy ☁️", "rainy 🌧️", "snowy ❄️"]
        temp = random.randint(15, 30)
        weather = random.choice(weather_options)
        return f"The weather in {city} is {weather} with a temperature of {temp}°C"
    
    def calculate(expression: str) -> str:
        """Safely calculate mathematical expressions"""
        try:
            # Allow common mathematical characters including ^ for exponentiation
            allowed_chars = set('0123456789+-*/.()^')
            if not all(c in allowed_chars or c.isspace() for c in expression):
                return "Error: Invalid characters in expression"
            
            # Store original expression for display
            original_expression = expression
            
            # Replace ^ with ** for Python exponentiation
            python_expression = expression.replace('^', '**')
            result = eval(python_expression)
            
            # Format result nicely - avoid LaTeX conflicts
            return f"The result of {original_expression} is {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"
    
    def get_current_time() -> str:
        """Get the current date and time"""
        return f"Current date and time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Tool definitions for OpenAI
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather information for a specific city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "The city name to get weather for"
                        }
                    },
                    "required": ["city"]
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
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to calculate (e.g., '2+2', '10*5')"
                        }
                    },
                    "required": ["expression"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current date and time",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    ]
    
    # Available functions mapping
    available_functions = {
        "get_weather": get_weather,
        "calculate": calculate,
        "get_current_time": get_current_time
    }
    
    st.markdown("### 🛠️ Available Tools")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🌤️ **Weather**\nGet weather for any city")
    with col2:
        st.info("🧮 **Calculator**\nPerform math calculations")
    with col3:
        st.info("⏰ **Time**\nGet current date/time")
    
    st.markdown("### 💬 Try Tool-Enhanced AI")
    
    user_prompt = st.text_area(
        "Ask something that requires tools:", 
        value="What's the weather like in Tokyo and what's 25 * 4?",
        height=100
    )
    
    if st.button("🚀 Ask AI with Tools", type="primary"):
        try:
            with st.spinner("🤔 AI is thinking and using tools..."):
                # First API call
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": user_prompt}],
                    tools=tools,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                
                # Show what the AI decided to do
                st.markdown("### 🧠 AI's Thinking Process:")
                if tool_calls:
                    st.success(f"🔧 AI decided to use {len(tool_calls)} tool(s)!")
                    
                    messages = [
                        {"role": "user", "content": user_prompt},
                        response_message.model_dump()
                    ]
                    
                    # Execute each tool call
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        
                        st.markdown(f"**🔧 Using tool: {function_name}**")
                        st.code(f"Arguments: {function_args}", language="json")
                        
                        # Call the function
                        function_response = available_functions[function_name](**function_args)
                        
                        st.markdown(f"**📊 Tool Result:**")
                        st.info(function_response)
                        
                        # Add tool response to messages
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })
                    
                    # Get final response from AI
                    final_response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages
                    )
                    
                    st.markdown("### 🎉 Final AI Response:")
                    st.markdown(f"**{final_response.choices[0].message.content}**")
                    
                else:
                    st.info("AI didn't need to use any tools for this request.")
                    st.markdown("### 🎉 AI Response:")
                    st.markdown(f"**{response_message.content}**")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Structured Output Example
    st.markdown("---")
    st.markdown("### 🏗️ Structured Tool Call Summary")
    st.markdown("Get organized results from multiple tool calls.")
    
    summary_prompt = st.text_area(
        "Ask for a comprehensive analysis:", 
        value="Get weather for Tokyo and London, calculate 15% tip on $120, and tell me the current time. Then summarize everything.",
        height=80
    )
    
    if st.button("📊 Get Structured Summary", type="secondary"):
        try:
            with st.spinner("🔄 Processing with structured output..."):
                # First, make tool calls as usual
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": summary_prompt}],
                    tools=tools,
                    tool_choice="auto"
                )
                
                response_message = response.choices[0].message
                tool_calls = response_message.tool_calls
                
                if tool_calls:
                    messages = [
                        {"role": "user", "content": summary_prompt},
                        response_message.model_dump()
                    ]
                    
                    # Execute tool calls
                    tool_results = []
                    for tool_call in tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        function_response = available_functions[function_name](**function_args)
                        tool_results.append(f"{function_name}: {function_response}")
                        
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })
                    
                    # Now get structured summary
                    structured_response = client.beta.chat.completions.parse(
                        model="gpt-4o-mini",
                        messages=messages + [
                            {"role": "user", "content": "Please provide a structured summary of all the tool results and analysis."}
                        ],
                        response_format=ToolCallSummary
                    )
                    
                    summary_data = structured_response.choices[0].message.parsed
                    
                    st.markdown("### 📊 Structured Summary:")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**🔧 Tools Used:**")
                        for tool in summary_data.tools_used:
                            st.info(f"• {tool}")
                        
                        st.markdown("**🔍 Key Findings:**")
                        for finding in summary_data.key_findings:
                            st.success(f"• {finding}")
                    
                    with col2:
                        st.markdown("**📝 Summary:**")
                        st.text_area("", value=summary_data.summary, height=200, disabled=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Code example
    st.markdown("---")
    st.markdown("### 👨‍💻 Want to see the code?")
    
    with st.expander("Click to show/hide the tool calling code"):
        st.code("""
import openai
import json

# Define your tools
def get_weather(city: str) -> str:
    # Your weather logic here
    return f"Weather in {city}: Sunny, 25°C"

# Tool definition for OpenAI
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    }
]

# Make the request with tools
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

# Check if AI wants to use tools
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # Execute the function
        if function_name == "get_weather":
            result = get_weather(**function_args)
            print(f"Tool result: {result}")
        """, language="python")
    
    # Example scenarios
    st.markdown("---")
    st.markdown("### 🎮 Try These Examples!")
    
    example_prompts = [
        "What's the weather in London and Paris?",
        "Calculate 15% tip on a $85 bill",
        "What time is it now and what's 24 * 7?",
        "I need weather for New York and calculate 100 / 4",
        "What's the current time and weather in Tokyo?"
    ]
    
    st.markdown("Click any example to try it:")
    cols = st.columns(2)
    for i, prompt in enumerate(example_prompts):
        with cols[i % 2]:
            if st.button(f"📝 {prompt}", key=f"example_{i}"):
                st.session_state.example_prompt = prompt
                st.rerun()
    
    # Use example prompt if selected
    if hasattr(st.session_state, 'example_prompt'):
        st.text_area("Selected example:", value=st.session_state.example_prompt, key="example_display")

else:
    st.info("👆 Please enter your OpenAI API key in the sidebar to try the examples!")

# Summary section
st.markdown("---")
st.markdown("### 🧠 Summary")
st.markdown("""
- **Tool Definition**: Describe available tools to AI
- **Auto Decision**: AI picks which tools to use
- **Execution**: Run tools and return results
- **Integration**: AI uses results in final response

**Result**: AI can interact with the real world! 🌟
""")

st.markdown("---")
st.markdown("### 🎯 Key Takeaways")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **✅ Superpowers Unlocked:**
    - Real-time data access
    - Perform calculations
    - Execute actions
    - Connect to APIs
    """)
with col2:
    st.markdown("""
    **🔄 The Process:**
    1. AI analyzes your request
    2. Decides which tools to use
    3. Executes tools with parameters
    4. Uses results to respond
    """)

st.markdown("**Next**: AI that thinks in loops like a real agent! 🔄") 
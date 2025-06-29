import streamlit as st

st.markdown("# ⚖️ ReAct vs Multi-Agent Architecture")
st.markdown("---")

st.markdown("""
### 🎯 Choose the Right Agent Architecture
Compare two approaches to building AI agents:

🔹 **ReAct (Single Agent)** - One AI reasons through problems step-by-step  
🔹 **Multi-Agent (Team)** - Multiple specialized AIs working together  
🔹 **Code Comparison** - Side-by-side implementations  
🔹 **Exa Integration** - How each approach handles real-time web search  

**Features:** Actual code examples, use case guidance, trade-off analysis.
""")


# Code Comparison
st.markdown("## 💻 Code Comparison")

tab1, tab2, tab3 = st.tabs(["🔄 ReAct Implementation", "🤝 Multi-Agent Implementation", "🌐 Exa Tool Comparison"])

with tab1:
    st.markdown("### ReAct Agent Code (OpenAI SDK)")
    st.code("""
# ReAct Agent - Single agent with tools
import openai
import json

def react_agent(client, user_request, tools, available_functions, max_iterations=5):
    messages = [
        {"role": "system", "content": "You are a ReAct agent. Think, act, observe, repeat."},
        {"role": "user", "content": user_request}
    ]
    
    for iteration in range(max_iterations):
        # Get AI response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message.model_dump())
        
        # Handle tool calls
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute tool
                result = available_functions[function_name](**function_args)
                
                # Add result to conversation
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result,
                })
        else:
            # No more tools needed, return final answer
            return response_message.content
    
    return "Max iterations reached"

# Usage
result = react_agent(client, "Research AI trends and analyze market", tools, functions)
print(result)
    """, language="python")
    
    st.markdown("""
    **🔄 ReAct Characteristics:**
    - **Sequential**: One step at a time
    - **Manual Tool Management**: You handle tool execution
    - **Simple**: Single agent handles everything
    - **Flexible**: Can adapt to any task
    - **Direct Control**: Full control over the conversation flow
    """)

with tab2:
    st.markdown("### Multi-Agent System Code (OpenAI Agents SDK)")
    st.code("""
# Multi-Agent System - Specialized team
from agents import Agent, Runner, function_tool

# Define tools using decorators
@function_tool
def search_tool(query: str) -> str:
    # Tool implementation
    return f"Search results for: {query}"

# Create specialized agents
research_agent = Agent(
    name="Research Specialist",
    instructions="You are a research expert. Find comprehensive information.",
    tools=[search_tool]
)

analysis_agent = Agent(
    name="Data Analyst", 
    instructions="You analyze data and provide insights.",
    tools=[]
)

writing_agent = Agent(
    name="Content Writer",
    instructions="You create polished, engaging content.",
    tools=[]
)

# Coordinator with handoffs
coordinator = Agent(
    name="Project Coordinator",
    instructions="Coordinate between specialists based on the task.",
    handoffs=[research_agent, analysis_agent, writing_agent]
)

# Usage
result = Runner.run_sync(
    coordinator, 
    "Research AI trends and analyze market"
)
print(result.final_output)
    """, language="python")
    
    st.markdown("""
    **🤝 Multi-Agent Characteristics:**
    - **Parallel**: Multiple agents can work simultaneously
    - **Automatic Tool Management**: SDK handles tool execution
    - **Specialized**: Each agent excels in their domain
    - **Scalable**: Easy to add new agents
    - **Declarative**: Define agents and let SDK manage workflow
    """)

with tab3:
    st.markdown("### 🌐 Exa Tool Implementation Comparison")
    
    st.markdown("#### 🔄 Exa in ReAct Agent (OpenAI SDK)")
    st.code("""
# Manual Exa tool implementation for ReAct
import exa_py
import os

def exa_web_search(query: str) -> str:
    \"\"\"Real-time web search using Exa AI\"\"\"
    try:
        exa = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])
        
        results = exa.search(
            query=query,
            num_results=3,
            use_autoprompt=True
        )
        
        # Get content for the results
        try:
            contents = exa.get_contents([result.id for result in results.results])
            content_map = {content.id: content.text for content in contents.contents if content.text}
        except:
            content_map = {}
        
        search_summary = f"Exa web search results for '{query}':\\n\\n"
        for i, result in enumerate(results.results, 1):
            search_summary += f"{i}. **{result.title}**\\n"
            search_summary += f"   URL: {result.url}\\n"
            if result.id in content_map and content_map[result.id]:
                search_summary += f"   Summary: {content_map[result.id][:200]}...\\n"
            search_summary += "\\n"
        
        return search_summary
        
    except Exception as e:
        return f"Exa search error: {str(e)}"

# Tool definition for OpenAI SDK
tools = [
    {
        "type": "function",
        "function": {
            "name": "exa_web_search",
            "description": "Search the web for real-time information using Exa AI",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    }
]

available_functions = {
    "exa_web_search": exa_web_search
}

# Use in ReAct agent
result = react_agent(client, "Search for latest AI news", tools, available_functions)
    """, language="python")
    
    st.markdown("#### 🤝 Exa in Multi-Agent (OpenAI Agents SDK)")
    st.code("""
# Declarative Exa tool implementation for Multi-Agent
from agents import Agent, Runner, function_tool
import exa_py
import os

@function_tool
def exa_web_search(query: str) -> str:
    \"\"\"Real-time web search using Exa AI\"\"\"
    try:
        exa = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])
        
        results = exa.search(
            query=query,
            num_results=3,
            use_autoprompt=True
        )
        
        # Get content for the results
        try:
            contents = exa.get_contents([result.id for result in results.results])
            content_map = {content.id: content.text for content in contents.contents if content.text}
        except:
            content_map = {}
        
        search_summary = f"Exa web search results for '{query}':\\n\\n"
        for i, result in enumerate(results.results, 1):
            search_summary += f"{i}. **{result.title}**\\n"
            search_summary += f"   URL: {result.url}\\n"
            if result.id in content_map and content_map[result.id]:
                search_summary += f"   Summary: {content_map[result.id][:200]}...\\n"
            search_summary += "\\n"
        
        return search_summary
        
    except Exception as e:
        return f"Exa search error: {str(e)}"

# Create Exa-powered agent
exa_agent = Agent(
    name="Exa Web Research Specialist",
    instructions=\"\"\"You are a web research specialist powered by Exa AI.
    Your job is to find real-time information from the web and provide insights.\"\"\",
    tools=[exa_web_search]
)

# Use in multi-agent system
coordinator = Agent(
    name="Research Coordinator",
    instructions="Coordinate web research tasks.",
    handoffs=[exa_agent]
)

result = Runner.run_sync(coordinator, "Search for latest AI news")
    """, language="python")
    
    st.markdown("### 🔍 Key Differences in Exa Implementation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔄 OpenAI SDK (ReAct)")
        st.info("""
        **Manual Tool Management:**
        - Define tool schema manually
        - Handle tool execution yourself
        - Manage conversation flow
        - Parse tool call arguments
        - Add results back to messages
        
        **Pros:**
        - Full control over execution
        - Custom error handling
        - Flexible tool chaining
        
        **Cons:**
        - More boilerplate code
        - Manual conversation management
        - Complex error handling
        """)
    
    with col2:
        st.markdown("#### 🤝 OpenAI Agents SDK (Multi-Agent)")
        st.info("""
        **Declarative Tool Management:**
        - Use @function_tool decorator
        - Automatic tool execution
        - SDK manages conversation
        - Type hints for parameters
        - Automatic result handling
        
        **Pros:**
        - Less boilerplate code
        - Automatic conversation flow
        - Built-in error handling
        
        **Cons:**
        - Less fine-grained control
        - SDK-specific patterns
        - Learning curve for SDK
        """)

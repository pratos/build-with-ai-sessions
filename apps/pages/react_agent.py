import streamlit as st
import openai
import json
import random
from datetime import datetime
import time

# Cost tracking (approximate costs in USD)
OPENAI_COSTS = {
    "gpt-4o-mini": {
        "input": 0.00015 / 1000,  # per token
        "output": 0.0006 / 1000   # per token
    }
}

def estimate_tokens(text):
    """Rough token estimation (1 token ≈ 4 characters)"""
    return len(text) // 4

def calculate_cost(model, input_text, output_text):
    """Calculate approximate cost for OpenAI API call"""
    if model not in OPENAI_COSTS:
        return "Not available"
    
    input_tokens = estimate_tokens(input_text)
    output_tokens = estimate_tokens(output_text)
    
    input_cost = input_tokens * OPENAI_COSTS[model]["input"]
    output_cost = output_tokens * OPENAI_COSTS[model]["output"]
    total_cost = input_cost + output_cost
    
    return f"${total_cost:.6f} (≈{input_tokens + output_tokens} tokens)"

st.markdown("# 🔄 ReAct Agent (LLM + Tools + Loop)")
st.markdown("---")

st.markdown("""
### 🎯 ReAct Agent = Reasoning + Acting
AI that thinks in loops:
1. 🤔 **Think**: What should I do?
2. 🔧 **Act**: Use a tool
3. 👀 **Observe**: Check results
4. 🔄 **Repeat** until done

**🌐 Enhanced with Exa**: While this demo uses mock tools, real ReAct agents can use Exa AI for:
- Real-time web search and research
- Company and market analysis
- Academic paper discovery
- Social media trend analysis

💡 **Try Exa yourself**: [Exa Playground](https://dashboard.exa.ai/playground/search)
""")

# Check for API keys from session state
api_key = st.session_state.get("openai_api_key")
exa_api_key = st.session_state.get("exa_api_key")

# Check if exa_py is available
try:
    import exa_py
    EXA_AVAILABLE = True
except ImportError:
    EXA_AVAILABLE = False

if api_key:
    client = openai.Client(api_key=api_key)
    
    # Tool selection toggle
    st.markdown("### 🔧 Tool Configuration")
    use_exa = st.toggle(
        "Use Exa AI Tools (Real-time web search)", 
        value=False,
        help="Toggle between mock tools and real Exa AI tools for web search",
        disabled=not (EXA_AVAILABLE and exa_api_key)
    )
    
    if use_exa and EXA_AVAILABLE and exa_api_key:
        st.success("✅ **Exa Tools Enabled**: Real-time web search, company research, and more!")
        tool_mode = "exa"
    else:
        if use_exa and not EXA_AVAILABLE:
            st.warning("📦 **Install Exa**: Run `pip install exa-py` to enable Exa tools")
        elif use_exa and not exa_api_key:
            st.warning("🔑 **EXA API Key Required**: Add your EXA API key in the sidebar")
        st.info("🔧 **Mock Tools Active**: Using demonstration tools with sample data")
        tool_mode = "mock"
    
    # Enhanced tools for ReAct agent
    def search_web(query: str) -> str:
        """Mock web search function"""
        search_results = {
            "python": "Python is a high-level programming language created by Guido van Rossum in 1991. It's known for its simplicity and readability.",
            "weather": f"Current weather data shows mixed conditions across different cities. Temperature ranges from 15-30°C globally.",
            "stock": "Stock markets are showing varied performance today. Tech stocks are generally up while energy stocks are mixed.",
            "news": "Latest news includes developments in AI technology, climate initiatives, and global economic updates.",
            "tokyo": "Tokyo is the capital of Japan, population ~14 million. Known for technology, culture, and cuisine.",
            "cooking": "Cooking tips: Start with fresh ingredients, season properly, and don't overcook vegetables."
        }
        
        # Find the most relevant result
        for key, result in search_results.items():
            if key.lower() in query.lower():
                return f"Search results for '{query}': {result}"
        
        return f"Search results for '{query}': Found general information about this topic."
    
    def get_weather(city: str) -> str:
        """Get weather for a city"""
        weather_options = ["sunny ☀️", "cloudy ☁️", "rainy 🌧️", "snowy ❄️", "partly cloudy ⛅"]
        temp = random.randint(10, 35)
        weather = random.choice(weather_options)
        humidity = random.randint(30, 80)
        return f"Weather in {city}: {weather}, {temp}°C, humidity {humidity}%"
    
    def calculate(expression: str) -> str:
        """Perform calculations"""
        try:
            # Allow common mathematical characters including ^ for exponentiation
            allowed_chars = set('0123456789+-*/.()^')
            if not all(c in allowed_chars or c.isspace() for c in expression):
                return "Error: Invalid characters in expression"
            
            # Replace ^ with ** for Python exponentiation
            expression = expression.replace('^', '**')
            result = eval(expression)
            return f"Calculation result: {expression.replace('**', '^')} = {result}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def save_note(content: str) -> str:
        """Save a note (mock function)"""
        return f"✅ Note saved: '{content[:50]}...' at {datetime.now().strftime('%H:%M:%S')}"
    
    # Real Exa AI tools
    def exa_web_search(query: str) -> str:
        """Real-time web search using Exa AI"""
        if not (EXA_AVAILABLE and exa_api_key):
            return "Exa search not available. Please enable Exa tools and ensure API key is set."
        
        try:
            import os
            os.environ["EXA_API_KEY"] = exa_api_key
            exa = exa_py.Exa(api_key=exa_api_key)
            
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
            
            search_summary = f"🌐 Exa web search results for '{query}':\n\n"
            for i, result in enumerate(results.results, 1):
                search_summary += f"{i}. **{result.title}**\n"
                search_summary += f"   URL: {result.url}\n"
                if result.id in content_map and content_map[result.id]:
                    search_summary += f"   Summary: {content_map[result.id][:200]}...\n"
                search_summary += "\n"
            
            return search_summary
            
        except Exception as e:
            return f"Exa search error: {str(e)}. Using fallback search instead."
    
    def exa_company_research(company_name: str) -> str:
        """Research companies using Exa AI"""
        if not (EXA_AVAILABLE and exa_api_key):
            return f"Exa company research not available for {company_name}."
        
        try:
            import os
            os.environ["EXA_API_KEY"] = exa_api_key
            exa = exa_py.Exa(api_key=exa_api_key)
            
            results = exa.search(
                query=f"{company_name} company business model revenue news",
                num_results=3,
                use_autoprompt=True
            )
            
            # Get content for the results
            try:
                contents = exa.get_contents([result.id for result in results.results])
                content_map = {content.id: content.text for content in contents.contents if content.text}
            except:
                content_map = {}
            
            research_summary = f"🏢 Exa company research for '{company_name}':\n\n"
            for i, result in enumerate(results.results, 1):
                research_summary += f"{i}. **{result.title}**\n"
                research_summary += f"   Source: {result.url}\n"
                if result.id in content_map and content_map[result.id]:
                    research_summary += f"   Info: {content_map[result.id][:300]}...\n"
                research_summary += "\n"
            
            return research_summary
            
        except Exception as e:
            return f"Exa company research error: {str(e)}."
    
    def exa_arxiv_search(topic: str) -> str:
        """Search for latest papers on arXiv using Exa AI"""
        if not (EXA_AVAILABLE and exa_api_key):
            return f"Exa arXiv search not available for {topic}."
        
        try:
            import os
            os.environ["EXA_API_KEY"] = exa_api_key
            exa = exa_py.Exa(api_key=exa_api_key)
            
            results = exa.search(
                query=f"{topic} site:arxiv.org",
                num_results=3,
                use_autoprompt=True,
                include_domains=["arxiv.org"]
            )
            
            # Get content for the results
            try:
                contents = exa.get_contents([result.id for result in results.results])
                content_map = {content.id: content.text for content in contents.contents if content.text}
            except:
                content_map = {}
            
            papers_summary = f"📚 Latest arXiv papers on '{topic}':\n\n"
            for i, result in enumerate(results.results, 1):
                papers_summary += f"{i}. **{result.title}**\n"
                papers_summary += f"   arXiv URL: {result.url}\n"
                if result.id in content_map and content_map[result.id]:
                    papers_summary += f"   Abstract: {content_map[result.id][:250]}...\n"
                papers_summary += "\n"
            
            return papers_summary
            
        except Exception as e:
            return f"Exa arXiv search error: {str(e)}."
    
    # Tool definitions based on mode
    if tool_mode == "exa":
        # Exa AI tools
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
            },
            {
                "type": "function",
                "function": {
                    "name": "exa_company_research",
                    "description": "Research companies and their business models using Exa AI",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "company_name": {"type": "string", "description": "Company name to research"}
                        },
                        "required": ["company_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "exa_arxiv_search",
                    "description": "Search for latest academic papers on arXiv using Exa AI",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string", "description": "Research topic to search for"}
                        },
                        "required": ["topic"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a city",
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
                    "name": "calculate",
                    "description": "Perform mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {"type": "string", "description": "Math expression"}
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_note",
                    "description": "Save important information as a note",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "description": "Note content to save"}
                        },
                        "required": ["content"]
                    }
                }
            }
        ]
        
        available_functions = {
            "exa_web_search": exa_web_search,
            "exa_company_research": exa_company_research,
            "exa_arxiv_search": exa_arxiv_search,
            "get_weather": get_weather,
            "calculate": calculate,
            "save_note": save_note
        }
    else:
        # Mock tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_web",
                    "description": "Search the web for information on any topic (mock data)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Search query"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a city",
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
                    "name": "calculate",
                    "description": "Perform mathematical calculations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {"type": "string", "description": "Math expression"}
                        },
                        "required": ["expression"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "save_note",
                    "description": "Save important information as a note",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {"type": "string", "description": "Note content to save"}
                        },
                        "required": ["content"]
                    }
                }
            }
        ]
        
        available_functions = {
            "search_web": search_web,
            "get_weather": get_weather,
            "calculate": calculate,
            "save_note": save_note
        }
    
    st.markdown("### 🛠️ Available Tools")
    
    if tool_mode == "exa":
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🌐 **Exa Web Search**\nReal-time web search")
            st.info("🏢 **Company Research**\nBusiness intelligence")
        with col2:
            st.info("📚 **arXiv Search**\nLatest research papers")
            st.info("🌤️ **Weather**\nCurrent conditions")
        with col3:
            st.info("🧮 **Calculator**\nMath calculations")
            st.info("📝 **Notes**\nSave information")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info("🔍 **Web Search**\nMock search data")
        with col2:
            st.info("🌤️ **Weather**\nRandom weather data")
        with col3:
            st.info("🧮 **Calculator**\nReal math calculations")
        with col4:
            st.info("📝 **Notes**\nSave important info")
    
    st.markdown("### 🤖 Try the ReAct Agent")
    
    # Different default prompts based on tool mode
    if tool_mode == "exa":
        default_prompt = "Research the latest developments in artificial intelligence, find recent news about OpenAI, search for academic papers on large language models, and calculate the potential market size if AI grows 25% annually from a $100B base."
    else:
        default_prompt = "I'm planning a trip to Tokyo next week. Help me research the city, check the weather, and calculate the budget if I spend $100 per day for 5 days."
    
    user_prompt = st.text_area(
        "Give the agent a complex task:", 
        value=default_prompt,
        height=120
    )
    
    max_iterations = st.slider("Maximum thinking iterations:", 1, 10, 5)
    
    if st.button("🚀 Start ReAct Agent", type="primary"):
        try:
            st.markdown("### 🧠 Agent's Thinking Process")
            
            # Initialize conversation
            messages = [
                {
                    "role": "system", 
                    "content": """You are a helpful ReAct agent. You can think step by step, use tools, and reason about what to do next.

For each step:
1. Think about what you need to do
2. Use appropriate tools if needed
3. Analyze the results
4. Decide on next steps
5. Continue until you have fully addressed the user's request

Be thorough and use multiple tools when helpful."""
                },
                {"role": "user", "content": user_prompt}
            ]
            
            iteration = 0
            execution_steps = []
            
            with st.container():
                while iteration < max_iterations:
                    iteration += 1
                    step_data = {
                        "iteration": iteration,
                        "thinking": None,
                        "tool_calls": [],
                        "final_response": None,
                        "error": None,
                        "api_cost": None,
                        "model_used": "gpt-4o-mini"
                    }
                    
                    try:
                        with st.spinner(f"Agent is thinking (iteration {iteration})..."):
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=messages,
                                tools=tools,
                                tool_choice="auto",
                                temperature=0.1
                            )
                        
                        response_message = response.choices[0].message
                        messages.append(response_message.model_dump())
                        
                        # Calculate API cost
                        input_text = " ".join([str(msg.get("content", "")) for msg in messages[:-1] if msg.get("content")])
                        output_text = str(response_message.content or "")
                        step_data["api_cost"] = calculate_cost("gpt-4o-mini", input_text, output_text)
                        
                        # Store agent's reasoning
                        if response_message.content:
                            step_data["thinking"] = response_message.content
                        
                        # Handle tool calls
                        if response_message.tool_calls:
                            for tool_call in response_message.tool_calls:
                                function_name = tool_call.function.name
                                function_args = json.loads(tool_call.function.arguments)
                                
                                tool_data = {
                                    "name": function_name,
                                    "args": function_args,
                                    "result": None,
                                    "raw_output": None,
                                    "error": None,
                                    "cost": "Not available"  # Tool execution cost
                                }
                                
                                try:
                                    # Execute tool
                                    function_response = available_functions[function_name](**function_args)
                                    tool_data["result"] = function_response
                                    tool_data["raw_output"] = str(function_response)  # Store raw output
                                    
                                    # Add tool response to conversation
                                    messages.append({
                                        "tool_call_id": tool_call.id,
                                        "role": "tool",
                                        "name": function_name,
                                        "content": function_response,
                                    })
                                    
                                except Exception as tool_error:
                                    tool_data["error"] = str(tool_error)
                                    # Add error response to conversation
                                    messages.append({
                                        "tool_call_id": tool_call.id,
                                        "role": "tool",
                                        "name": function_name,
                                        "content": f"Error: {str(tool_error)}",
                                    })
                                
                                step_data["tool_calls"].append(tool_data)
                        
                        else:
                            # No more tool calls, agent is done
                            step_data["final_response"] = response_message.content
                            execution_steps.append(step_data)
                            break
                        
                        execution_steps.append(step_data)
                        
                    except Exception as e:
                        step_data["error"] = str(e)
                        execution_steps.append(step_data)
                        st.error(f"❌ Error in iteration {iteration}: {str(e)}")
                        break
                    
                    # Small delay for better UX
                    time.sleep(0.5)
                
                if iteration >= max_iterations and not any(step.get("final_response") for step in execution_steps):
                    st.warning(f"⏰ Agent reached maximum iterations ({max_iterations}). Task may not be fully complete.")
                
                # Display execution steps in collapsible format
                st.markdown("### 📋 Execution Steps")
                
                for step in execution_steps:
                    iteration_num = step["iteration"]
                    
                    # Determine step status
                    if step.get("error"):
                        status_icon = "❌"
                        status_color = "red"
                    elif step.get("final_response"):
                        status_icon = "✅"
                        status_color = "green"
                    elif step.get("tool_calls"):
                        status_icon = "🔧"
                        status_color = "blue"
                    else:
                        status_icon = "🤔"
                        status_color = "orange"
                    
                    # Create expandable section for each step
                    with st.expander(f"{status_icon} Step {iteration_num}: {'ERROR' if step.get('error') else 'COMPLETE' if step.get('final_response') else 'TOOL USAGE' if step.get('tool_calls') else 'THINKING'}", expanded=False):
                        
                        # Show step metadata
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Model:** {step.get('model_used', 'gpt-4o-mini')}")
                        with col2:
                            st.markdown(f"**API Cost:** {step.get('api_cost', 'Not available')}")
                        
                        # Show thinking
                        if step.get("thinking"):
                            st.markdown("**🤔 Agent's Thinking:**")
                            st.info(step["thinking"])
                        
                        # Show tool calls
                        if step.get("tool_calls"):
                            st.markdown("**🔧 Tools Used:**")
                            for i, tool_call in enumerate(step["tool_calls"]):
                                st.markdown(f"**Tool {i+1}: `{tool_call['name']}`** | Cost: {tool_call.get('cost', 'Not available')}")
                                
                                # Show arguments
                                with st.expander(f"📝 Arguments for {tool_call['name']}", expanded=False):
                                    st.code(json.dumps(tool_call["args"], indent=2), language="json")
                                
                                # Show result or error
                                if tool_call.get("error"):
                                    st.error(f"❌ Tool Error: {tool_call['error']}")
                                elif tool_call.get("result"):
                                    st.success(f"✅ Tool Result: {tool_call['result']}")
                                    
                                    # Show raw output in expandable section
                                    if tool_call.get("raw_output"):
                                        with st.expander(f"🔍 Raw Output from {tool_call['name']}", expanded=False):
                                            st.code(tool_call["raw_output"], language="text")
                        
                        # Show final response
                        if step.get("final_response"):
                            st.markdown("**🎉 Final Response:**")
                            st.success(step["final_response"])
                        
                        # Show step error
                        if step.get("error"):
                            st.error(f"❌ Step Error: {step['error']}")
                
                # Show final summary
                if execution_steps:
                    final_step = execution_steps[-1]
                    if final_step.get("final_response"):
                        st.markdown("### 🎯 Task Completed Successfully!")
                        st.balloons()
                    elif final_step.get("error"):
                        st.markdown("### ❌ Task Failed")
                        st.error("The agent encountered an error and could not complete the task.")
                    else:
                        st.markdown("### ⏸️ Task Incomplete")
                        st.warning("The agent reached the maximum number of iterations without completing the task.")
                    
                    # Show cost summary
                    st.markdown("### 💰 Cost Summary")
                    total_steps = len(execution_steps)
                    api_calls = sum(1 for step in execution_steps if step.get("api_cost") and step["api_cost"] != "Not available")
                    tool_calls = sum(len(step.get("tool_calls", [])) for step in execution_steps)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Steps", total_steps)
                    with col2:
                        st.metric("API Calls", api_calls)
                    with col3:
                        st.metric("Tool Calls", tool_calls)
                    
                    # Estimate total cost (rough)
                    total_cost = 0
                    cost_available = False
                    for step in execution_steps:
                        if step.get("api_cost") and "$" in str(step["api_cost"]):
                            try:
                                cost_str = step["api_cost"].split("$")[1].split(" ")[0]
                                total_cost += float(cost_str)
                                cost_available = True
                            except:
                                pass
                    
                    if cost_available:
                        st.info(f"💵 **Estimated Total Cost:** ${total_cost:.6f}")
                    else:
                        st.info("💵 **Total Cost:** Not available")
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Code example
    st.markdown("---")
    st.markdown("### 👨‍💻 Want to see the ReAct code?")
    
    with st.expander("Click to show/hide the ReAct agent code"):
        st.code("""
import openai
import json

def react_agent(client, user_request, tools, available_functions, max_iterations=5):
    messages = [
        {
            "role": "system", 
            "content": "You are a ReAct agent. Think step by step, use tools, and reason about next steps."
        },
        {"role": "user", "content": user_request}
    ]
    
    for iteration in range(max_iterations):
        print(f"\\n--- Iteration {iteration + 1} ---")
        
        # Get AI response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        messages.append(response_message.model_dump())
        
        # Show thinking
        if response_message.content:
            print(f"Agent thinks: {response_message.content}")
        
        # Handle tool calls
        if response_message.tool_calls:
            print("Agent is using tools...")
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"Using {function_name} with {function_args}")
                
                # Execute function
                result = available_functions[function_name](**function_args)
                print(f"Tool result: {result}")
                
                # Add result to messages
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": result,
                })
        else:
            # No more tools needed, agent is done
            print("Agent completed the task!")
            break
    
    return messages

# Usage
result = react_agent(client, "Plan a trip to Tokyo", tools, available_functions)
        """, language="python")
    
    st.markdown("### 🌐 Adding Exa AI to ReAct Agents")
    with st.expander("Click to show/hide Exa integration code"):
        st.code("""
import exa_py
import os

def create_exa_tool():
    \"\"\"Create an Exa-powered web search tool for ReAct agents\"\"\"
    
    def exa_web_search(query: str) -> str:
        \"\"\"Real-time web search using Exa AI\"\"\"
        exa = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])
        
        results = exa.search(
            query=query,
            num_results=3,
            text=True,
            highlights=True
        )
        
        search_summary = f"Web search results for '{query}':\\n\\n"
        for i, result in enumerate(results.results, 1):
            search_summary += f"{i}. **{result.title}**\\n"
            search_summary += f"   URL: {result.url}\\n"
            if result.highlights:
                search_summary += f"   Key info: {result.highlights[0][:200]}...\\n"
            search_summary += "\\n"
        
        return search_summary
    
    return {
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
    }, exa_web_search

def create_exa_company_research_tool():
    \"\"\"Create an Exa-powered company research tool\"\"\"
    
    def exa_company_research(company_name: str) -> str:
        \"\"\"Research companies using Exa AI\"\"\"
        exa = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])
        
        results = exa.search(
            query=f"{company_name} company business model revenue",
            num_results=3,
            text=True,
            category="company"
        )
        
        research_summary = f"Company research for '{company_name}':\\n\\n"
        for i, result in enumerate(results.results, 1):
            research_summary += f"{i}. **{result.title}**\\n"
            research_summary += f"   Source: {result.url}\\n"
            if result.text:
                research_summary += f"   Info: {result.text[:300]}...\\n"
            research_summary += "\\n"
        
        return research_summary
    
    return {
        "type": "function", 
        "function": {
            "name": "exa_company_research",
            "description": "Research companies and their business models using Exa AI",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {"type": "string", "description": "Company name to research"}
                },
                "required": ["company_name"]
            }
        }
    }, exa_company_research

# Usage in ReAct Agent
exa_search_tool, exa_search_func = create_exa_tool()
exa_company_tool, exa_company_func = create_exa_company_research_tool()

tools = [exa_search_tool, exa_company_tool]  # Add other tools as needed
available_functions = {
    "exa_web_search": exa_search_func,
    "exa_company_research": exa_company_func
}

# Run ReAct agent with Exa tools
result = react_agent(
    client, 
    "Research Tesla's latest developments and market position", 
    tools, 
    available_functions
)
        """, language="python")
        
        st.markdown("""
        **🔑 Setup Instructions:**
        1. Install Exa: `pip install exa-py`
        2. Get API key from [exa.ai](https://exa.ai/)
        3. Set environment variable: `export EXA_API_KEY="your-key-here"`
        4. Add Exa tools to your ReAct agent's tool list
        
        **💡 Benefits of Exa in ReAct:**
        - **Real-time data**: Get current information, not training data
        - **Specialized search**: Company research, academic papers, news
        - **High-quality results**: Exa's AI understands context better than keyword search
        - **Structured data**: Get clean, formatted results perfect for AI processing
        """)
    
    # Example scenarios
    st.markdown("---")
    st.markdown("### 🎮 Try These Complex Examples!")
    
    if tool_mode == "exa":
        example_prompts = [
            "Research Tesla's latest developments, find recent academic papers on electric vehicles, check the weather in Austin (Tesla's HQ), and calculate Tesla's potential revenue if they sell 3 million cars at $50k average.",
            "Find the latest AI research papers, search for news about GPT models, research OpenAI as a company, and calculate the cost if I want to process 1 million tokens daily.",
            "Research the latest developments in quantum computing, find academic papers on quantum algorithms, search for quantum computing companies, and save a summary of the key findings.",
            "Search for recent climate change research, find papers on renewable energy, research companies like Tesla and Rivian, and calculate carbon savings if 10% of cars go electric."
        ]
    else:
        example_prompts = [
            "I want to start learning Python programming. Research it, find the current weather in Silicon Valley (where many tech companies are), and calculate how many hours I need to study if I want to learn for 2 hours daily for 30 days.",
            "Help me plan a dinner party for 8 people. Research cooking tips, check the weather for this weekend, calculate the budget if I spend $25 per person, and save the key information as notes.",
            "I'm considering investing in tech stocks. Search for recent tech news, calculate what 10% of my $5000 savings would be, check the weather in New York (financial center), and save a summary.",
            "Plan my morning routine: check today's weather, calculate how long I have if I wake up at 7 AM and need to leave by 9 AM, search for productivity tips, and save the plan."
        ]
    
    st.markdown("**These examples show how the agent thinks through complex, multi-step tasks:**")
    
    for i, prompt in enumerate(example_prompts):
        with st.expander(f"📝 Example {i+1}: {prompt[:50]}..."):
            st.markdown(f"**Full task:** {prompt}")
            if st.button(f"Try this example", key=f"react_example_{i}"):
                st.session_state.react_example_prompt = prompt
                st.rerun()
    
    # Use example prompt if selected
    if hasattr(st.session_state, 'react_example_prompt'):
        st.text_area("Selected example:", value=st.session_state.react_example_prompt, key="react_example_display")

else:
    st.info("👆 Please enter your OpenAI API key in the sidebar to try the ReAct agent!")

# Summary section
st.markdown("---")
st.markdown("### 🧠 Why ReAct?")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **🔄 The ReAct Loop:**
    1. **Reason**: Think about the task
    2. **Act**: Use tools to gather info
    3. **Observe**: Analyze the results
    4. **Repeat**: Continue until done
    """)

with col2:
    st.markdown("""
    **🆚 vs Simple Tool Calling:**
    - Simple: One question → One tool → Done
    - ReAct: Complex task → Multiple steps → Complete solution
    """)

st.markdown("---")
st.markdown("### 🎯 Key Benefits")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    **🧠 Smarter**
    - Breaks down complex tasks
    - Adapts based on results
    - Multi-step reasoning
    """)
with col2:
    st.markdown("""
    **🔧 More Capable**
    - Uses multiple tools
    - Chains actions together
    - Handles uncertainty
    """)
with col3:
    st.markdown("""
    **👀 Transparent**
    - Shows thinking process
    - Explains each step
    - Easy to debug
    """)

st.markdown("**Next**: Multiple AI agents working together! 🤝") 
import streamlit as st
import asyncio
import random
from datetime import datetime
import os
import concurrent.futures

# Check if exa_py is available
try:
    import exa_py
    EXA_AVAILABLE = True
except ImportError:
    EXA_AVAILABLE = False

# Check if openai-agents is available
try:
    from agents import Agent, Runner, function_tool
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False

st.markdown("# 🤝 Multi-Agent Workflow")
st.markdown("---")

st.markdown("""
### 🎯 Multi-Agent = Specialized AI Team
Multiple expert AIs working together:

- 🔍 **Research Agent**: General information
- 🌐 **Exa Agent**: Real-time web search & analysis
- 🧠 **Parallel Research Coordinator**: Manages academic research across platforms
- 📚 **arXiv Specialist**: Latest academic papers
- 🐦 **Twitter Specialist**: Social discussions & expert opinions  
- 💻 **Papers with Code Specialist**: Implementations & benchmarks
- 🤔 **Strategic Thinking Analyst**: Deep analysis & synthesis
- 📊 **Analysis Agent**: Data insights
- ✍️ **Writing Agent**: Content creation
- 🎨 **Creative Agent**: Creative enhancement

They work in parallel and hand off tasks for comprehensive results.

💡 **Try Exa yourself**: [Exa Playground](https://dashboard.exa.ai/playground/search)
""")

if not AGENTS_AVAILABLE:
    st.error("""
    ❌ **OpenAI Agents SDK not available**
    
    To use this demo, you need to install the OpenAI Agents SDK:
    ```bash
    pip install openai-agents
    ```
    
    This is a powerful framework for building multi-agent workflows!
    """)
    st.stop()

# Check for API key from session state
api_key = st.session_state.get("openai_api_key")

if api_key:
    # Set the API key for the agents SDK
    os.environ["OPENAI_API_KEY"] = api_key
    
    # Define tools that agents can use
    @function_tool
    def search_information(query: str) -> str:
        """Search for information on any topic"""
        search_results = {
            "climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns. Human activities, particularly burning fossil fuels, are the main driver.",
            "artificial intelligence": "AI is the simulation of human intelligence in machines. It includes machine learning, deep learning, and natural language processing.",
            "renewable energy": "Renewable energy comes from sources that naturally replenish, like solar, wind, hydro, and geothermal power.",
            "space exploration": "Space exploration involves the discovery and exploration of celestial structures in outer space by means of space technology.",
            "quantum computing": "Quantum computing uses quantum mechanics to process information in ways that classical computers cannot.",
            "biotechnology": "Biotechnology uses living systems and organisms to develop products and technologies for various applications."
        }
        
        for key, result in search_results.items():
            if key.lower() in query.lower():
                return f"Research findings on '{query}': {result}"
        
        return f"General information found about '{query}': This is an interesting topic with various applications and implications."
    
    @function_tool
    def exa_web_search(query: str) -> str:
        """Perform real-time web search using Exa AI"""
        if not EXA_AVAILABLE:
            return "Exa search not available. Install exa-py package and add EXA_API_KEY to use real web search."
        
        exa_api_key = os.environ.get("EXA_API_KEY")
        if not exa_api_key:
            return "EXA_API_KEY not found in environment variables. Add your Exa API key to enable real web search."
        
        try:
            exa = exa_py.Exa(api_key=exa_api_key)
            results = exa.search(
                query=query,
                num_results=3,
                text=True,
                highlights=True
            )
            
            search_summary = f"Exa web search results for '{query}':\n\n"
            for i, result in enumerate(results.results, 1):
                search_summary += f"{i}. **{result.title}**\n"
                search_summary += f"   URL: {result.url}\n"
                if hasattr(result, 'highlights') and result.highlights:
                    search_summary += f"   Key info: {result.highlights[0][:200]}...\n"
                elif hasattr(result, 'text') and result.text:
                    search_summary += f"   Summary: {result.text[:200]}...\n"
                search_summary += "\n"
            
            return search_summary
            
        except Exception as e:
            return f"Exa search error: {str(e)}. Using fallback search instead."
    
    @function_tool
    def exa_company_research(company_name: str) -> str:
        """Research companies using Exa AI"""
        if not EXA_AVAILABLE:
            return f"Exa research not available. Mock data: {company_name} is a company with various business operations."
        
        exa_api_key = os.environ.get("EXA_API_KEY")
        if not exa_api_key:
            return f"EXA_API_KEY not found. Mock data: {company_name} appears to be an established company in its sector."
        
        try:
            exa = exa_py.Exa(api_key=exa_api_key)
            results = exa.search(
                query=f"{company_name} company business model revenue",
                num_results=3,
                text=True,
                category="company"
            )
            
            research_summary = f"Exa company research for '{company_name}':\n\n"
            for i, result in enumerate(results.results, 1):
                research_summary += f"{i}. **{result.title}**\n"
                research_summary += f"   Source: {result.url}\n"
                if hasattr(result, 'text') and result.text:
                    research_summary += f"   Info: {result.text[:300]}...\n"
                research_summary += "\n"
            
            return research_summary
            
        except Exception as e:
            return f"Exa company research error: {str(e)}. Using fallback data."
    
    @function_tool
    def exa_arxiv_search(topic: str) -> str:
        """Search for latest papers on arXiv using Exa AI"""
        if not EXA_AVAILABLE:
            return f"Exa arXiv search not available. Mock data: Found several papers related to {topic} on arXiv."
        
        exa_api_key = os.environ.get("EXA_API_KEY")
        if not exa_api_key:
            return f"EXA_API_KEY not found. Mock data: Recent arXiv papers on {topic} show active research."
        
        try:
            exa = exa_py.Exa(api_key=exa_api_key)
            results = exa.search(
                query=f"{topic} site:arxiv.org",
                num_results=5,
                text=True,
                include_domains=["arxiv.org"]
            )
            
            papers_summary = f"Latest arXiv papers on '{topic}':\n\n"
            for i, result in enumerate(results.results, 1):
                papers_summary += f"{i}. **{result.title}**\n"
                papers_summary += f"   arXiv URL: {result.url}\n"
                if hasattr(result, 'text') and result.text:
                    papers_summary += f"   Abstract: {result.text[:250]}...\n"
                papers_summary += "\n"
            
            return papers_summary
            
        except Exception as e:
            return f"Exa arXiv search error: {str(e)}. Using fallback data."
    
    @function_tool
    def exa_twitter_search(topic: str) -> str:
        """Search for latest tweets and discussions on Twitter using Exa AI"""
        if not EXA_AVAILABLE:
            return f"Exa Twitter search not available. Mock data: Found recent discussions about {topic} on Twitter."
        
        exa_api_key = os.environ.get("EXA_API_KEY")
        if not exa_api_key:
            return f"EXA_API_KEY not found. Mock data: Twitter shows active discussions about {topic}."
        
        try:
            exa = exa_py.Exa(api_key=exa_api_key)
            results = exa.search(
                query=f"{topic} site:twitter.com OR site:x.com",
                num_results=5,
                text=True,
                include_domains=["twitter.com", "x.com"]
            )
            
            twitter_summary = f"Latest Twitter discussions on '{topic}':\n\n"
            for i, result in enumerate(results.results, 1):
                twitter_summary += f"{i}. **{result.title}**\n"
                twitter_summary += f"   Tweet URL: {result.url}\n"
                if hasattr(result, 'text') and result.text:
                    twitter_summary += f"   Content: {result.text[:200]}...\n"
                twitter_summary += "\n"
            
            return twitter_summary
            
        except Exception as e:
            return f"Exa Twitter search error: {str(e)}. Using fallback data."
    
    @function_tool
    def exa_paperswithcode_search(topic: str) -> str:
        """Search for latest papers and code implementations on Papers with Code using Exa AI"""
        if not EXA_AVAILABLE:
            return f"Exa Papers with Code search not available. Mock data: Found implementations for {topic}."
        
        exa_api_key = os.environ.get("EXA_API_KEY")
        if not exa_api_key:
            return f"EXA_API_KEY not found. Mock data: Papers with Code shows recent work on {topic}."
        
        try:
            exa = exa_py.Exa(api_key=exa_api_key)
            results = exa.search(
                query=f"{topic} site:paperswithcode.com",
                num_results=5,
                text=True,
                include_domains=["paperswithcode.com"]
            )
            
            pwc_summary = f"Latest Papers with Code on '{topic}':\n\n"
            for i, result in enumerate(results.results, 1):
                pwc_summary += f"{i}. **{result.title}**\n"
                pwc_summary += f"   PwC URL: {result.url}\n"
                if hasattr(result, 'text') and result.text:
                    pwc_summary += f"   Details: {result.text[:250]}...\n"
                pwc_summary += "\n"
            
            return pwc_summary
            
        except Exception as e:
            return f"Exa Papers with Code search error: {str(e)}. Using fallback data."
    
    @function_tool
    def analyze_data(data: str) -> str:
        """Analyze data and provide insights"""
        analysis_types = [
            "shows strong positive trends with 15% growth potential",
            "indicates moderate risk with stable long-term outlook", 
            "demonstrates high innovation potential in emerging markets",
            "reveals significant opportunities for improvement and optimization",
            "suggests diversification strategies would be beneficial"
        ]
        
        analysis = random.choice(analysis_types)
        return f"Analysis of the provided data: {analysis}. Recommendation: Consider strategic implementation with careful monitoring."
    
    @function_tool
    def get_market_data(topic: str) -> str:
        """Get market data and trends"""
        market_data = {
            "tech": "Tech sector showing 12% growth, driven by AI and cloud computing innovations",
            "energy": "Renewable energy market expanding rapidly with 25% year-over-year growth",
            "finance": "Financial markets showing stability with emerging fintech opportunities",
            "healthcare": "Healthcare technology advancing with personalized medicine trends",
            "education": "EdTech sector growing with increased demand for online learning solutions"
        }
        
        for key, data in market_data.items():
            if key.lower() in topic.lower():
                return f"Market data for {topic}: {data}"
        
        return f"Market data for {topic}: Steady growth with emerging opportunities in digital transformation."
    
    # Create specialized agents
    research_agent = Agent(
        name="Research Specialist",
        instructions="""You are a research specialist. Your job is to:
        1. Find comprehensive information on any topic
        2. Gather relevant data and facts
        3. Provide detailed research findings
        4. Hand off to Analysis Agent when research is complete
        
        Always be thorough and factual in your research.""",
        tools=[search_information, get_market_data]
    )
    
    exa_agent = Agent(
        name="Exa Web Analyst",
        instructions="""You are an Exa-powered web research and analysis specialist. Your job is to:
        1. Perform real-time web searches using Exa AI
        2. Research companies and market trends
        3. Analyze current web information and news
        4. Provide up-to-date insights from the web
        5. Hand off to other agents when web research is complete
        
        Always use real-time web data when available and provide current, accurate information.""",
        tools=[exa_web_search, exa_company_research]
    )
    
    # Specialized research agents for parallel processing
    arxiv_agent = Agent(
        name="arXiv Research Specialist",
        instructions="""You are an arXiv research specialist. Your job is to:
        1. Search for the latest academic papers on arXiv
        2. Find cutting-edge research and preprints
        3. Summarize paper abstracts and key findings
        4. Identify trending research topics and methodologies
        
        Focus on recent, high-quality academic work and emerging research trends.""",
        tools=[exa_arxiv_search]
    )
    
    twitter_agent = Agent(
        name="Twitter Research Specialist", 
        instructions="""You are a Twitter research specialist. Your job is to:
        1. Search for latest discussions and trends on Twitter/X
        2. Find expert opinions and community discussions
        3. Identify viral content and emerging conversations
        4. Track real-time sentiment and public opinion
        
        Focus on current discussions, expert takes, and community insights.""",
        tools=[exa_twitter_search]
    )
    
    paperswithcode_agent = Agent(
        name="Papers with Code Specialist",
        instructions="""You are a Papers with Code research specialist. Your job is to:
        1. Search for latest papers with code implementations
        2. Find state-of-the-art models and benchmarks
        3. Identify reproducible research and open-source implementations
        4. Track performance improvements and new datasets
        
        Focus on practical, implementable research with code availability.""",
        tools=[exa_paperswithcode_search]
    )
    
    analysis_agent = Agent(
        name="Data Analyst", 
        instructions="""You are a data analysis expert. Your job is to:
        1. Analyze research data and findings
        2. Identify trends, patterns, and insights
        3. Provide data-driven recommendations
        4. Hand off to Writing Agent for final report
        
        Always provide clear, actionable insights.""",
        tools=[analyze_data]
    )
    
    writing_agent = Agent(
        name="Content Writer",
        instructions="""You are a professional content writer. Your job is to:
        1. Take research and analysis from other agents
        2. Create well-structured, engaging content
        3. Ensure clarity and readability
        4. Provide final polished output
        
        Always write in a clear, professional, and engaging style.""",
        tools=[]
    )
    
    creative_agent = Agent(
        name="Creative Director",
        instructions="""You are a creative director. Your job is to:
        1. Add creative flair to content
        2. Suggest innovative approaches
        3. Enhance presentation and engagement
        4. Provide creative recommendations
        
        Always think outside the box and add creative value.""",
        tools=[]
    )
    
    # Thinking model agent for synthesis and analysis
    thinking_agent = Agent(
        name="Strategic Thinking Analyst",
        instructions="""You are a strategic thinking analyst with deep analytical capabilities. Your job is to:
        1. Synthesize information from multiple research sources
        2. Identify patterns, connections, and insights across different data sources
        3. Perform critical analysis and reasoning about research findings
        4. Generate strategic recommendations based on comprehensive analysis
        5. Think step-by-step through complex problems and provide reasoning
        
        Always provide thoughtful analysis, connect dots between different sources, and offer strategic insights.
        Use a thinking approach: first analyze what you know, then reason through implications, then provide conclusions.""",
        tools=[]
    )
    
    # Parallel research coordinator for comprehensive research
    parallel_research_coordinator = Agent(
        name="Parallel Research Coordinator",
        instructions="""You are a parallel research coordinator managing specialized research agents. Your job is to:
        1. Coordinate simultaneous research across arXiv, Twitter, and Papers with Code
        2. Gather comprehensive information from multiple academic and social sources
        3. Hand off synthesized results to the Strategic Thinking Analyst for deep analysis
        4. Ensure all research perspectives are captured before analysis
        
        For research topics, always use all three specialists in parallel:
        - arXiv Research Specialist: For latest academic papers and preprints
        - Twitter Research Specialist: For community discussions and expert opinions
        - Papers with Code Specialist: For implementations and practical applications
        
        After gathering all research, hand off to Strategic Thinking Analyst for synthesis.""",
        handoffs=[arxiv_agent, twitter_agent, paperswithcode_agent, thinking_agent, writing_agent]
    )
    
    # Main coordinator agent that can hand off to specialists
    coordinator_agent = Agent(
        name="Project Coordinator",
        instructions="""You are a project coordinator managing a team of specialists:
        - Research Specialist: For finding general information and data
        - Exa Web Analyst: For real-time web search and current information
        - Parallel Research Coordinator: For comprehensive academic and social research
        - Data Analyst: For analyzing findings and providing insights  
        - Content Writer: For creating polished written content
        - Creative Director: For adding creative elements
        - Strategic Thinking Analyst: For deep analysis and synthesis
        
        Based on the user's request, decide which agent should handle the task first.
        For academic research topics, prefer the Parallel Research Coordinator.
        For current events, market trends, or company research, prefer the Exa Web Analyst.
        Coordinate handoffs between agents to deliver comprehensive results.""",
        handoffs=[research_agent, exa_agent, parallel_research_coordinator, analysis_agent, writing_agent, creative_agent, thinking_agent]
    )
    
    st.markdown("### 👥 Meet Your Agent Team")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🔍 **Research Specialist**\nGeneral information")
        st.info("🌐 **Exa Web Analyst**\nReal-time web search")
        st.info("🧠 **Parallel Coordinator**\nManages parallel research")
    
    with col2:
        st.info("📚 **arXiv Specialist**\nLatest academic papers")
        st.info("🐦 **Twitter Specialist**\nSocial discussions")
        st.info("💻 **Papers with Code**\nImplementations & benchmarks")
    
    with col3:
        st.info("🤔 **Strategic Thinking**\nDeep analysis & synthesis")
        st.info("📊 **Data Analyst**\nInsights from data")
        st.info("✍️ **Content Writer**\nPolished content")
    
    st.success("🤝 **Project Coordinator** - Manages the full team and coordinates handoffs")
    
    # Exa setup info and explanation
    st.markdown("### 🌐 Exa AI Integration")
    
    exa_api_key = st.session_state.get("exa_api_key")
    
    if EXA_AVAILABLE and exa_api_key:
        os.environ["EXA_API_KEY"] = exa_api_key
        st.success("✅ **Exa AI Enabled**: Real-time web search and research capabilities active!")
        st.info("🔍 **Exa Tools Available**: Web search, company research, arXiv papers, Twitter discussions, Papers with Code")
    elif not EXA_AVAILABLE:
        st.warning("📦 **Install Exa**: Run `pip install exa-py` to enable real-time web search")
        st.info("🔧 **Fallback Mode**: Using mock data for demonstration")
    elif not exa_api_key:
        st.warning("🔑 **Add EXA API Key**: Enter your Exa API key in the sidebar for real-time search")
        st.info("🔧 **Fallback Mode**: Using mock data for demonstration")
    
    with st.expander("🤔 What is Exa AI?"):
        st.markdown("""
        **Exa AI** is a next-generation search engine designed for AI applications:
        
        🧠 **AI-Native Search**: Unlike Google's keyword matching, Exa understands meaning and context
        
        🎯 **Specialized Searches**: 
        - Company research with business insights
        - Academic papers from arXiv
        - Social media discussions from Twitter/X
        - Code implementations from Papers with Code
        
        📊 **Structured Results**: Returns clean, formatted data perfect for AI processing
        
        ⚡ **Real-Time**: Get current information, not just training data
        
        💡 **Try it yourself**: [Exa Playground](https://dashboard.exa.ai/playground/search)
        """)
    
    st.markdown("### 🚀 Try Multi-Agent Collaboration")
    
    user_request = st.text_area(
        "What would you like the agent team to work on?",
        value="Research the latest developments in large language models across arXiv papers, Twitter discussions, and Papers with Code implementations. Provide a comprehensive analysis with strategic insights.",
        height=120
    )
    
    if st.button("🎯 Start Agent Team", type="primary"):
        execution_log = []
        start_time = datetime.now()
        
        try:
            # Initialize execution tracking
            execution_log.append({
                "timestamp": start_time,
                "step": "initialization",
                "agent": "System",
                "action": "Starting multi-agent workflow",
                "status": "in_progress",
                "details": f"Request: {user_request[:100]}{'...' if len(user_request) > 100 else ''}",
                "error": None
            })
            
            with st.spinner("🤝 Agent team is collaborating..."):
                # Handle asyncio event loop for Streamlit
                def run_agent_workflow():
                    """Run the agent workflow in a separate thread with its own event loop"""
                    workflow_log = []
                    
                    try:
                        # Create a new event loop for this thread
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        
                        workflow_log.append({
                            "timestamp": datetime.now(),
                            "step": "setup",
                            "agent": "System",
                            "action": "Created new event loop",
                            "status": "success",
                            "details": "Event loop initialized for multi-agent execution",
                            "error": None
                        })
                        
                        # Run the agent workflow
                        workflow_log.append({
                            "timestamp": datetime.now(),
                            "step": "execution",
                            "agent": "Project Coordinator",
                            "action": "Starting agent collaboration",
                            "status": "in_progress",
                            "details": "Coordinator analyzing request and delegating to appropriate agents",
                            "error": None
                        })
                        
                        result = Runner.run_sync(coordinator_agent, user_request)
                        
                        workflow_log.append({
                            "timestamp": datetime.now(),
                            "step": "completion",
                            "agent": "System",
                            "action": "Workflow completed successfully",
                            "status": "success",
                            "details": f"Final output length: {len(result.final_output)} characters",
                            "error": None
                        })
                        
                        return result, workflow_log
                        
                    except Exception as e:
                        workflow_log.append({
                            "timestamp": datetime.now(),
                            "step": "error",
                            "agent": "System",
                            "action": "Workflow failed",
                            "status": "error",
                            "details": f"Error type: {type(e).__name__}",
                            "error": str(e)
                        })
                        raise e
                    finally:
                        loop.close()
                
                # Run in a separate thread to avoid event loop conflicts
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_agent_workflow)
                    result, workflow_log = future.result(timeout=60)  # 60 second timeout
                    execution_log.extend(workflow_log)
                
                # Final success log
                execution_log.append({
                    "timestamp": datetime.now(),
                    "step": "final",
                    "agent": "System",
                    "action": "Multi-agent workflow completed",
                    "status": "success",
                    "details": f"Total execution time: {datetime.now() - start_time}",
                    "error": None
                })
                
                # Display results
                st.markdown("### 🎉 Team Results")
                st.success(result.final_output)
                
                # Display detailed execution log
                st.markdown("### 📋 Execution Log")
                
                for i, log_entry in enumerate(execution_log):
                    # Determine status icon and color
                    if log_entry["status"] == "success":
                        status_icon = "✅"
                    elif log_entry["status"] == "error":
                        status_icon = "❌"
                    elif log_entry["status"] == "in_progress":
                        status_icon = "🔄"
                    else:
                        status_icon = "ℹ️"
                    
                    # Create expandable section for each log entry
                    timestamp_str = log_entry["timestamp"].strftime("%H:%M:%S.%f")[:-3]
                    with st.expander(f"{status_icon} [{timestamp_str}] {log_entry['agent']}: {log_entry['action']}", expanded=False):
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Agent:** {log_entry['agent']}")
                            st.markdown(f"**Step:** {log_entry['step']}")
                            st.markdown(f"**Status:** {log_entry['status']}")
                        
                        with col2:
                            st.markdown(f"**Action:** {log_entry['action']}")
                            st.markdown(f"**Timestamp:** {timestamp_str}")
                        
                        if log_entry.get("details"):
                            st.markdown("**Details:**")
                            st.info(log_entry["details"])
                        
                        if log_entry.get("error"):
                            st.markdown("**Error:**")
                            st.error(log_entry["error"])
                
                # Show the agent workflow messages if available
                st.markdown("### 👥 Agent Collaboration Flow")
                
                if hasattr(result, 'messages') and result.messages:
                    agent_steps = []
                    for i, message in enumerate(result.messages):
                        if hasattr(message, 'role') and message.role == 'assistant':
                            agent_name = getattr(message, 'name', 'Unknown Agent')
                            content = getattr(message, 'content', '')
                            
                            if content:
                                agent_steps.append({
                                    "step_number": len(agent_steps) + 1,
                                    "agent_name": agent_name,
                                    "content": content,
                                    "message_index": i
                                })
                    
                    if agent_steps:
                        for step in agent_steps:
                            with st.expander(f"🤖 Step {step['step_number']}: {step['agent_name']}", expanded=False):
                                st.markdown("**Agent Output:**")
                                st.markdown(step['content'])
                                
                                # Add some metadata
                                st.markdown("---")
                                st.caption(f"Message index: {step['message_index']} | Agent: {step['agent_name']}")
                    else:
                        st.info("No detailed agent messages available, but workflow completed successfully!")
                else:
                    st.info("Agent workflow completed successfully!")
                
                # Show execution summary
                st.markdown("### 📊 Execution Summary")
                total_time = datetime.now() - start_time
                success_count = sum(1 for log in execution_log if log["status"] == "success")
                error_count = sum(1 for log in execution_log if log["status"] == "error")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Time", f"{total_time.total_seconds():.2f}s")
                with col2:
                    st.metric("Total Steps", len(execution_log))
                with col3:
                    st.metric("Successful Steps", success_count)
                with col4:
                    st.metric("Errors", error_count)
                
                if error_count == 0:
                    st.balloons()
                    
        except concurrent.futures.TimeoutError:
            execution_log.append({
                "timestamp": datetime.now(),
                "step": "timeout",
                "agent": "System",
                "action": "Workflow timed out",
                "status": "error",
                "details": "Execution exceeded 60 second timeout",
                "error": "TimeoutError: Agent workflow timed out"
            })
            
            st.error("⏰ Agent workflow timed out. Please try again with a simpler request.")
            
            # Still show execution log for debugging
            if execution_log:
                st.markdown("### 📋 Execution Log (Before Timeout)")
                for i, log_entry in enumerate(execution_log):
                    status_icon = "❌" if log_entry["status"] == "error" else "✅" if log_entry["status"] == "success" else "🔄"
                    timestamp_str = log_entry["timestamp"].strftime("%H:%M:%S.%f")[:-3]
                    
                    with st.expander(f"{status_icon} [{timestamp_str}] {log_entry['agent']}: {log_entry['action']}", expanded=False):
                        st.markdown(f"**Status:** {log_entry['status']}")
                        if log_entry.get("details"):
                            st.info(log_entry["details"])
                        if log_entry.get("error"):
                            st.error(log_entry["error"])
            
        except Exception as e:
            execution_log.append({
                "timestamp": datetime.now(),
                "step": "fatal_error",
                "agent": "System",
                "action": "Fatal error occurred",
                "status": "error",
                "details": f"Error type: {type(e).__name__}",
                "error": str(e)
            })
            
            st.error(f"❌ Error: {str(e)}")
            
            # Show detailed error information
            with st.expander("🔍 Error Details", expanded=True):
                st.code(f"""
Error Type: {type(e).__name__}
Error Message: {str(e)}
Execution Time: {datetime.now() - start_time}
                """)
            
            # Show execution log for debugging
            if execution_log:
                st.markdown("### 📋 Execution Log (Before Error)")
                for i, log_entry in enumerate(execution_log):
                    status_icon = "❌" if log_entry["status"] == "error" else "✅" if log_entry["status"] == "success" else "🔄"
                    timestamp_str = log_entry["timestamp"].strftime("%H:%M:%S.%f")[:-3]
                    
                    with st.expander(f"{status_icon} [{timestamp_str}] {log_entry['agent']}: {log_entry['action']}", expanded=False):
                        st.markdown(f"**Status:** {log_entry['status']}")
                        if log_entry.get("details"):
                            st.info(log_entry["details"])
                        if log_entry.get("error"):
                            st.error(log_entry["error"])
            
            # Provide helpful error guidance
            if "event loop" in str(e).lower():
                st.info("💡 This appears to be an asyncio event loop issue. Try refreshing the page and running again.")
            elif "api" in str(e).lower() or "key" in str(e).lower():
                st.info("💡 This might be an API key issue. Check that your OpenAI API key is valid and has sufficient credits.")
            elif "timeout" in str(e).lower():
                st.info("💡 The request may be too complex. Try a simpler request or increase the timeout.")
            else:
                st.info("💡 Try refreshing the page and running again. If the issue persists, check your API keys and internet connection.")
    
    # Code example
    st.markdown("---")
    st.markdown("### 👨‍💻 Want to see the multi-agent code?")
    
    with st.expander("Click to show/hide the OpenAI Agents SDK code"):
        st.code("""
from agents import Agent, Runner, function_tool
import asyncio

# Define tools
@function_tool
def search_information(query: str) -> str:
    # Your search logic here
    return f"Research findings on {query}"

@function_tool
def analyze_data(data: str) -> str:
    # Your analysis logic here
    return f"Analysis results: {data}"

# Create specialized agents
research_agent = Agent(
    name="Research Specialist",
    instructions="You are a research expert. Find comprehensive information.",
    tools=[search_information]
)

analysis_agent = Agent(
    name="Data Analyst", 
    instructions="You analyze data and provide insights.",
    tools=[analyze_data]
)

writing_agent = Agent(
    name="Content Writer",
    instructions="You create polished, engaging content.",
    tools=[]
)

# Coordinator agent with handoffs
coordinator_agent = Agent(
    name="Project Coordinator",
    instructions="Coordinate between specialists based on the task.",
    handoffs=[research_agent, analysis_agent, writing_agent]
)

# Run the multi-agent workflow
async def main():
    result = await Runner.run(
        coordinator_agent, 
        "Research renewable energy and create a report"
    )
    print(result.final_output)

# For synchronous execution
result = Runner.run_sync(coordinator_agent, "Your request here")
print(result.final_output)
        """, language="python")
    
    st.markdown("### 🌐 Adding Exa AI to Multi-Agent Systems")
    with st.expander("Click to show/hide Exa multi-agent integration"):
        st.code("""
import exa_py
import os
from agents import Agent, Runner, function_tool

# Exa-powered research tools
@function_tool
def exa_web_search(query: str) -> str:
    \"\"\"Real-time web search using Exa AI\"\"\"
    exa = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])
    results = exa.search(query=query, num_results=3, text=True, highlights=True)
    
    search_summary = f"Web search results for '{query}':\\n\\n"
    for i, result in enumerate(results.results, 1):
        search_summary += f"{i}. **{result.title}**\\n"
        search_summary += f"   URL: {result.url}\\n"
        if result.highlights:
            search_summary += f"   Key info: {result.highlights[0][:200]}...\\n"
        search_summary += "\\n"
    return search_summary

@function_tool
def exa_arxiv_search(topic: str) -> str:
    \"\"\"Search for latest papers on arXiv using Exa AI\"\"\"
    exa = exa_py.Exa(api_key=os.environ["EXA_API_KEY"])
    results = exa.search(
        query=f"{topic} site:arxiv.org",
        num_results=5,
        text=True,
        include_domains=["arxiv.org"]
    )
    
    papers_summary = f"Latest arXiv papers on '{topic}':\\n\\n"
    for i, result in enumerate(results.results, 1):
        papers_summary += f"{i}. **{result.title}**\\n"
        papers_summary += f"   arXiv URL: {result.url}\\n"
        if result.text:
            papers_summary += f"   Abstract: {result.text[:250]}...\\n"
        papers_summary += "\\n"
    return papers_summary

@function_tool
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

# Create specialized Exa-powered agents
web_research_agent = Agent(
    name="Exa Web Research Specialist",
    instructions=\"\"\"You are a web research specialist powered by Exa AI.
    Your job is to find real-time information from the web, analyze current trends,
    and provide up-to-date insights. Always use Exa search for current information.\"\"\",
    tools=[exa_web_search, exa_company_research]
)

academic_research_agent = Agent(
    name="Academic Research Specialist",
    instructions=\"\"\"You are an academic research specialist powered by Exa AI.
    Your job is to find the latest research papers, analyze academic trends,
    and summarize cutting-edge findings from arXiv.\"\"\",
    tools=[exa_arxiv_search]
)

synthesis_agent = Agent(
    name="Research Synthesis Analyst",
    instructions=\"\"\"You are a synthesis analyst. Your job is to:
    1. Take research from multiple agents (web, academic, etc.)
    2. Identify patterns and connections across different sources
    3. Provide comprehensive analysis and strategic insights
    4. Create actionable recommendations based on all findings\"\"\",
    tools=[]
)

# Parallel Research Coordinator
parallel_coordinator = Agent(
    name="Parallel Research Coordinator",
    instructions=\"\"\"You coordinate parallel research across multiple agents.
    For any research topic, delegate to:
    - Web Research Specialist for current web information
    - Academic Research Specialist for latest papers
    Then hand off to Synthesis Analyst for comprehensive analysis.\"\"\",
    handoffs=[web_research_agent, academic_research_agent, synthesis_agent]
)

# Usage example
async def research_with_exa(topic: str):
    result = await Runner.run(
        parallel_coordinator,
        f"Research the latest developments in {topic} from both web sources and academic papers. Provide comprehensive analysis with strategic insights."
    )
    return result.final_output

# Run the research
result = Runner.run_sync(
    parallel_coordinator,
    "Research the latest developments in large language models"
)
print(result.final_output)
        """, language="python")
        
        st.markdown("""
        **🚀 Key Benefits of Exa in Multi-Agent Systems:**
        
        **🔄 Parallel Research**: Multiple agents can search different sources simultaneously:
        - One agent searches web sources
        - Another searches academic papers  
        - Third agent searches social media discussions
        - Fourth agent searches code repositories
        
        **🎯 Specialized Expertise**: Each agent becomes an expert in their domain:
        - **Web Agent**: Current news, trends, company information
        - **Academic Agent**: Latest research papers, scientific developments
        - **Social Agent**: Public opinion, expert discussions
        - **Code Agent**: Implementation examples, benchmarks
        
        **🧠 Intelligent Synthesis**: Strategic thinking agent combines all findings:
        - Identifies patterns across different sources
        - Connects academic research to practical applications
        - Provides comprehensive analysis and recommendations
        
        **⚡ Real-Time Intelligence**: Unlike static training data, Exa provides:
        - Current market conditions
        - Latest research developments
        - Recent news and trends
        - Up-to-date social discussions
        """)
        
        st.markdown("""
        **🔑 Setup Instructions:**
        1. **Install packages**: `pip install exa-py openai-agents`
        2. **Get API keys**: 
           - Exa API key from [exa.ai](https://exa.ai/)
           - OpenAI API key from [platform.openai.com](https://platform.openai.com/)
        3. **Set environment variables**:
           ```bash
           export EXA_API_KEY="your-exa-key-here"
           export OPENAI_API_KEY="your-openai-key-here"
           ```
        4. **Run your multi-agent system** with real-time intelligence!
        """)
    
    # Example scenarios
    st.markdown("---")
    st.markdown("### 🎮 Try These Multi-Agent Examples!")
    
    example_requests = [
        "Research the latest developments in diffusion models across arXiv, Twitter discussions, and Papers with Code. Provide strategic analysis on emerging trends and implementation opportunities.",
        "Investigate current multimodal AI research from academic papers, social media expert opinions, and code repositories. Synthesize findings with deep analytical insights.",
        "Study recent advances in reinforcement learning from human feedback (RLHF) across all research platforms. Generate strategic recommendations for practical applications.",
        "Research emerging trends in computer vision and foundation models. Gather insights from papers, community discussions, and implementations for comprehensive analysis.",
        "Explore the latest in AI safety and alignment research across academic and social platforms. Provide thoughtful analysis on current approaches and future directions."
    ]
    
    st.markdown("**These examples showcase different agents collaborating:**")
    
    for i, request in enumerate(example_requests):
        with st.expander(f"🎯 Example {i+1}: {request[:50]}..."):
            st.markdown(f"**Full request:** {request}")
            st.markdown("**Agent flow:** Parallel Research (arXiv + Twitter + Papers with Code) → Strategic Thinking Analysis → Writing")
            if st.button("Try this example", key=f"multi_example_{i}"):
                st.session_state.multi_example_request = request
                st.rerun()
    
    # Use example request if selected
    if hasattr(st.session_state, 'multi_example_request'):
        st.text_area("Selected example:", value=st.session_state.multi_example_request, key="multi_example_display")

else:
    st.info("👆 Please enter your OpenAI API key in the sidebar to try the multi-agent system!")

# Summary section
st.markdown("---")
st.markdown("### 🧠 Why Multi-Agent?")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **🎯 Specialization Benefits:**
    - Each agent has specific expertise
    - Better quality in their domain
    - More focused and efficient
    - Easier to debug and improve
    """)

with col2:
    st.markdown("""
    **🤝 Collaboration Power:**
    - Agents hand off tasks naturally
    - Complex workflows become manageable
    - Parallel processing capabilities
    - Scalable to many agents
    """)

st.markdown("---")
st.markdown("### 🆚 Single Agent vs Multi-Agent")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **🤖 Single Agent:**
    - One AI does everything
    - Jack of all trades, master of none
    - Can get overwhelmed with complex tasks
    - Harder to optimize for specific needs
    """)

with col2:
    st.markdown("""
    **👥 Multi-Agent:**
    - Specialized experts working together
    - Each agent masters their domain
    - Complex tasks broken down naturally
    - Easy to add new capabilities
    """)

 
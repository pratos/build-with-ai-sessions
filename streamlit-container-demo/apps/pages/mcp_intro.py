import streamlit as st

def show():
    st.title("🔌 Model Context Protocol (MCP) Introduction")
    st.markdown("*The universal standard for connecting AI to external tools and data*")
    
    # Hero section with key concept
    st.markdown("---")
    st.markdown("""
    ## 🎯 What is MCP?
    
    The **Model Context Protocol (MCP)** is an open standard for connecting AI assistants to the systems where data lives, 
    including content repositories, business tools, and development environments.
    
    **Think of MCP as the "USB-C for AI applications"** - a universal connector that replaces fragmented integrations with a single protocol.
    """)
    
    # Key benefits from Anthropic blog
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Key Benefits")
        st.markdown("""
        • **Universal Standard**: One protocol for all AI-data connections
        • **Simplified Integration**: Replace custom implementations with standardized approach
        • **Better Model Performance**: Provide relevant, up-to-date context to LLMs
        • **Scalable Architecture**: Easily add new data sources and tools
        • **Open Source**: Community-driven development and adoption
        """)
    
    with col2:
        st.markdown("### 🔧 Core Components")
        st.markdown("""
        • **Hosts**: AI applications that initiate connections (Claude Desktop, IDEs)
        • **Clients**: Connectors within host applications (1:1 with servers)
        • **Servers**: Services providing context and capabilities
        • **Protocol**: JSON-RPC 2.0 based communication standard
        """)
    
    # Architecture overview
    st.markdown("---")
    st.markdown("## 🏗️ MCP Architecture")
    
    st.markdown("""
    MCP follows a **client-server architecture** where each host can run multiple client instances:
    
    ```
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   MCP HOST      │    │   MCP CLIENT    │    │   MCP SERVER    │
    │                 │    │                 │    │                 │
    │ • Claude Desktop│◄──►│ • Protocol      │◄──►│ • Tools         │
    │ • IDE           │    │   Handler       │    │ • Resources     │
    │ • Custom App    │    │ • Security      │    │ • Prompts       │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
    ```
    """)
    st.image(
        "https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8dcc7dee-68d4-48cd-986c-190f40d16d5a_1536x1024.png",
        caption="MCP Architecture",
        use_column_width=True,
        width=1000,
    )
    st.text("Source: Addy Osmani's Substack")
    
    # The problem MCP solves
    st.markdown("---")
    st.markdown("## 🎯 The Problem MCP Solves")
    
    st.error("""
    **Before MCP: The N×M Problem**
    
    • Every AI application needed custom integrations for each data source
    • Fragmented implementations across teams and companies
    • Difficult to scale as systems grew
    • Models isolated from real-world, current data
    """)
    
    st.success("""
    **With MCP: The N+M Solution**
    
    • Build once, use everywhere approach
    • Standardized protocol for all integrations
    • Easy to add new AI applications or data sources
    • Models get access to live, relevant context
    """)
    
    # Three core primitives
    st.markdown("---")
    st.markdown("## 🔍 MCP Core Primitives")
    
    tab1, tab2, tab3 = st.tabs(["🛠️ Tools", "📚 Resources", "💬 Prompts"])
    
    with tab1:
        st.markdown("""
        ### Tools (Model-Controlled)
        Functions that LLMs can call to perform actions or retrieve information.
        
        **Examples:**
        - Weather API calls
        - Database queries  
        - File system operations
        - Web searches
        - Calculator functions
        
        **Key Features:**
        - Model decides when to invoke
        - Can have side effects
        - Structured input/output
        """)
    
    with tab2:
        st.markdown("""
        ### Resources (Application-Controlled)
        Data sources that provide context to language models.
        
        **Examples:**
        - File contents
        - Database schemas
        - API documentation
        - Configuration files
        - Knowledge bases
        
        **Key Features:**
        - Read-only access
        - URI-based identification
        - Subscription support for updates
        """)
    
    with tab3:
        st.markdown("""
        ### Prompts (User-Controlled)
        Pre-defined templates for common interactions.
        
        **Examples:**
        - Code review templates
        - Analysis workflows
        - Report generation
        - Task instructions
        - Best practice guides
        
        **Key Features:**
        - User-initiated
        - Parameterizable
        - Reusable across contexts
        """)
    
    # Useful images and resources
    st.markdown("---")
    st.markdown("## 📸 Visual Resources & Links")
    
    st.markdown("### 🖼️ Architecture Diagrams & Images")
    
    st.markdown("**AWS MCP Integration:**")
    st.image(
        "https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2025/05/23/ML-18605-bedrock-kb-architecture-884x630.png",
        caption="AWS MCP Integration",
        use_column_width=True,
        width=1000,
    )
    st.text("Source: AWS")
    
    st.markdown("**Community Diagrams:**")
    st.image(
        "https://composio.dev/wp-content/uploads/2025/03/Noah-MCP-1024x576.png",
        caption="MCPs as USB-C",
        use_column_width=True,
        width=1000,
    )
    st.text("Source: Noah")
    
    # Early adopters and ecosystem
    st.markdown("---")
    st.markdown("## 🌟 Early Adopters & Ecosystem")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🏢 Enterprise Adopters
        - **Block**: Building agentic systems with MCP
        - **Apollo**: Enhanced platform capabilities
        - **AWS**: MCP integration for cloud services
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Development Tools
        - **Zed**: IDE integration
        - **Replit**: Cloud development
        - **Codeium**: AI coding assistant
        - **Sourcegraph**: Code intelligence
        """)
    
    # Getting started
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    st.info("""
    **Ready to explore MCP?**
    
    1. **Learn the Basics**: Check out the simple MCP example in the next page
    2. **Compare Approaches**: See how MCP compares to traditional APIs
    3. **Build Your Own**: Create MCP servers for your data sources
    
    **Official Resources:**
    - [MCP Documentation](https://modelcontextprotocol.io/)
    - [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
    - [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
    - [Pre-built Servers](https://github.com/modelcontextprotocol/servers)
    """)
    
    # Quote from Anthropic blog
    st.markdown("---")
    st.markdown("""
    > *"MCP addresses the challenge of connecting AI systems with data sources, replacing fragmented integrations 
    > with a single protocol. The result is a simpler, more reliable way to give AI systems access to the data they need."*
    > 
    > — Anthropic Team
    """) 

# Call the show function when this file is executed
if __name__ == "__main__" or "streamlit" in globals():
    show() 
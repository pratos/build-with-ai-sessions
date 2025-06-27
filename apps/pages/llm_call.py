import streamlit as st
import openai
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
import json

st.markdown("# 💬 Basic LLM Call")
st.markdown("---")

st.markdown("""
### 🎯 Master LLM Fundamentals
Learn the building blocks of AI applications:

🔹 **Simple Conversations** - Send prompts, get responses  
🔹 **Structured Output** - Get JSON instead of text using Pydantic models  
🔹 **Usage Tracking** - Monitor tokens and costs  
🔹 **Model Selection** - Compare GPT-4o-mini, GPT-3.5-turbo, and GPT-4  

**💡 What you'll learn:** How to make basic OpenAI API calls and extract structured data for real applications.
""")

# Check for API key from session state
api_key = st.session_state.get("openai_api_key")

if api_key:
    client = openai.Client(api_key=api_key)
    
    # Simple example
    st.markdown("### 💬 Try a Simple Conversation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_prompt = st.text_area(
            "What would you like to ask the AI?", 
            value="Write a short poem about coding",
            height=100
        )
    
    with col2:
        model = st.selectbox("Choose Model:", ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"])
        temperature = st.slider("Creativity (Temperature):", 0.0, 1.0, 0.7, 0.1)
    
    if st.button("🚀 Send to AI", type="primary"):
        try:
            with st.spinner("🤔 AI is thinking..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": user_prompt}],
                    temperature=temperature
                )
            
            st.markdown("### 🎉 AI Response:")
            st.markdown(f"**{response.choices[0].message.content}**")
            
            # Show some stats
            st.markdown("### 📊 Usage Stats:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Input Tokens", response.usage.prompt_tokens)
            with col2:
                st.metric("Output Tokens", response.usage.completion_tokens)
            with col3:
                st.metric("Total Tokens", response.usage.total_tokens)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Code example section
    st.markdown("---")
    st.markdown("### 👨‍💻 Want to see the code?")
    
    with st.expander("Click to show/hide the Python code"):
        st.code("""
import openai

# Initialize the client
client = openai.Client(api_key="your-api-key-here")

# Make a simple request
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Write a short poem about coding"}
    ],
    temperature=0.7
)

# Get the response
print(response.choices[0].message.content)
        """, language="python")
    
    # Structured output example
    st.markdown("---")
    st.markdown("### 🏗️ Structured Output")
    st.markdown("Get JSON instead of just text for better integration.")
    
    # Define a Pydantic model for structured output
    class EmailStructure(BaseModel):
        subject: str
        body: str
        tone: str
        urgency: Optional[str] = None
    
    email_prompt = st.text_area(
        "Email Request:", 
        value="Write a professional email asking for a day off",
        height=80
    )
    
    if st.button("📧 Generate Structured Email", type="secondary"):
        try:
            with st.spinner("✨ Creating structured response..."):
                response = client.beta.chat.completions.parse(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional email assistant."},
                        {"role": "user", "content": email_prompt}
                    ],
                    response_format=EmailStructure
                )
            
            email_data = response.choices[0].message.parsed
            
            st.markdown("### 📧 Structured Email Output:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Subject:**")
                st.info(email_data.subject)
                st.markdown("**Tone:**")
                st.info(email_data.tone)
                if email_data.urgency:
                    st.markdown("**Urgency:**")
                    st.info(email_data.urgency)
            
            with col2:
                st.markdown("**Email Body:**")
                st.text_area("", value=email_data.body, height=200, disabled=True)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Show Pydantic class and code for structured output
    with st.expander("👨‍💻 Show Pydantic Class & Structured Output Code"):
        st.markdown("**Pydantic Model Definition:**")
        st.code("""
class EmailStructure(BaseModel):
    subject: str
    body: str
    tone: str
    urgency: Optional[str] = None
        """, language="python")
        
        st.markdown("**LLM Call with Structured Output:**")
        st.code("""
# Make structured output request
response = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a professional email assistant."},
        {"role": "user", "content": email_prompt}
    ],
    response_format=EmailStructure
)

# Parse the structured response
email_data = response.choices[0].message.parsed

# Access structured fields
print(f"Subject: {email_data.subject}")
print(f"Body: {email_data.body}")
print(f"Tone: {email_data.tone}")
if email_data.urgency:
    print(f"Urgency: {email_data.urgency}")
        """, language="python")
    
    # Research Paper Data Extraction
    st.markdown("---")
    st.markdown("### 📄 Research Paper Data Extraction")
    st.markdown("Extract structured data from academic papers with email validation.")
    
    class ResearchPaperData(BaseModel):
        """Structured data extraction from research papers"""
        authors: List[str] = Field(description="List of all authors mentioned in the paper")
        author_emails: List[EmailStr] = Field(description="List of email addresses of the authors")
        title: str = Field(description="Title of the research paper")
        novel_architecture_patterns: List[str] = Field(
            description="List of novel architecture patterns, frameworks, or methodologies introduced in the paper"
        )
        
        @field_validator('author_emails')
        @classmethod
        def validate_emails(cls, v):
            """Validate that all emails are properly formatted"""
            if not v:
                raise ValueError("At least one author email must be provided")
            
            # Additional validation beyond EmailStr
            for email in v:
                if '@' not in str(email):
                    raise ValueError(f"Invalid email format: {email}")
                if len(str(email)) < 5:
                    raise ValueError(f"Email too short: {email}")
            return v
        
        @field_validator('authors')
        @classmethod
        def validate_authors(cls, v):
            """Validate authors list"""
            if not v:
                raise ValueError("At least one author must be provided")
            if len(v) != len(set(v)):
                raise ValueError("Duplicate authors found")
            return v
        
        @field_validator('novel_architecture_patterns')
        @classmethod
        def validate_patterns(cls, v):
            """Validate architecture patterns"""
            if not v:
                raise ValueError("At least one novel architecture pattern must be identified")
            return v
    
    # Sample research paper text for demonstration
    sample_paper_text = """Title: "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context"

Authors: Zihang Dai, Zhilin Yang, Yiming Yang, Jaime Carbonell, Quoc V. Le, Ruslan Salakhutdinov

Contact: zihangd@cs.cmu.edu, zhiliny@cs.cmu.edu, yiming@cs.cmu.edu

Abstract: This paper introduces Transformer-XL, a novel neural architecture that enables 
learning dependency beyond a fixed length without disrupting temporal coherence. The key 
innovation is the segment-level recurrence mechanism and relative positional encoding scheme.

Novel Contributions:
1. Segment-level recurrence mechanism for longer context modeling
2. Relative positional encoding to handle variable sequence lengths
3. Attention caching mechanism for computational efficiency
4. State reuse across segments for better memory utilization"""
    
    # Text input for paper content
    paper_content = st.text_area(
        "📄 Enter research paper content:",
        value=sample_paper_text,
        height=200,
        help="Paste the research paper text here for data extraction"
    )
    
    if st.button("🔍 Extract Paper Data", type="secondary"):
        if not paper_content.strip():
            st.error("Please enter some paper content to analyze.")
        else:
            try:
                with st.spinner("🤖 Extracting structured data from paper..."):
                    completion = client.beta.chat.completions.parse(
                        model=model,
                        messages=[
                            {
                                "role": "system", 
                                "content": """You are an expert research paper analyst. Extract structured data from academic papers including:
                                - All authors mentioned
                                - Email addresses of authors (if available)
                                - Paper title
                                - Novel architecture patterns, frameworks, or methodologies introduced
                                
                                Be thorough and accurate in your extraction."""
                            },
                            {
                                "role": "user", 
                                "content": f"Extract structured data from this research paper:\n\n{paper_content}"
                            }
                        ],
                        response_format=ResearchPaperData,
                    )
                
                # Display results
                paper_data = completion.choices[0].message.parsed
                
                st.success("✅ Successfully extracted paper data!")
                
                # Display extracted data in organized sections
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("👥 Authors")
                    for i, author in enumerate(paper_data.authors, 1):
                        st.write(f"{i}. {author}")
                    
                    st.subheader("📧 Author Emails")
                    for i, email in enumerate(paper_data.author_emails, 1):
                        st.write(f"{i}. {email}")
                
                with col2:
                    st.subheader("📄 Paper Title")
                    st.write(paper_data.title)
                    
                    st.subheader("🏗️ Novel Architecture Patterns")
                    for i, pattern in enumerate(paper_data.novel_architecture_patterns, 1):
                        st.write(f"{i}. {pattern}")
                
                # Show raw structured data
                with st.expander("🔍 View Raw Structured Data"):
                    st.json(paper_data.model_dump())
                    
            except Exception as e:
                st.error(f"Error during extraction: {str(e)}")
    
    with st.expander("👨‍💻 Show Research Paper Extraction Code"):
        st.markdown("### Pydantic Model with Email Validation")
        st.code("""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List

class ResearchPaperData(BaseModel):
    \"\"\"Structured data extraction from research papers\"\"\"
    authors: List[str] = Field(description="List of all authors mentioned in the paper")
    author_emails: List[EmailStr] = Field(description="List of email addresses of the authors")
    title: str = Field(description="Title of the research paper")
    novel_architecture_patterns: List[str] = Field(
        description="List of novel architecture patterns, frameworks, or methodologies introduced in the paper"
    )
    
    @field_validator('author_emails')
    @classmethod
    def validate_emails(cls, v):
        \"\"\"Validate that all emails are properly formatted\"\"\"
        if not v:
            raise ValueError("At least one author email must be provided")
        
        # Additional validation beyond EmailStr
        for email in v:
            if '@' not in str(email):
                raise ValueError(f"Invalid email format: {email}")
            if len(str(email)) < 5:
                raise ValueError(f"Email too short: {email}")
        return v
    
    @field_validator('authors')
    @classmethod
    def validate_authors(cls, v):
        \"\"\"Validate authors list\"\"\"
        if not v:
            raise ValueError("At least one author must be provided")
        if len(v) != len(set(v)):
            raise ValueError("Duplicate authors found")
        return v
    
    @field_validator('novel_architecture_patterns')
    @classmethod
    def validate_patterns(cls, v):
        \"\"\"Validate architecture patterns\"\"\"
        if not v:
            raise ValueError("At least one novel architecture pattern must be identified")
        return v
        """, language="python")
        
        st.markdown("### LLM Call with Structured Parsing")
        st.code("""
# Extract structured data from research paper
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": \"\"\"You are an expert research paper analyst. Extract structured data from academic papers including:
            - All authors mentioned
            - Email addresses of authors (if available)  
            - Paper title
            - Novel architecture patterns, frameworks, or methodologies introduced
            
            Be thorough and accurate in your extraction.\"\"\"
        },
        {
            "role": "user", 
            "content": f"Extract structured data from this research paper:\\n\\n{paper_content}"
        }
    ],
    response_format=ResearchPaperData,
)

# Access the parsed structured data
paper_data = completion.choices[0].message.parsed

# Use the extracted data
print(f"Title: {paper_data.title}")
print(f"Authors: {paper_data.authors}")
print(f"Emails: {paper_data.author_emails}")
print(f"Novel Patterns: {paper_data.novel_architecture_patterns}")
        """, language="python")
        
        st.markdown("### Key Features")
        st.markdown("""
        - **Email Validation**: Uses `EmailStr` type + custom `@field_validator` decorator
        - **Required Fields**: All fields are required with descriptive error messages
        - **Duplicate Prevention**: Validates no duplicate authors
        - **Comprehensive Extraction**: Captures authors, emails, title, and novel patterns
        - **Production Ready**: Includes proper error handling and validation
        """)

else:
    st.info("👆 Please enter your OpenAI API key in the sidebar to try the examples!")

# Summary section
st.markdown("---")
st.markdown("### 🧠 Summary")
st.markdown("""
- **Basic LLM**: Send prompt → get response
- **Temperature**: Controls creativity (0 = focused, 1 = creative)
- **Structured Output**: Get JSON for better integration
- **Tokens**: AI processes text in chunks (~3/4 of a word)

**Next**: Add tools to make AI more powerful 🔧
""")

st.markdown("---")
st.markdown("### 🎯 Key Takeaways")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **✅ Pros:**
    - Simple and straightforward
    - Great for text generation
    - Fast responses
    """)
with col2:
    st.markdown("""
    **❌ Limitations:**
    - No access to real-time data
    - Can't perform actions
    - Limited to training knowledge
    """)

 
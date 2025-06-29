# Use the official uv image based on Python 3.12 slim
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for Streamlit and curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install dependencies first for better caching
COPY apps/pyproject.toml apps/uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

# Copy the application code
COPY apps/ ./

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash streamlit \
    && chown -R streamlit:streamlit /app

# Switch to non-root user
USER streamlit

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/_stcore/health || exit 1

# Set environment variables for production
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=true
ENV ENVIRONMENT=production

# Ensure no default API keys are available in production
ENV OPENAI_API_KEY=""
ENV EXA_API_KEY=""

# Run Streamlit using uv
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true", "--browser.gatherUsageStats=false"]
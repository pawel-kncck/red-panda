FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    bash \
    curl \
    tini \
    build-essential \
    procps \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install global npm packages
RUN npm install -g @anthropic-ai/claude-code

# Create a non-root user
RUN useradd -m -s /bin/bash developer && \
    mkdir -p /workspace /home/developer/.vscode-server /home/developer/.vscode-server-insiders && \
    chown -R developer:developer /workspace /home/developer

# Install Python development tools
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    black \
    mypy \
    ruff \
    pytest \
    coverage \
    alembic \
    ipython

WORKDIR /workspace

USER developer

# Add local bin to PATH for user-installed packages
ENV PATH="/home/developer/.local/bin:${PATH}"

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/bin/bash"]
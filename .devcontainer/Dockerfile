# .devcontainer/Dockerfile (Alternative Python-based)
FROM python:3.11-slim-bookworm

# Install Node.js 20.x and other dev basics
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates bash curl tini build-essential procps && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Claude Code CLI - install with error checking
RUN npm i -g @anthropic-ai/claude-code && \
    which claude || (echo "Claude Code installation failed" && exit 1)

# Create a non-root user (Python image doesn't have 'node' user)
RUN useradd -m -s /bin/bash developer && \
    mkdir -p /workspace /home/developer/.vscode-server /home/developer/.vscode-server-insiders && \
    chown -R developer:developer /workspace /home/developer

WORKDIR /workspace

# Note: Claude Code installs as 'claude' not 'claude-code'
# Create a wrapper with a different name to avoid conflicts
RUN echo '#!/bin/bash\nclaude --dangerously-skip-permissions "$@"' > /usr/local/bin/claude-dev && \
    chmod +x /usr/local/bin/claude-dev

USER developer

ENTRYPOINT ["/usr/bin/tini", "--"]
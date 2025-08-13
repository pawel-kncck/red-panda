# .devcontainer/Dockerfile
FROM node:20-bookworm-slim

# Dev basics + tini for clean signals (runs as root at build time)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git ca-certificates bash curl tini && \
    rm -rf /var/lib/apt/lists/*

# Claude Code CLI (still as root during build)
RUN npm i -g @anthropic-ai/claude-code

# Prepare workspace and VS Code directories with proper ownership
RUN mkdir -p /workspace /home/node/.vscode-server /home/node/.vscode-server-insiders && \
    chown -R node:node /workspace /home/node

WORKDIR /workspace
USER node

ENTRYPOINT ["/usr/bin/tini", "--"]
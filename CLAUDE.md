# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## IMPORTANT: Roadmap Maintenance

**Always keep `specs/roadmap.md` updated with progress.** After completing any tasks or phases:
1. Mark completed items with `[x]` checkboxes
2. Update status descriptions
3. Add completion dates where applicable
4. Document any deviations from the original plan
5. Commit roadmap updates along with the code changes

## IMPORTANT: Git Commit Strategy

**Every change must be committed to git.** Follow these rules:

1. **Commit Granularity**: Align commits with your todo list items. Each completed todo should have its own commit.
2. **Commit Frequently**: Don't batch multiple features/fixes into one commit.
3. **Clear Messages**: Write descriptive commit messages that explain what was changed and why.

### Commit Message Format:
```
<type>: <description>

[optional body with more details]
```

Types: `feat` (new feature), `fix` (bug fix), `refactor`, `docs`, `test`, `chore` (maintenance)

Examples:
- `feat: Add conversation model and migration`
- `fix: Correct API key encryption in user model`
- `refactor: Replace items routes with code blocks`
- `docs: Update API documentation for chat endpoints`

### Workflow:
1. Complete a todo item
2. Run linting/formatting
3. Test the changes
4. Commit immediately with clear message
5. Move to next todo item

## Project Overview

**Red Panda** is a data analysis tool that wraps LLM code interpreter functionality with a focus on code reusability. The project is built on the FastAPI full-stack template and aims to store all generated Python code separately for reuse across different datasets and markets.

**Current Status**: Base template deployed, no Red Panda-specific features implemented yet. See `specs/prd.md` and `specs/roadmap.md` for detailed requirements and implementation plan.

## Development Commands

### Backend (FastAPI)
```bash
# Run development server with hot-reload
cd backend
fastapi dev app/main.py

# Run tests with coverage
cd backend
./scripts/test.sh
# Or run specific test
pytest app/tests/api/routes/test_users.py::test_create_user

# Lint and type checking
cd backend
./scripts/lint.sh

# Auto-format code
cd backend
./scripts/format.sh

# Database migrations
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
alembic downgrade -1  # Rollback one migration
```

### Frontend (React/TypeScript)
```bash
# Run development server
cd frontend
npm run dev

# Build for production
cd frontend
npm run build

# Lint and auto-fix
cd frontend
npm run lint

# Generate API client from OpenAPI spec
cd frontend
npm run generate-client
```

### Docker Compose Stack
```bash
# Start entire stack with hot-reload
docker compose watch

# Start specific services
docker compose up backend frontend db

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Access services:
# - Frontend: http://localhost:5173
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Adminer (DB admin): http://localhost:8080
# - Traefik dashboard: http://localhost:8090
```

## Architecture

### Tech Stack
- **Backend**: FastAPI, SQLModel ORM, PostgreSQL, Alembic migrations
- **Frontend**: React 18, TypeScript, Chakra UI v3, TanStack Router/Query, Vite
- **Auth**: JWT tokens, bcrypt password hashing
- **Infrastructure**: Docker Compose, Traefik reverse proxy

### Database Models (Current)
- `User`: Authentication and user management (UUID primary keys)
- `Item`: Example CRUD model (to be replaced with Red Panda models)

### API Structure
```
backend/app/
├── api/
│   ├── deps.py          # Common dependencies (auth, DB session)
│   ├── main.py          # API router configuration
│   └── routes/          # API endpoints
│       ├── login.py     # Auth endpoints
│       ├── users.py     # User CRUD
│       └── items.py     # To be replaced with Red Panda routes
├── core/
│   ├── config.py        # Settings management (reads from ../.env)
│   ├── db.py            # Database connection
│   └── security.py      # Password hashing, JWT tokens
├── models.py            # SQLModel definitions
└── crud.py              # Database operations
```

### Frontend Routing
- Uses TanStack Router with file-based routing
- Protected routes check auth in `_layout.tsx`
- API client auto-generated from OpenAPI spec in `src/client/`

## Red Panda Implementation Plan

### Phase 0 (Current): Template Cleanup
- Remove Items functionality (repurpose for CodeBlocks)
- Update branding to "Red Panda"
- Configure environment variables

### Core Models to Add
1. **Conversation**: Chat sessions with LLM
2. **CodeBlock**: Extracted code with metadata (CORE FEATURE)
3. **Message**: Chat messages with code references
4. **File**: CSV uploads for analysis

### Key Services to Implement
1. **LLMService**: OpenAI/Anthropic integration with streaming
2. **CodeParser**: Extract and analyze code from LLM responses
3. **FileService**: CSV upload and metadata extraction

### API Endpoints Needed
- `/api/conversations`: CRUD for chat sessions
- `/api/chat`: Stream LLM responses
- `/api/code-blocks`: Search, filter, export code
- `/api/files`: Upload and manage CSVs

## Environment Configuration

Key environment variables in `.env`:
```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app

# Backend
SECRET_KEY=changethis  # Generate new for production
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis

# Frontend
FRONTEND_HOST=http://localhost:5173

# Domain (for Traefik routing)
DOMAIN=localhost
```

## Testing Strategy

- **Backend**: Pytest with test database, located in `backend/app/tests/`
- **Frontend**: Playwright E2E tests in `frontend/tests/`
- **Test users**: Created via fixtures in `conftest.py`
- **Coverage**: Run `./scripts/test.sh` for coverage report

## IMPORTANT: Frontend Testing and Debugging

**Always use Playwright MCP tools for frontend testing and debugging.** When working with the frontend:

1. **Use Playwright MCP for Browser Interaction**: 
   - Use `mcp__playwright__browser_*` tools to navigate, interact with, and debug the frontend
   - Always check console messages with `mcp__playwright__browser_console_messages` to catch JavaScript errors
   - Take snapshots with `mcp__playwright__browser_snapshot` to understand the current state

2. **Error Detection Workflow**:
   - After making frontend changes, navigate to the affected pages
   - Check browser console for errors immediately
   - Fix any errors found before proceeding
   - Verify fixes by rechecking the console

3. **Benefits**:
   - Real-time error detection from browser console
   - Visual verification of UI changes
   - Catch runtime errors that static analysis might miss
   - Test user interactions and flows

Example workflow:
```
1. Make frontend changes
2. Use mcp__playwright__browser_navigate to open the page
3. Use mcp__playwright__browser_console_messages to check for errors
4. Fix any errors found
5. Verify fixes by rechecking console and taking snapshots
```

## Migration from Template to Red Panda

When implementing Red Panda features:
1. Keep authentication system intact
2. Replace Item model/routes with CodeBlock
3. Convert sidebar from static navigation to conversation list
4. Add BYOK API key fields to User model
5. Implement streaming responses using FastAPI's StreamingResponse

## Critical Implementation Notes

1. **Code Extraction**: The core feature - ensure robust parsing of code blocks from LLM responses
2. **Storage**: Code blocks must have searchable metadata (imports, functions, variables)
3. **Streaming**: Use Server-Sent Events (SSE) for LLM responses, not WebSockets
4. **Security**: Encrypt API keys using existing security module
5. **File Storage**: Start with local storage in `/app/uploads/{user_id}/`, prepare S3 migration path

## Development Workflow

1. Always run format/lint before committing:
   ```bash
   cd backend && ./scripts/format.sh && ./scripts/lint.sh
   cd frontend && npm run lint
   ```

2. Test database changes locally before creating migrations

3. Frontend API client must be regenerated after backend API changes:
   ```bash
   cd frontend && npm run generate-client
   ```

4. Use UUID for all new model primary keys (following template pattern)
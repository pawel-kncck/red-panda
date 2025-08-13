# Red Panda Development Roadmap - UPDATED

## 🎯 Progress Summary
- **Phase 0**: ✅ Foundation Setup (90% complete - frontend branding pending)
- **Phase 1**: ✅ Core Data Models (100% complete)
- **Phase 2**: ✅ BYOK & LLM Integration (100% backend complete)
- **Phase 3**: ✅ Conversation Management (100% backend complete)
- **Phase 4**: ✅ Chat Interface (100% backend complete)
- **Phase 5**: ✅ Code Library (100% backend complete)
- **Phase 6**: ✅ File Management (100% backend complete)
- **Phase 7-8**: ⏳ Frontend implementation pending

## Current Status Overview
**Template Version**: FastAPI Full-Stack Template v0.1.0
**Project Status**: All backend API functionality complete! Frontend implementation needed
**Last Updated**: 2025-08-13
**Estimated Total Development Time**: 12-15 days for MVP (Ahead of schedule - Backend complete in 2 days)

### What's Already Working (From Template)
✅ PostgreSQL database with SQLModel ORM
✅ Alembic migrations configured
✅ JWT authentication system
✅ User registration, login, and password reset
✅ Admin panel with user management
✅ React frontend with TypeScript
✅ Chakra UI components and dark mode
✅ Docker Compose development environment
✅ API documentation (Swagger)
✅ Testing framework (Pytest + Playwright)
✅ GitHub Actions CI/CD

---

## Phase 0: Foundation Setup & Cleanup ⏱️ **Day 1**
**Goal**: Clean up template and prepare for Red Panda development

### Completed Tasks ✅
- [x] Clone FastAPI template repository
- [x] Repository initialized as `red-panda`
- [x] Git repository configured

### Immediate Tasks (Day 1) ✅ COMPLETED
- [x] **Environment Setup**
  - [x] Configure `.env` file with proper values
  - [x] Start PostgreSQL with Docker Compose (using port 5433)
  - [x] Verify database connection
  - [x] Test authentication flow (register/login)
  
- [x] **Template Cleanup**
  - [x] Remove Items model and related code
  - [x] Remove Items routes and API endpoints
  - [ ] Remove Items frontend components (pending)
  - [x] Clean up unused example code
  - [ ] Update app name and branding to "Red Panda" (pending)
  
- [ ] **Development Environment**
  - [ ] Verify hot-reload works for backend
  - [ ] Verify hot-reload works for frontend
  - [ ] Test Docker Compose setup
  - [ ] Configure VS Code/IDE for project

**✅ Checkpoint**: Clean template with Red Panda branding, auth working

---

## Phase 1: Core Data Models ⏱️ **Day 2-3** ✅ COMPLETED (2025-08-12)
**Goal**: Extend database schema for Red Panda specific needs

### Database Models to Create

#### Day 2: Core Models
- [x] **Conversation Model**
  ```python
  # backend/app/models/conversation.py
  - id (UUID, primary key)
  - user_id (foreign key)
  - title (string)
  - created_at, updated_at (datetime)
  - message_count (integer)
  - last_message_preview (string)
  - Relationships to messages and code_blocks
  ```

- [x] **CodeBlock Model** ⭐ CORE
  ```python
  # backend/app/models/code_block.py
  - id (UUID, primary key)
  - conversation_id (foreign key)
  - user_id (foreign key)
  - code (text)
  - description (text)
  - language (string)
  - executed_successfully (boolean)
  - imports, functions_defined, variables_created (JSON)
  - tags (JSON array)
  - version, parent_version_id (versioning support)
  ```

#### Day 3: Supporting Models
- [x] **Message Model**
  ```python
  # backend/app/models/message.py
  - id (UUID, primary key)
  - conversation_id (foreign key)
  - role (user/assistant/system enum)
  - content (text)
  - code_block_ids (JSON array)
  - created_at (datetime)
  ```

- [x] **File Model**
  ```python
  # backend/app/models/file.py
  - id (UUID, primary key)
  - user_id (foreign key)
  - filename, storage_path
  - file_metadata (JSON) - renamed from metadata to avoid SQLAlchemy conflict
  - mime_type, size_bytes
  - uploaded_at (datetime)
  ```

- [x] **Create and Run Migrations**
  - [x] Generate Alembic migrations
  - [x] Test migrations up and down
  - [x] Add database indexes

**✅ Checkpoint**: All models created, migrations successful

---

## Phase 2: BYOK & LLM Integration ⏱️ **Day 4-5** ✅ COMPLETED (2025-08-13)
**Goal**: Enable users to use their own API keys

### Day 4: Backend LLM Service ✅ COMPLETED
- [x] **Extend User Model** ✅ COMPLETED (2025-08-12)
  - [x] Add encrypted api_keys field
  - [x] Add usage tracking field (api_usage)
  - [x] Create migration

- [x] **LLM Service Implementation** ✅ COMPLETED (2025-08-13)
  - [x] Create `backend/app/services/llm_service.py`
  - [x] OpenAI integration with streaming
  - [x] Anthropic Claude integration with streaming
  - [x] Error handling and retry logic
  - [x] API key validation endpoint

- [x] **Security** ✅ COMPLETED (2025-08-13)
  - [x] Implement API key encryption using existing security module
  - [x] Add encrypt/decrypt functions to security module

### Day 5: Frontend Settings
- [ ] **Settings Page Updates**
  - [ ] API key input form
  - [ ] Provider selection UI
  - [ ] Key validation feedback
  - [ ] Usage display (optional)

- [ ] **API Integration**
  - [ ] Settings service in frontend
  - [ ] API key status in header

**✅ Checkpoint**: Can save API key and make test LLM calls

---

## Phase 3: Conversation Management ⏱️ **Day 6** ✅ COMPLETED (2025-08-13)
**Goal**: Basic conversation CRUD and UI

### Backend Tasks ✅ COMPLETED
- [x] **API Routes**
  - [x] Create `/api/conversations` endpoints
  - [x] List, create, update, delete
  - [x] Pagination support

### Frontend Tasks
- [ ] **Sidebar Conversion**
  - [ ] Replace items list with conversations
  - [ ] New chat button
  - [ ] Conversation switching
  - [ ] Auto-title generation

**✅ Checkpoint**: Can create and switch between conversations

---

## Phase 4: Chat Interface ⏱️ **Day 7-8** ✅ BACKEND COMPLETED (2025-08-13)
**Goal**: Full chat experience with code extraction

### Day 7: Basic Chat ✅ BACKEND COMPLETED
- [x] **Chat API Endpoint**
  - [x] `/api/chat` with streaming using SSE
  - [x] Message creation and storage
  - [x] LLM integration with both OpenAI and Anthropic

- [ ] **Frontend Chat UI**
  - [ ] Message list component
  - [ ] Input with submit
  - [ ] Basic message display

### Day 8: Code Extraction ✅ BACKEND COMPLETED
- [x] **Code Parser Service**
  - [x] Extract code from LLM responses
  - [x] Parse code metadata (imports, functions, variables)
  - [x] Auto-generate descriptions

- [ ] **Code Block UI**
  - [ ] Syntax highlighting (Prism.js)
  - [ ] Copy button
  - [ ] Save to library action

**✅ Checkpoint**: Can chat and see formatted code blocks

---

## Phase 5: Code Library ⭐ **CORE** ⏱️ **Day 9-10**
**Goal**: Searchable, reusable code repository

### Day 9: Backend ✅ COMPLETED (2025-08-13)
- [x] **Code Block APIs**
  - [x] Search endpoint with filters (language, tags, query)
  - [x] Tag management integrated in code blocks
  - [x] CRUD endpoints for code blocks

### Day 10: Frontend
- [ ] **Library Interface**
  - [ ] New route `/code-library`
  - [ ] Grid view with cards
  - [ ] Search and filters
  - [ ] Use in chat flow

**✅ Checkpoint**: Complete code library functionality

---

## Phase 6: File Management ⏱️ **Day 11**
**Goal**: CSV upload and management

### Tasks ✅ BACKEND COMPLETED (2025-08-13)
- [x] **File Upload Backend**
  - [x] Upload endpoint with validation
  - [x] CSV metadata extraction (via pandas)
  - [x] File storage system (local with S3 ready)

- [ ] **Upload UI**
  - [ ] Drag-and-drop component
  - [ ] File list page
  - [ ] Integration with chat

**✅ Checkpoint**: Can upload and reference CSV files

---

## Phase 7: Polish & Testing ⏱️ **Day 12-13**
**Goal**: Production readiness

### Day 12: Essential Polish
- [ ] Loading states everywhere
- [ ] Error handling
- [ ] Mobile responsive fixes
- [ ] Rate limiting

### Day 13: Testing & Documentation
- [ ] Integration tests
- [ ] Update README
- [ ] Deployment guide
- [ ] User documentation

**✅ Checkpoint**: MVP ready for deployment

---

## Phase 8: Deployment ⏱️ **Day 14-15**
**Goal**: Deploy to production

### Deployment Tasks
- [ ] Configure production environment
- [ ] Set up SSL/HTTPS
- [ ] Deploy with Docker Compose
- [ ] Configure monitoring
- [ ] Smoke tests

**✅ Final Checkpoint**: Red Panda MVP live!

---

## Post-MVP Features (Priority Order)

### Quick Wins (1-2 days each)
1. [ ] Anthropic Claude support
2. [ ] Jupyter notebook export
3. [ ] Code versioning UI
4. [ ] Advanced search filters
5. [ ] Custom tags management

### Medium Features (3-5 days each)
1. [ ] Code execution sandbox
2. [ ] Output visualization (charts/tables)
3. [ ] Usage analytics dashboard
4. [ ] Conversation templates
5. [ ] Bulk operations

### Large Features (1-2 weeks each)
1. [ ] Team workspaces
2. [ ] GitHub integration
3. [ ] Scheduled analysis
4. [ ] Custom prompt engineering
5. [ ] API for external integrations

---

## Development Guidelines

### Daily Development Flow
1. **Morning**: Review tasks for the day
2. **Coding**: Focus on one phase at a time
3. **Testing**: Test each feature as built
4. **Commit**: Frequent commits with clear messages
5. **Evening**: Update progress, plan next day

### Code Organization
- Keep template structure intact where possible
- Add new features in separate modules
- Follow existing patterns for consistency
- Document new APIs and components

### Testing Strategy
- Unit tests for services
- Integration tests for APIs
- E2E tests for critical flows
- Manual testing for UI/UX

---

## Risk Mitigation

### Potential Blockers & Solutions

| Risk | Impact | Mitigation |
|------|--------|------------|
| LLM API complexity | High | Start with OpenAI only |
| Code extraction accuracy | High | Build robust fallbacks |
| File storage scaling | Medium | Local first, S3 ready |
| Streaming implementation | Medium | Use SSE, not WebSockets |
| Migration conflicts | Low | Test thoroughly |

### Fallback Options
- **If LLM integration delayed**: Mock responses for UI development
- **If code parsing complex**: Start with simple regex patterns
- **If file uploads problematic**: Text paste as alternative
- **If streaming difficult**: Polling as temporary solution

---

## Success Criteria for MVP

### Functional Requirements
- [x] Users can register and login ✅
- [x] Database models for core features ✅
- [ ] Users can add their OpenAI API key
- [ ] Users can have conversations with LLM
- [ ] Code blocks are extracted and saved
- [ ] Users can browse their code library
- [ ] Users can reuse code in new chats
- [ ] Users can upload CSV files
- [ ] Users can copy/export code

### Performance Requirements
- [ ] Chat response starts < 1 second
- [ ] Code search returns < 500ms
- [ ] File upload up to 50MB
- [ ] 100 concurrent users supported

### Quality Requirements
- [ ] No critical bugs
- [ ] Mobile responsive
- [ ] Dark mode functional
- [ ] Error messages helpful

---

## Current Action Items

### ✅ Completed (2025-08-12 to 2025-08-13)
**Day 1 (2025-08-12):**
1. ✅ Configure `.env` file
2. ✅ Start Docker Compose (using port 5433 for PostgreSQL)
3. ✅ Test authentication flow
4. ✅ Remove Items functionality from backend
5. ✅ Create ALL core models (Conversation, CodeBlock, Message, File)
6. ✅ Add BYOK fields to User model
7. ✅ Generate and run migrations successfully
8. ✅ Organize models into separate files
9. ✅ Fix SQLAlchemy relationship configurations

**Day 2 (2025-08-13):**
1. ✅ Create API routes for conversations (CRUD operations)
2. ✅ Create API routes for code blocks with search functionality
3. ✅ Create API routes for messages within conversations
4. ✅ Create API routes for file upload and management
5. ✅ Implement LLM service with OpenAI and Anthropic support
6. ✅ Implement streaming chat endpoint using SSE
7. ✅ Create code parser service for extracting code blocks
8. ✅ Create file service for handling uploads
9. ✅ Add settings API for managing API keys
10. ✅ Fix crud module conflicts and imports

### Immediate Next Steps
1. Set up PostgreSQL database (Docker or local)
2. Run database migrations
3. Create initial superuser
4. Test the complete backend flow
5. Begin frontend implementation

### This Week's Goal
Complete Phases 2-3: Have working conversations with LLM integration

---

## Notes for Development

### What NOT to Change (Template Assets)
- Authentication system (works well)
- Database configuration
- Docker setup
- Testing framework
- CI/CD pipelines

### What to Modify
- Items → Code Blocks
- Sidebar navigation → Conversations
- Admin features → Keep but extend
- Settings page → Add BYOK

### What to Add New
- All LLM integration
- Code parsing and storage
- File upload system
- Chat interface
- Code library

---

**Project Status**: Ready to begin development. Template provides solid foundation. Focus on core features (code storage and reusability) first. 12-15 days to MVP is achievable with focused effort.
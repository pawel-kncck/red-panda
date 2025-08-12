# Red Panda Development Roadmap - UPDATED

## Current Status Overview
**Template Version**: FastAPI Full-Stack Template v0.1.0
**Project Status**: Initial setup - template cloned, no customization
**Estimated Total Development Time**: 12-15 days for MVP

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

### Immediate Tasks (Day 1)
- [ ] **Environment Setup**
  - [ ] Configure `.env` file with proper values
  - [ ] Start PostgreSQL with Docker Compose
  - [ ] Verify database connection
  - [ ] Test authentication flow (register/login)
  
- [ ] **Template Cleanup**
  - [ ] Remove Items model and related code
  - [ ] Remove Items routes and API endpoints
  - [ ] Remove Items frontend components
  - [ ] Clean up unused example code
  - [ ] Update app name and branding to "Red Panda"
  
- [ ] **Development Environment**
  - [ ] Verify hot-reload works for backend
  - [ ] Verify hot-reload works for frontend
  - [ ] Test Docker Compose setup
  - [ ] Configure VS Code/IDE for project

**✅ Checkpoint**: Clean template with Red Panda branding, auth working

---

## Phase 1: Core Data Models ⏱️ **Day 2-3**
**Goal**: Extend database schema for Red Panda specific needs

### Database Models to Create

#### Day 2: Core Models
- [ ] **Conversation Model**
  ```python
  # backend/app/models/conversation.py
  - id (UUID, primary key)
  - user_id (foreign key)
  - title (string)
  - created_at, updated_at (datetime)
  - message_count (integer)
  ```

- [ ] **CodeBlock Model** ⭐ CORE
  ```python
  # backend/app/models/code_block.py
  - id (UUID, primary key)
  - conversation_id (foreign key)
  - user_id (foreign key)
  - code (text)
  - description (text)
  - metadata (JSON)
  ```

#### Day 3: Supporting Models
- [ ] **Message Model**
  ```python
  # backend/app/models/message.py
  - id (UUID, primary key)
  - conversation_id (foreign key)
  - role (user/assistant)
  - content (text)
  - code_block_ids (JSON array)
  ```

- [ ] **File Model**
  ```python
  # backend/app/models/file.py
  - id (UUID, primary key)
  - user_id (foreign key)
  - filename, storage_path
  - metadata (JSON)
  ```

- [ ] **Create and Run Migrations**
  - [ ] Generate Alembic migrations
  - [ ] Test migrations up and down
  - [ ] Add database indexes

**✅ Checkpoint**: All models created, migrations successful

---

## Phase 2: BYOK & LLM Integration ⏱️ **Day 4-5**
**Goal**: Enable users to use their own API keys

### Day 4: Backend LLM Service
- [ ] **Extend User Model**
  - [ ] Add encrypted api_keys field
  - [ ] Add usage tracking field
  - [ ] Create migration

- [ ] **LLM Service Implementation**
  - [ ] Create `backend/app/services/llm_service.py`
  - [ ] OpenAI integration with streaming
  - [ ] Error handling and retry logic
  - [ ] API key validation endpoint

- [ ] **Security**
  - [ ] Implement API key encryption
  - [ ] Add to security module

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

## Phase 3: Conversation Management ⏱️ **Day 6**
**Goal**: Basic conversation CRUD and UI

### Backend Tasks
- [ ] **API Routes**
  - [ ] Create `/api/conversations` endpoints
  - [ ] List, create, update, delete
  - [ ] Pagination support

### Frontend Tasks
- [ ] **Sidebar Conversion**
  - [ ] Replace items list with conversations
  - [ ] New chat button
  - [ ] Conversation switching
  - [ ] Auto-title generation

**✅ Checkpoint**: Can create and switch between conversations

---

## Phase 4: Chat Interface ⏱️ **Day 7-8**
**Goal**: Full chat experience with code extraction

### Day 7: Basic Chat
- [ ] **Chat API Endpoint**
  - [ ] `/api/chat` with streaming
  - [ ] Message creation and storage
  - [ ] LLM integration

- [ ] **Frontend Chat UI**
  - [ ] Message list component
  - [ ] Input with submit
  - [ ] Basic message display

### Day 8: Code Extraction
- [ ] **Code Parser Service**
  - [ ] Extract code from LLM responses
  - [ ] Parse code metadata
  - [ ] Auto-generate descriptions

- [ ] **Code Block UI**
  - [ ] Syntax highlighting (Prism.js)
  - [ ] Copy button
  - [ ] Save to library action

**✅ Checkpoint**: Can chat and see formatted code blocks

---

## Phase 5: Code Library ⭐ **CORE** ⏱️ **Day 9-10**
**Goal**: Searchable, reusable code repository

### Day 9: Backend
- [ ] **Code Block APIs**
  - [ ] Search endpoint with filters
  - [ ] Tag management
  - [ ] Export endpoints

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

### Tasks
- [ ] **File Upload Backend**
  - [ ] Upload endpoint with validation
  - [ ] CSV metadata extraction
  - [ ] File storage system

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
- [x] Users can register and login
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

### Immediate Next Steps (Do Today)
1. Configure `.env` file
2. Start Docker Compose
3. Test authentication flow
4. Remove Items functionality
5. Update branding

### Tomorrow's Focus
1. Create Conversation model
2. Create CodeBlock model
3. Generate migrations
4. Test database schema

### This Week's Goal
Complete Phases 0-3: Have working conversations with LLM integration

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
# Product Requirements Document (PRD) - UPDATED
## Red Panda - Reusable Code Interpreter for Data Analysis

### Executive Summary
Red Panda is a data analysis tool that wraps LLM code interpreter functionality with a focus on code reusability. Unlike traditional AI chat interfaces, Red Panda stores all generated Python code separately, enabling data analysts and scientists to reuse, validate, and adapt code for different datasets and markets. Built on the FastAPI full-stack template with a BYOK (Bring Your Own Key) model.

### Current Implementation Status
**Base Template**: FastAPI Full-Stack Template v0.1.0
**Status**: Initial setup phase - template deployed, no custom features implemented

#### What's Currently Available (From Template):
✅ **Authentication System**
- JWT-based authentication
- User registration and login
- Password reset via email
- User profile management

✅ **Admin Features**
- User management (CRUD operations)
- Superuser privileges
- Admin dashboard

✅ **Database Layer**
- PostgreSQL with SQLModel ORM
- Alembic migrations configured
- UUID-based primary keys

✅ **Frontend Foundation**
- React 18 with TypeScript
- Chakra UI v3 component library
- TanStack Router for navigation
- TanStack Query for data fetching
- Dark mode support
- Responsive design

✅ **Development Infrastructure**
- Docker Compose setup
- Hot-reload for development
- API documentation (Swagger/OpenAPI)
- Testing framework (Pytest + Playwright)
- CI/CD with GitHub Actions

✅ **Security**
- Secure password hashing (bcrypt)
- CORS configuration
- Environment variable management
- Sentry error tracking integration

#### What Needs to Be Built (Red Panda Specific):
❌ **Core Features**
- LLM integration (OpenAI/Anthropic)
- BYOK API key management
- Conversation management
- Code block extraction and storage
- Code library interface
- CSV file handling
- Data analysis chat interface

### Problem Statement
Data professionals using LLM-based code interpreters face three critical challenges:
- **No Code Reusability**: Generated code is trapped within chat conversations, requiring regeneration for similar tasks
- **No Validation Path**: Cannot independently verify LLM outputs by running the exact code locally
- **No Cross-Market Repeatability**: Cannot easily apply the same analysis to different datasets or market segments

### Product Vision
Create the most efficient bridge between AI-assisted analysis and production-ready, reusable data science code.

### Target Users
- **Primary**: Data Analysts who need quick, reusable analysis templates
- **Secondary**: Data Scientists validating AI-generated approaches
- **Tertiary**: Business Analysts working with recurring reports across markets/segments

---

## Core Features to Implement

### 1. Authentication & BYOK Setup 🔧 **PARTIAL**
**Status**: Authentication exists, BYOK needs implementation

**User Story**: As a user, I want to securely use my own LLM API key so I maintain control over costs and data privacy.

**Already Available**:
- ✅ Email/password authentication
- ✅ User management system
- ✅ Settings page structure

**To Implement**:
- ❌ Secure API key storage (encrypted field in User model)
- ❌ Support for OpenAI and Anthropic API keys
- ❌ API key validation on entry
- ❌ Usage tracking per user
- ❌ API key status indicator in header

**Database Schema Addition**:
```python
# Add to User model
api_keys: dict = Field(default={}, sa_column=Column(JSON))  # Encrypted
api_usage: dict = Field(default={}, sa_column=Column(JSON))
```

### 2. Conversation Management ❌ **NOT STARTED**
**User Story**: As a user, I want to organize and access my analysis conversations so I can reference previous work.

**Requirements**:
- Conversation model and CRUD operations
- Conversation list in sidebar (replace current navigation)
- Auto-generated conversation titles
- Rename/delete capabilities
- Search functionality
- Timestamp and preview display

**New Models Needed**:
```python
class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    title: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    message_count: int = Field(default=0)
    last_message_preview: str | None = Field(default=None, max_length=500)
```

### 3. Code Storage & Management ⭐ **CORE FEATURE** ❌ **NOT STARTED**
**User Story**: As a data analyst, I want all Python code stored separately so I can reuse it across different markets and validate results independently.

**Requirements**:
- Code block model with comprehensive metadata
- Automatic extraction from LLM responses
- Tagging and categorization system
- Version tracking
- Search and filter capabilities

**Database Schema**:
```python
class CodeBlock(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id")
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    code: str
    description: str  # Auto-generated
    language: str = Field(default="python", max_length=20)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    executed_successfully: bool | None = None
    imports: list[str] = Field(default=[], sa_column=Column(JSON))
    functions_defined: list[str] = Field(default=[], sa_column=Column(JSON))
    variables_created: list[str] = Field(default=[], sa_column=Column(JSON))
    tags: list[str] = Field(default=[], sa_column=Column(JSON))
    version: int = Field(default=1)
    parent_version_id: UUID | None = Field(default=None, foreign_key="codeblock.id")
```

### 4. Code Library Interface ❌ **NOT STARTED**
**User Story**: As a user, I want to browse, search, and reuse my code collection across different analyses.

**Frontend Components Needed**:
- New route: `/code-library`
- Grid/list view toggle
- Advanced search and filters
- Code preview with syntax highlighting
- Export functionality
- "Use in chat" action

### 5. Data Analysis Chat Interface ❌ **NOT STARTED**
**User Story**: As a user, I want to analyze my data through natural language queries and see both explanations and executable code.

**Components to Build**:
- Replace current Items functionality with Chat
- Message input with file attachment
- Streaming response display
- Code block rendering with actions
- Output visualization support

### 6. CSV File Management ❌ **NOT STARTED**
**User Story**: As a user, I want to upload and manage CSV files for analysis across different conversations.

**Requirements**:
- New File model and storage system
- Drag-and-drop upload interface
- File metadata extraction
- Cross-conversation file access

**Database Schema**:
```python
class File(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    filename: str = Field(max_length=255)
    storage_path: str = Field(max_length=500)
    size_bytes: int
    mime_type: str = Field(max_length=100)
    metadata: dict = Field(default={}, sa_column=Column(JSON))
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
```

### 7. LLM Integration Service ❌ **NOT STARTED**
**Backend Service Architecture**:
```python
# backend/app/services/llm_service.py
class LLMService:
    def __init__(self, api_key: str, provider: str = "openai"):
        pass
    
    async def generate(self, prompt: str, context: dict) -> dict:
        pass
    
    async def stream_generate(self, prompt: str, context: dict):
        pass

# backend/app/services/code_parser.py
class CodeParser:
    def extract_code_blocks(self, llm_response: str) -> list[dict]:
        pass
    
    def analyze_code(self, code: str) -> dict:
        # Extract imports, functions, variables
        pass
```

---

## Technical Architecture Updates

### Backend Structure (FastAPI)
```
backend/app/
├── models/              # NEW MODELS NEEDED
│   ├── conversation.py  ❌
│   ├── code_block.py    ❌
│   ├── file.py          ❌
│   └── message.py       ❌
├── api/routes/          # NEW ROUTES NEEDED
│   ├── conversations.py ❌
│   ├── code_blocks.py   ❌
│   ├── files.py         ❌
│   ├── llm.py           ❌
│   └── (existing routes) ✅
├── services/            # NEW SERVICES NEEDED
│   ├── llm_service.py   ❌
│   ├── code_executor.py ❌
│   ├── code_parser.py   ❌
│   └── file_service.py  ❌
└── core/                # EXISTING, NEEDS EXTENSION
    ├── config.py        🔧 (add LLM configs)
    └── security.py      🔧 (add encryption for API keys)
```

### Frontend Structure (React + TypeScript)
```
frontend/src/
├── components/          # NEW COMPONENTS NEEDED
│   ├── Chat/           ❌
│   │   ├── MessageList.tsx
│   │   ├── MessageInput.tsx
│   │   ├── CodeBlock.tsx
│   │   └── OutputDisplay.tsx
│   ├── CodeLibrary/    ❌
│   │   ├── CodeGrid.tsx
│   │   ├── CodeCard.tsx
│   │   └── CodeFilters.tsx
│   ├── FileUpload/     ❌
│   │   └── CSVUploader.tsx
│   └── (existing)      ✅
├── routes/             # ROUTES TO ADD/MODIFY
│   ├── _layout/
│   │   ├── chat.tsx    ❌ (replace items.tsx)
│   │   ├── library.tsx ❌
│   │   └── files.tsx   ❌
│   └── (existing)      ✅
└── services/           # NEW SERVICES NEEDED
    ├── llmService.ts   ❌
    ├── codeStorage.ts  ❌
    └── fileService.ts  ❌
```

---

## MVP Scope (Phase 1)

### Must Have for MVP
1. ✅ Basic authentication (EXISTS)
2. ❌ BYOK API key management
3. ❌ Conversation creation and list
4. ❌ Chat interface with LLM integration
5. ❌ **Code block storage and retrieval** ⭐
6. ❌ Basic code library view
7. ❌ CSV upload capability
8. ❌ Copy code to clipboard

### Nice to Have (Phase 2)
- Code execution in sandbox
- Output visualization rendering
- Code versioning UI
- Advanced search and filters
- Jupyter notebook export
- Multiple LLM provider support

### Out of Scope for MVP
- Real-time collaboration
- Scheduled analysis runs
- Custom models/fine-tuning
- Mobile app
- Team sharing features

---

## Migration Path from Current State

### Phase 0: Template Cleanup ✅ **READY TO START**
- Remove Items functionality (or repurpose for code blocks)
- Remove unnecessary example code
- Update branding and app name
- Configure environment for development

### Phase 1: Core Models & Database
- Create all new models
- Generate and run migrations
- Set up database indexes

### Phase 2: LLM Integration
- Implement BYOK system
- Create LLM service layer
- Add streaming support

### Phase 3: Chat & Conversations
- Build conversation management
- Create chat interface
- Integrate with LLM service

### Phase 4: Code Library (CORE)
- Implement code extraction
- Build storage system
- Create library interface

### Phase 5: File Management
- Add file upload system
- Integrate with chat

### Phase 6: Polish & Deploy
- Testing and bug fixes
- Performance optimization
- Production deployment

---

## Success Metrics

### Primary KPIs
- **Code Reuse Rate**: >40% of code blocks used more than once
- **Cross-Market Application**: Average code block used on 3+ different datasets
- **Time Saved**: 60% reduction in analysis time for recurring tasks

### Technical Metrics
- Page load time: <2 seconds
- LLM response streaming: <500ms to first token
- Code search: <200ms response time
- File upload: Support up to 50MB CSV files

---

## Risk Assessment

### Technical Risks
1. **LLM API Rate Limits**: Implement queuing and retry logic
2. **Code Extraction Accuracy**: Build robust parsing with fallbacks
3. **Storage Scaling**: Plan S3 migration path early
4. **Security**: Ensure proper API key encryption

### Mitigation Strategies
- Start with single LLM provider (OpenAI)
- Use existing template security features
- Implement comprehensive error handling
- Add monitoring from day one

---

## Appendix: Technology Stack Comparison

| Component | Template Provides | Red Panda Needs | Status |
|-----------|------------------|-----------------|---------|
| Auth | JWT + User Mgmt | API Key Storage | 🔧 Extend |
| Database | PostgreSQL + SQLModel | Custom Models | ❌ Build |
| Frontend | React + Chakra UI | Chat Interface | ❌ Build |
| API | FastAPI + CRUD | LLM Integration | ❌ Build |
| Files | Static Assets | CSV Storage | ❌ Build |
| Search | None | Code Search | ❌ Build |
| Realtime | None | SSE Streaming | ❌ Build |

**Current State**: FastAPI template successfully deployed, ready for Red Panda specific development.
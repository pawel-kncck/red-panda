# Red Panda Frontend Implementation Plan

## Overview
This document provides a comprehensive, step-by-step guide for implementing the Red Panda frontend. The backend is 100% complete with all APIs ready. This plan focuses exclusively on building the React/TypeScript frontend with Chakra UI.

**Estimated Time**: 5-7 days
**Current State**: Template UI with authentication working
**Goal**: Full-featured data analysis tool with chat interface, code library, and file management

---

## Phase 0: Setup & Prerequisites (2-3 hours)

### 0.1 Environment Verification
```bash
# Terminal 1: Start backend
cd backend
fastapi dev app/main.py

# Terminal 2: Start frontend
cd frontend
npm install
npm run dev
```

### 0.2 Regenerate API Client
```bash
cd frontend
npm run generate-client
```
This will update `src/client/` with all new types for:
- Conversation, ConversationCreate, ConversationUpdate
- CodeBlock, CodeBlockCreate, CodeBlockUpdate
- Message, MessageCreate
- File, FileCreate
- ChatRequest, ChatResponse
- Settings endpoints

### 0.3 Install Additional Dependencies
```bash
cd frontend
npm install --save \
  prismjs@^1.29.0 \
  @types/prismjs@^1.26.0 \
  prism-react-renderer@^2.3.0 \
  react-markdown@^9.0.0 \
  remark-gfm@^4.0.0 \
  react-dropzone@^14.2.3 \
  eventsource-parser@^1.1.0 \
  date-fns@^3.0.0 \
  react-intersection-observer@^9.5.0
```

### 0.4 Update App Branding
File: `frontend/index.html`
```html
<title>Red Panda - Reusable Code Interpreter</title>
```

File: `frontend/src/theme.tsx`
```typescript
// Update brand colors
const theme = createSystem(defaultConfig, {
  theme: {
    tokens: {
      colors: {
        brand: {
          50: { value: "#fee8e7" },
          100: { value: "#fcc5c2" },
          200: { value: "#fa9e9a" },
          300: { value: "#f87771" },
          400: { value: "#f65953" },
          500: { value: "#f43c35" },  // Red Panda primary
          600: { value: "#e6332e" },
          700: { value: "#d42925" },
          800: { value: "#c3201d" },
          900: { value: "#a20e0b" },
        }
      }
    }
  }
})
```

---

## Phase 1: Foundation - Types & Services (Day 1 Morning)

### 1.1 Create Type Definitions
File: `frontend/src/types/index.ts`
```typescript
// Re-export generated types with better names
export type {
  Conversation,
  ConversationCreate,
  ConversationUpdate,
  ConversationPublic,
  CodeBlock,
  CodeBlockCreate,
  CodeBlockUpdate,
  CodeBlockPublic,
  Message,
  MessageCreate,
  MessagePublic,
  FilePublic,
  ChatRequest,
  UserSettingsUpdate,
} from '@/client'

export enum MessageRole {
  USER = 'user',
  ASSISTANT = 'assistant',
  SYSTEM = 'system'
}

export enum LLMProvider {
  OPENAI = 'openai',
  ANTHROPIC = 'anthropic'
}

export interface StreamingChatResponse {
  id: string
  type: 'content' | 'code_block' | 'error' | 'done'
  content?: string
  code_block?: CodeBlock
  error?: string
}
```

### 1.2 Create API Service Layer
File: `frontend/src/services/api.ts`
```typescript
import { client } from '@/client'
import type { 
  Conversation, 
  ConversationCreate,
  CodeBlock,
  Message,
  ChatRequest 
} from '@/types'

export const conversationService = {
  list: (skip = 0, limit = 20) => 
    client.GET('/api/conversations', { 
      params: { query: { skip, limit } } 
    }),
  
  get: (id: string) => 
    client.GET('/api/conversations/{conversation_id}', { 
      params: { path: { conversation_id: id } } 
    }),
  
  create: (data: ConversationCreate) => 
    client.POST('/api/conversations', { body: data }),
  
  update: (id: string, data: Partial<Conversation>) => 
    client.PATCH('/api/conversations/{conversation_id}', { 
      params: { path: { conversation_id: id } },
      body: data 
    }),
  
  delete: (id: string) => 
    client.DELETE('/api/conversations/{conversation_id}', { 
      params: { path: { conversation_id: id } } 
    })
}

export const messageService = {
  list: (conversationId: string) => 
    client.GET('/api/conversations/{conversation_id}/messages', {
      params: { path: { conversation_id: conversationId } }
    })
}

export const codeBlockService = {
  list: (skip = 0, limit = 20, search?: string, tags?: string[]) => 
    client.GET('/api/code-blocks', { 
      params: { 
        query: { skip, limit, search, tags: tags?.join(',') } 
      } 
    }),
  
  get: (id: string) => 
    client.GET('/api/code-blocks/{code_block_id}', { 
      params: { path: { code_block_id: id } } 
    }),
  
  update: (id: string, data: Partial<CodeBlock>) => 
    client.PATCH('/api/code-blocks/{code_block_id}', { 
      params: { path: { code_block_id: id } },
      body: data 
    })
}

export const fileService = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return client.POST('/api/files/upload', { 
      body: formData as any 
    })
  },
  
  list: () => client.GET('/api/files'),
  
  delete: (id: string) => 
    client.DELETE('/api/files/{file_id}', { 
      params: { path: { file_id: id } } 
    })
}
```

### 1.3 Create Chat Streaming Service
File: `frontend/src/services/chat.ts`
```typescript
import { EventSourceParserStream } from 'eventsource-parser/stream'
import type { ChatRequest, StreamingChatResponse } from '@/types'

export class ChatService {
  private abortController?: AbortController

  async streamChat(
    request: ChatRequest,
    onMessage: (response: StreamingChatResponse) => void,
    onError: (error: Error) => void,
    onComplete: () => void
  ) {
    this.abortController = new AbortController()
    
    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(request),
        signal: this.abortController.signal
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body!
        .pipeThrough(new TextDecoderStream())
        .pipeThrough(new EventSourceParserStream())
        .getReader()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        if (value.data === '[DONE]') {
          onComplete()
          break
        }

        try {
          const parsed = JSON.parse(value.data) as StreamingChatResponse
          onMessage(parsed)
        } catch (e) {
          console.error('Failed to parse SSE message:', e)
        }
      }
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        onError(error)
      }
    }
  }

  abort() {
    this.abortController?.abort()
  }
}

export const chatService = new ChatService()
```

---

## Phase 2: Conversation Management (Day 1 Afternoon - Day 2 Morning)

### 2.1 Create Conversation Hooks
File: `frontend/src/hooks/useConversations.ts`
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { conversationService } from '@/services/api'
import type { ConversationCreate } from '@/types'

export const useConversations = () => {
  return useQuery({
    queryKey: ['conversations'],
    queryFn: async () => {
      const response = await conversationService.list(0, 100)
      return response.data
    }
  })
}

export const useConversation = (id: string | undefined) => {
  return useQuery({
    queryKey: ['conversation', id],
    queryFn: async () => {
      if (!id) return null
      const response = await conversationService.get(id)
      return response.data
    },
    enabled: !!id
  })
}

export const useCreateConversation = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: ConversationCreate) => 
      conversationService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] })
    }
  })
}

export const useUpdateConversation = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: Partial<Conversation> }) => 
      conversationService.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['conversation', variables.id] })
      queryClient.invalidateQueries({ queryKey: ['conversations'] })
    }
  })
}

export const useDeleteConversation = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => conversationService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['conversations'] })
    }
  })
}
```

### 2.2 Replace Sidebar with Conversations
File: `frontend/src/components/Common/ConversationSidebar.tsx`
```typescript
import { Box, Button, Flex, Text, IconButton, Spinner } from "@chakra-ui/react"
import { Link as RouterLink, useParams, useNavigate } from "@tanstack/react-router"
import { FiPlus, FiMessageSquare, FiTrash2, FiEdit2 } from "react-icons/fi"
import { format } from 'date-fns'
import { useConversations, useCreateConversation, useDeleteConversation } from '@/hooks/useConversations'

interface ConversationSidebarProps {
  onClose?: () => void
}

export const ConversationSidebar = ({ onClose }: ConversationSidebarProps) => {
  const navigate = useNavigate()
  const params = useParams({ from: '/_layout/chat/$conversationId' })
  const { data: conversations, isLoading } = useConversations()
  const createMutation = useCreateConversation()
  const deleteMutation = useDeleteConversation()

  const handleNewChat = async () => {
    const result = await createMutation.mutateAsync({
      title: "New Conversation"
    })
    if (result.data?.id) {
      navigate({ to: '/chat/$conversationId', params: { conversationId: result.data.id } })
      onClose?.()
    }
  }

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (confirm('Delete this conversation?')) {
      await deleteMutation.mutateAsync(id)
      if (params.conversationId === id) {
        navigate({ to: '/chat' })
      }
    }
  }

  return (
    <Box h="full" display="flex" flexDirection="column">
      <Box p={4}>
        <Button 
          leftIcon={<FiPlus />} 
          colorScheme="brand" 
          width="full"
          onClick={handleNewChat}
          isLoading={createMutation.isPending}
        >
          New Chat
        </Button>
      </Box>

      <Box flex="1" overflowY="auto" px={2}>
        <Text fontSize="xs" px={2} py={2} fontWeight="bold" color="gray.500">
          Conversations
        </Text>
        
        {isLoading ? (
          <Flex justify="center" py={4}>
            <Spinner size="sm" />
          </Flex>
        ) : (
          <Box>
            {conversations?.items?.map((conv) => (
              <RouterLink 
                key={conv.id} 
                to="/chat/$conversationId" 
                params={{ conversationId: conv.id }}
                onClick={onClose}
              >
                <Flex
                  px={3}
                  py={2}
                  mb={1}
                  borderRadius="md"
                  bg={params.conversationId === conv.id ? "gray.100" : undefined}
                  _hover={{ bg: "gray.50" }}
                  _dark={{
                    bg: params.conversationId === conv.id ? "gray.700" : undefined,
                    _hover: { bg: "gray.700" }
                  }}
                  align="center"
                  gap={2}
                >
                  <Icon as={FiMessageSquare} />
                  <Box flex="1" minW="0">
                    <Text fontSize="sm" isTruncated>{conv.title}</Text>
                    <Text fontSize="xs" color="gray.500">
                      {format(new Date(conv.updated_at), 'MMM d, h:mm a')}
                    </Text>
                  </Box>
                  <IconButton
                    aria-label="Delete conversation"
                    icon={<FiTrash2 />}
                    size="xs"
                    variant="ghost"
                    onClick={(e) => handleDelete(conv.id, e)}
                  />
                </Flex>
              </RouterLink>
            ))}
          </Box>
        )}
      </Box>

      <Box p={4} borderTop="1px" borderColor="gray.200" _dark={{ borderColor: "gray.700" }}>
        <RouterLink to="/library" onClick={onClose}>
          <Button variant="ghost" width="full" justifyContent="start">
            📚 Code Library
          </Button>
        </RouterLink>
        <RouterLink to="/files" onClick={onClose}>
          <Button variant="ghost" width="full" justifyContent="start">
            📁 Files
          </Button>
        </RouterLink>
        <RouterLink to="/settings" onClick={onClose}>
          <Button variant="ghost" width="full" justifyContent="start">
            ⚙️ Settings
          </Button>
        </RouterLink>
      </Box>
    </Box>
  )
}
```

### 2.3 Update Sidebar Component
File: `frontend/src/components/Common/Sidebar.tsx`
Replace the existing SidebarItems import and usage with:
```typescript
import { ConversationSidebar } from "./ConversationSidebar"

// In the component, replace <SidebarItems /> with:
<ConversationSidebar onClose={onClose} />
```

---

## Phase 3: Chat Interface (Day 2-3)

### 3.1 Create Message Components
File: `frontend/src/components/Chat/MessageItem.tsx`
```typescript
import { Box, Flex, Text, IconButton, useToast } from "@chakra-ui/react"
import { FiCopy, FiSave } from "react-icons/fi"
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { CodeBlock } from './CodeBlock'
import type { Message, MessageRole } from '@/types'

interface MessageItemProps {
  message: Message
  onSaveCode?: (code: string, description: string) => void
}

export const MessageItem = ({ message, onSaveCode }: MessageItemProps) => {
  const toast = useToast()
  const isUser = message.role === MessageRole.USER

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toast({
      title: "Copied to clipboard",
      status: "success",
      duration: 2000,
    })
  }

  return (
    <Flex 
      gap={3} 
      p={4}
      bg={isUser ? "blue.50" : "gray.50"}
      _dark={{
        bg: isUser ? "blue.900" : "gray.800"
      }}
    >
      <Box 
        w={8} 
        h={8} 
        borderRadius="full" 
        bg={isUser ? "blue.500" : "brand.500"}
        color="white"
        display="flex"
        alignItems="center"
        justifyContent="center"
        fontSize="sm"
        fontWeight="bold"
        flexShrink={0}
      >
        {isUser ? "U" : "AI"}
      </Box>

      <Box flex="1">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || '')
              const language = match ? match[1] : 'text'
              const codeString = String(children).replace(/\n$/, '')
              
              if (!inline && match) {
                return (
                  <CodeBlock
                    code={codeString}
                    language={language}
                    onCopy={() => copyToClipboard(codeString)}
                    onSave={onSaveCode ? () => onSaveCode(codeString, '') : undefined}
                  />
                )
              }
              
              return (
                <Text as="code" bg="gray.100" _dark={{ bg: "gray.700" }} px={1} borderRadius="sm" {...props}>
                  {children}
                </Text>
              )
            }
          }}
        >
          {message.content}
        </ReactMarkdown>

        {message.code_block_ids && message.code_block_ids.length > 0 && (
          <Text fontSize="xs" color="gray.500" mt={2}>
            {message.code_block_ids.length} code block(s) saved
          </Text>
        )}
      </Box>
    </Flex>
  )
}
```

### 3.2 Create Code Block Component
File: `frontend/src/components/Chat/CodeBlock.tsx`
```typescript
import { Box, Button, Flex, Text } from "@chakra-ui/react"
import { Highlight, themes } from 'prism-react-renderer'
import Prism from 'prismjs'

// Import additional languages
import 'prismjs/components/prism-python'
import 'prismjs/components/prism-javascript'
import 'prismjs/components/prism-typescript'
import 'prismjs/components/prism-jsx'
import 'prismjs/components/prism-tsx'
import 'prismjs/components/prism-sql'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-json'

interface CodeBlockProps {
  code: string
  language: string
  onCopy?: () => void
  onSave?: () => void
}

export const CodeBlock = ({ code, language, onCopy, onSave }: CodeBlockProps) => {
  return (
    <Box my={2} borderRadius="md" overflow="hidden" border="1px" borderColor="gray.200">
      <Flex 
        bg="gray.100" 
        _dark={{ bg: "gray.800" }}
        px={3} 
        py={1} 
        justify="space-between" 
        align="center"
      >
        <Text fontSize="xs" fontWeight="medium">{language}</Text>
        <Flex gap={2}>
          {onCopy && (
            <Button size="xs" variant="ghost" onClick={onCopy}>
              Copy
            </Button>
          )}
          {onSave && (
            <Button size="xs" variant="ghost" onClick={onSave}>
              Save to Library
            </Button>
          )}
        </Flex>
      </Flex>
      
      <Highlight
        theme={themes.github}
        code={code.trim()}
        language={language as any}
      >
        {({ className, style, tokens, getLineProps, getTokenProps }) => (
          <Box
            as="pre"
            className={className}
            style={style}
            p={3}
            overflowX="auto"
            fontSize="sm"
          >
            {tokens.map((line, i) => (
              <div key={i} {...getLineProps({ line })}>
                {line.map((token, key) => (
                  <span key={key} {...getTokenProps({ token })} />
                ))}
              </div>
            ))}
          </Box>
        )}
      </Highlight>
    </Box>
  )
}
```

### 3.3 Create Message Input
File: `frontend/src/components/Chat/MessageInput.tsx`
```typescript
import { useState, useRef } from 'react'
import { Box, Button, Flex, IconButton, Textarea, Text } from "@chakra-ui/react"
import { FiSend, FiPaperclip, FiX } from "react-icons/fi"

interface MessageInputProps {
  onSend: (message: string, fileId?: string) => void
  isLoading?: boolean
  selectedFile?: { id: string; name: string }
  onFileSelect?: () => void
  onFileRemove?: () => void
}

export const MessageInput = ({ 
  onSend, 
  isLoading, 
  selectedFile,
  onFileSelect,
  onFileRemove 
}: MessageInputProps) => {
  const [message, setMessage] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = () => {
    if (message.trim() && !isLoading) {
      onSend(message.trim(), selectedFile?.id)
      setMessage('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <Box p={4} borderTop="1px" borderColor="gray.200" _dark={{ borderColor: "gray.700" }}>
      {selectedFile && (
        <Flex 
          mb={2} 
          p={2} 
          bg="blue.50" 
          _dark={{ bg: "blue.900" }}
          borderRadius="md"
          align="center"
          justify="space-between"
        >
          <Text fontSize="sm">📎 {selectedFile.name}</Text>
          <IconButton
            aria-label="Remove file"
            icon={<FiX />}
            size="xs"
            variant="ghost"
            onClick={onFileRemove}
          />
        </Flex>
      )}
      
      <Flex gap={2}>
        <IconButton
          aria-label="Attach file"
          icon={<FiPaperclip />}
          onClick={onFileSelect}
          isDisabled={isLoading}
        />
        
        <Textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          rows={1}
          resize="none"
          flex="1"
          isDisabled={isLoading}
        />
        
        <IconButton
          aria-label="Send message"
          icon={<FiSend />}
          colorScheme="brand"
          onClick={handleSubmit}
          isDisabled={!message.trim() || isLoading}
          isLoading={isLoading}
        />
      </Flex>
    </Box>
  )
}
```

### 3.4 Create Main Chat Interface
File: `frontend/src/components/Chat/ChatInterface.tsx`
```typescript
import { useState, useEffect, useRef } from 'react'
import { Box, Flex, Spinner, Text, useToast } from "@chakra-ui/react"
import { MessageItem } from './MessageItem'
import { MessageInput } from './MessageInput'
import { useMessages } from '@/hooks/useMessages'
import { useUpdateConversation } from '@/hooks/useConversations'
import { chatService } from '@/services/chat'
import { codeBlockService } from '@/services/api'
import type { Message, MessageRole, LLMProvider } from '@/types'

interface ChatInterfaceProps {
  conversationId: string
  provider?: LLMProvider
  model?: string
}

export const ChatInterface = ({ 
  conversationId, 
  provider = LLMProvider.OPENAI,
  model = "gpt-4"
}: ChatInterfaceProps) => {
  const toast = useToast()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamingMessage, setStreamingMessage] = useState<string>('')
  const { data: messages, isLoading, refetch } = useMessages(conversationId)
  const updateConversation = useUpdateConversation()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingMessage])

  const handleSendMessage = async (content: string, fileId?: string) => {
    setIsStreaming(true)
    setStreamingMessage('')

    const isFirstMessage = !messages || messages.length === 0

    chatService.streamChat(
      {
        conversation_id: conversationId,
        message: content,
        provider,
        model,
        file_id: fileId
      },
      (response) => {
        if (response.type === 'content') {
          setStreamingMessage(prev => prev + (response.content || ''))
        } else if (response.type === 'code_block' && response.code_block) {
          toast({
            title: "Code block saved",
            description: `${response.code_block.language} code saved to library`,
            status: "success",
            duration: 3000,
          })
        }
      },
      (error) => {
        toast({
          title: "Error",
          description: error.message,
          status: "error",
          duration: 5000,
        })
        setIsStreaming(false)
      },
      () => {
        setIsStreaming(false)
        setStreamingMessage('')
        refetch()
        
        // Auto-generate title from first message
        if (isFirstMessage) {
          const title = content.slice(0, 50) + (content.length > 50 ? '...' : '')
          updateConversation.mutate({ 
            id: conversationId, 
            data: { title } 
          })
        }
      }
    )
  }

  const handleSaveCode = async (code: string, description: string) => {
    try {
      await codeBlockService.create({
        conversation_id: conversationId,
        code,
        description: description || "Code from chat",
        language: "python"
      })
      toast({
        title: "Code saved to library",
        status: "success",
        duration: 3000,
      })
    } catch (error) {
      toast({
        title: "Failed to save code",
        status: "error",
        duration: 5000,
      })
    }
  }

  if (isLoading) {
    return (
      <Flex h="full" align="center" justify="center">
        <Spinner size="lg" />
      </Flex>
    )
  }

  return (
    <Flex direction="column" h="full">
      <Box flex="1" overflowY="auto" pb={4}>
        {messages?.length === 0 && !streamingMessage && (
          <Flex align="center" justify="center" h="full" p={8}>
            <Box textAlign="center">
              <Text fontSize="2xl" fontWeight="bold" mb={2}>
                Start a new conversation
              </Text>
              <Text color="gray.500">
                Ask questions about your data or request analysis
              </Text>
            </Box>
          </Flex>
        )}

        {messages?.map((message) => (
          <MessageItem 
            key={message.id} 
            message={message}
            onSaveCode={handleSaveCode}
          />
        ))}

        {streamingMessage && (
          <MessageItem 
            message={{
              id: 'streaming',
              content: streamingMessage,
              role: MessageRole.ASSISTANT,
              conversation_id: conversationId,
              created_at: new Date().toISOString()
            } as Message}
            onSaveCode={handleSaveCode}
          />
        )}

        <div ref={messagesEndRef} />
      </Box>

      <MessageInput 
        onSend={handleSendMessage}
        isLoading={isStreaming}
      />
    </Flex>
  )
}
```

### 3.5 Create Chat Route
File: `frontend/src/routes/_layout/chat.tsx`
```typescript
import { createFileRoute, redirect } from '@tanstack/react-router'
import { Box } from '@chakra-ui/react'
import { ChatInterface } from '@/components/Chat/ChatInterface'

export const Route = createFileRoute('/_layout/chat')({
  beforeLoad: async ({ context }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({ to: '/login' })
    }
  },
  component: ChatIndex,
})

function ChatIndex() {
  return (
    <Box h="full" display="flex" alignItems="center" justifyContent="center">
      <Box textAlign="center" color="gray.500">
        Select a conversation or create a new one to start chatting
      </Box>
    </Box>
  )
}
```

File: `frontend/src/routes/_layout/chat/$conversationId.tsx`
```typescript
import { createFileRoute } from '@tanstack/react-router'
import { Box } from '@chakra-ui/react'
import { ChatInterface } from '@/components/Chat/ChatInterface'

export const Route = createFileRoute('/_layout/chat/$conversationId')({
  component: ChatConversation,
})

function ChatConversation() {
  const { conversationId } = Route.useParams()
  
  return (
    <Box h="full">
      <ChatInterface conversationId={conversationId} />
    </Box>
  )
}
```

---

## Phase 4: Code Library (Day 3-4)

### 4.1 Create Code Library Hooks
File: `frontend/src/hooks/useCodeBlocks.ts`
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { codeBlockService } from '@/services/api'
import type { CodeBlockUpdate } from '@/types'

export const useCodeBlocks = (search?: string, tags?: string[]) => {
  return useQuery({
    queryKey: ['codeBlocks', search, tags],
    queryFn: async () => {
      const response = await codeBlockService.list(0, 100, search, tags)
      return response.data
    }
  })
}

export const useCodeBlock = (id: string | undefined) => {
  return useQuery({
    queryKey: ['codeBlock', id],
    queryFn: async () => {
      if (!id) return null
      const response = await codeBlockService.get(id)
      return response.data
    },
    enabled: !!id
  })
}

export const useUpdateCodeBlock = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string, data: CodeBlockUpdate }) => 
      codeBlockService.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['codeBlock', variables.id] })
      queryClient.invalidateQueries({ queryKey: ['codeBlocks'] })
    }
  })
}
```

### 4.2 Create Code Card Component
File: `frontend/src/components/CodeLibrary/CodeCard.tsx`
```typescript
import { Box, Badge, Button, Flex, Text, IconButton, useToast } from "@chakra-ui/react"
import { FiCopy, FiEdit2, FiCode } from "react-icons/fi"
import { format } from 'date-fns'
import type { CodeBlock } from '@/types'

interface CodeCardProps {
  codeBlock: CodeBlock
  onEdit: (id: string) => void
  onUseInChat: (code: string) => void
}

export const CodeCard = ({ codeBlock, onEdit, onUseInChat }: CodeCardProps) => {
  const toast = useToast()

  const copyToClipboard = () => {
    navigator.clipboard.writeText(codeBlock.code)
    toast({
      title: "Copied to clipboard",
      status: "success",
      duration: 2000,
    })
  }

  const truncatedCode = codeBlock.code.split('\n').slice(0, 5).join('\n')

  return (
    <Box
      p={4}
      borderWidth="1px"
      borderRadius="md"
      _hover={{ shadow: "md" }}
      transition="all 0.2s"
    >
      <Flex justify="space-between" align="start" mb={2}>
        <Box flex="1">
          <Text fontWeight="bold" fontSize="sm" noOfLines={1}>
            {codeBlock.description || "Untitled Code"}
          </Text>
          <Text fontSize="xs" color="gray.500">
            {format(new Date(codeBlock.created_at), 'MMM d, yyyy')}
          </Text>
        </Box>
        <Badge colorScheme="blue" fontSize="xs">
          {codeBlock.language}
        </Badge>
      </Flex>

      <Box 
        bg="gray.50" 
        _dark={{ bg: "gray.800" }}
        p={2} 
        borderRadius="sm" 
        mb={3}
        fontFamily="mono"
        fontSize="xs"
        overflowX="auto"
      >
        <Text as="pre" whiteSpace="pre-wrap">
          {truncatedCode}
          {codeBlock.code.split('\n').length > 5 && '\n...'}
        </Text>
      </Box>

      {codeBlock.tags && codeBlock.tags.length > 0 && (
        <Flex gap={1} mb={3} flexWrap="wrap">
          {codeBlock.tags.map((tag) => (
            <Badge key={tag} size="sm" variant="subtle">
              {tag}
            </Badge>
          ))}
        </Flex>
      )}

      <Flex gap={2}>
        <Button size="sm" leftIcon={<FiCopy />} onClick={copyToClipboard}>
          Copy
        </Button>
        <Button size="sm" leftIcon={<FiCode />} onClick={() => onUseInChat(codeBlock.code)}>
          Use in Chat
        </Button>
        <IconButton
          aria-label="Edit"
          icon={<FiEdit2 />}
          size="sm"
          variant="ghost"
          onClick={() => onEdit(codeBlock.id)}
        />
      </Flex>
    </Box>
  )
}
```

### 4.3 Create Code Library Page
File: `frontend/src/components/CodeLibrary/CodeLibraryPage.tsx`
```typescript
import { useState } from 'react'
import { 
  Box, 
  Button, 
  Flex, 
  Grid, 
  Input, 
  InputGroup, 
  InputLeftElement, 
  Text,
  Spinner,
  Tag,
  TagLabel,
  TagCloseButton,
  Wrap
} from "@chakra-ui/react"
import { FiSearch, FiFilter } from "react-icons/fi"
import { useNavigate } from '@tanstack/react-router'
import { useCodeBlocks } from '@/hooks/useCodeBlocks'
import { CodeCard } from './CodeCard'
import { CodeEditModal } from './CodeEditModal'

export const CodeLibraryPage = () => {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [editingId, setEditingId] = useState<string | null>(null)
  const { data: codeBlocks, isLoading } = useCodeBlocks(search, selectedTags)

  const allTags = Array.from(
    new Set(
      codeBlocks?.items?.flatMap(cb => cb.tags || []) || []
    )
  )

  const handleUseInChat = (code: string) => {
    // Navigate to chat with code in context
    // This would need to be implemented with proper state management
    navigate({ to: '/chat' })
  }

  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    )
  }

  return (
    <Box p={6}>
      <Flex justify="space-between" align="center" mb={6}>
        <Box>
          <Text fontSize="2xl" fontWeight="bold">Code Library</Text>
          <Text color="gray.500">
            {codeBlocks?.total || 0} code blocks saved
          </Text>
        </Box>
      </Flex>

      <Box mb={6}>
        <InputGroup mb={4}>
          <InputLeftElement pointerEvents="none">
            <FiSearch />
          </InputLeftElement>
          <Input
            placeholder="Search code blocks..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </InputGroup>

        {allTags.length > 0 && (
          <Box>
            <Text fontSize="sm" fontWeight="medium" mb={2}>
              Filter by tags:
            </Text>
            <Wrap>
              {allTags.map(tag => (
                <Tag
                  key={tag}
                  size="md"
                  variant={selectedTags.includes(tag) ? "solid" : "outline"}
                  colorScheme="blue"
                  cursor="pointer"
                  onClick={() => toggleTag(tag)}
                >
                  <TagLabel>{tag}</TagLabel>
                </Tag>
              ))}
            </Wrap>
          </Box>
        )}
      </Box>

      {isLoading ? (
        <Flex justify="center" py={8}>
          <Spinner size="lg" />
        </Flex>
      ) : codeBlocks?.items?.length === 0 ? (
        <Box textAlign="center" py={8}>
          <Text color="gray.500">No code blocks found</Text>
        </Box>
      ) : (
        <Grid
          templateColumns="repeat(auto-fill, minmax(350px, 1fr))"
          gap={4}
        >
          {codeBlocks?.items?.map((codeBlock) => (
            <CodeCard
              key={codeBlock.id}
              codeBlock={codeBlock}
              onEdit={setEditingId}
              onUseInChat={handleUseInChat}
            />
          ))}
        </Grid>
      )}

      {editingId && (
        <CodeEditModal
          codeBlockId={editingId}
          onClose={() => setEditingId(null)}
        />
      )}
    </Box>
  )
}
```

### 4.4 Create Library Route
File: `frontend/src/routes/_layout/library.tsx`
```typescript
import { createFileRoute } from '@tanstack/react-router'
import { CodeLibraryPage } from '@/components/CodeLibrary/CodeLibraryPage'

export const Route = createFileRoute('/_layout/library')({
  component: CodeLibrary,
})

function CodeLibrary() {
  return <CodeLibraryPage />
}
```

---

## Phase 5: Settings & File Management (Day 4-5)

### 5.1 Update Settings for API Keys
File: `frontend/src/components/Settings/APIKeySettings.tsx`
```typescript
import { useState } from 'react'
import { 
  Box, 
  Button, 
  FormControl, 
  FormLabel, 
  Input, 
  Select,
  VStack,
  Text,
  Alert,
  AlertIcon,
  InputGroup,
  InputRightElement,
  IconButton,
  useToast
} from "@chakra-ui/react"
import { FiEye, FiEyeOff } from "react-icons/fi"
import { client } from '@/client'
import type { LLMProvider } from '@/types'

export const APIKeySettings = () => {
  const toast = useToast()
  const [provider, setProvider] = useState<LLMProvider>(LLMProvider.OPENAI)
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [isValidating, setIsValidating] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  const handleValidate = async () => {
    setIsValidating(true)
    try {
      const response = await client.POST('/api/settings/validate-api-key', {
        body: { provider, api_key: apiKey }
      })
      
      if (response.data?.valid) {
        toast({
          title: "API key is valid",
          status: "success",
          duration: 3000,
        })
      } else {
        toast({
          title: "Invalid API key",
          status: "error",
          duration: 5000,
        })
      }
    } catch (error) {
      toast({
        title: "Validation failed",
        status: "error",
        duration: 5000,
      })
    } finally {
      setIsValidating(false)
    }
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      await client.PUT('/api/settings/api-keys', {
        body: {
          provider,
          api_key: apiKey
        }
      })
      
      toast({
        title: "API key saved",
        description: "Your API key has been securely stored",
        status: "success",
        duration: 3000,
      })
      
      setApiKey('')
    } catch (error) {
      toast({
        title: "Failed to save API key",
        status: "error",
        duration: 5000,
      })
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <Box>
      <Text fontSize="lg" fontWeight="bold" mb={4}>
        API Key Management
      </Text>

      <Alert status="info" mb={4}>
        <AlertIcon />
        Your API keys are encrypted and stored securely. They are never shared or logged.
      </Alert>

      <VStack spacing={4} align="stretch">
        <FormControl>
          <FormLabel>Provider</FormLabel>
          <Select 
            value={provider} 
            onChange={(e) => setProvider(e.target.value as LLMProvider)}
          >
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
          </Select>
        </FormControl>

        <FormControl>
          <FormLabel>API Key</FormLabel>
          <InputGroup>
            <Input
              type={showKey ? "text" : "password"}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder={`Enter your ${provider === 'openai' ? 'OpenAI' : 'Anthropic'} API key`}
            />
            <InputRightElement>
              <IconButton
                aria-label={showKey ? "Hide" : "Show"}
                icon={showKey ? <FiEyeOff /> : <FiEye />}
                size="sm"
                variant="ghost"
                onClick={() => setShowKey(!showKey)}
              />
            </InputRightElement>
          </InputGroup>
        </FormControl>

        <Flex gap={2}>
          <Button
            onClick={handleValidate}
            isLoading={isValidating}
            isDisabled={!apiKey}
          >
            Validate Key
          </Button>
          <Button
            colorScheme="brand"
            onClick={handleSave}
            isLoading={isSaving}
            isDisabled={!apiKey}
          >
            Save Key
          </Button>
        </Flex>
      </VStack>
    </Box>
  )
}
```

### 5.2 Create File Upload Component
File: `frontend/src/components/Files/FileUploader.tsx`
```typescript
import { useCallback } from 'react'
import { Box, Text, VStack, Icon, useToast } from "@chakra-ui/react"
import { useDropzone } from 'react-dropzone'
import { FiUploadCloud } from "react-icons/fi"
import { fileService } from '@/services/api'

interface FileUploaderProps {
  onUploadComplete: () => void
}

export const FileUploader = ({ onUploadComplete }: FileUploaderProps) => {
  const toast = useToast()

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      try {
        await fileService.upload(file)
        toast({
          title: "File uploaded",
          description: `${file.name} uploaded successfully`,
          status: "success",
          duration: 3000,
        })
      } catch (error) {
        toast({
          title: "Upload failed",
          description: `Failed to upload ${file.name}`,
          status: "error",
          duration: 5000,
        })
      }
    }
    onUploadComplete()
  }, [onUploadComplete, toast])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    }
  })

  return (
    <Box
      {...getRootProps()}
      p={8}
      border="2px dashed"
      borderColor={isDragActive ? "brand.500" : "gray.300"}
      borderRadius="lg"
      cursor="pointer"
      transition="all 0.2s"
      _hover={{ borderColor: "brand.400" }}
    >
      <input {...getInputProps()} />
      <VStack spacing={3}>
        <Icon as={FiUploadCloud} boxSize={12} color="gray.400" />
        <Text fontWeight="medium">
          {isDragActive ? "Drop files here" : "Drag & drop files here"}
        </Text>
        <Text fontSize="sm" color="gray.500">
          or click to browse (CSV, XLS, XLSX)
        </Text>
      </VStack>
    </Box>
  )
}
```

### 5.3 Create Files Page
File: `frontend/src/routes/_layout/files.tsx`
```typescript
import { createFileRoute } from '@tanstack/react-router'
import { FilesPage } from '@/components/Files/FilesPage'

export const Route = createFileRoute('/_layout/files')({
  component: Files,
})

function Files() {
  return <FilesPage />
}
```

---

## Testing Checklist

### Component Testing
- [ ] Conversation sidebar creates/deletes conversations
- [ ] Chat interface sends/receives messages
- [ ] Code blocks are extracted and displayed
- [ ] Code library search and filters work
- [ ] File upload accepts CSV files
- [ ] API key validation works

### E2E Testing Scenarios
1. **New User Flow**
   - Register → Add API key → Create conversation → Send message → View code

2. **Code Reuse Flow**
   - Send message with code → Save to library → Search in library → Use in new chat

3. **File Analysis Flow**
   - Upload CSV → Create conversation → Reference file → Get analysis with code

### Manual Testing
- [ ] Dark mode consistency
- [ ] Mobile responsive layout
- [ ] Loading states present
- [ ] Error handling works
- [ ] Keyboard shortcuts (Enter to send)

---

## Common Issues & Solutions

### Issue: API client types not found
**Solution**: Run `npm run generate-client` after backend is running

### Issue: SSE streaming not working
**Solution**: Ensure backend CORS allows streaming responses

### Issue: Code highlighting not working
**Solution**: Import specific Prism language components

### Issue: File uploads failing
**Solution**: Check backend file size limits and storage permissions

---

## Deployment Checklist

### Pre-deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] API endpoints verified
- [ ] Build successful (`npm run build`)

### Production Config
- [ ] Update API base URL
- [ ] Enable production error tracking
- [ ] Configure CDN for assets
- [ ] Set up monitoring

---

## Success Metrics

### Functional
- ✅ Users can chat with LLM
- ✅ Code blocks automatically extracted
- ✅ Code library searchable
- ✅ Files uploadable
- ✅ API keys managed securely

### Performance
- Page load < 2s
- Chat response < 1s
- Search results < 500ms
- Smooth scrolling in chat

---

## Next Steps After Implementation

1. **Enhance Code Parser**: Add support for more languages
2. **Add Code Execution**: Sandbox for running Python code
3. **Implement Visualizations**: Charts and graphs from data
4. **Add Export Features**: Jupyter notebook export
5. **Team Features**: Sharing and collaboration

---

This plan provides everything needed to implement the Red Panda frontend systematically and successfully!
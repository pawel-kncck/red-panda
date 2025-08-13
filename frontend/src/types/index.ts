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
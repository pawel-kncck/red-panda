// Re-export generated types with better names
export type {
  ConversationCreate,
  ConversationUpdate,
  ConversationPublic,
  CodeBlockCreate,
  CodeBlockUpdate,
  CodeBlockPublic,
  MessageCreate,
  MessagePublic,
  FilePublic,
  ChatRequest,
} from "@/client"

// Type aliases for simpler names
export type Conversation = ConversationPublic
export type CodeBlock = CodeBlockPublic
export type Message = MessagePublic

export enum MessageRole {
  USER = "user",
  ASSISTANT = "assistant",
  SYSTEM = "system",
}

export enum LLMProvider {
  OPENAI = "openai",
  ANTHROPIC = "anthropic",
}

export interface StreamingChatResponse {
  id: string
  type: "content" | "code_block" | "error" | "done"
  content?: string
  code_block?: CodeBlock
  error?: string
}

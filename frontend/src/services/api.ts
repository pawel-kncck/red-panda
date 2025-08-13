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
    }),
  
  create: (data: any) => 
    client.POST('/api/code-blocks', { body: data })
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
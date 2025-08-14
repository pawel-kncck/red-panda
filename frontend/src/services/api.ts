import { client } from "@/client"
import type {
  CodeBlock,
  Conversation,
  ConversationCreate,
} from "@/types"

export const conversationService = {
  list: (skip = 0, limit = 20) =>
    client.GET("/api/v1/conversations/", {
      params: { query: { skip, limit } },
    }),

  get: (id: string) =>
    client.GET(`/api/v1/conversations/${id}`, {}),

  create: (data: ConversationCreate) =>
    client.POST("/api/v1/conversations/", { body: data }),

  update: (id: string, data: Partial<Conversation>) =>
    client.PATCH(`/api/v1/conversations/${id}`, { body: data }),

  delete: (id: string) =>
    client.DELETE(`/api/v1/conversations/${id}`, {}),
}

export const messageService = {
  list: (conversationId: string) =>
    client.GET(`/api/v1/conversations/${conversationId}/messages/`, {}),
}

export const codeBlockService = {
  list: (skip = 0, limit = 20, search?: string, tags?: string[]) =>
    client.GET("/api/v1/code-blocks/", {
      params: {
        query: { skip, limit, search, tags: tags?.join(",") },
      },
    }),

  get: (id: string) =>
    client.GET(`/api/v1/code-blocks/${id}`, {}),

  update: (id: string, data: Partial<CodeBlock>) =>
    client.PATCH(`/api/v1/code-blocks/${id}`, { body: data }),

  create: (data: any) => client.POST("/api/v1/code-blocks/", { body: data }),
}

export const fileService = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append("file", file)
    return client.POST("/api/v1/files/upload", {
      body: formData as any,
    })
  },

  list: () => client.GET("/api/v1/files/", {}),

  delete: (id: string) =>
    client.DELETE(`/api/v1/files/${id}`, {}),
}

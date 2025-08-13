import { conversationService } from "@/services/api"
import type { Conversation, ConversationCreate } from "@/types"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

export const useConversations = () => {
  return useQuery({
    queryKey: ["conversations"],
    queryFn: async () => {
      const response = await conversationService.list(0, 100)
      return response.data
    },
  })
}

export const useConversation = (id: string | undefined) => {
  return useQuery({
    queryKey: ["conversation", id],
    queryFn: async () => {
      if (!id) return null
      const response = await conversationService.get(id)
      return response.data
    },
    enabled: !!id,
  })
}

export const useCreateConversation = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ConversationCreate) => conversationService.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] })
    },
  })
}

export const useUpdateConversation = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Conversation> }) =>
      conversationService.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["conversation", variables.id],
      })
      queryClient.invalidateQueries({ queryKey: ["conversations"] })
    },
  })
}

export const useDeleteConversation = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => conversationService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] })
    },
  })
}

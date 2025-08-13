import { useQuery } from '@tanstack/react-query'
import { messageService } from '@/services/api'

export const useMessages = (conversationId: string) => {
  return useQuery({
    queryKey: ['messages', conversationId],
    queryFn: async () => {
      const response = await messageService.list(conversationId)
      return response.data?.items || []
    },
    enabled: !!conversationId
  })
}
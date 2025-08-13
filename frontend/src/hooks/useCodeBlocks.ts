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
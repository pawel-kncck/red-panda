import { useState } from 'react'
import { 
  Box, 
  Flex, 
  Text, 
  Table, 
  Thead, 
  Tbody, 
  Tr, 
  Th, 
  Td, 
  IconButton,
  Spinner,
  useToast
} from "@chakra-ui/react"
import { FiTrash2, FiDownload } from "react-icons/fi"
import { format } from 'date-fns'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { fileService } from '@/services/api'
import { FileUploader } from './FileUploader'

export const FilesPage = () => {
  const toast = useToast()
  const queryClient = useQueryClient()
  
  const { data: files, isLoading, refetch } = useQuery({
    queryKey: ['files'],
    queryFn: async () => {
      const response = await fileService.list()
      return response.data?.items || []
    }
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => fileService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['files'] })
      toast({
        title: "File deleted",
        status: "success",
        duration: 3000,
      })
    },
    onError: () => {
      toast({
        title: "Failed to delete file",
        status: "error",
        duration: 5000,
      })
    }
  })

  const handleDelete = (id: string, name: string) => {
    if (confirm(`Delete ${name}?`)) {
      deleteMutation.mutate(id)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <Box p={6}>
      <Flex justify="space-between" align="center" mb={6}>
        <Box>
          <Text fontSize="2xl" fontWeight="bold">Files</Text>
          <Text color="gray.500">
            {files?.length || 0} files uploaded
          </Text>
        </Box>
      </Flex>

      <FileUploader onUploadComplete={() => refetch()} />

      <Box mt={8}>
        <Text fontSize="lg" fontWeight="bold" mb={4}>
          Uploaded Files
        </Text>

        {isLoading ? (
          <Flex justify="center" py={8}>
            <Spinner size="lg" />
          </Flex>
        ) : files?.length === 0 ? (
          <Box textAlign="center" py={8} bg="gray.50" borderRadius="md">
            <Text color="gray.500">No files uploaded yet</Text>
          </Box>
        ) : (
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Name</Th>
                <Th>Size</Th>
                <Th>Type</Th>
                <Th>Uploaded</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            <Tbody>
              {files?.map((file: any) => (
                <Tr key={file.id}>
                  <Td>{file.filename}</Td>
                  <Td>{formatFileSize(file.size)}</Td>
                  <Td>{file.content_type}</Td>
                  <Td>{format(new Date(file.created_at), 'MMM d, yyyy')}</Td>
                  <Td>
                    <Flex gap={2}>
                      <IconButton
                        aria-label="Delete file"
                        icon={<FiTrash2 />}
                        size="sm"
                        variant="ghost"
                        colorScheme="red"
                        onClick={() => handleDelete(file.id, file.filename)}
                        isLoading={deleteMutation.isPending}
                      />
                    </Flex>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        )}
      </Box>
    </Box>
  )
}
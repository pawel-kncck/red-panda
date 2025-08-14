import { fileService } from "@/services/api"
import {
  Box,
  Flex,
  IconButton,
  Spinner,
  Table,
  Text,
} from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { format } from "date-fns"
import { FiTrash2 } from "react-icons/fi"
import { toaster } from "@/components/ui/toaster"
import { FileUploader } from "./FileUploader"

export const FilesPage = () => {
  const queryClient = useQueryClient()

  const {
    data: files,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ["files"],
    queryFn: async () => {
      const response = await fileService.list()
      return (response as any).data?.items || []
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => fileService.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["files"] })
      toaster.create({
        title: "File deleted",
        type: "success",
        duration: 3000,
      })
    },
    onError: () => {
      toaster.create({
        title: "Failed to delete file",
        type: "error",
        duration: 5000,
      })
    },
  })

  const handleDelete = (id: string, name: string) => {
    if (confirm(`Delete ${name}?`)) {
      deleteMutation.mutate(id)
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <Box p={6}>
      <Flex justify="space-between" align="center" mb={6}>
        <Box>
          <Text fontSize="2xl" fontWeight="bold">
            Files
          </Text>
          <Text color="gray.500">{files?.length || 0} files uploaded</Text>
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
          <Table.Root>
            <Table.Header>
              <Table.Row>
                <Table.ColumnHeader>Name</Table.ColumnHeader>
                <Table.ColumnHeader>Size</Table.ColumnHeader>
                <Table.ColumnHeader>Type</Table.ColumnHeader>
                <Table.ColumnHeader>Uploaded</Table.ColumnHeader>
                <Table.ColumnHeader>Actions</Table.ColumnHeader>
              </Table.Row>
            </Table.Header>
            <Table.Body>
              {files?.map((file: any) => (
                <Table.Row key={file.id}>
                  <Table.Cell>{file.filename}</Table.Cell>
                  <Table.Cell>{formatFileSize(file.size)}</Table.Cell>
                  <Table.Cell>{file.content_type}</Table.Cell>
                  <Table.Cell>{format(new Date(file.created_at), "MMM d, yyyy")}</Table.Cell>
                  <Table.Cell>
                    <Flex gap={2}>
                      <IconButton
                        aria-label="Delete file"
                        size="sm"
                        variant="ghost"
                        colorScheme="red"
                        onClick={() => handleDelete(file.id, file.filename)}
                        loading={deleteMutation.isPending}
                      >
                        <FiTrash2 />
                      </IconButton>
                    </Flex>
                  </Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table.Root>
        )}
      </Box>
    </Box>
  )
}

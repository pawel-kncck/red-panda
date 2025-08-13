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
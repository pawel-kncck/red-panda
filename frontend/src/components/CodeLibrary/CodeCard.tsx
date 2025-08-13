import { Box, Badge, Button, Flex, Text, IconButton, useToast } from "@chakra-ui/react"
import { FiCopy, FiEdit2, FiCode } from "react-icons/fi"
import { format } from 'date-fns'
import type { CodeBlock } from '@/types'

interface CodeCardProps {
  codeBlock: CodeBlock
  onEdit: (id: string) => void
  onUseInChat: (code: string) => void
}

export const CodeCard = ({ codeBlock, onEdit, onUseInChat }: CodeCardProps) => {
  const toast = useToast()

  const copyToClipboard = () => {
    navigator.clipboard.writeText(codeBlock.code)
    toast({
      title: "Copied to clipboard",
      status: "success",
      duration: 2000,
    })
  }

  const truncatedCode = codeBlock.code.split('\n').slice(0, 5).join('\n')

  return (
    <Box
      p={4}
      borderWidth="1px"
      borderRadius="md"
      _hover={{ shadow: "md" }}
      transition="all 0.2s"
    >
      <Flex justify="space-between" align="start" mb={2}>
        <Box flex="1">
          <Text fontWeight="bold" fontSize="sm" noOfLines={1}>
            {codeBlock.description || "Untitled Code"}
          </Text>
          <Text fontSize="xs" color="gray.500">
            {format(new Date(codeBlock.created_at), 'MMM d, yyyy')}
          </Text>
        </Box>
        <Badge colorScheme="blue" fontSize="xs">
          {codeBlock.language}
        </Badge>
      </Flex>

      <Box 
        bg="gray.50" 
        _dark={{ bg: "gray.800" }}
        p={2} 
        borderRadius="sm" 
        mb={3}
        fontFamily="mono"
        fontSize="xs"
        overflowX="auto"
      >
        <Text as="pre" whiteSpace="pre-wrap">
          {truncatedCode}
          {codeBlock.code.split('\n').length > 5 && '\n...'}
        </Text>
      </Box>

      {codeBlock.tags && codeBlock.tags.length > 0 && (
        <Flex gap={1} mb={3} flexWrap="wrap">
          {codeBlock.tags.map((tag) => (
            <Badge key={tag} size="sm" variant="subtle">
              {tag}
            </Badge>
          ))}
        </Flex>
      )}

      <Flex gap={2}>
        <Button size="sm" leftIcon={<FiCopy />} onClick={copyToClipboard}>
          Copy
        </Button>
        <Button size="sm" leftIcon={<FiCode />} onClick={() => onUseInChat(codeBlock.code)}>
          Use in Chat
        </Button>
        <IconButton
          aria-label="Edit"
          icon={<FiEdit2 />}
          size="sm"
          variant="ghost"
          onClick={() => onEdit(codeBlock.id)}
        />
      </Flex>
    </Box>
  )
}
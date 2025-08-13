import { Box, Button, Flex, IconButton, Text, Textarea } from "@chakra-ui/react"
import { useRef, useState } from "react"
import { FiPaperclip, FiSend, FiX } from "react-icons/fi"

interface MessageInputProps {
  onSend: (message: string, fileId?: string) => void
  loading?: boolean
  selectedFile?: { id: string; name: string }
  onFileSelect?: () => void
  onFileRemove?: () => void
}

export const MessageInput = ({
  onSend,
  loading,
  selectedFile,
  onFileSelect,
  onFileRemove,
}: MessageInputProps) => {
  const [message, setMessage] = useState("")
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = () => {
    if (message.trim() && !loading) {
      onSend(message.trim(), selectedFile?.id)
      setMessage("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <Box
      p={4}
      borderTop="1px"
      borderColor="gray.200"
      _dark={{ borderColor: "gray.700" }}
    >
      {selectedFile && (
        <Flex
          mb={2}
          p={2}
          bg="blue.50"
          _dark={{ bg: "blue.900" }}
          borderRadius="md"
          align="center"
          justify="space-between"
        >
          <Text fontSize="sm">📎 {selectedFile.name}</Text>
          <IconButton
            aria-label="Remove file"
            size="xs"
            variant="ghost"
            onClick={onFileRemove}
          >
            <FiX />
          </IconButton>
        </Flex>
      )}

      <Flex gap={2}>
        <IconButton
          aria-label="Attach file"
          onClick={onFileSelect}
          disabled={loading}
        >
          <FiPaperclip />
        </IconButton>

        <Textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          rows={1}
          resize="none"
          flex="1"
          disabled={loading}
        />

        <IconButton
          aria-label="Send message"
          colorScheme="brand"
          onClick={handleSubmit}
          disabled={!message.trim() || loading}
          loading={loading}
        >
          <FiSend />
        </IconButton>
      </Flex>
    </Box>
  )
}

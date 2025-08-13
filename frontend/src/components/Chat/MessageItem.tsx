import type { Message } from "@/types"
import { MessageRole } from "@/types"
import { Box, Flex, Text } from "@chakra-ui/react"
import { toaster } from "@/components/ui/toaster"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { CodeBlock } from "./CodeBlock"

interface MessageItemProps {
  message: Message
  onSaveCode?: (code: string, description: string) => void
}

export const MessageItem = ({ message, onSaveCode }: MessageItemProps) => {
  const isUser = message.role === MessageRole.USER

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    toaster.create({
      title: "Copied to clipboard",
      status: "success",
      duration: 2000,
    })
  }

  return (
    <Flex
      gap={3}
      p={4}
      bg={isUser ? "blue.50" : "gray.50"}
      _dark={{
        bg: isUser ? "blue.900" : "gray.800",
      }}
    >
      <Box
        w={8}
        h={8}
        borderRadius="full"
        bg={isUser ? "blue.500" : "brand.500"}
        color="white"
        display="flex"
        alignItems="center"
        justifyContent="center"
        fontSize="sm"
        fontWeight="bold"
        flexShrink={0}
      >
        {isUser ? "U" : "AI"}
      </Box>

      <Box flex="1">
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          components={{
            code({ inline, className, children }) {
              const match = /language-(\w+)/.exec(className || "")
              const language = match ? match[1] : "text"
              const codeString = String(children).replace(/\n$/, "")

              if (!inline && match) {
                return (
                  <CodeBlock
                    code={codeString}
                    language={language}
                    onCopy={() => copyToClipboard(codeString)}
                    onSave={
                      onSaveCode ? () => onSaveCode(codeString, "") : undefined
                    }
                  />
                )
              }

              return (
                <Text
                  as="code"
                  bg="gray.100"
                  _dark={{ bg: "gray.700" }}
                  px={1}
                  borderRadius="sm"
                >
                  {children}
                </Text>
              )
            },
          }}
        >
          {message.content}
        </ReactMarkdown>

        {message.code_block_ids && message.code_block_ids.length > 0 && (
          <Text fontSize="xs" color="gray.500" mt={2}>
            {message.code_block_ids.length} code block(s) saved
          </Text>
        )}
      </Box>
    </Flex>
  )
}

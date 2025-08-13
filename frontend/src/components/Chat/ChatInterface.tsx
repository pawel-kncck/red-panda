import { useState, useEffect, useRef } from 'react'
import { Box, Flex, Spinner, Text, useToast } from "@chakra-ui/react"
import { MessageItem } from './MessageItem'
import { MessageInput } from './MessageInput'
import { useMessages } from '@/hooks/useMessages'
import { useUpdateConversation } from '@/hooks/useConversations'
import { chatService } from '@/services/chat'
import { codeBlockService } from '@/services/api'
import type { Message, MessageRole, LLMProvider } from '@/types'

interface ChatInterfaceProps {
  conversationId: string
  provider?: LLMProvider
  model?: string
}

export const ChatInterface = ({ 
  conversationId, 
  provider = LLMProvider.OPENAI,
  model = "gpt-4"
}: ChatInterfaceProps) => {
  const toast = useToast()
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [streamingMessage, setStreamingMessage] = useState<string>('')
  const { data: messages, isLoading, refetch } = useMessages(conversationId)
  const updateConversation = useUpdateConversation()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, streamingMessage])

  const handleSendMessage = async (content: string, fileId?: string) => {
    setIsStreaming(true)
    setStreamingMessage('')

    const isFirstMessage = !messages || messages.length === 0

    chatService.streamChat(
      {
        conversation_id: conversationId,
        message: content,
        provider,
        model,
        file_id: fileId
      },
      (response) => {
        if (response.type === 'content') {
          setStreamingMessage(prev => prev + (response.content || ''))
        } else if (response.type === 'code_block' && response.code_block) {
          toast({
            title: "Code block saved",
            description: `${response.code_block.language} code saved to library`,
            status: "success",
            duration: 3000,
          })
        }
      },
      (error) => {
        toast({
          title: "Error",
          description: error.message,
          status: "error",
          duration: 5000,
        })
        setIsStreaming(false)
      },
      () => {
        setIsStreaming(false)
        setStreamingMessage('')
        refetch()
        
        // Auto-generate title from first message
        if (isFirstMessage) {
          const title = content.slice(0, 50) + (content.length > 50 ? '...' : '')
          updateConversation.mutate({ 
            id: conversationId, 
            data: { title } 
          })
        }
      }
    )
  }

  const handleSaveCode = async (code: string, description: string) => {
    try {
      await codeBlockService.create({
        conversation_id: conversationId,
        code,
        description: description || "Code from chat",
        language: "python"
      })
      toast({
        title: "Code saved to library",
        status: "success",
        duration: 3000,
      })
    } catch (error) {
      toast({
        title: "Failed to save code",
        status: "error",
        duration: 5000,
      })
    }
  }

  if (isLoading) {
    return (
      <Flex h="full" align="center" justify="center">
        <Spinner size="lg" />
      </Flex>
    )
  }

  return (
    <Flex direction="column" h="full">
      <Box flex="1" overflowY="auto" pb={4}>
        {messages?.length === 0 && !streamingMessage && (
          <Flex align="center" justify="center" h="full" p={8}>
            <Box textAlign="center">
              <Text fontSize="2xl" fontWeight="bold" mb={2}>
                Start a new conversation
              </Text>
              <Text color="gray.500">
                Ask questions about your data or request analysis
              </Text>
            </Box>
          </Flex>
        )}

        {messages?.map((message) => (
          <MessageItem 
            key={message.id} 
            message={message}
            onSaveCode={handleSaveCode}
          />
        ))}

        {streamingMessage && (
          <MessageItem 
            message={{
              id: 'streaming',
              content: streamingMessage,
              role: MessageRole.ASSISTANT,
              conversation_id: conversationId,
              created_at: new Date().toISOString()
            } as Message}
            onSaveCode={handleSaveCode}
          />
        )}

        <div ref={messagesEndRef} />
      </Box>

      <MessageInput 
        onSend={handleSendMessage}
        isLoading={isStreaming}
      />
    </Flex>
  )
}
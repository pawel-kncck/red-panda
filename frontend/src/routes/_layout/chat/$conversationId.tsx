import { createFileRoute } from '@tanstack/react-router'
import { Box } from '@chakra-ui/react'
import { ChatInterface } from '@/components/Chat/ChatInterface'

export const Route = createFileRoute('/_layout/chat/$conversationId')({
  component: ChatConversation,
})

function ChatConversation() {
  const { conversationId } = Route.useParams()
  
  return (
    <Box h="full">
      <ChatInterface conversationId={conversationId} />
    </Box>
  )
}
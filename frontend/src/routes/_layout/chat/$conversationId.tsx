import { ChatInterface } from "@/components/Chat/ChatInterface"
import { Box } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/chat/$conversationId")({
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

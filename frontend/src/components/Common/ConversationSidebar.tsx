import {
  useConversations,
  useCreateConversation,
  useDeleteConversation,
} from "@/hooks/useConversations"
import {
  Box,
  Button,
  Flex,
  Icon,
  IconButton,
  Spinner,
  Text,
} from "@chakra-ui/react"
import {
  Link as RouterLink,
  useNavigate,
  useParams,
} from "@tanstack/react-router"
import { format } from "date-fns"
import { FiMessageSquare, FiTrash2 } from "react-icons/fi"

interface ConversationSidebarProps {
  onClose?: () => void
}

export const ConversationSidebar = ({ onClose }: ConversationSidebarProps) => {
  const navigate = useNavigate()
  const params = useParams({ from: "/_layout/chat/$conversationId" }) as { conversationId?: string }
  const { data: conversations, isLoading } = useConversations()
  const createMutation = useCreateConversation()
  const deleteMutation = useDeleteConversation()

  const handleNewChat = async () => {
    const result = await createMutation.mutateAsync({
      title: "New Conversation",
    })
    if ((result as any)?.id) {
      navigate({
        to: "/chat/$conversationId",
        params: { conversationId: (result as any).id },
      })
      onClose?.()
    }
  }

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (confirm("Delete this conversation?")) {
      await deleteMutation.mutateAsync(id)
      if (params.conversationId === id) {
        navigate({ to: "/chat" })
      }
    }
  }

  return (
    <Box h="full" display="flex" flexDirection="column">
      <Box p={4}>
        <Button
          colorScheme="brand"
          width="full"
          onClick={handleNewChat}
          loading={createMutation.isPending}
        >
          New Chat
        </Button>
      </Box>

      <Box flex="1" overflowY="auto" px={2}>
        <Text fontSize="xs" px={2} py={2} fontWeight="bold" color="gray.500">
          Conversations
        </Text>

        {isLoading ? (
          <Flex justify="center" py={4}>
            <Spinner size="sm" />
          </Flex>
        ) : (
          <Box>
            {conversations?.items?.map((conv: any) => (
              <RouterLink
                key={conv.id}
                to="/chat/$conversationId"
                params={{ conversationId: conv.id }}
                onClick={onClose}
              >
                <Flex
                  px={3}
                  py={2}
                  mb={1}
                  borderRadius="md"
                  bg={
                    params.conversationId === conv.id ? "gray.100" : undefined
                  }
                  _hover={{ bg: "gray.50" }}
                  _dark={{
                    bg:
                      params.conversationId === conv.id
                        ? "gray.700"
                        : undefined,
                    _hover: { bg: "gray.700" },
                  }}
                  align="center"
                  gap={2}
                >
                  <Icon as={FiMessageSquare} />
                  <Box flex="1" minW="0">
                    <Text fontSize="sm" truncate>
                      {conv.title}
                    </Text>
                    <Text fontSize="xs" color="gray.500">
                      {format(new Date(conv.updated_at), "MMM d, h:mm a")}
                    </Text>
                  </Box>
                  <IconButton
                    aria-label="Delete conversation"
                    size="xs"
                    variant="ghost"
                    onClick={(e) => handleDelete(conv.id, e)}
                  >
                    <FiTrash2 />
                  </IconButton>
                </Flex>
              </RouterLink>
            ))}
          </Box>
        )}
      </Box>

      <Box
        p={4}
        borderTop="1px"
        borderColor="gray.200"
        _dark={{ borderColor: "gray.700" }}
      >
        <RouterLink to="/library" onClick={onClose}>
          <Button variant="ghost" width="full" justifyContent="start">
            📚 Code Library
          </Button>
        </RouterLink>
        <RouterLink to="/files" onClick={onClose}>
          <Button variant="ghost" width="full" justifyContent="start">
            📁 Files
          </Button>
        </RouterLink>
        <RouterLink to="/settings" onClick={onClose}>
          <Button variant="ghost" width="full" justifyContent="start">
            ⚙️ Settings
          </Button>
        </RouterLink>
      </Box>
    </Box>
  )
}

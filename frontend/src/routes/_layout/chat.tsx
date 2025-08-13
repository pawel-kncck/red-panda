import { createFileRoute, redirect } from '@tanstack/react-router'
import { Box } from '@chakra-ui/react'

export const Route = createFileRoute('/_layout/chat')({
  beforeLoad: async ({ context }) => {
    if (!context.auth.isAuthenticated) {
      throw redirect({ to: '/login' })
    }
  },
  component: ChatIndex,
})

function ChatIndex() {
  return (
    <Box h="full" display="flex" alignItems="center" justifyContent="center">
      <Box textAlign="center" color="gray.500">
        Select a conversation or create a new one to start chatting
      </Box>
    </Box>
  )
}
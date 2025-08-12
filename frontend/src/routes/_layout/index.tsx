import { Box, Container, Text } from "@chakra-ui/react"
import { createFileRoute } from "@tanstack/react-router"

import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  return (
    <>
      <Container maxW="full">
        <Box pt={12} m={4}>
          <Text fontSize="2xl" truncate maxW="sm">
            Hi, {currentUser?.full_name || currentUser?.email} 👋🏼
          </Text>
          <Text>Welcome to Red Panda - Your Code Reusability Platform!</Text>
          <Box mt={8}>
            <Text fontSize="lg" fontWeight="semibold" mb={2}>
              🚀 Getting Started
            </Text>
            <Text color="gray.600">
              Red Panda helps you store, organize, and reuse code from your data analysis conversations.
              Start a new conversation with an LLM, and all generated code will be automatically saved for future use.
            </Text>
          </Box>
        </Box>
      </Container>
    </>
  )
}

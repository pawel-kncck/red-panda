import { useState } from 'react'
import { 
  Box, 
  Button, 
  Flex, 
  Grid, 
  Input, 
  InputGroup, 
  InputLeftElement, 
  Text,
  Spinner,
  Tag,
  TagLabel,
  TagCloseButton,
  Wrap
} from "@chakra-ui/react"
import { FiSearch, FiFilter } from "react-icons/fi"
import { useNavigate } from '@tanstack/react-router'
import { useCodeBlocks } from '@/hooks/useCodeBlocks'
import { CodeCard } from './CodeCard'
import { CodeEditModal } from './CodeEditModal'

export const CodeLibraryPage = () => {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [editingId, setEditingId] = useState<string | null>(null)
  const { data: codeBlocks, isLoading } = useCodeBlocks(search, selectedTags)

  const allTags = Array.from(
    new Set(
      codeBlocks?.items?.flatMap(cb => cb.tags || []) || []
    )
  )

  const handleUseInChat = (code: string) => {
    // Navigate to chat with code in context
    // This would need to be implemented with proper state management
    navigate({ to: '/chat' })
  }

  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag)
        : [...prev, tag]
    )
  }

  return (
    <Box p={6}>
      <Flex justify="space-between" align="center" mb={6}>
        <Box>
          <Text fontSize="2xl" fontWeight="bold">Code Library</Text>
          <Text color="gray.500">
            {codeBlocks?.total || 0} code blocks saved
          </Text>
        </Box>
      </Flex>

      <Box mb={6}>
        <InputGroup mb={4}>
          <InputLeftElement pointerEvents="none">
            <FiSearch />
          </InputLeftElement>
          <Input
            placeholder="Search code blocks..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </InputGroup>

        {allTags.length > 0 && (
          <Box>
            <Text fontSize="sm" fontWeight="medium" mb={2}>
              Filter by tags:
            </Text>
            <Wrap>
              {allTags.map(tag => (
                <Tag
                  key={tag}
                  size="md"
                  variant={selectedTags.includes(tag) ? "solid" : "outline"}
                  colorScheme="blue"
                  cursor="pointer"
                  onClick={() => toggleTag(tag)}
                >
                  <TagLabel>{tag}</TagLabel>
                </Tag>
              ))}
            </Wrap>
          </Box>
        )}
      </Box>

      {isLoading ? (
        <Flex justify="center" py={8}>
          <Spinner size="lg" />
        </Flex>
      ) : codeBlocks?.items?.length === 0 ? (
        <Box textAlign="center" py={8}>
          <Text color="gray.500">No code blocks found</Text>
        </Box>
      ) : (
        <Grid
          templateColumns="repeat(auto-fill, minmax(350px, 1fr))"
          gap={4}
        >
          {codeBlocks?.items?.map((codeBlock) => (
            <CodeCard
              key={codeBlock.id}
              codeBlock={codeBlock}
              onEdit={setEditingId}
              onUseInChat={handleUseInChat}
            />
          ))}
        </Grid>
      )}

      {editingId && (
        <CodeEditModal
          codeBlockId={editingId}
          onClose={() => setEditingId(null)}
        />
      )}
    </Box>
  )
}
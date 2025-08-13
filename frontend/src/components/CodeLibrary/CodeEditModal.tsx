import { useState, useEffect } from 'react'
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalCloseButton,
  Button,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  useToast,
  VStack,
  Tag,
  TagLabel,
  TagCloseButton,
  Wrap,
  HStack
} from "@chakra-ui/react"
import { useCodeBlock, useUpdateCodeBlock } from '@/hooks/useCodeBlocks'

interface CodeEditModalProps {
  codeBlockId: string
  onClose: () => void
}

export const CodeEditModal = ({ codeBlockId, onClose }: CodeEditModalProps) => {
  const { data: codeBlock } = useCodeBlock(codeBlockId)
  const updateMutation = useUpdateCodeBlock()
  const toast = useToast()
  
  const [description, setDescription] = useState('')
  const [tags, setTags] = useState<string[]>([])
  const [newTag, setNewTag] = useState('')
  const [code, setCode] = useState('')

  useEffect(() => {
    if (codeBlock) {
      setDescription(codeBlock.description || '')
      setTags(codeBlock.tags || [])
      setCode(codeBlock.code)
    }
  }, [codeBlock])

  const handleAddTag = () => {
    if (newTag && !tags.includes(newTag)) {
      setTags([...tags, newTag])
      setNewTag('')
    }
  }

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(tag => tag !== tagToRemove))
  }

  const handleSave = async () => {
    try {
      await updateMutation.mutateAsync({
        id: codeBlockId,
        data: {
          description,
          tags,
          code
        }
      })
      toast({
        title: "Code block updated",
        status: "success",
        duration: 3000,
      })
      onClose()
    } catch (error) {
      toast({
        title: "Failed to update code block",
        status: "error",
        duration: 5000,
      })
    }
  }

  return (
    <Modal isOpen onClose={onClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Edit Code Block</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <VStack spacing={4}>
            <FormControl>
              <FormLabel>Description</FormLabel>
              <Input
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief description of this code"
              />
            </FormControl>

            <FormControl>
              <FormLabel>Tags</FormLabel>
              <Wrap mb={2}>
                {tags.map(tag => (
                  <Tag key={tag} size="md" colorScheme="blue">
                    <TagLabel>{tag}</TagLabel>
                    <TagCloseButton onClick={() => handleRemoveTag(tag)} />
                  </Tag>
                ))}
              </Wrap>
              <HStack>
                <Input
                  value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  placeholder="Add a tag"
                  onKeyPress={(e) => e.key === 'Enter' && handleAddTag()}
                />
                <Button onClick={handleAddTag}>Add</Button>
              </HStack>
            </FormControl>

            <FormControl>
              <FormLabel>Code</FormLabel>
              <Textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                fontFamily="mono"
                fontSize="sm"
                rows={15}
              />
            </FormControl>
          </VStack>
        </ModalBody>
        <ModalFooter>
          <Button variant="ghost" mr={3} onClick={onClose}>
            Cancel
          </Button>
          <Button 
            colorScheme="brand" 
            onClick={handleSave}
            isLoading={updateMutation.isPending}
          >
            Save Changes
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  )
}
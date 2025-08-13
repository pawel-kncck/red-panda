import { useState } from 'react'
import { 
  Box, 
  Button, 
  FormControl, 
  FormLabel, 
  Input, 
  Select,
  VStack,
  Text,
  Alert,
  AlertIcon,
  InputGroup,
  InputRightElement,
  IconButton,
  useToast,
  Flex
} from "@chakra-ui/react"
import { FiEye, FiEyeOff } from "react-icons/fi"
import { client } from '@/client'
import type { LLMProvider } from '@/types'

export const APIKeySettings = () => {
  const toast = useToast()
  const [provider, setProvider] = useState<LLMProvider>(LLMProvider.OPENAI)
  const [apiKey, setApiKey] = useState('')
  const [showKey, setShowKey] = useState(false)
  const [isValidating, setIsValidating] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  const handleValidate = async () => {
    setIsValidating(true)
    try {
      const response = await client.POST('/api/settings/validate-api-key', {
        body: { provider, api_key: apiKey }
      })
      
      if (response.data?.valid) {
        toast({
          title: "API key is valid",
          status: "success",
          duration: 3000,
        })
      } else {
        toast({
          title: "Invalid API key",
          status: "error",
          duration: 5000,
        })
      }
    } catch (error) {
      toast({
        title: "Validation failed",
        status: "error",
        duration: 5000,
      })
    } finally {
      setIsValidating(false)
    }
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      await client.PUT('/api/settings/api-keys', {
        body: {
          provider,
          api_key: apiKey
        }
      })
      
      toast({
        title: "API key saved",
        description: "Your API key has been securely stored",
        status: "success",
        duration: 3000,
      })
      
      setApiKey('')
    } catch (error) {
      toast({
        title: "Failed to save API key",
        status: "error",
        duration: 5000,
      })
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <Box>
      <Text fontSize="lg" fontWeight="bold" mb={4}>
        API Key Management
      </Text>

      <Alert status="info" mb={4}>
        <AlertIcon />
        Your API keys are encrypted and stored securely. They are never shared or logged.
      </Alert>

      <VStack spacing={4} align="stretch">
        <FormControl>
          <FormLabel>Provider</FormLabel>
          <Select 
            value={provider} 
            onChange={(e) => setProvider(e.target.value as LLMProvider)}
          >
            <option value="openai">OpenAI</option>
            <option value="anthropic">Anthropic</option>
          </Select>
        </FormControl>

        <FormControl>
          <FormLabel>API Key</FormLabel>
          <InputGroup>
            <Input
              type={showKey ? "text" : "password"}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder={`Enter your ${provider === 'openai' ? 'OpenAI' : 'Anthropic'} API key`}
            />
            <InputRightElement>
              <IconButton
                aria-label={showKey ? "Hide" : "Show"}
                icon={showKey ? <FiEyeOff /> : <FiEye />}
                size="sm"
                variant="ghost"
                onClick={() => setShowKey(!showKey)}
              />
            </InputRightElement>
          </InputGroup>
        </FormControl>

        <Flex gap={2}>
          <Button
            onClick={handleValidate}
            isLoading={isValidating}
            isDisabled={!apiKey}
          >
            Validate Key
          </Button>
          <Button
            colorScheme="brand"
            onClick={handleSave}
            isLoading={isSaving}
            isDisabled={!apiKey}
          >
            Save Key
          </Button>
        </Flex>
      </VStack>
    </Box>
  )
}
import { client } from "@/client"
import type { LLMProvider } from "@/types"
import { LLMProvider as LLMProviderEnum } from "@/types"
import {
  Alert,
  Box,
  Button,
  Flex,
  IconButton,
  Input,
  NativeSelectField,
  NativeSelectRoot,
  Stack,
  Text,
} from "@chakra-ui/react"
import { toaster } from "@/components/ui/toaster"
import { Field } from "@/components/ui/field"
import { InputGroup } from "@/components/ui/input-group"
import { useState } from "react"
import { FiEye, FiEyeOff } from "react-icons/fi"

export const APIKeySettings = () => {
  const [provider, setProvider] = useState<LLMProvider>(LLMProviderEnum.OPENAI)
  const [apiKey, setApiKey] = useState("")
  const [showKey, setShowKey] = useState(false)
  const [isValidating, setIsValidating] = useState(false)
  const [isSaving, setIsSaving] = useState(false)

  const handleValidate = async () => {
    setIsValidating(true)
    try {
      const response = await client.POST("/api/settings/validate-api-key", {
        body: { provider, api_key: apiKey },
      })

      if ((response as any).data?.valid) {
        toaster.create({
          title: "API key is valid",
          type: "success",
          duration: 3000,
        })
      } else {
        toaster.create({
          title: "Invalid API key",
          type: "error",
          duration: 5000,
        })
      }
    } catch (error) {
      toaster.create({
        title: "Validation failed",
        type: "error",
        duration: 5000,
      })
    } finally {
      setIsValidating(false)
    }
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      await client.POST("/api/settings/api-keys", {
        body: {
          provider,
          api_key: apiKey,
        },
      })

      toaster.create({
        title: "API key saved",
        description: "Your API key has been securely stored",
        type: "success",
        duration: 3000,
      })

      setApiKey("")
    } catch (error) {
      toaster.create({
        title: "Failed to save API key",
        type: "error",
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

      <Alert.Root status="info" mb={4}>
        <Alert.Indicator />
        <Alert.Content>
          Your API keys are encrypted and stored securely. They are never shared
          or logged.
        </Alert.Content>
      </Alert.Root>

      <Stack gap={4}>
        <Field label="Provider">
          <NativeSelectRoot>
            <NativeSelectField
              value={provider}
              onChange={(e) => setProvider(e.target.value as LLMProvider)}
            >
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
            </NativeSelectField>
          </NativeSelectRoot>
        </Field>

        <Field label="API Key">
          <InputGroup
            endElement={
              <IconButton
                aria-label={showKey ? "Hide" : "Show"}
                size="sm"
                variant="ghost"
                onClick={() => setShowKey(!showKey)}
              >
                {showKey ? <FiEyeOff /> : <FiEye />}
              </IconButton>
            }
          >
            <Input
              type={showKey ? "text" : "password"}
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder={`Enter your ${provider === "openai" ? "OpenAI" : "Anthropic"} API key`}
            />
          </InputGroup>
        </Field>

        <Flex gap={2}>
          <Button
            onClick={handleValidate}
            loading={isValidating}
            disabled={!apiKey}
          >
            Validate Key
          </Button>
          <Button
            colorScheme="brand"
            onClick={handleSave}
            loading={isSaving}
            disabled={!apiKey}
          >
            Save Key
          </Button>
        </Flex>
      </Stack>
    </Box>
  )
}

import { OpenAPI } from "./core/OpenAPI"
import {
  ChatService,
  CodeBlocksService,
  ConversationsService,
  FilesService,
  LoginService,
  MessagesService,
  SettingsService,
  UsersService,
  UtilsService,
} from "./sdk.gen"

// Configure OpenAPI client
const token = localStorage.getItem("access_token")
if (token) {
  OpenAPI.TOKEN = token
}
OpenAPI.BASE = import.meta.env.VITE_API_URL || ""

// Create a client object that matches the expected API
export const client = {
  // Auth endpoints
  POST: (url: string, options?: any) => {
    if (url === "/api/v1/login/access-token") {
      return LoginService.loginAccessToken({ formData: options.body })
    }
    if (url === "/api/v1/login/test-token") {
      return LoginService.testToken()
    }
    if (url === "/api/v1/users/signup") {
      return UsersService.registerUser({ requestBody: options.body })
    }
    if (url.startsWith("/api/v1/password-recovery/")) {
      const email = url.split("/").pop()!
      return LoginService.recoverPassword({ email })
    }
    if (url === "/api/v1/reset-password/") {
      return LoginService.resetPassword({ requestBody: options.body })
    }
    // Conversations
    if (url === "/api/v1/conversations/") {
      return ConversationsService.createNewConversation({ requestBody: options.body })
    }
    // Messages
    if (url.includes("/messages/")) {
      const parts = url.split("/")
      const conversationId = parts[parts.indexOf("conversations") + 1]
      return MessagesService.createNewMessage({ conversationId, requestBody: options.body })
    }
    // Code blocks
    if (url === "/api/v1/code-blocks/") {
      return CodeBlocksService.createNewCodeBlock({ requestBody: options.body })
    }
    // Files
    if (url === "/api/v1/files/upload") {
      return FilesService.uploadFile({ formData: options.body })
    }
    // Settings
    if (url === "/api/v1/settings/api-keys") {
      return SettingsService.setApiKey({ requestBody: options.body })
    }
    // Users
    if (url === "/api/v1/users/") {
      return UsersService.createUser({ requestBody: options.body })
    }
    // Chat
    if (url === "/api/v1/chat/complete") {
      return ChatService.chatCompletion({ requestBody: options.body })
    }
    if (url === "/api/v1/chat/stream") {
      return ChatService.chatStream({ requestBody: options.body })
    }
    // Utils
    if (url === "/api/v1/utils/test-email/") {
      return UtilsService.testEmail({ requestBody: options.body })
    }
    throw new Error(`Unhandled POST endpoint: ${url}`)
  },

  GET: (url: string, options?: any) => {
    // Users
    if (url === "/api/v1/users/") {
      return UsersService.readUsers(options?.params?.query || {})
    }
    if (url === "/api/v1/users/me") {
      return UsersService.readUserMe()
    }
    if (url.startsWith("/api/v1/users/") && url.split("/").length === 5) {
      const userId = url.split("/").pop()!
      return UsersService.readUserById({ userId })
    }
    // Conversations
    if (url === "/api/v1/conversations/") {
      return ConversationsService.readConversations(
        options?.params?.query || {},
      )
    }
    if (url.match(/^\/api\/v1\/conversations\/[^/]+$/)) {
      const conversationId = url.split("/").pop()!
      return ConversationsService.readConversation({ conversationId })
    }
    // Messages
    if (url.includes("/messages/")) {
      const parts = url.split("/")
      const conversationId = parts[parts.indexOf("conversations") + 1]
      return MessagesService.readMessages({
        conversationId,
        ...options?.params?.query,
      })
    }
    // Code blocks
    if (url === "/api/v1/code-blocks/") {
      return CodeBlocksService.readCodeBlocks(options?.params?.query || {})
    }
    if (url === "/api/v1/code-blocks/search") {
      return CodeBlocksService.searchUserCodeBlocks(
        options?.params?.query || {},
      )
    }
    if (url.match(/^\/api\/v1\/code-blocks\/conversation\//)) {
      const conversationId = url.split("/").pop()!
      return CodeBlocksService.readConversationCodeBlocks({ conversationId })
    }
    if (url.match(/^\/api\/v1\/code-blocks\/[^/]+$/)) {
      const codeBlockId = url.split("/").pop()!
      return CodeBlocksService.readCodeBlock({ codeBlockId })
    }
    // Files
    if (url === "/api/v1/files/") {
      return FilesService.readFiles(options?.params?.query || {})
    }
    if (url.match(/^\/api\/v1\/files\/[^/]+$/)) {
      const fileId = url.split("/").pop()!
      return FilesService.readFile({ fileId })
    }
    if (url.includes("/content")) {
      const parts = url.split("/")
      const fileId = parts[parts.indexOf("files") + 1]
      return FilesService.readFileContent({ fileId, ...options?.params?.query })
    }
    // Settings
    if (url === "/api/v1/settings/api-keys/status") {
      return SettingsService.getApiKeysStatus()
    }
    if (url === "/api/v1/settings/api-usage") {
      return SettingsService.getApiUsage()
    }
    // Utils
    if (url === "/api/v1/utils/health-check/") {
      return UtilsService.healthCheck()
    }
    throw new Error(`Unhandled GET endpoint: ${url}`)
  },

  PATCH: (url: string, options?: any) => {
    // Users
    if (url === "/api/v1/users/me") {
      return UsersService.updateUserMe({ requestBody: options.body })
    }
    if (url === "/api/v1/users/me/password") {
      return UsersService.updatePasswordMe({ requestBody: options.body })
    }
    if (url.startsWith("/api/v1/users/") && url.split("/").length === 5) {
      const userId = url.split("/").pop()!
      return UsersService.updateUser({ userId, requestBody: options.body })
    }
    // Conversations
    if (url.match(/^\/api\/v1\/conversations\/[^/]+$/)) {
      const conversationId = url.split("/").pop()!
      return ConversationsService.updateExistingConversation({
        conversationId,
        requestBody: options.body,
      })
    }
    // Code blocks
    if (url.match(/^\/api\/v1\/code-blocks\/[^/]+$/)) {
      const codeBlockId = url.split("/").pop()!
      return CodeBlocksService.updateExistingCodeBlock({
        codeBlockId,
        requestBody: options.body,
      })
    }
    throw new Error(`Unhandled PATCH endpoint: ${url}`)
  },

  DELETE: (url: string, _options?: any) => {
    // Users
    if (url === "/api/v1/users/me") {
      return UsersService.deleteUserMe()
    }
    if (url.startsWith("/api/v1/users/") && url.split("/").length === 5) {
      const userId = url.split("/").pop()!
      return UsersService.deleteUser({ userId })
    }
    // Conversations
    if (url.match(/^\/api\/v1\/conversations\/[^/]+$/)) {
      const conversationId = url.split("/").pop()!
      return ConversationsService.deleteExistingConversation({ conversationId })
    }
    // Messages
    if (url.includes("/messages/")) {
      const parts = url.split("/")
      const conversationId = parts[parts.indexOf("conversations") + 1]
      const messageId = parts.pop()!
      return MessagesService.deleteExistingMessage({
        conversationId,
        messageId,
      })
    }
    // Code blocks
    if (url.match(/^\/api\/v1\/code-blocks\/[^/]+$/)) {
      const codeBlockId = url.split("/").pop()!
      return CodeBlocksService.deleteExistingCodeBlock({ codeBlockId })
    }
    // Files
    if (url.match(/^\/api\/v1\/files\/[^/]+$/)) {
      const fileId = url.split("/").pop()!
      return FilesService.deleteUploadedFile({ fileId })
    }
    // Settings
    if (url.startsWith("/api/v1/settings/api-keys/")) {
      const provider = url.split("/").pop()! as any
      return SettingsService.deleteApiKey({ provider })
    }
    throw new Error(`Unhandled DELETE endpoint: ${url}`)
  },
}

import { EventSourceParserStream } from 'eventsource-parser/stream'
import type { ChatRequest, StreamingChatResponse } from '@/types'

export class ChatService {
  private abortController?: AbortController

  async streamChat(
    request: ChatRequest,
    onMessage: (response: StreamingChatResponse) => void,
    onError: (error: Error) => void,
    onComplete: () => void
  ) {
    this.abortController = new AbortController()
    
    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify(request),
        signal: this.abortController.signal
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body!
        .pipeThrough(new TextDecoderStream())
        .pipeThrough(new EventSourceParserStream())
        .getReader()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        if (value.data === '[DONE]') {
          onComplete()
          break
        }

        try {
          const parsed = JSON.parse(value.data) as StreamingChatResponse
          onMessage(parsed)
        } catch (e) {
          console.error('Failed to parse SSE message:', e)
        }
      }
    } catch (error: any) {
      if (error.name !== 'AbortError') {
        onError(error)
      }
    }
  }

  abort() {
    this.abortController?.abort()
  }
}

export const chatService = new ChatService()
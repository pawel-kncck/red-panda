import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/chat")({
  component: () => <div>Hello /_layout/chat!</div>,
})

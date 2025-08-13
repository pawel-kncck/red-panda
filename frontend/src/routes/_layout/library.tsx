import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/library")({
  component: () => <div>Hello /_layout/library!</div>,
})

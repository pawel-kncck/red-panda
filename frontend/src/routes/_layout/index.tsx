import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useEffect } from "react"

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
})

function Dashboard() {
  const navigate = useNavigate()

  useEffect(() => {
    // Redirect to chat page on landing
    navigate({ to: "/chat" })
  }, [navigate])

  return null
}

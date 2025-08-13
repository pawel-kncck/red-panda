import { FilesPage } from "@/components/Files/FilesPage"
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/_layout/files")({
  component: Files,
})

function Files() {
  return <FilesPage />
}

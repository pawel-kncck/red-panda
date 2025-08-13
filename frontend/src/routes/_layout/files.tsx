import { createFileRoute } from '@tanstack/react-router'
import { FilesPage } from '@/components/Files/FilesPage'

export const Route = createFileRoute('/_layout/files')({
  component: Files,
})

function Files() {
  return <FilesPage />
}
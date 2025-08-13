import { createFileRoute } from '@tanstack/react-router'
import { CodeLibraryPage } from '@/components/CodeLibrary/CodeLibraryPage'

export const Route = createFileRoute('/_layout/library')({
  component: CodeLibrary,
})

function CodeLibrary() {
  return <CodeLibraryPage />
}
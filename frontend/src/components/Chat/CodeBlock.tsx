import { Box, Button, Flex, Text } from "@chakra-ui/react"
import { Highlight, themes } from "prism-react-renderer"
import Prism from "prismjs"

// Import additional languages
import "prismjs/components/prism-python"
import "prismjs/components/prism-javascript"
import "prismjs/components/prism-typescript"
import "prismjs/components/prism-jsx"
import "prismjs/components/prism-tsx"
import "prismjs/components/prism-sql"
import "prismjs/components/prism-bash"
import "prismjs/components/prism-json"

interface CodeBlockProps {
  code: string
  language: string
  onCopy?: () => void
  onSave?: () => void
}

export const CodeBlock = ({
  code,
  language,
  onCopy,
  onSave,
}: CodeBlockProps) => {
  return (
    <Box
      my={2}
      borderRadius="md"
      overflow="hidden"
      border="1px"
      borderColor="gray.200"
    >
      <Flex
        bg="gray.100"
        _dark={{ bg: "gray.800" }}
        px={3}
        py={1}
        justify="space-between"
        align="center"
      >
        <Text fontSize="xs" fontWeight="medium">
          {language}
        </Text>
        <Flex gap={2}>
          {onCopy && (
            <Button size="xs" variant="ghost" onClick={onCopy}>
              Copy
            </Button>
          )}
          {onSave && (
            <Button size="xs" variant="ghost" onClick={onSave}>
              Save to Library
            </Button>
          )}
        </Flex>
      </Flex>

      <Highlight
        theme={themes.github}
        code={code.trim()}
        language={language as any}
      >
        {({ className, style, tokens, getLineProps, getTokenProps }) => (
          <Box
            as="pre"
            className={className}
            style={style}
            p={3}
            overflowX="auto"
            fontSize="sm"
          >
            {tokens.map((line, i) => (
              <div key={i} {...getLineProps({ line })}>
                {line.map((token, key) => (
                  <span key={key} {...getTokenProps({ token })} />
                ))}
              </div>
            ))}
          </Box>
        )}
      </Highlight>
    </Box>
  )
}

"""Service for parsing and extracting code from LLM responses."""
import re
import ast
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class CodeParser:
    """Parse and extract code blocks from text."""
    
    @staticmethod
    def extract_code_blocks(text: str) -> List[Dict[str, Any]]:
        """Extract all code blocks from text with their metadata."""
        code_blocks = []
        
        # Pattern to match code blocks with optional language
        # Matches ```language\ncode\n``` or ```\ncode\n```
        pattern = r'```(?:(\w+))?\n(.*?)```'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            language = match.group(1) or "python"  # Default to Python
            code = match.group(2).strip()
            
            if code:
                metadata = CodeParser.extract_python_metadata(code) if language == "python" else {}
                
                code_block = {
                    "language": language,
                    "code": code,
                    "metadata": metadata,
                    "description": CodeParser.generate_description(code, language),
                }
                code_blocks.append(code_block)
        
        # Also look for inline code that might be substantial
        # Pattern for code between single backticks that's multi-line or > 50 chars
        inline_pattern = r'`([^`]{50,})`'
        inline_matches = re.finditer(inline_pattern, text)
        
        for match in inline_matches:
            code = match.group(1).strip()
            if '\n' in code or len(code) > 100:
                code_blocks.append({
                    "language": "python",
                    "code": code,
                    "metadata": CodeParser.extract_python_metadata(code),
                    "description": CodeParser.generate_description(code, "python"),
                })
        
        return code_blocks
    
    @staticmethod
    def extract_python_metadata(code: str) -> Dict[str, List[str]]:
        """Extract metadata from Python code."""
        metadata = {
            "imports": [],
            "functions": [],
            "classes": [],
            "variables": [],
        }
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        metadata["imports"].append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        import_str = f"{module}.{alias.name}" if module else alias.name
                        metadata["imports"].append(import_str)
                
                elif isinstance(node, ast.FunctionDef):
                    metadata["functions"].append(node.name)
                
                elif isinstance(node, ast.ClassDef):
                    metadata["classes"].append(node.name)
                
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            metadata["variables"].append(target.id)
        
        except SyntaxError:
            # If code doesn't parse, try to extract what we can with regex
            # Extract imports
            import_pattern = r'^(?:from\s+(\S+)\s+)?import\s+(.+)$'
            for line in code.split('\n'):
                match = re.match(import_pattern, line.strip())
                if match:
                    if match.group(1):  # from X import Y
                        imports = match.group(2).split(',')
                        for imp in imports:
                            metadata["imports"].append(f"{match.group(1)}.{imp.strip()}")
                    else:  # import X
                        imports = match.group(2).split(',')
                        metadata["imports"].extend([imp.strip() for imp in imports])
            
            # Extract function definitions
            func_pattern = r'^def\s+(\w+)\s*\('
            for line in code.split('\n'):
                match = re.match(func_pattern, line.strip())
                if match:
                    metadata["functions"].append(match.group(1))
            
            # Extract class definitions
            class_pattern = r'^class\s+(\w+)'
            for line in code.split('\n'):
                match = re.match(class_pattern, line.strip())
                if match:
                    metadata["classes"].append(match.group(1))
        
        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}")
        
        # Remove duplicates
        for key in metadata:
            metadata[key] = list(set(metadata[key]))
        
        return metadata
    
    @staticmethod
    def generate_description(code: str, language: str) -> str:
        """Generate a description of what the code does."""
        lines = code.split('\n')
        
        # Look for docstrings or comments at the beginning
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line.startswith('"""') or line.startswith("'''"):
                # Extract docstring
                docstring_pattern = r'^["\']+(.*?)["\'"]+$'
                match = re.match(docstring_pattern, line)
                if match:
                    return match.group(1).strip()
            elif line.startswith('#'):
                return line[1:].strip()
        
        # Try to generate description from code structure
        if language == "python":
            metadata = CodeParser.extract_python_metadata(code)
            
            if metadata["functions"]:
                func_list = ", ".join(metadata["functions"][:3])
                return f"Defines functions: {func_list}"
            elif metadata["classes"]:
                class_list = ", ".join(metadata["classes"][:3])
                return f"Defines classes: {class_list}"
            elif metadata["imports"]:
                return f"Imports and uses {', '.join(metadata['imports'][:3])}"
            elif len(lines) == 1:
                return f"Single line: {lines[0][:100]}"
        
        # Default description
        return f"{language.capitalize()} code block with {len(lines)} lines"
    
    @staticmethod
    def extract_tags_from_text(text: str) -> List[str]:
        """Extract potential tags from the surrounding text."""
        tags = []
        
        # Common keywords that might indicate tags
        keywords = [
            "pandas", "numpy", "matplotlib", "seaborn", "sklearn",
            "tensorflow", "pytorch", "data", "analysis", "visualization",
            "machine learning", "deep learning", "api", "database",
            "csv", "json", "file", "processing", "cleaning", "transformation",
        ]
        
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                tags.append(keyword)
        
        # Look for hashtag-style tags
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, text)
        tags.extend(hashtags)
        
        return list(set(tags))[:10]  # Limit to 10 tags
    
    @staticmethod
    def merge_code_blocks(blocks: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Merge multiple code blocks into one if they're related."""
        if not blocks:
            return None
        
        if len(blocks) == 1:
            return blocks[0]
        
        # Only merge if all blocks are the same language
        languages = set(block["language"] for block in blocks)
        if len(languages) > 1:
            return None
        
        merged_code = "\n\n".join(block["code"] for block in blocks)
        merged_metadata = {
            "imports": [],
            "functions": [],
            "classes": [],
            "variables": [],
        }
        
        for block in blocks:
            for key in merged_metadata:
                if key in block.get("metadata", {}):
                    merged_metadata[key].extend(block["metadata"][key])
        
        # Remove duplicates
        for key in merged_metadata:
            merged_metadata[key] = list(set(merged_metadata[key]))
        
        return {
            "language": blocks[0]["language"],
            "code": merged_code,
            "metadata": merged_metadata,
            "description": f"Merged {len(blocks)} code blocks",
        }


# Global instance
code_parser = CodeParser()
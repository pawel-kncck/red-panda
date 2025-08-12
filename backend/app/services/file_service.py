"""Service for handling file uploads and CSV processing."""
import csv
import io
import os
import uuid
from pathlib import Path
from typing import BinaryIO, Optional

import pandas as pd
from fastapi import UploadFile

from app.core.config import settings


class FileService:
    """Service for handling file uploads and processing."""
    
    def __init__(self):
        # Create upload directory if it doesn't exist
        self.upload_dir = Path(settings.UPLOAD_DIR) if hasattr(settings, 'UPLOAD_DIR') else Path("/app/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def get_user_upload_dir(self, user_id: uuid.UUID) -> Path:
        """Get or create user-specific upload directory."""
        user_dir = self.upload_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir
    
    async def save_upload_file(
        self,
        upload_file: UploadFile,
        user_id: uuid.UUID,
    ) -> tuple[str, dict]:
        """Save an uploaded file and return storage path and metadata."""
        # Generate unique filename
        file_id = uuid.uuid4()
        file_extension = Path(upload_file.filename).suffix
        stored_filename = f"{file_id}{file_extension}"
        
        # Get user directory and full path
        user_dir = self.get_user_upload_dir(user_id)
        file_path = user_dir / stored_filename
        
        # Save file
        content = await upload_file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Extract metadata based on file type
        metadata = {"original_filename": upload_file.filename}
        
        if upload_file.content_type == "text/csv" or file_extension.lower() == ".csv":
            metadata.update(self.extract_csv_metadata(file_path))
        
        return str(file_path), metadata
    
    def extract_csv_metadata(self, file_path: Path, preview_rows: int = 5) -> dict:
        """Extract metadata from a CSV file."""
        try:
            # Read CSV with pandas for better handling
            df = pd.read_csv(file_path, nrows=preview_rows + 100)  # Read extra for stats
            
            # Get basic info
            metadata = {
                "columns": df.columns.tolist(),
                "row_count": len(df),
                "column_count": len(df.columns),
                "column_types": {col: str(dtype) for col, dtype in df.dtypes.items()},
                "file_size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2),
            }
            
            # Add preview rows
            if preview_rows > 0:
                preview_df = df.head(preview_rows)
                metadata["preview_rows"] = preview_df.to_dict(orient="records")
            
            # Add basic statistics for numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                metadata["numeric_columns"] = numeric_cols
                metadata["basic_stats"] = {}
                for col in numeric_cols:
                    metadata["basic_stats"][col] = {
                        "mean": float(df[col].mean()) if not df[col].isna().all() else None,
                        "min": float(df[col].min()) if not df[col].isna().all() else None,
                        "max": float(df[col].max()) if not df[col].isna().all() else None,
                    }
            
            # Check for full row count
            with open(file_path, 'r') as f:
                row_count = sum(1 for line in f) - 1  # Subtract header
                metadata["total_row_count"] = row_count
            
            return metadata
            
        except Exception as e:
            return {
                "error": f"Failed to parse CSV: {str(e)}",
                "columns": [],
                "row_count": 0,
            }
    
    def delete_file(self, file_path: str) -> bool:
        """Delete a file from storage."""
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                return True
            return False
        except Exception:
            return False
    
    def get_file_content(self, file_path: str, max_rows: Optional[int] = None) -> Optional[dict]:
        """Read and return file content."""
        try:
            path = Path(file_path)
            if not path.exists():
                return None
            
            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path, nrows=max_rows)
                return {
                    "content": df.to_dict(orient="records"),
                    "columns": df.columns.tolist(),
                    "row_count": len(df),
                }
            else:
                # For non-CSV files, return raw content
                with open(path, 'r') as f:
                    content = f.read()
                return {"content": content, "type": "text"}
                
        except Exception as e:
            return {"error": str(e)}
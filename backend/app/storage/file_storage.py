import os
import uuid
import shutil
from typing import Tuple, Optional
from app.core.config import settings

class FileStorage:
    """Safe local file storage for Knowledge Vault with extension and size validation."""

    def __init__(self, upload_dir: str = None):
        self.upload_dir = upload_dir or settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)

    def save_file(self, filename: str, file_bytes: bytes, mime_type: str) -> Tuple[str, str, int]:
        """
        Saves uploaded file securely with a unique identifier.
        Returns: (relative_file_path, sanitized_filename, file_size)
        """
        ext = os.path.splitext(filename)[1].lower()
        if ext not in settings.ALLOWED_EXTENSIONS:
            raise ValueError(f"File extension '{ext}' is not permitted. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}")

        size = len(file_bytes)
        if size > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValueError(f"File size ({round(size / (1024*1024), 2)}MB) exceeds limit of {settings.MAX_FILE_SIZE_MB}MB")

        unique_id = str(uuid.uuid4())
        safe_name = f"{unique_id}{ext}"
        target_path = os.path.join(self.upload_dir, safe_name)

        with open(target_path, "wb") as f:
            f.write(file_bytes)

        return target_path, filename, size

    def extract_text(self, file_path: str, mime_type: str) -> str:
        """Extract text from PDF, Markdown, or text files for AI indexing."""
        if not os.path.exists(file_path):
            return ""

        ext = os.path.splitext(file_path)[1].lower()
        
        # PDF parsing with PyMuPDF
        if ext == ".pdf":
            try:
                import fitz  # PyMuPDF
                doc = fitz.open(file_path)
                text_parts = []
                for page in doc:
                    text_parts.append(page.get_text())
                return "\n".join(text_parts).strip()
            except Exception as e:
                return f"[PDF parsing notice: PyMuPDF extraction produced limited text: {e}]"

        # Text and Markdown
        if ext in [".txt", ".md", ".json"]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read().strip()
            except Exception:
                return ""

        # Image fallback
        if ext in [".png", ".jpg", ".jpeg", ".webp"]:
            try:
                import pytesseract
                from PIL import Image
                img = Image.open(file_path)
                ocr_text = pytesseract.image_to_string(img)
                return ocr_text.strip() if ocr_text else "[Technical diagram / illustration saved in Knowledge Vault]"
            except Exception:
                return "[Technical diagram / screenshot stored in Knowledge Vault]"

        return ""

    def delete_file(self, file_path: str) -> bool:
        """Safely delete uploaded file from disk."""
        try:
            if file_path and os.path.exists(file_path):
                # Verify file is inside upload directory to prevent arbitrary deletion
                normalized_dir = os.path.abspath(self.upload_dir)
                normalized_path = os.path.abspath(file_path)
                if normalized_path.startswith(normalized_dir):
                    os.remove(normalized_path)
                    return True
        except Exception:
            pass
        return False

file_storage = FileStorage()

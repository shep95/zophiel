import os
import datetime
import json
from typing import Dict, Any, Optional

# Attempt imports for third-party libraries
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import exifread
except ImportError:
    exifread = None

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    Image = None

class ZephonMetadata:
    """
    ZEPHON: The Searcher of Secrets.
    Advanced Metadata Extraction Module for Tier-1 Intelligence.
    """

    def __init__(self):
        self.supported_extensions = ['.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png', '.tiff', '.webp']

    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Main entry point for metadata extraction.
        """
        if not os.path.exists(file_path):
            return {"error": "File not found"}

        _, ext = os.path.splitext(file_path.lower())
        
        base_meta = self._get_filesystem_meta(file_path)
        content_meta = {}

        if ext == '.pdf':
            content_meta = self._extract_pdf(file_path)
        elif ext == '.docx':
            content_meta = self._extract_docx(file_path)
        elif ext in ['.jpg', '.jpeg', '.png', '.tiff', '.webp']:
            content_meta = self._extract_image(file_path)
        else:
            content_meta = {"warning": "Deep extraction not supported for this file type"}

        # Merge results
        return {**base_meta, "deep_metadata": content_meta}

    def _get_filesystem_meta(self, file_path: str) -> Dict[str, Any]:
        stat = os.stat(file_path)
        return {
            "filename": os.path.basename(file_path),
            "size_bytes": stat.st_size,
            "created_at": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed_at": datetime.datetime.fromtimestamp(stat.st_atime).isoformat(),
            "absolute_path": os.path.abspath(file_path)
        }

    def _extract_pdf(self, file_path: str) -> Dict[str, Any]:
        if not PdfReader:
            return {"error": "pypdf library missing"}
        
        try:
            reader = PdfReader(file_path)
            meta = reader.metadata
            if not meta:
                return {}
            
            # Clean keys (remove slash)
            return {k.strip('/'): v for k, v in meta.items()}
        except Exception as e:
            return {"error": str(e)}

    def _extract_docx(self, file_path: str) -> Dict[str, Any]:
        if not Document:
            return {"error": "python-docx library missing"}

        try:
            doc = Document(file_path)
            core_props = doc.core_properties
            return {
                "author": core_props.author,
                "created": core_props.created.isoformat() if core_props.created else None,
                "modified": core_props.modified.isoformat() if core_props.modified else None,
                "last_modified_by": core_props.last_modified_by,
                "revision": core_props.revision,
                "title": core_props.title,
                "subject": core_props.subject,
                "keywords": core_props.keywords,
                "comments": core_props.comments,
                "category": core_props.category
            }
        except Exception as e:
            return {"error": str(e)}

    def _extract_image(self, file_path: str) -> Dict[str, Any]:
        results = {}
        
        # Method 1: PIL
        if Image:
            try:
                img = Image.open(file_path)
                exif_data = img.getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        results[f"PIL_{tag}"] = str(value)
            except Exception as e:
                results["PIL_Error"] = str(e)

        # Method 2: ExifRead (Better for raw GPS)
        if exifread:
            try:
                with open(file_path, 'rb') as f:
                    tags = exifread.process_file(f)
                    for tag, value in tags.items():
                        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                            results[tag] = str(value)
            except Exception as e:
                results["ExifRead_Error"] = str(e)
                
        return results

"""
Font Validator Service
Validates and extracts metadata from uploaded font files using fonttools library
"""
import hashlib
import io
from dataclasses import dataclass, field
from typing import Optional
from fontTools.ttLib import TTFont
from fontTools.ttLib.ttFont import TTLibError


@dataclass
class FontMetadata:
    """Extracted metadata from a font file."""
    # Basic info
    font_name: str = ""
    family_name: str = ""
    subfamily: str = ""  # e.g., "Bold Italic"
    version: str = ""
    
    # Licensing & Attribution
    copyright: str = ""
    license: str = ""
    designer: str = ""
    vendor: str = ""
    
    # Technical
    glyph_count: int = 0
    units_per_em: int = 1000
    supported_scripts: list[str] = field(default_factory=list)
    
    # File info
    file_format: str = ""
    file_hash: str = ""
    file_size_bytes: int = 0
    
    # Validation
    is_valid: bool = True
    validation_errors: list[str] = field(default_factory=list)


class InvalidFontError(Exception):
    """Raised when a font file is invalid or cannot be parsed."""
    pass


class FontValidator:
    """
    Service for validating and extracting metadata from font files.
    
    Supports TTF, OTF, WOFF, and WOFF2 formats.
    Uses fonttools library for parsing and validation.
    """
    
    # Magic bytes for font format detection
    FORMAT_SIGNATURES = {
        b'\x00\x01\x00\x00': 'ttf',  # TrueType
        b'OTTO': 'otf',               # OpenType with CFF
        b'true': 'ttf',               # TrueType (Mac)
        b'typ1': 'ttf',               # Type 1 PostScript
        b'wOFF': 'woff',              # WOFF
        b'wOF2': 'woff2',             # WOFF2
    }
    
    # MIME types for each format
    MIME_TYPES = {
        'ttf': 'font/ttf',
        'otf': 'font/otf',
        'woff': 'font/woff',
        'woff2': 'font/woff2',
    }
    
    # Name table IDs (see https://docs.microsoft.com/en-us/typography/opentype/spec/name)
    NAME_IDS = {
        0: 'copyright',
        1: 'family_name',
        2: 'subfamily',
        3: 'unique_id',
        4: 'full_name',
        5: 'version',
        6: 'postscript_name',
        7: 'trademark',
        8: 'manufacturer',
        9: 'designer',
        10: 'description',
        11: 'vendor_url',
        12: 'designer_url',
        13: 'license',
        14: 'license_url',
    }
    
    # Unicode blocks for script detection
    SCRIPT_RANGES = {
        'latin': [(0x0000, 0x007F), (0x0080, 0x00FF), (0x0100, 0x017F), (0x0180, 0x024F)],
        'cyrillic': [(0x0400, 0x04FF), (0x0500, 0x052F), (0x2DE0, 0x2DFF), (0xA640, 0xA69F)],
        'greek': [(0x0370, 0x03FF), (0x1F00, 0x1FFF)],
        'arabic': [(0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF)],
        'hebrew': [(0x0590, 0x05FF)],
        'devanagari': [(0x0900, 0x097F), (0xA8E0, 0xA8FF)],
        'thai': [(0x0E00, 0x0E7F)],
        'hangul': [(0x1100, 0x11FF), (0x3130, 0x318F), (0xAC00, 0xD7AF)],
        'cjk': [(0x4E00, 0x9FFF), (0x3400, 0x4DBF), (0x20000, 0x2A6DF)],
        'japanese': [(0x3040, 0x309F), (0x30A0, 0x30FF), (0x31F0, 0x31FF)],
        'tamil': [(0x0B80, 0x0BFF)],
        'bengali': [(0x0980, 0x09FF)],
        'telugu': [(0x0C00, 0x0C7F)],
        'kannada': [(0x0C80, 0x0CFF)],
        'malayalam': [(0x0D00, 0x0D7F)],
        'gujarati': [(0x0A80, 0x0AFF)],
        'vietnamese': [(0x1E00, 0x1EFF)],  # Latin Extended Additional
    }
    
    def detect_format(self, file_bytes: bytes) -> str:
        """
        Detect font format from magic bytes.
        
        Args:
            file_bytes: Raw font file bytes
            
        Returns:
            Format string: 'ttf', 'otf', 'woff', or 'woff2'
            
        Raises:
            InvalidFontError: If format cannot be detected
        """
        if len(file_bytes) < 4:
            raise InvalidFontError("File too small to be a valid font")
        
        magic = file_bytes[:4]
        
        for signature, format_name in self.FORMAT_SIGNATURES.items():
            if magic == signature:
                return format_name
        
        raise InvalidFontError(f"Unknown font format. Magic bytes: {magic.hex()}")
    
    def calculate_hash(self, file_bytes: bytes) -> str:
        """
        Calculate SHA-256 hash of font file for deduplication.
        
        Args:
            file_bytes: Raw font file bytes
            
        Returns:
            Hex-encoded SHA-256 hash
        """
        return hashlib.sha256(file_bytes).hexdigest()
    
    def get_mime_type(self, file_format: str) -> str:
        """
        Get MIME type for a font format.
        
        Args:
            file_format: Font format ('ttf', 'otf', 'woff', 'woff2')
            
        Returns:
            MIME type string
        """
        return self.MIME_TYPES.get(file_format, 'application/octet-stream')
    
    def extract_supported_scripts(self, font: TTFont) -> list[str]:
        """
        Analyze Unicode coverage to determine script support.
        
        Args:
            font: Parsed TTFont object
            
        Returns:
            List of supported script names
        """
        supported_scripts = []
        
        try:
            # Get cmap table (character to glyph mapping)
            cmap = font.getBestCmap()
            if not cmap:
                return ['latin']  # Assume basic Latin if no cmap
            
            codepoints = set(cmap.keys())
            
            for script_name, ranges in self.SCRIPT_RANGES.items():
                for start, end in ranges:
                    # Check if any codepoint in this range is supported
                    for cp in range(start, end + 1):
                        if cp in codepoints:
                            supported_scripts.append(script_name)
                            break
                    if script_name in supported_scripts:
                        break
            
            if not supported_scripts:
                supported_scripts = ['latin']  # Default
                
        except Exception:
            supported_scripts = ['latin']  # Default on error
        
        return list(set(supported_scripts))  # Remove duplicates
    
    def extract_name_records(self, font: TTFont) -> dict[str, str]:
        """
        Extract name table records from font.
        
        Args:
            font: Parsed TTFont object
            
        Returns:
            Dictionary of name field values
        """
        records = {}
        
        try:
            name_table = font.get('name')
            if not name_table:
                return records
            
            # Preference order: Windows Unicode, Mac Roman, others
            platforms = [
                (3, 1),  # Windows, Unicode BMP
                (1, 0),  # Mac, Roman
                (0, 3),  # Unicode
            ]
            
            for platform_id, encoding_id in platforms:
                for record in name_table.names:
                    if record.platformID == platform_id and record.platEncID == encoding_id:
                        name_id = record.nameID
                        if name_id in self.NAME_IDS:
                            field_name = self.NAME_IDS[name_id]
                            if field_name not in records:
                                try:
                                    records[field_name] = record.toUnicode()
                                except Exception:
                                    continue
                                    
        except Exception:
            pass
        
        return records
    
    def validate_and_extract(self, file_bytes: bytes) -> FontMetadata:
        """
        Parse font file, validate structure, and extract metadata.
        
        This is the main entry point for font validation.
        
        Args:
            file_bytes: Raw font file bytes
            
        Returns:
            FontMetadata with all extracted information and validation status
            
        Raises:
            InvalidFontError: If file is fundamentally invalid
        """
        metadata = FontMetadata()
        metadata.file_size_bytes = len(file_bytes)
        metadata.file_hash = self.calculate_hash(file_bytes)
        
        # Detect format
        try:
            metadata.file_format = self.detect_format(file_bytes)
        except InvalidFontError as e:
            metadata.is_valid = False
            metadata.validation_errors.append(str(e))
            raise
        
        # Parse font with fonttools
        try:
            font_stream = io.BytesIO(file_bytes)
            font = TTFont(font_stream)
        except TTLibError as e:
            metadata.is_valid = False
            metadata.validation_errors.append(f"Failed to parse font: {str(e)}")
            raise InvalidFontError(f"Failed to parse font: {str(e)}")
        except Exception as e:
            metadata.is_valid = False
            metadata.validation_errors.append(f"Unexpected error parsing font: {str(e)}")
            raise InvalidFontError(f"Unexpected error parsing font: {str(e)}")
        
        try:
            # Extract name records
            name_records = self.extract_name_records(font)
            
            metadata.font_name = name_records.get('full_name', name_records.get('postscript_name', ''))
            metadata.family_name = name_records.get('family_name', '')
            metadata.subfamily = name_records.get('subfamily', '')
            metadata.version = name_records.get('version', '')
            metadata.copyright = name_records.get('copyright', '')
            metadata.license = name_records.get('license', '')
            metadata.designer = name_records.get('designer', '')
            metadata.vendor = name_records.get('manufacturer', '')
            
            # Extract technical details
            if 'head' in font:
                metadata.units_per_em = font['head'].unitsPerEm
            
            # Count glyphs
            if 'glyf' in font:
                metadata.glyph_count = len(font.getGlyphOrder())
            elif 'CFF ' in font:
                metadata.glyph_count = len(font.getGlyphOrder())
            else:
                metadata.glyph_count = 0
            
            # Extract supported scripts
            metadata.supported_scripts = self.extract_supported_scripts(font)
            
            # Validate required elements
            if not metadata.family_name:
                metadata.validation_errors.append("Missing family name in font metadata")
            
            if metadata.glyph_count == 0:
                metadata.validation_errors.append("No glyphs found in font")
            
            if metadata.validation_errors:
                metadata.is_valid = False
            
        except Exception as e:
            metadata.validation_errors.append(f"Error extracting metadata: {str(e)}")
            metadata.is_valid = False
        
        finally:
            try:
                font.close()
            except Exception:
                pass
        
        return metadata
    
    def validate_file(self, file_bytes: bytes) -> tuple[bool, list[str]]:
        """
        Quick validation check without full metadata extraction.
        
        Args:
            file_bytes: Raw font file bytes
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Check minimum size
        if len(file_bytes) < 12:
            errors.append("File too small to be a valid font")
            return False, errors
        
        # Check format
        try:
            self.detect_format(file_bytes)
        except InvalidFontError as e:
            errors.append(str(e))
            return False, errors
        
        # Try to parse
        try:
            font_stream = io.BytesIO(file_bytes)
            font = TTFont(font_stream)
            
            # Check for required tables
            required_tables = ['head', 'name', 'cmap']
            for table in required_tables:
                if table not in font:
                    errors.append(f"Missing required table: {table}")
            
            font.close()
            
        except Exception as e:
            errors.append(f"Failed to parse font: {str(e)}")
            return False, errors
        
        return len(errors) == 0, errors
    
    def is_duplicate(self, file_hash: str, existing_hashes: set[str]) -> bool:
        """
        Check if a font is a duplicate based on hash.
        
        Args:
            file_hash: SHA-256 hash of the font file
            existing_hashes: Set of existing font hashes
            
        Returns:
            True if duplicate, False otherwise
        """
        return file_hash in existing_hashes


# Singleton instance for convenience
font_validator = FontValidator()


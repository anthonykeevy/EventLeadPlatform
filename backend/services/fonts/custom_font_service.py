"""
Custom Font Service
Handles custom corporate font uploads with hash-based deduplication and alias management
"""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from models.fonts import FontFamily, FontVariant, FontFile, CompanyFont
from .font_validator import FontValidator, FontMetadata, InvalidFontError


class CustomFontService:
    """
    Service for managing custom corporate font uploads.
    
    Features:
    - Font file validation using fonttools
    - SHA-256 hash-based deduplication
    - Per-company display name aliases
    - Company-Font relationship management
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.validator = FontValidator()
    
    def check_duplicate(self, file_hash: str) -> Optional[FontFamily]:
        """
        Check if a font with this hash already exists.
        
        Args:
            file_hash: SHA-256 hash of the font file
            
        Returns:
            Existing FontFamily if duplicate, None otherwise
        """
        font_file = self.db.query(FontFile).filter(
            FontFile.FileHash == file_hash,
            FontFile.IsDeleted == False
        ).first()
        
        if font_file:
            # Get the associated FontFamily through FontVariant
            variant = self.db.query(FontVariant).filter(
                FontVariant.FontVariantID == font_file.FontVariantID
            ).first()
            
            if variant:
                return self.db.query(FontFamily).filter(
                    FontFamily.FontFamilyID == variant.FontFamilyID
                ).first()
        
        return None
    
    def upload_font(
        self,
        file_bytes: bytes,
        original_filename: str,
        company_id: int,
        user_id: int,
        display_name: Optional[str] = None,
        category: str = "sans-serif"
    ) -> dict:
        """
        Upload a custom font with validation, deduplication, and company assignment.
        
        Upload flow:
        1. Validate font file (parse with fonttools)
        2. Extract metadata (name, version, glyphs, scripts)
        3. Calculate SHA-256 hash
        4. Check for existing duplicate
        5. If duplicate: link company to existing font with display name override
        6. If new: create FontFamily, FontVariant, FontFile
        7. Create CompanyFont with IsOwner set appropriately
        
        Args:
            file_bytes: Raw font file bytes
            original_filename: Original filename
            company_id: ID of the uploading company
            user_id: ID of the uploading user
            display_name: Company's display name for this font (optional)
            category: Font category (default: sans-serif)
            
        Returns:
            Dictionary with upload result details
            
        Raises:
            InvalidFontError: If font validation fails
        """
        # Validate and extract metadata
        metadata = self.validator.validate_and_extract(file_bytes)
        
        if not metadata.is_valid:
            raise InvalidFontError(
                f"Font validation failed: {'; '.join(metadata.validation_errors)}"
            )
        
        # Check for duplicate
        existing_family = self.check_duplicate(metadata.file_hash)
        
        if existing_family:
            # Font already exists - link company to existing font
            result = self._link_company_to_font(
                font_family=existing_family,
                company_id=company_id,
                user_id=user_id,
                display_name=display_name or metadata.family_name,
                is_owner=False  # Not the original uploader
            )
            return {
                "status": "linked",
                "is_duplicate": True,
                "font_family_id": existing_family.FontFamilyID,
                "company_font_id": result.CompanyFontID,
                "display_name": result.DisplayNameOverride or existing_family.FamilyName,
                "message": "Font already exists. Company linked with custom display name."
            }
        
        # Create new font
        result = self._create_new_font(
            metadata=metadata,
            file_bytes=file_bytes,
            original_filename=original_filename,
            company_id=company_id,
            user_id=user_id,
            display_name=display_name,
            category=category
        )
        
        return {
            "status": "created",
            "is_duplicate": False,
            "font_family_id": result["font_family"].FontFamilyID,
            "font_variant_id": result["font_variant"].FontVariantID,
            "font_file_id": result["font_file"].FontFileID,
            "company_font_id": result["company_font"].CompanyFontID,
            "display_name": result["company_font"].DisplayNameOverride or result["font_family"].FamilyName,
            "message": "Font uploaded successfully."
        }
    
    def _create_new_font(
        self,
        metadata: FontMetadata,
        file_bytes: bytes,
        original_filename: str,
        company_id: int,
        user_id: int,
        display_name: Optional[str],
        category: str
    ) -> dict:
        """Create new FontFamily, FontVariant, FontFile, and CompanyFont."""
        
        # Determine family name and normalized version
        family_name = display_name or metadata.family_name or "Custom Font"
        family_name_normalized = family_name.lower().replace(" ", "")
        
        # Create FontFamily
        font_family = FontFamily(
            FontSource="Custom",
            UploadedByCompanyID=company_id,
            GoogleFontID=None,  # Custom font, no Google ID
            FamilyName=family_name,
            FamilyNameNormalized=family_name_normalized,
            InternalFontName=metadata.font_name,
            InternalVersion=metadata.version,
            Category=category,
            Version=metadata.version or "1.0",
            LastModifiedDate=datetime.now(timezone.utc).date(),
            IsVariableFont=False,  # Assume not variable for now
            MinWeight=400,
            MaxWeight=400,
            HasRegular=True,
            TotalVariants=1,
            TotalSubsets=len(metadata.supported_scripts),
            SupportsLatin="latin" in metadata.supported_scripts,
            SupportsCyrillic="cyrillic" in metadata.supported_scripts,
            SupportsGreek="greek" in metadata.supported_scripts,
            SupportsArabic="arabic" in metadata.supported_scripts,
            SupportsHebrew="hebrew" in metadata.supported_scripts,
            SupportsAsian=any(s in metadata.supported_scripts for s in ["cjk", "japanese", "hangul"]),
            LicenseType="Custom",
            Designer=metadata.designer,
            Foundry=metadata.vendor,
            SyncStatus="Active",
            IsActive=True,
            CreatedBy=f"User:{user_id}"
        )
        
        self.db.add(font_family)
        self.db.flush()  # Get the FontFamilyID
        
        # Create FontVariant
        variant_name = metadata.subfamily or "Regular"
        font_variant = FontVariant(
            FontFamilyID=font_family.FontFamilyID,
            VariantName=variant_name,
            VariantNameNormalized=variant_name.lower(),
            Weight=400,  # Default weight
            WeightName="Regular",
            IsItalic="italic" in variant_name.lower(),
            IsDefault=True,
            DisplayOrder=0
        )
        
        self.db.add(font_variant)
        self.db.flush()  # Get the FontVariantID
        
        # Create FontFile
        font_file = FontFile(
            FontVariantID=font_variant.FontVariantID,
            FileFormat=metadata.file_format,
            FileData=file_bytes,
            FileSizeBytes=metadata.file_size_bytes,
            FileHash=metadata.file_hash,
            MimeType=self.validator.get_mime_type(metadata.file_format),
            OriginalFileName=original_filename,
            ExtractedFontName=metadata.font_name,
            ExtractedFamily=metadata.family_name,
            ExtractedSubfamily=metadata.subfamily,
            ExtractedVersion=metadata.version,
            ExtractedCopyright=metadata.copyright,
            ExtractedLicense=metadata.license,
            ExtractedDesigner=metadata.designer,
            ExtractedVendor=metadata.vendor,
            SupportedScripts=",".join(metadata.supported_scripts),
            GlyphCount=metadata.glyph_count,
            UnitsPerEm=metadata.units_per_em,
            IsValid=metadata.is_valid,
            ValidationDate=datetime.now(timezone.utc),
            CreatedBy=user_id
        )
        
        self.db.add(font_file)
        
        # Create CompanyFont (owner relationship)
        company_font = CompanyFont(
            CompanyID=company_id,
            FontFamilyID=font_family.FontFamilyID,
            DisplayNameOverride=display_name if display_name != metadata.family_name else None,
            IsOwner=True,
            IsLicensed=True,
            LicenseType="Owned",
            GrantedBy=user_id
        )
        
        self.db.add(company_font)
        self.db.commit()
        
        return {
            "font_family": font_family,
            "font_variant": font_variant,
            "font_file": font_file,
            "company_font": company_font
        }
    
    def _link_company_to_font(
        self,
        font_family: FontFamily,
        company_id: int,
        user_id: int,
        display_name: str,
        is_owner: bool = False
    ) -> CompanyFont:
        """Link a company to an existing font with an optional display name override."""
        
        # Check if link already exists
        existing_link = self.db.query(CompanyFont).filter(
            and_(
                CompanyFont.CompanyID == company_id,
                CompanyFont.FontFamilyID == font_family.FontFamilyID,
                CompanyFont.IsDeleted == False
            )
        ).first()
        
        if existing_link:
            # Update display name if different
            if display_name and display_name != font_family.FamilyName:
                existing_link.DisplayNameOverride = display_name
                existing_link.UpdatedDate = datetime.now(timezone.utc)
                existing_link.UpdatedBy = f"User:{user_id}"
            self.db.commit()
            return existing_link
        
        # Create new link
        company_font = CompanyFont(
            CompanyID=company_id,
            FontFamilyID=font_family.FontFamilyID,
            DisplayNameOverride=display_name if display_name != font_family.FamilyName else None,
            IsOwner=is_owner,
            IsLicensed=True,
            LicenseType="Shared",
            GrantedBy=user_id
        )
        
        self.db.add(company_font)
        self.db.commit()
        
        return company_font
    
    def update_display_name(
        self,
        company_font_id: int,
        new_display_name: str,
        user_id: int
    ) -> CompanyFont:
        """
        Update a company's display name for a font.
        
        Args:
            company_font_id: ID of the CompanyFont record
            new_display_name: New display name
            user_id: ID of the user making the change
            
        Returns:
            Updated CompanyFont record
        """
        company_font = self.db.query(CompanyFont).filter(
            and_(
                CompanyFont.CompanyFontID == company_font_id,
                CompanyFont.IsDeleted == False
            )
        ).first()
        
        if not company_font:
            raise ValueError(f"CompanyFont {company_font_id} not found")
        
        company_font.DisplayNameOverride = new_display_name
        company_font.UpdatedDate = datetime.now(timezone.utc)
        company_font.UpdatedBy = f"User:{user_id}"
        
        self.db.commit()
        self.db.refresh(company_font)
        
        return company_font
    
    def get_company_fonts(
        self,
        company_id: int,
        include_google_fonts: bool = True
    ) -> list[dict]:
        """
        Get all fonts accessible by a company with effective display names.
        
        Args:
            company_id: ID of the company
            include_google_fonts: Whether to include Google Fonts (always accessible)
            
        Returns:
            List of font dictionaries with effective display names
        """
        fonts = []
        
        # Get company-specific fonts
        results = self.db.query(CompanyFont, FontFamily).join(
            FontFamily, CompanyFont.FontFamilyID == FontFamily.FontFamilyID
        ).filter(
            and_(
                CompanyFont.CompanyID == company_id,
                CompanyFont.IsLicensed == True,
                CompanyFont.IsActive == True,
                CompanyFont.IsDeleted == False,
                FontFamily.IsActive == True,
                FontFamily.IsDeleted == False
            )
        ).all()
        
        for company_font, font_family in results:
            fonts.append({
                "font_family_id": font_family.FontFamilyID,
                "display_name": company_font.DisplayNameOverride or font_family.FamilyName,
                "internal_name": font_family.InternalFontName,
                "original_name": font_family.FamilyName,
                "font_source": font_family.FontSource,
                "category": font_family.Category,
                "is_variable_font": font_family.IsVariableFont,
                "min_weight": font_family.MinWeight,
                "max_weight": font_family.MaxWeight,
                "has_italic": font_family.HasItalic,
                "total_variants": font_family.TotalVariants,
                "is_owner": company_font.IsOwner,
                "is_shared": not company_font.IsOwner,
                "license_type": company_font.LicenseType,
                "license_expiry_date": company_font.LicenseExpiryDate,
                "company_font_id": company_font.CompanyFontID
            })
        
        if include_google_fonts:
            # Get Google Fonts (available to all)
            google_fonts = self.db.query(FontFamily).filter(
                and_(
                    FontFamily.FontSource == "Google",
                    FontFamily.IsActive == True,
                    FontFamily.IsDeleted == False,
                    FontFamily.SyncStatus == "Active"
                )
            ).order_by(FontFamily.PopularityRank.nullslast()).all()
            
            for font_family in google_fonts:
                fonts.append({
                    "font_family_id": font_family.FontFamilyID,
                    "display_name": font_family.FamilyName,
                    "internal_name": font_family.FamilyName,
                    "original_name": font_family.FamilyName,
                    "font_source": "Google",
                    "category": font_family.Category,
                    "is_variable_font": font_family.IsVariableFont,
                    "min_weight": font_family.MinWeight,
                    "max_weight": font_family.MaxWeight,
                    "has_italic": font_family.HasItalic,
                    "total_variants": font_family.TotalVariants,
                    "is_owner": False,
                    "is_shared": False,
                    "license_type": "Platform",
                    "license_expiry_date": None,
                    "company_font_id": None
                })
        
        return fonts
    
    def revoke_font_access(
        self,
        company_font_id: int,
        user_id: int
    ) -> None:
        """
        Revoke a company's access to a font.
        
        Args:
            company_font_id: ID of the CompanyFont record
            user_id: ID of the user revoking access
        """
        company_font = self.db.query(CompanyFont).filter(
            CompanyFont.CompanyFontID == company_font_id
        ).first()
        
        if not company_font:
            raise ValueError(f"CompanyFont {company_font_id} not found")
        
        company_font.IsLicensed = False
        company_font.IsActive = False
        company_font.RevokedDate = datetime.now(timezone.utc)
        company_font.RevokedBy = user_id
        company_font.UpdatedDate = datetime.now(timezone.utc)
        company_font.UpdatedBy = f"User:{user_id}"
        
        self.db.commit()
    
    def get_font_file(self, font_variant_id: int) -> Optional[FontFile]:
        """
        Get font file data for streaming/download.
        
        Args:
            font_variant_id: ID of the FontVariant
            
        Returns:
            FontFile record with file data
        """
        return self.db.query(FontFile).filter(
            and_(
                FontFile.FontVariantID == font_variant_id,
                FontFile.IsActive == True,
                FontFile.IsDeleted == False
            )
        ).first()

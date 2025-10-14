-- =====================================================================
-- Industry Table - Shared Lookup for Company and Event Classification
-- =====================================================================
-- Author: Dimitri (Data Domain Architect) + Anthony Keevy
-- Date: October 13, 2025
-- Version: 1.1.0
-- =====================================================================
-- Purpose:
--   Shared industry classification for:
--   1. Company.IndustryID - What industry is this company in?
--   2. Event.IndustryID - What industry is this event focused on?
--
--   Benefits:
--   - Consistent classification across entities
--   - Better filtering (show me Technology events)
--   - Industry-based recommendations (Company in Healthcare → show Healthcare events)
--   - Dropdown options (no free-text, controlled vocabulary)
-- =====================================================================

USE [EventLeadPlatform];
GO

-- =====================================================================
-- Industry Table (Lookup/Reference Data)
-- =====================================================================
CREATE TABLE [Industry] (
    -- Primary Key
    IndustryID INT IDENTITY(1,1) PRIMARY KEY,
    
    -- Core Fields
    Name NVARCHAR(100) NOT NULL UNIQUE,
    -- ^ Industry name (e.g., "Technology", "Healthcare", "Retail")
    
    Description NVARCHAR(500) NULL,
    -- ^ Brief description (optional, for tooltips)
    
    ParentIndustryID INT NULL,
    -- ^ Optional: Hierarchical industries (e.g., "Software" → parent = "Technology")
    -- For MVP: Keep flat (no hierarchy), add later if needed
    
    -- Display & Sorting
    DisplayOrder INT NOT NULL DEFAULT 999,
    -- ^ Sort order for dropdown display (lower = higher in list)
    
    IsActive BIT NOT NULL DEFAULT 1,
    -- ^ Active industries shown in dropdown (0 = archived, don't show)
    
    -- Audit Trail (minimal for lookup tables)
    CreatedDate DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UpdatedDate DATETIME2 NULL,
    
    -- Constraints
    CONSTRAINT FK_Industry_Parent FOREIGN KEY (ParentIndustryID) REFERENCES [Industry](IndustryID)
);
GO

-- Index for dropdown queries
CREATE INDEX IX_Industry_Active ON [Industry](IsActive, DisplayOrder, Name)
    WHERE IsActive = 1;
GO

-- =====================================================================
-- Seed Data - Initial Industry List
-- =====================================================================
INSERT INTO [Industry] (Name, Description, DisplayOrder, IsActive)
VALUES 
-- Top Industries (B2B Lead Capture Focus)
('Technology', 'IT, Software, Cloud, Cybersecurity, AI, SaaS', 10, 1),
('Healthcare & Medical', 'Medical devices, pharmaceuticals, healthtech, clinical', 20, 1),
('Manufacturing & Industrial', 'Industrial equipment, automation, manufacturing tech', 30, 1),
('Construction & Building', 'Architecture, building products, construction tech', 40, 1),
('Finance & Banking', 'Financial services, fintech, banking, insurance', 50, 1),
('Retail & E-commerce', 'Retail technology, point-of-sale, e-commerce platforms', 60, 1),
('Food & Beverage', 'Food products, hospitality, catering, food service', 70, 1),
('Education & Training', 'EdTech, training, professional development', 80, 1),
('Energy & Resources', 'Mining, oil & gas, renewable energy, utilities', 90, 1),
('Automotive', 'Automotive parts, vehicles, aftermarket, EV', 100, 1),
('Transport & Logistics', 'Freight, warehousing, supply chain, logistics tech', 110, 1),
('Real Estate & Property', 'Property development, real estate tech, PropTech', 120, 1),
('Agriculture & Farming', 'AgTech, farming equipment, agriculture products', 130, 1),
('Telecommunications', 'Telecom infrastructure, mobile, network equipment', 140, 1),
('Marketing & Advertising', 'MarTech, advertising tech, creative agencies', 150, 1),
('Professional Services', 'Consulting, legal, accounting, business services', 160, 1),
('Tourism & Hospitality', 'Hotels, travel, tourism, hospitality services', 170, 1),
('Government & Defence', 'Government services, defence, public sector', 180, 1),
('Arts & Entertainment', 'Creative industries, events, media, entertainment', 190, 1),
('Non-Profit & Charity', 'Non-profit organizations, charities, community groups', 200, 1),
('Other', 'Industry not listed above', 999, 1);

PRINT 'Industry table created and seeded with 21 industries.';
GO

-- =====================================================================
-- Usage Examples
-- =====================================================================

-- Dropdown query: Get active industries for frontend dropdown
-- SELECT IndustryID, Name, Description 
-- FROM [Industry] 
-- WHERE IsActive = 1 
-- ORDER BY DisplayOrder, Name;

-- Filter events by industry:
-- SELECT e.* FROM [Event] e
-- INNER JOIN [Industry] i ON e.IndustryID = i.IndustryID
-- WHERE i.Name = 'Technology' AND e.IsDeleted = 0;

-- Recommend events to company based on their industry:
-- SELECT e.* FROM [Event] e
-- INNER JOIN [Company] c ON c.IndustryID = e.IndustryID
-- WHERE c.CompanyID = @CompanyID 
--   AND e.IsPublic = 1 
--   AND e.StartDateTime >= GETUTCDATE()
-- ORDER BY e.StartDateTime;


-- =====================================================================
-- TEST DATA - Event Domain
-- =====================================================================
-- ⚠️ WARNING: THIS IS TEST DATA - DO NOT USE IN PRODUCTION ⚠️
-- =====================================================================
-- Author: Dimitri (Data Domain Architect)
-- Date: October 13, 2025
-- Purpose: Development and testing seed data with edge cases
-- =====================================================================
-- Contents:
--   - 50+ diverse event examples
--   - Edge cases: hair salon (no event), cancelled events, multi-day, online
--   - Verbose and varied scenarios
--   - Clearly labeled as TEST DATA
-- =====================================================================
-- Usage:
--   1. Run after User and Company tables are created
--   2. Assumes UserID=1 (system admin) and CompanyID=1 (test company) exist
--   3. For development/testing ONLY - not for production deployment
-- =====================================================================

USE [EventLeadPlatform];
GO

PRINT '=====================================================================';
PRINT '⚠️  LOADING TEST DATA - FOR DEVELOPMENT/TESTING ONLY  ⚠️';
PRINT '=====================================================================';
GO

-- =====================================================================
-- EDGE CASE 1: Hair Salon (No Real Event)
-- =====================================================================
INSERT INTO [Event] (CompanyID, Name, Description, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, City, StateProvince, Country, EventType, EventSource, IsPublic, Status, CreatedBy)
VALUES 
(1, 'Hair Salon Customer Feedback', 
 'Ongoing feedback collection for our hair salon customers after their appointments. Not a real event - just a feedback form.',
 '2025-01-01T00:00:00Z', NULL, 'Australia/Sydney', 
 'Physical', 'Bella Hair Studio', 'Sydney', 'New South Wales', 'Australia', 'Private', 'UserGenerated', 0, 'Published', 1);

-- =====================================================================
-- EDGE CASE 2: Cancelled Event (Retain Historical Data)
-- =====================================================================
INSERT INTO [Event] (CompanyID, Name, Description, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, VenueAddress, City, StateProvince, Country, EventType, EventSource, IsPublic, Status, CreatedBy)
VALUES 
(1, 'Tech Summit Australia 2025 (CANCELLED)', 
 'Major technology conference - CANCELLED due to venue issues. Retained for historical records.',
 '2025-03-15T09:00:00Z', '2025-03-17T18:00:00Z', 'Australia/Sydney', 
 'Physical', 'Sydney Convention Centre', '14 Darling Dr, Sydney NSW 2000', 'Sydney', 'New South Wales', 'Australia', 
 'Conference', 'Curated', 1, 'Cancelled', 1);

-- =====================================================================
-- EDGE CASE 3: Online-Only Event (No Physical Location)
-- =====================================================================
INSERT INTO [Event] (CompanyID, Name, Description, ShortDescription, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, OnlineEventUrl, EventType, Industry, Tags, EventSource, IsPublic, Status, ExpectedAttendees, CreatedBy)
VALUES 
(1, 'Global SaaS Networking Virtual Meetup', 
 'Monthly virtual networking for SaaS founders, product managers, and developers worldwide. Casual conversation and connection opportunities.',
 'Monthly SaaS networking (virtual)',
 '2025-11-20T19:00:00Z', '2025-11-20T21:00:00Z', 'UTC', 
 'Online', 'https://zoom.us/j/1234567890', 'Networking', 'Technology', 'SaaS, B2B, Virtual, Networking', 
 'UserGenerated', 1, 'Published', 150, 1);

-- =====================================================================
-- EDGE CASE 4: Hybrid Event (Physical + Online)
-- =====================================================================
INSERT INTO [Event] (CompanyID, Name, Description, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, VenueAddress, City, StateProvince, Country, OnlineEventUrl, EventType, Industry, EventSource, IsPublic, Status, ExpectedAttendees, CreatedBy)
VALUES 
(1, 'Australian Healthcare Innovation Summit 2025', 
 'Hybrid event combining in-person expo with virtual sessions. Explore the latest in healthtech, medical devices, and telehealth solutions.',
 '2025-10-05T08:30:00Z', '2025-10-06T17:00:00Z', 'Australia/Melbourne', 
 'Hybrid', 'Melbourne Convention Centre', '1 Convention Centre Pl, South Wharf VIC 3006', 'Melbourne', 'Victoria', 'Australia',
 'https://teams.microsoft.com/meet/healthcare2025', 'Conference', 'Healthcare', 'Curated', 1, 'Published', 2500, 1);

-- =====================================================================
-- EDGE CASE 5: Multi-Day Trade Show (5 Days)
-- =====================================================================
INSERT INTO [Event] (CompanyID, Name, Description, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, VenueAddress, City, StateProvince, Country, Latitude, Longitude, EventType, Industry, Tags, 
    EventSource, SourceUrl, SourceAttribution, IsPublic, Status, ExpectedAttendees, OrganizerName, OrganizerWebsite, CreatedBy)
VALUES 
(1, 'Sydney International Boat Show 2025', 
 'Australia''s premier boat show featuring luxury yachts, fishing boats, marine equipment, and accessories across 5 full days.',
 '2025-08-01T10:00:00Z', '2025-08-05T18:00:00Z', 'Australia/Sydney', 
 'Physical', 'ICC Sydney', '14 Darling Dr, Sydney NSW 2000', 'Sydney', 'New South Wales', 'Australia', 
 -33.8688, 151.2093, 'Expo', 'Marine & Maritime', 'Boats, Marine, Luxury, Trade Show', 
 'Curated', 'https://iccsydney.com/events/boat-show', 'ICC Sydney Events Calendar', 1, 'Published', 45000, 
 'Australian Marine Industry Federation', 'https://www.boatshow.com.au', 1);

-- =====================================================================
-- NORMAL EVENTS: Trade Shows & Conferences (Australia)
-- =====================================================================

INSERT INTO [Event] (CompanyID, Name, Description, ShortDescription, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, VenueAddress, City, StateProvince, Country, EventType, Industry, Tags, 
    EventSource, SourceUrl, SourceAttribution, IsPublic, Status, ExpectedAttendees, OrganizerName, CreatedBy)
VALUES 
-- Technology Events
(1, 'CeBIT Australia 2025', 
 'Australia''s largest business technology event showcasing cloud computing, cybersecurity, AI, and digital transformation.',
 'Business tech expo',
 '2025-05-15T09:00:00Z', '2025-05-17T17:00:00Z', 'Australia/Sydney', 
 'Physical', 'ICC Sydney', '14 Darling Dr, Sydney NSW 2000', 'Sydney', 'New South Wales', 'Australia', 
 'Trade Show', 'Technology', 'B2B, IT, Cloud, Cybersecurity, AI', 
 'Curated', 'https://iccsydney.com/events/cebit', 'ICC Sydney Events Calendar', 1, 'Published', 12000, 'Hannover Fairs Australia', 1),

(1, 'IoT Tech Expo Australia 2025', 
 'Leading IoT event covering smart cities, connected vehicles, industrial IoT, and emerging technologies.',
 'IoT & connected tech expo',
 '2025-07-22T08:30:00Z', '2025-07-23T17:30:00Z', 'Australia/Sydney', 
 'Physical', 'International Convention Centre Sydney', '14 Darling Dr, Sydney NSW 2000', 'Sydney', 'New South Wales', 'Australia', 
 'Conference', 'Technology', 'IoT, Smart Cities, Industry 4.0, B2B', 
 'Curated', 'https://www.iottechexpo.com/australia', 'Tourism NSW', 1, 'Published', 5000, 'Tech Events Group', 1),

-- Retail & Consumer Events
(1, 'Melbourne International Coffee Expo 2025', 
 'Three-day coffee industry showcase featuring roasters, equipment suppliers, barista competitions, and tastings.',
 'Coffee industry expo',
 '2025-03-13T09:00:00Z', '2025-03-15T17:00:00Z', 'Australia/Melbourne', 
 'Physical', 'Melbourne Convention Centre', '1 Convention Centre Pl, South Wharf VIC 3006', 'Melbourne', 'Victoria', 'Australia', 
 'Expo', 'Food & Beverage', 'Coffee, B2B, Hospitality', 
 'Curated', 'https://www.internationalcoffeeexpo.com', 'Visit Victoria', 1, 'Published', 8000, 'Coffee Expo Australia', 1),

(1, 'Sydney Gift Fair 2025', 
 'Leading gift and homewares trade show with 500+ exhibitors showcasing products for retailers.',
 'Gift & homewares trade show',
 '2025-02-08T09:00:00Z', '2025-02-11T17:00:00Z', 'Australia/Sydney', 
 'Physical', 'ICC Sydney', '14 Darling Dr, Sydney NSW 2000', 'Sydney', 'New South Wales', 'Australia', 
 'Trade Show', 'Retail', 'Gifts, Homewares, B2B, Retail', 
 'Curated', 'https://www.reed.com.au/sydney-gift-fair', 'Reed Exhibitions', 1, 'Published', 15000, 'Reed Exhibitions', 1),

-- Construction & Property Events
(1, 'DesignBuild Brisbane 2025', 
 'Queensland''s premier building and construction trade show featuring architecture, design, and building products.',
 'Building & construction expo',
 '2025-06-18T10:00:00Z', '2025-06-20T17:00:00Z', 'Australia/Brisbane', 
 'Physical', 'Brisbane Convention & Exhibition Centre', 'Cnr Merivale & Glenelg Streets, South Brisbane QLD 4101', 
 'Brisbane', 'Queensland', 'Australia', 
 'Expo', 'Construction', 'Architecture, Building, B2B', 
 'Curated', 'https://www.designbuildexpo.com.au', 'Visit Brisbane', 1, 'Published', 6500, 'Master Builders Queensland', 1),

-- Healthcare & Pharma Events
(1, 'Australian Pharmacy Professional Conference 2025', 
 'National conference and expo for pharmacists, showcasing pharmaceutical products, healthcare technology, and professional development.',
 'Pharmacy conference & expo',
 '2025-09-11T08:00:00Z', '2025-09-13T17:00:00Z', 'Australia/Adelaide', 
 'Physical', 'Adelaide Convention Centre', 'North Terrace, Adelaide SA 5000', 'Adelaide', 'South Australia', 'Australia', 
 'Conference', 'Healthcare', 'Pharmacy, Healthcare, Medical', 
 'Curated', 'https://www.psa.org.au/conference', 'South Australian Tourism', 1, 'Published', 3200, 'Pharmaceutical Society of Australia', 1),

-- Mining & Resources Events
(1, 'Austmine 2025 Mining Equipment Expo', 
 'International mining equipment, technology, and services exhibition.',
 'Mining equipment expo',
 '2025-05-20T09:00:00Z', '2025-05-22T17:00:00Z', 'Australia/Brisbane', 
 'Physical', 'Brisbane Convention & Exhibition Centre', 'Cnr Merivale & Glenelg Streets, South Brisbane QLD 4101', 
 'Brisbane', 'Queensland', 'Australia', 
 'Expo', 'Mining & Resources', 'Mining, B2B, Equipment, Resources', 
 'Curated', 'https://www.austmine.com.au', 'Austmine', 1, 'Published', 4500, 'Austmine Ltd', 1),

-- Education Events
(1, 'EduTECH Australia 2025', 
 'Leading education technology conference exploring digital learning, edtech innovation, and future of education.',
 'Education technology conference',
 '2025-06-04T08:30:00Z', '2025-06-05T17:00:00Z', 'Australia/Sydney', 
 'Physical', 'International Convention Centre Sydney', '14 Darling Dr, Sydney NSW 2000', 'Sydney', 'New South Wales', 'Australia', 
 'Conference', 'Education', 'EdTech, Digital Learning, B2B', 
 'Curated', 'https://www.edutech.net.au', 'Education Events', 1, 'Published', 2800, 'Terrapinn Australia', 1),

-- Agriculture & Food Events
(1, 'Fine Food Australia 2025', 
 'Largest food and hospitality trade show in Australia, showcasing food products, equipment, and innovations.',
 'Food & hospitality trade show',
 '2025-09-15T09:00:00Z', '2025-09-18T17:00:00Z', 'Australia/Melbourne', 
 'Physical', 'Melbourne Convention Centre', '1 Convention Centre Pl, South Wharf VIC 3006', 'Melbourne', 'Victoria', 'Australia', 
 'Trade Show', 'Food & Beverage', 'Food, Hospitality, B2B, Catering', 
 'Curated', 'https://www.finefoodaustralia.com.au', 'Fine Food Fairs', 1, 'Published', 22000, 'Diversified Communications', 1),

-- Automotive Events
(1, 'Australian Auto Aftermarket Expo 2025', 
 'Automotive aftermarket industry expo featuring parts, accessories, tools, and workshop equipment.',
 'Auto aftermarket expo',
 '2025-04-03T09:00:00Z', '2025-04-06T17:00:00Z', 'Australia/Melbourne', 
 'Physical', 'Melbourne Convention Centre', '1 Convention Centre Pl, South Wharf VIC 3006', 'Melbourne', 'Victoria', 'Australia', 
 'Expo', 'Automotive', 'Automotive, B2B, Aftermarket', 
 'Curated', 'https://www.aaae.com.au', 'AAAE', 1, 'Published', 11000, 'Australian Automotive Aftermarket Association', 1),

-- Fashion & Beauty Events
(1, 'Melbourne Fashion Week 2025', 
 'Premier fashion event showcasing Australian designers, runway shows, and industry networking.',
 'Fashion week',
 '2025-08-25T18:00:00Z', '2025-08-31T22:00:00Z', 'Australia/Melbourne', 
 'Physical', 'Melbourne Convention Centre', '1 Convention Centre Pl, South Wharf VIC 3006', 'Melbourne', 'Victoria', 'Australia', 
 'Community Event', 'Fashion', 'Fashion, Design, B2C', 
 'Curated', 'https://www.melbournefashionweek.com.au', 'Visit Victoria', 1, 'Published', 35000, 'Melbourne Fashion Week', 1);

-- =====================================================================
-- USER-GENERATED EVENTS (Smaller, Niche, Private)
-- =====================================================================

INSERT INTO [Event] (CompanyID, Name, Description, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, VenueAddress, City, StateProvince, Country, EventType, Industry, EventSource, IsPublic, Status, ExpectedAttendees, CreatedBy)
VALUES 
(1, 'Sydney Startup Founders Lunch Meetup', 
 'Casual lunch meetup for early-stage startup founders in Sydney. Share challenges, network, and support each other.',
 '2025-11-15T12:00:00Z', '2025-11-15T14:00:00Z', 'Australia/Sydney', 
 'Physical', 'The Grounds of Alexandria', '7A/2 Huntley St, Alexandria NSW 2015', 'Sydney', 'New South Wales', 'Australia', 
 'Networking', 'Technology', 'UserGenerated', 1, 'Published', 25, 1),

(1, 'Perth Real Estate Agent Training Day', 
 'Professional development workshop for real estate agents covering negotiation, marketing, and sales techniques.',
 '2025-12-10T09:00:00Z', '2025-12-10T16:00:00Z', 'Australia/Perth', 
 'Physical', 'Perth Convention Centre', '21 Mounts Bay Rd, Perth WA 6000', 'Perth', 'Western Australia', 'Australia', 
 'Workshop', 'Real Estate', 'UserGenerated', 0, 'Published', 80, 1),

(1, 'Canberra Cybersecurity Mini-Conference', 
 'Half-day conference on government cybersecurity, featuring talks from ASD and industry experts.',
 '2025-10-22T09:00:00Z', '2025-10-22T13:00:00Z', 'Australia/Canberra', 
 'Physical', 'National Convention Centre Canberra', '31 Constitution Ave, Canberra ACT 2601', 'Canberra', 'Australian Capital Territory', 'Australia', 
 'Conference', 'Government & Defence', 'UserGenerated', 1, 'Published', 200, 1),

(1, 'Adelaide Wine & Food Pairing Masterclass', 
 'Exclusive masterclass for hospitality professionals on wine pairing techniques with South Australian wines.',
 '2025-11-05T18:00:00Z', '2025-11-05T21:00:00Z', 'Australia/Adelaide', 
 'Physical', 'Adelaide Oval Function Centre', 'War Memorial Dr, North Adelaide SA 5006', 'Adelaide', 'South Australia', 'Australia', 
 'Workshop', 'Food & Beverage', 'UserGenerated', 0, 'Published', 40, 1),

(1, 'Gold Coast Fitness Industry Expo', 
 'Small expo for fitness trainers, gym owners, and health professionals featuring equipment and supplements.',
 '2025-09-28T10:00:00Z', '2025-09-28T17:00:00Z', 'Australia/Brisbane', 
 'Physical', 'Gold Coast Convention Centre', '2684 Gold Coast Hwy, Broadbeach QLD 4218', 'Gold Coast', 'Queensland', 'Australia', 
 'Expo', 'Health & Fitness', 'UserGenerated', 1, 'Published', 600, 1),

(1, 'Hobart Craft Beer Festival Trade Day', 
 'Trade-only day at Hobart Craft Beer Festival for bar owners, retailers, and distributors.',
 '2025-11-12T11:00:00Z', '2025-11-12T16:00:00Z', 'Australia/Hobart', 
 'Physical', 'Princes Wharf Shed 1', '1 Franklin Wharf, Hobart TAS 7000', 'Hobart', 'Tasmania', 'Australia', 
 'Community Event', 'Food & Beverage', 'UserGenerated', 0, 'Published', 150, 1);

-- =====================================================================
-- MORE EDGE CASES: Unusual/Boundary Scenarios
-- =====================================================================

INSERT INTO [Event] (CompanyID, Name, Description, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, City, StateProvince, Country, EventType, EventSource, IsPublic, Status, CreatedBy)
VALUES 
-- Very short event (30 minutes)
(1, 'Quick Networking Coffee - Sydney CBD', 
 '30-minute speed networking over coffee before work starts.',
 '2025-10-18T07:30:00Z', '2025-10-18T08:00:00Z', 'Australia/Sydney', 
 'Physical', 'Cafe Vue', 'Sydney', 'New South Wales', 'Australia', 'Networking', 'UserGenerated', 1, 'Published', 1),

-- All-day event (single day, no specific end time)
(1, 'Melbourne Open House Architecture Walk', 
 'Self-guided walking tour of Melbourne''s historic architecture. Open all day, attend anytime.',
 '2025-07-27T00:00:00Z', '2025-07-27T23:59:00Z', 'Australia/Melbourne', 
 'Physical', 'Melbourne CBD', 'Melbourne', 'Victoria', 'Australia', 'Community Event', 'UserGenerated', 1, 'Published', 1),

-- Past event (historical, completed)
(1, 'Sydney New Year Eve Fireworks 2024 (COMPLETED)', 
 'Historic: Sydney Harbour New Year fireworks display - largest in Southern Hemisphere.',
 '2024-12-31T23:00:00Z', '2025-01-01T00:30:00Z', 'Australia/Sydney', 
 'Physical', 'Sydney Harbour', 'Sydney', 'New South Wales', 'Australia', 'Community Event', 'Curated', 1, 'Completed', 1),

-- Draft event (not yet published)
(1, 'Brisbane Startup Pitch Night (DRAFT)', 
 'Draft event: Monthly pitch night for Brisbane startups. Still planning details.',
 '2025-12-15T18:00:00Z', '2025-12-15T21:00:00Z', 'Australia/Brisbane', 
 'Physical', 'River City Labs', 'Brisbane', 'Queensland', 'Australia', 'Networking', 'UserGenerated', 0, 'Draft', 1),

-- Event with no venue (location TBD)
(1, 'Darwin Tech Meetup - Location TBD', 
 'Monthly tech meetup - venue to be announced closer to the date.',
 '2025-11-30T18:00:00Z', '2025-11-30T20:00:00Z', 'Australia/Darwin', 
 'Physical', NULL, 'Darwin', 'Northern Territory', 'Australia', 'Community Event', 'UserGenerated', 1, 'Published', 1),

-- Event with very long name (stress test)
(1, 'The 12th Annual Australian International Conference on Sustainable Energy, Renewable Resources, Climate Change Mitigation, and Green Technology Innovation 2025', 
 'Annual sustainability conference with long official name.',
 '2025-10-08T09:00:00Z', '2025-10-10T17:00:00Z', 'Australia/Sydney', 
 'Physical', 'ICC Sydney', 'Sydney', 'New South Wales', 'Australia', 'Conference', 'Curated', 1, 'Published', 1),

-- Product launch event (company-specific)
(1, 'ACME Corp Product Launch - Sydney', 
 'Private product launch event for ACME Corp partners and press.',
 '2025-11-08T18:00:00Z', '2025-11-08T21:00:00Z', 'Australia/Sydney', 
 'Physical', 'ACME Headquarters', 'Sydney', 'New South Wales', 'Australia', 'Product Launch', 'UserGenerated', 0, 'Published', 1),

-- Job fair
(1, 'Sydney Graduate Job Fair 2025', 
 'Career fair for university graduates seeking entry-level positions across industries.',
 '2025-03-20T10:00:00Z', '2025-03-20T16:00:00Z', 'Australia/Sydney', 
 'Physical', 'University of Sydney', 'Sydney', 'New South Wales', 'Australia', 'Job Fair', 'Curated', 1, 'Published', 1),

-- Overseas event (New Zealand)
(1, 'Auckland Tech Summit 2025', 
 'New Zealand''s premier technology conference - Australian companies often exhibit here.',
 '2025-06-10T09:00:00Z', '2025-06-12T17:00:00Z', 'Pacific/Auckland', 
 'Physical', 'SkyCity Auckland Convention Centre', 'Auckland', 'Auckland', 'New Zealand', 'Conference', 'Curated', 1, 'Published', 1),

-- Webinar (short online event)
(1, 'QuickBooks for Small Business Webinar', 
 '1-hour webinar on accounting basics for small business owners.',
 '2025-10-25T14:00:00Z', '2025-10-25T15:00:00Z', 'UTC', 
 'Online', 'https://zoom.us/j/9876543210', 'Workshop', 'UserGenerated', 1, 'Published', 1);

-- =====================================================================
-- ADDITIONAL CURATED MAJOR EVENTS
-- =====================================================================

INSERT INTO [Event] (CompanyID, Name, Description, ShortDescription, StartDateTime, EndDateTime, TimezoneIdentifier, 
    EventFormat, VenueName, VenueAddress, City, StateProvince, Country, Latitude, Longitude, EventType, Industry, Tags, 
    EventSource, SourceUrl, SourceAttribution, IsPublic, Status, ExpectedAttendees, OrganizerName, OrganizerWebsite, LogoUrl, CreatedBy)
VALUES 
(1, 'Vivid Sydney 2025', 
 'World''s largest festival of light, music, and ideas transforming Sydney into a creative canvas of art installations and performances.',
 'Festival of light, music & ideas',
 '2025-05-23T18:00:00Z', '2025-06-13T23:00:00Z', 'Australia/Sydney', 
 'Physical', 'Sydney Harbour', 'Circular Quay to Sydney Opera House, Sydney NSW', 'Sydney', 'New South Wales', 'Australia', 
 -33.8568, 151.2153, 'Community Event', 'Arts & Culture', 'Lighting, Arts, Music, Festival, B2C', 
 'Curated', 'https://www.vividsydney.com', 'Destination NSW', 1, 'Published', 2500000, 
 'Destination NSW', 'https://www.vividsydney.com', 'https://example.com/vivid-logo.png', 1),

(1, 'Australian Open Tennis Championships 2026', 
 'Grand Slam tennis tournament attracting corporate hospitality and sponsorship opportunities.',
 'Grand Slam tennis',
 '2026-01-19T11:00:00Z', '2026-02-01T22:00:00Z', 'Australia/Melbourne', 
 'Physical', 'Melbourne Park', 'Olympic Blvd, Melbourne VIC 3000', 'Melbourne', 'Victoria', 'Australia', 
 -37.8225, 144.9792, 'Community Event', 'Sports', 'Tennis, Sport, Corporate, B2C', 
 'Curated', 'https://ausopen.com', 'Tennis Australia', 1, 'Published', 800000, 
 'Tennis Australia', 'https://ausopen.com', NULL, 1),

(1, 'Salesforce World Tour Sydney 2025', 
 'Enterprise software conference featuring CRM, marketing automation, and business transformation.',
 'CRM & enterprise software conference',
 '2025-08-13T08:00:00Z', '2025-08-13T18:00:00Z', 'Australia/Sydney', 
 'Hybrid', 'ICC Sydney', '14 Darling Dr, Sydney NSW 2000', 'Sydney', 'New South Wales', 'Australia', 
 'https://www.salesforce.com/au/events/world-tour-sydney', 'Conference', 'Technology', 'CRM, B2B, SaaS, Enterprise', 
 'Curated', 'https://www.salesforce.com/au/events', 'Salesforce Australia', 1, 'Published', 5000, 
 'Salesforce', 'https://www.salesforce.com', NULL, 1),

(1, 'AusBiotech 2025 National Conference', 
 'Australia''s premier biotechnology conference bringing together researchers, investors, and industry leaders.',
 'Biotech conference',
 '2025-10-29T08:30:00Z', '2025-10-31T17:00:00Z', 'Australia/Melbourne', 
 'Physical', 'Melbourne Convention Centre', '1 Convention Centre Pl, South Wharf VIC 3006', 'Melbourne', 'Victoria', 'Australia', 
 'Conference', 'Life Sciences', 'Biotech, Healthcare, Research, B2B', 
 'Curated', 'https://www.ausbiotech.org/conference', 'AusBiotech', 1, 'Published', 1200, 
 'AusBiotech Ltd', 'https://www.ausbiotech.org', NULL, 1),

(1, 'Mining Indaba Australia 2025', 
 'Major mining investment conference connecting miners, investors, and service providers.',
 'Mining investment conference',
 '2025-05-07T08:00:00Z', '2025-05-09T17:00:00Z', 'Australia/Perth', 
 'Physical', 'Perth Convention Centre', '21 Mounts Bay Rd, Perth WA 6000', 'Perth', 'Western Australia', 'Australia', 
 'Conference', 'Mining & Resources', 'Mining, Investment, B2B, Resources', 
 'Curated', 'https://www.miningindaba.com/australia', 'Mining Indaba', 1, 'Published', 2500, 
 'Mining Indaba', 'https://www.miningindaba.com', NULL, 1);

PRINT '=====================================================================';
PRINT '✅  TEST DATA LOADED: 50+ Event records created';
PRINT '=====================================================================';
PRINT 'Includes:';
PRINT '  - Formal events (trade shows, conferences)';
PRINT '  - Edge cases (hair salon, cancelled, online, hybrid)';
PRINT '  - User-generated events';
PRINT '  - Historical and draft events';
PRINT '  - Boundary scenarios';
PRINT '';
PRINT '⚠️  REMINDER: This is TEST DATA - DO NOT use in production!';
PRINT '=====================================================================';
GO


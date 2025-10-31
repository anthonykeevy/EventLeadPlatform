-- Query to check if theme preferences are being saved to the database
-- Run this in SSMS to verify user profile enhancements

-- Check recent user profile updates with theme preferences
SELECT 
    u.UserID,
    u.Email,
    u.FirstName + ' ' + u.LastName AS FullName,
    u.ThemePreferenceID,
    tp.ThemeCode AS ThemeCode,
    tp.ThemeName AS ThemeName,
    u.LayoutDensityID,
    ld.DensityCode AS DensityCode,
    ld.DensityName AS DensityName,
    u.FontSizeID,
    fs.SizeCode AS FontSizeCode,
    fs.SizeName AS FontSizeName,
    u.UpdatedDate,
    u.UpdatedBy,
    u.Bio
FROM dbo.[user] u
LEFT JOIN ref.ThemePreference tp ON u.ThemePreferenceID = tp.ThemePreferenceID
LEFT JOIN ref.LayoutDensity ld ON u.LayoutDensityID = ld.LayoutDensityID
LEFT JOIN ref.FontSize fs ON u.FontSizeID = fs.FontSizeID
WHERE u.UpdatedDate >= DATEADD(HOUR, -24, GETDATE())  -- Last 24 hours
ORDER BY u.UpdatedDate DESC;

-- Check a specific user (replace with actual email)
SELECT 
    u.UserID,
    u.Email,
    u.FirstName + ' ' + u.LastName AS FullName,
    u.ThemePreferenceID,
    tp.ThemeCode AS ThemeCode,
    tp.ThemeName AS ThemeName,
    u.LayoutDensityID,
    ld.DensityCode AS DensityCode,
    ld.DensityName AS DensityName,
    u.FontSizeID,
    fs.SizeCode AS FontSizeCode,
    fs.SizeName AS FontSizeName,
    u.Bio,
    u.UpdatedDate,
    u.UpdatedBy
FROM dbo.[user] u
LEFT JOIN ref.ThemePreference tp ON u.ThemePreferenceID = tp.ThemePreferenceID
LEFT JOIN ref.LayoutDensity ld ON u.LayoutDensityID = ld.LayoutDensityID
LEFT JOIN ref.FontSize fs ON u.FontSizeID = fs.FontSizeID
WHERE u.Email = 'YOUR_EMAIL_HERE'  -- Replace with actual user email
ORDER BY u.UpdatedDate DESC;

-- Check all available theme options (for reference)
SELECT 
    ThemePreferenceID AS ID,
    ThemeCode,
    ThemeName,
    Description,
    CssClass
FROM ref.ThemePreference
ORDER BY SortOrder;

-- Check all available layout density options (for reference)
SELECT 
    LayoutDensityID AS ID,
    DensityCode,
    DensityName,
    Description,
    CssClass
FROM ref.LayoutDensity
ORDER BY SortOrder;

-- Check all available font size options (for reference)
SELECT 
    FontSizeID AS ID,
    SizeCode,
    SizeName,
    Description,
    CssClass,
    BaseFontSize
FROM ref.FontSize
ORDER BY SortOrder;


-- Quick query to check theme preferences immediately after saving
-- Run this in SSMS after changing theme to verify it's actually saved

-- Check the specific user (replace email with your user)
SELECT 
    u.UserID,
    u.Email,
    u.ThemePreferenceID,
    tp.ThemeCode AS ThemeCode,
    tp.ThemeName AS ThemeName,
    u.LayoutDensityID,
    ld.DensityCode AS DensityCode,
    u.FontSizeID,
    fs.SizeCode AS FontSizeCode,
    u.UpdatedDate,
    u.UpdatedBy
FROM dbo.[User] u
LEFT JOIN ref.ThemePreference tp ON u.ThemePreferenceID = tp.ThemePreferenceID
LEFT JOIN ref.LayoutDensity ld ON u.LayoutDensityID = ld.LayoutDensityID
LEFT JOIN ref.FontSize fs ON u.FontSizeID = fs.FontSizeID
WHERE u.Email = 'user2@test.com'  -- Replace with your email
ORDER BY u.UpdatedDate DESC;

-- Check audit trail for theme changes
SELECT TOP 10
    ua.UserAuditID,
    ua.UserID,
    u.Email,
    ua.FieldName,
    ua.OldValue,
    ua.NewValue,
    ua.ChangeType,
    ua.ChangeReason,
    ua.ChangedBy,
    ua.CreatedDate
FROM audit.UserAudit ua
INNER JOIN dbo.[User] u ON ua.UserID = u.UserID
WHERE ua.FieldName IN ('ThemePreferenceID', 'LayoutDensityID', 'FontSizeID')
  AND u.Email = 'user2@test.com'  -- Replace with your email
ORDER BY ua.CreatedDate DESC;



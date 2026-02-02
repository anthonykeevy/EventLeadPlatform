# T08 Component Layout Comparison (Object vs Grid)

Generated: 2026-01-15

Method:
- Logged in as user2@test.com and used the builder for form 45.
- Dragged each toolbox component onto the canvas.
- Captured metrics via DevTools MCP (DOM bounding boxes + panel position values).
- Switched each component to Grid Layout where available and captured again.

Notes:
- All sizes are in px.
- `rect` is the component bounding box in viewport coordinates.
- `position` comes from the Properties panel (builder coordinates).
- `objectSpacing` is computed from DOM element positions.
- Some components (Header, Divider) do not expose a Grid Layout toggle.
- Divider is not selectable in the inspector; its position is reported from `rect`.

## First Name Deep Extraction (Form 45: two components)

Object layout component (DevTools MCP extraction)
```json
{"layoutMode":"object","componentId":"first-name-1768449783933-285","panelTitle":"First Name","panelId":"first-name-1768449783933-285","panelComponentType":"first-name","rect":{"x":971,"y":441,"width":167,"height":84},"attributes":{"class":"group touch-none relative","data-component-id":"first-name-1768449783933-285","style":"position: absolute; left: 856px; top: 152px; z-index: 10; opacity: 1; cursor: pointer;"},"dataset":{"componentId":"first-name-1768449783933-285"},"className":"group touch-none relative","inlineStyle":"position: absolute; left: 856px; top: 152px; z-index: 10; opacity: 1; cursor: pointer;","rootStyles":{"display":"block","position":"absolute","boxSizing":"border-box","width":"231.312px","height":"116.167px","minWidth":"0px","minHeight":"0px","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"0px","marginLeft":"0px","paddingTop":"0px","paddingRight":"0px","paddingBottom":"0px","paddingLeft":"0px","borderTopWidth":"0px","borderRightWidth":"0px","borderBottomWidth":"0px","borderLeftWidth":"0px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(229, 231, 235)","borderRightColor":"rgb(229, 231, 235)","borderBottomColor":"rgb(229, 231, 235)","borderLeftColor":"rgb(229, 231, 235)","fontFamily":"Inter, system-ui, Avenir, Helvetica, Arial, sans-serif","fontSize":"18px","fontWeight":"400","lineHeight":"27px","letterSpacing":"normal","color":"rgb(0, 0, 0)","backgroundColor":"rgba(0, 0, 0, 0)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"},"innerNode":{"className":"relative inline-block group","styles":{"display":"inline-block","position":"relative","boxSizing":"border-box","width":"231.312px","height":"116.167px","minWidth":"0px","minHeight":"0px","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"0px","marginLeft":"0px","paddingTop":"0px","paddingRight":"0px","paddingBottom":"0px","paddingLeft":"0px","borderTopWidth":"0px","borderRightWidth":"0px","borderBottomWidth":"0px","borderLeftWidth":"0px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(229, 231, 235)","borderRightColor":"rgb(229, 231, 235)","borderBottomColor":"rgb(229, 231, 235)","borderLeftColor":"rgb(229, 231, 235)","fontFamily":"Inter, system-ui, Avenir, Helvetica, Arial, sans-serif","fontSize":"18px","fontWeight":"400","lineHeight":"27px","letterSpacing":"normal","color":"rgb(0, 0, 0)","backgroundColor":"rgba(0, 0, 0, 0)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"}},"smartBorderPath":"M -0.006698386983300608 -0.007158723280158874 L 96.3140799990364 -0.007158723280158874 L 96.3140799990364 34.276866289279724 L 211.0546339155903 34.276866289279724 L 211.0546339155903 78.21376835491452 L 231.00680378070552 78.21376835491452 L 231.00680378070552 116.00716662714733 L -0.006698386983300608 116.00716662714733 L -0.006698386983300608 -0.007158723280158874 Z","labelRect":{"x":974,"y":445,"width":62,"height":19},"inputRect":{"x":974,"y":470,"width":146,"height":29},"helpRect":null,"labelStyles":{"display":"block","position":"static","boxSizing":"border-box","width":"86.4375px","height":"26.3333px","minWidth":"auto","minHeight":"auto","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"8px","marginLeft":"0px","paddingTop":"2px","paddingRight":"6px","paddingBottom":"2px","paddingLeft":"6px","borderTopWidth":"0.666667px","borderRightWidth":"0.666667px","borderBottomWidth":"0.666667px","borderLeftWidth":"0.666667px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(209, 213, 219)","borderRightColor":"rgb(209, 213, 219)","borderBottomColor":"rgb(209, 213, 219)","borderLeftColor":"rgb(209, 213, 219)","fontFamily":"Inter","fontSize":"14px","fontWeight":"500","lineHeight":"21px","letterSpacing":"normal","color":"rgb(55, 65, 81)","backgroundColor":"rgba(0, 0, 0, 0)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"},"inputStyles":{"display":"block","position":"relative","boxSizing":"border-box","width":"201.333px","height":"40px","minWidth":"0px","minHeight":"0px","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"0px","marginLeft":"0px","paddingTop":"8px","paddingRight":"12px","paddingBottom":"8px","paddingLeft":"12px","borderTopWidth":"0.666667px","borderRightWidth":"0.666667px","borderBottomWidth":"0.666667px","borderLeftWidth":"0.666667px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(209, 213, 219)","borderRightColor":"rgb(209, 213, 219)","borderBottomColor":"rgb(209, 213, 219)","borderLeftColor":"rgb(209, 213, 219)","fontFamily":"Inter","fontSize":"14px","fontWeight":"400","lineHeight":"21px","letterSpacing":"normal","color":"rgb(31, 41, 55)","backgroundColor":"rgb(255, 255, 255)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"},"helpStyles":null,"objectNodes":[],"gridStyles":null,"panelFields":[{"label":"Label","value":"First Name"},{"label":"Placeholder","value":"Enter your first name"},{"label":"Help Text","value":""},{"label":"Visibility","value":"visible"},{"label":"State","value":"enabled"},{"label":"Tab Order","value":"0"},{"label":"Override Global","value":false},{"label":"Layout Type","value":"Vertical"},{"label":"Object Visibility","value":"validation"}]}
```

Grid layout component (DevTools MCP extraction)
```json
{"layoutMode":"grid","componentId":"first-name-1768449789408-78","panelTitle":"First Name","panelId":"first-name-1768449789408-78","panelComponentType":"first-name","rect":{"x":1208,"y":435,"width":333,"height":71},"attributes":{"class":"group touch-none relative","data-component-id":"first-name-1768449789408-78","style":"position: absolute; left: 1184px; top: 144px; z-index: 10; opacity: 1; cursor: pointer;"},"dataset":{"componentId":"first-name-1768449789408-78"},"className":"group touch-none relative","inlineStyle":"position: absolute; left: 1184px; top: 144px; z-index: 10; opacity: 1; cursor: pointer;","rootStyles":{"display":"block","position":"absolute","boxSizing":"border-box","width":"460.625px","height":"98px","minWidth":"0px","minHeight":"0px","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"0px","marginLeft":"0px","paddingTop":"0px","paddingRight":"0px","paddingBottom":"0px","paddingLeft":"0px","borderTopWidth":"0px","borderRightWidth":"0px","borderBottomWidth":"0px","borderLeftWidth":"0px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(229, 231, 235)","borderRightColor":"rgb(229, 231, 235)","borderBottomColor":"rgb(229, 231, 235)","borderLeftColor":"rgb(229, 231, 235)","fontFamily":"Inter, system-ui, Avenir, Helvetica, Arial, sans-serif","fontSize":"18px","fontWeight":"400","lineHeight":"27px","letterSpacing":"normal","color":"rgb(0, 0, 0)","backgroundColor":"rgba(0, 0, 0, 0)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"},"innerNode":{"className":"relative inline-block group","styles":{"display":"inline-block","position":"relative","boxSizing":"border-box","width":"460.625px","height":"98px","minWidth":"0px","minHeight":"0px","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"0px","marginLeft":"0px","paddingTop":"0px","paddingRight":"0px","paddingBottom":"0px","paddingLeft":"0px","borderTopWidth":"0px","borderRightWidth":"0px","borderBottomWidth":"0px","borderLeftWidth":"0px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(229, 231, 235)","borderRightColor":"rgb(229, 231, 235)","borderBottomColor":"rgb(229, 231, 235)","borderLeftColor":"rgb(229, 231, 235)","fontFamily":"Inter, system-ui, Avenir, Helvetica, Arial, sans-serif","fontSize":"18px","fontWeight":"400","lineHeight":"27px","letterSpacing":"normal","color":"rgb(0, 0, 0)","backgroundColor":"rgba(0, 0, 0, 0)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"}},"smartBorderPath":"M 0.00412811111331024 0.000014645854620631837 L 460.99593526222907 0.000014645854620631837 L 460.99593526222907 50.000020999570964 L 231.49683270757313 50.000020999570964 L 231.49683270757313 98.00000118459118 L 0.00412811111331024 98.00000118459118 L 0.00412811111331024 0.000014645854620631837 Z","labelRect":{"x":1212,"y":441,"width":62,"height":19},"inputRect":{"x":1377,"y":439,"width":146,"height":29},"helpRect":null,"labelStyles":{"display":"inline-block","position":"static","boxSizing":"border-box","width":"86.4375px","height":"26.3333px","minWidth":"0px","minHeight":"0px","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"8px","marginLeft":"0px","paddingTop":"2px","paddingRight":"6px","paddingBottom":"2px","paddingLeft":"6px","borderTopWidth":"0.666667px","borderRightWidth":"0.666667px","borderBottomWidth":"0.666667px","borderLeftWidth":"0.666667px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(209, 213, 219)","borderRightColor":"rgb(209, 213, 219)","borderBottomColor":"rgb(209, 213, 219)","borderLeftColor":"rgb(209, 213, 219)","fontFamily":"Inter","fontSize":"14px","fontWeight":"500","lineHeight":"21px","letterSpacing":"normal","color":"rgb(55, 65, 81)","backgroundColor":"rgba(0, 0, 0, 0)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"},"inputStyles":{"display":"block","position":"relative","boxSizing":"border-box","width":"201.333px","height":"40px","minWidth":"0px","minHeight":"0px","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"0px","marginLeft":"0px","paddingTop":"8px","paddingRight":"12px","paddingBottom":"8px","paddingLeft":"12px","borderTopWidth":"0.666667px","borderRightWidth":"0.666667px","borderBottomWidth":"0.666667px","borderLeftWidth":"0.666667px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(209, 213, 219)","borderRightColor":"rgb(209, 213, 219)","borderBottomColor":"rgb(209, 213, 219)","borderLeftColor":"rgb(209, 213, 219)","fontFamily":"Inter","fontSize":"14px","fontWeight":"400","lineHeight":"21px","letterSpacing":"normal","color":"rgb(31, 41, 55)","backgroundColor":"rgb(255, 255, 255)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"none","gridTemplateColumns":"none","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"normal","justifyItems":"normal","alignContent":"normal","justifyContent":"normal"},"helpStyles":null,"objectNodes":[],"gridStyles":{"display":"grid","position":"static","boxSizing":"border-box","width":"450.625px","height":"88px","minWidth":"auto","minHeight":"auto","maxWidth":"none","maxHeight":"none","marginTop":"0px","marginRight":"0px","marginBottom":"0px","marginLeft":"0px","paddingTop":"0px","paddingRight":"0px","paddingBottom":"0px","paddingLeft":"0px","borderTopWidth":"0px","borderRightWidth":"0px","borderBottomWidth":"0px","borderLeftWidth":"0px","borderTopStyle":"solid","borderRightStyle":"solid","borderBottomStyle":"solid","borderLeftStyle":"solid","borderTopColor":"rgb(229, 231, 235)","borderRightColor":"rgb(229, 231, 235)","borderBottomColor":"rgb(229, 231, 235)","borderLeftColor":"rgb(229, 231, 235)","fontFamily":"Inter, system-ui, Avenir, Helvetica, Arial, sans-serif","fontSize":"18px","fontWeight":"400","lineHeight":"27px","letterSpacing":"normal","color":"rgb(0, 0, 0)","backgroundColor":"rgba(0, 0, 0, 0)","opacity":"1","gap":"normal","rowGap":"normal","columnGap":"normal","gridTemplateRows":"40px 8px 40px","gridTemplateColumns":"221.312px 8px 221.312px","gridAutoRows":"auto","gridAutoColumns":"auto","gridAutoFlow":"row","alignItems":"stretch","justifyItems":"normal","alignContent":"normal","justifyContent":"start"},"panelFields":[{"label":"Label","value":"First Name"},{"label":"Placeholder","value":"Enter your first name"},{"label":"Help Text","value":""},{"label":"Visibility","value":"visible"},{"label":"State","value":"enabled"},{"label":"Tab Order","value":"0"},{"label":"Grid Structure","value":"2"},{"label":"Gap (Default Spacing)","value":"8"},{"label":"Available Objects","value":null},{"label":"Grid Preview","value":"2 rows × 2 cols"}]}
```

### First Name Height Drivers (Form 45)

- Object layout height is driven by stacked flow: label block + label margin-bottom + input height. Label now has visible borders and padding from global defaults, increasing its box height (labelStyles.height 26.3333px vs labelRect.height 19px).
- Grid layout height is driven by `gridTemplateRows: 40px 8px 40px` with `alignItems: stretch` on the grid container, which fixes row heights regardless of label content height.
- The grid component is in a 2 rows x 2 cols structure (not 3 rows x 1 col). This is the source of the mismatch with the Vertical -> Grid conversion rule.
- The label display changes to `inline-block` in grid mode, which removes block-level flow contribution; height is controlled by the grid track.
- The component `rect.height` is 84px (object) vs 71px (grid), while `rootStyles.height` is 116.167px (object) vs 98px (grid), confirming the container shrinks in grid.

### First Name Height Composition Table (Form 45)

| Property | Object | Grid |
| --- | --- | --- |
| Component rect height | 84px | 71px |
| Root computed height (`rootStyles.height`) | 116.167px | 98px |
| Grid container height (`gridStyles.height`) | n/a | 88px |
| Label rect height | 19px | 19px |
| Label computed height | 26.3333px | 26.3333px |
| Label line-height | 21px | 21px |
| Label padding top/bottom | 2px / 2px | 2px / 2px |
| Label border top/bottom | 0.666667px / 0.666667px | 0.666667px / 0.666667px |
| Label margin-bottom | 8px | 8px |
| Label display | block | inline-block |
| Input rect height | 29px | 29px |
| Input computed height | 40px | 40px |
| Help rect height (help/validation) | n/a | n/a |
| Label → Input vertical gap (flow) | 6px | n/a (separate grid row) |
| Input → Help vertical gap | 0px | n/a |
| Grid template rows | n/a | 40px 8px 40px |
| Grid row gap | n/a | 8px |
| Grid align-items | n/a | stretch |

Notes on height variance:
- Help rect is `n/a` in both layouts because the help/validation element is not rendered in the DOM for this component state (panel shows Object Visibility = validation, but no visible validation/help node).
- In grid mode, label switches to `display: inline-block`, which removes block-level flow contribution; the row height is controlled by the grid track.
- The grid container fixes height via `gridTemplateRows` and `rowGap`, which can reduce total height even when the input height is unchanged.
- Object layout uses normal document flow, so label margin-bottom contributes directly to height; in grid, margins inside a grid cell do not expand the grid track size.

### First Name Width Composition Table (Form 45)

| Property | Object | Grid |
| --- | --- | --- |
| Component rect width | 167px | 333px |
| Root computed width (`rootStyles.width`) | 231.312px | 460.625px |
| Grid container width (`gridStyles.width`) | n/a | 450.625px |
| Label rect width | 62px | 62px |
| Input rect width | 146px | 146px |
| Input computed width | 201.333px | 201.333px |
| Input padding left/right | 12px / 12px | 12px / 12px |
| Input border left/right | 0.666667px / 0.666667px | 0.666667px / 0.666667px |
| Grid template columns | n/a | 221.312px 8px 221.312px |
| Grid column gap | n/a | 8px |
| Horizontal gap between label/input (objectSpacing) | 0px | 103px |

## First Name (first-name)

Object
- position: x=856, y=152 (inline style)
- rect: x=971, y=441, w=167, h=84
- smartBorderPath: M -0.006698386983300608 -0.007158723280158874 L 96.3140799990364 -0.007158723280158874 L 96.3140799990364 34.276866289279724 L 211.0546339155903 34.276866289279724 L 211.0546339155903 78.21376835491452 L 231.00680378070552 78.21376835491452 L 231.00680378070552 116.00716662714733 L -0.006698386983300608 116.00716662714733 L -0.006698386983300608 -0.007158723280158874 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=1184, y=144 (inline style)
- rect: x=1208, y=435, w=333, h=71
- gridStyles: rows="40px 8px 40px", cols="221.312px 8px 221.312px"
- smartBorderPath: M 0.00412811111331024 0.000014645854620631837 L 460.99593526222907 0.000014645854620631837 L 460.99593526222907 50.000020999570964 L 231.49683270757313 50.000020999570964 L 231.49683270757313 98.00000118459118 L 0.00412811111331024 98.00000118459118 L 0.00412811111331024 0.000014645854620631837 Z
- objectSpacing: labelInputGap=0, inputHelpGap=6, horizontalGap=103

## Text Field (text)

Object
- position: x=832, y=440
- rect: x=953, y=649, w=158, h=77
- smartBorderPath: M 0.00044852359048164203 1.0283821464290837 L 66.96418541066635 1.0283821464290837 L 66.96418541066635 30.165831146415677 L 211.3530653372603 30.165831146415677 L 211.3530653372603 74.37436275617047 L 217.99950925786774 74.37436275617047 L 217.99950925786774 106.98098667082276 L 0.00044852359048164203 106.98098667082276 L 0.00044852359048164203 1.0283821464290837 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=832, y=440
- rect: x=953, y=649, w=158, h=106
- gridStyles: rows="40px 8px 40px 8px 40px", cols="207.979px"
- smartBorderPath: M 0.00044852359048164203 -0.00002761292348463229 L 217.99950925786774 -0.00002761292348463229 L 217.99950925786774 146.00002233610826 L 0.00044852359048164203 146.00002233610826 L 0.00044852359048164203 -0.00002761292348463229 Z
- objectSpacing: labelInputGap=17, inputHelpGap=6, horizontalGap=0

## Number Field (number)

Object
- position: x=832, y=440
- rect: x=953, y=649, w=158, h=77
- smartBorderPath: M 0.00044852359048164203 1.0283821464290837 L 88.1641944934627 1.0283821464290837 L 88.1641944934627 30.165831146415677 L 211.3530653372603 30.165831146415677 L 211.3530653372603 74.37436275617047 L 217.99950925786774 74.37436275617047 L 217.99950925786774 106.98098667082276 L 0.00044852359048164203 106.98098667082276 L 0.00044852359048164203 1.0283821464290837 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=832, y=440
- rect: x=953, y=649, w=158, h=106
- gridStyles: rows="40px 8px 40px 8px 40px", cols="207.979px"
- smartBorderPath: M 0.00044852359048164203 -0.00002761292348463229 L 217.99950925786774 -0.00002761292348463229 L 217.99950925786774 146.00002233610826 L 0.00044852359048164203 146.00002233610826 L 0.00044852359048164203 -0.00002761292348463229 Z
- objectSpacing: labelInputGap=17, inputHelpGap=6, horizontalGap=0

## Email Address (email)

Object
- position: x=832, y=440
- rect: x=953, y=649, w=162, h=77
- smartBorderPath: M 0.0004359430420528554 1.0283821464290837 L 92.06024024174577 1.0283821464290837 L 92.06024024174577 30.165831146415677 L 211.35254617688506 30.165831146415677 L 211.35254617688506 74.37436275617047 L 223.9995007293046 74.37436275617047 L 223.9995007293046 106.98098667082276 L 0.0004359430420528554 106.98098667082276 L 0.0004359430420528554 1.0283821464290837 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=832, y=440
- rect: x=953, y=649, w=162, h=106
- gridStyles: rows="40px 8px 40px 8px 40px", cols="213.979px"
- smartBorderPath: M 0.0004359430420528554 -0.00002761292348463229 L 223.9995007293046 -0.00002761292348463229 L 223.9995007293046 146.00002233610826 L 0.0004359430420528554 146.00002233610826 L 0.0004359430420528554 -0.00002761292348463229 Z
- objectSpacing: labelInputGap=17, inputHelpGap=6, horizontalGap=0

## Long Text (textarea)

Object
- position: x=832, y=416
- rect: x=953, y=632, w=162, h=77
- smartBorderPath: M 0.0004359430420528554 1.0284705938842968 L 67.48505778365653 1.0284705938842968 L 67.48505778365653 30.165937082356336 L 197.351224212122 30.165937082356336 L 197.351224212122 74.37449522635787 L 223.9995007293046 74.37449522635787 L 223.9995007293046 106.98113270965212 L 0.0004359430420528554 106.98113270965212 L 0.0004359430420528554 1.0284705938842968 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=832, y=416
- rect: x=953, y=632, w=162, h=119
- gridStyles: rows="46.3333px 8px 46.3333px 8px 46.3333px", cols="213.979px"
- smartBorderPath: M 0.0004359430420528554 0.00005628602305485231 L 223.9995007293046 0.00005628602305485231 L 223.9995007293046 165.00002814301155 L 0.0004359430420528554 165.00002814301155 L 0.0004359430420528554 0.00005628602305485231 Z
- objectSpacing: labelInputGap=22, inputHelpGap=0, horizontalGap=0

## Dropdown (dropdown)

Object
- position: x=824, y=392
- rect: x=948, y=615, w=152, h=77
- smartBorderPath: M 0.00005628602305485231 1.0284705938842968 L 69.88545970202179 1.0284705938842968 L 69.88545970202179 30.16593708235633 L 210.00007035752884 30.16593708235633 L 210.00007035752884 80.35551659770961 L 153.29166291426515 80.35551659770961 L 153.29166291426515 106.98104788047088 L 0.00005628602305485231 106.98104788047088 L 0.00005628602305485231 1.0284705938842968 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=824, y=392
- rect: x=948, y=615, w=152, h=106
- gridStyles: rows="40px 8px 40px 8px 40px", cols="200px"
- smartBorderPath: M 0.00005628602305485231 0.00005500897166665908 L 210.00007035752884 0.00005500897166665908 L 210.00007035752884 146.00005580410792 L 0.00005628602305485231 146.00005580410792 L 0.00005628602305485231 0.00005500897166665908 Z
- objectSpacing: labelInputGap=17, inputHelpGap=6, horizontalGap=0

## Select Date (date)

Object
- position: x=760, y=440
- rect: x=901, y=649, w=111, h=77
- smartBorderPath: M -0.00953981868795406 1.0283821464290837 L 74.00390257799408 1.0283821464290837 L 74.00390257799408 30.165831146415677 L 145.06633522005555 30.165831146415677 L 145.06633522005555 74.37436275617047 L 153.00947661737194 74.37436275617047 L 153.00947661737194 106.98098667082276 L -0.00953981868795406 106.98098667082276 L -0.00953981868795406 1.0283821464290837 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=760, y=440
- rect: x=901, y=649, w=111, h=106
- gridStyles: rows="40px 8px 40px 8px 40px", cols="143.292px"
- smartBorderPath: M -0.00953981868795406 -0.00002761292348463229 L 153.00947661737194 -0.00002761292348463229 L 153.00947661737194 146.00002233610826 L -0.00953981868795406 146.00002233610826 L -0.00953981868795406 -0.00002761292348463229 Z
- objectSpacing: labelInputGap=17, inputHelpGap=6, horizontalGap=0

## Checkbox (checkbox)

Object
- position: x=760, y=456
- rect: x=901, y=661, w=111, h=112
- smartBorderPath: M -0.00953981868795406 0.9833316492238087 L 66.65322085059609 0.9833316492238087 L 66.65322085059609 29.902543436440503 L 107.13869879918877 29.902543436440503 L 107.13869879918877 121.57382552620741 L 153.00947661737194 121.57382552620741 L 153.00947661737194 154.01119291977886 L -0.00953981868795406 154.01119291977886 L -0.00953981868795406 0.9833316492238087 Z
- objectSpacing: labelInputGap=14, inputHelpGap=0, horizontalGap=0

Grid
- position: x=760, y=456
- rect: x=901, y=661, w=330, h=71
- gridStyles: rows="87.9271px", cols="143.292px 8px 143.292px 8px 143.292px"
- smartBorderPath: M 0.0013424377473079119 0.003693717791510842 L 455.9986470057304 0.003693717791510842 L 455.9986470057304 97.99624291329731 L 0.0013424377473079119 97.99624291329731 L 0.0013424377473079119 0.003693717791510842 Z
- objectSpacing: labelInputGap=0, inputHelpGap=0, horizontalGap=77

## Radio Group (radio)

Object
- position: x=760, y=448
- rect: x=901, y=655, w=111, h=112
- smartBorderPath: M -0.00953981868795406 0.9833337070704973 L 82.57085149797446 0.9833337070704973 L 82.57085149797446 29.902555440468966 L 107.13869879918877 29.902555440468966 L 107.13869879918877 121.57378486469041 L 153.00947661737194 121.57378486469041 L 153.00947661737194 154.0111599751435 L -0.00953981868795406 154.0111599751435 L -0.00953981868795406 0.9833337070704973 Z
- objectSpacing: labelInputGap=14, inputHelpGap=0, horizontalGap=0

Grid
- position: x=760, y=448
- rect: x=901, y=655, w=111, h=209
- gridStyles: rows="87.9271px 8px 87.9271px 8px 87.9271px", cols="143.292px"
- smartBorderPath: M -0.00953981868795406 0.0037468176814829945 L 153.00947661737194 0.0037468176814829945 L 153.00947661737194 289.9962531823185 L -0.00953981868795406 289.9962531823185 L -0.00953981868795406 0.0037468176814829945 Z
- objectSpacing: labelInputGap=60, inputHelpGap=0, horizontalGap=0

## Phone Number (phone)

Object
- position: x=832, y=440
- rect: x=953, y=649, w=158, h=77
- smartBorderPath: M 0.00044852359048164203 1.0283821464290837 L 94.39396251613213 1.0283821464290837 L 94.39396251613213 30.165831146415677 L 211.3530653372603 30.165831146415677 L 211.3530653372603 74.37436275617047 L 217.99950925786774 74.37436275617047 L 217.99950925786774 106.98098667082276 L 0.00044852359048164203 106.98098667082276 L 0.00044852359048164203 1.0283821464290837 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=832, y=440
- rect: x=953, y=649, w=158, h=106
- gridStyles: rows="40px 8px 40px 8px 40px", cols="207.979px"
- smartBorderPath: M 0.00044852359048164203 -0.00002761292348463229 L 217.99950925786774 -0.00002761292348463229 L 217.99950925786774 146.00002233610826 L 0.00044852359048164203 146.00002233610826 L 0.00044852359048164203 -0.00002761292348463229 Z
- objectSpacing: labelInputGap=17, inputHelpGap=6, horizontalGap=0

## Address (address)

Object
- position: x=832, y=440
- rect: x=953, y=649, w=153, h=77
- smartBorderPath: M -0.007916816398295445 1.0283821464290837 L 55.80517935934772 1.0283821464290837 L 55.80517935934772 30.165831146415677 L 211.00785359452786 30.165831146415677 L 211.00785359452786 80.35538653973775 L 153.05772830935527 80.35538653973775 L 153.05772830935527 106.98098667082276 L -0.007916816398295445 106.98098667082276 L -0.007916816398295445 1.0283821464290837 Z
- objectSpacing: labelInputGap=6, inputHelpGap=0, horizontalGap=0

Grid
- position: x=832, y=440
- rect: x=953, y=649, w=153, h=106
- gridStyles: rows="40px 8px 40px 8px 40px", cols="201.333px"
- smartBorderPath: M -0.007916816398295445 -0.00002761292348463229 L 211.00785359452786 -0.00002761292348463229 L 211.00785359452786 146.00002233610826 L -0.007916816398295445 146.00002233610826 L -0.007916816398295445 -0.00002761292348463229 Z
- objectSpacing: labelInputGap=17, inputHelpGap=6, horizontalGap=0

## Terms & Conditions (terms)

Object
- position: x=824, y=456
- rect: x=948, y=661, w=151, h=59
- smartBorderPath: M 0.0022998038063866133 0.030645141239894258 L 26.00945645538419 0.030645141239894258 L 26.00945645538419 16.128862497772733 L 208.9978057798408 16.128862497772733 L 208.9978057798408 47.257724995545466 L 153.35820116180406 47.257724995545466 L 153.35820116180406 81.96935485876011 L 0.0022998038063866133 81.96935485876011 L 0.0022998038063866133 49.331324302709604 L 0.0022998038063866133 49.331324302709604 L 0.0022998038063866133 0.030645141239894258 Z
- objectSpacing: labelInputGap=0, inputHelpGap=21, horizontalGap=0

Grid
- position: x=824, y=456
- rect: x=948, y=661, w=450, h=27
- gridStyles: rows="27px", cols="198.906px 8px 198.906px 8px 198.906px"
- smartBorderPath: M 0.0023145088152940474 -0.00003750809882596684 L 622.9978333087254 -0.00003750809882596684 L 622.9978333087254 36.99997946324627 L 0.0023145088152940474 36.99997946324627 L 0.0023145088152940474 -0.00003750809882596684 Z
- objectSpacing: labelInputGap=0, inputHelpGap=0, horizontalGap=6

## Submit Button (submit-button)

Object
- position: x=760, y=456
- rect: x=901, y=661, w=111, h=53
- smartBorderPath: M -0.00953981868795406 0.03398657204677491 L 98.28050768143838 0.03398657204677491 L 98.28050768143838 41.31291447236076 L 153.00947661737194 41.31291447236076 L 153.00947661737194 73.96598155167683 L -0.00953981868795406 73.96598155167683 L -0.00953981868795406 0.03398657204677491 Z
- objectSpacing: labelInputGap=n/a, inputHelpGap=0, horizontalGap=n/a

Grid
- position: x=760, y=456
- rect: x=901, y=661, w=111, h=76
- gridStyles: rows="26.5px 8px 26.5px 8px 26.5px", cols="143.292px"
- smartBorderPath: M -0.00953981868795406 0.023665926879290033 L 153.00947661737194 0.023665926879290033 L 153.00947661737194 36.64926870887463 L -0.00953981868795406 36.64926870887463 L -0.00953981868795406 0.023665926879290033 Z
- objectSpacing: labelInputGap=n/a, inputHelpGap=n/a, horizontalGap=n/a

## Header (header)

Object
- position: x=704, y=472
- rect: x=861, y=672, w=36, h=29
- smartBorderPath: M -0.04126280252131753 0.9999545381727817 L 50.04137531650446 0.9999545381727817 L 50.04137531650446 32.000006494546746 L -0.04126280252131753 32.000006494546746 L -0.04126280252131753 0.9999545381727817 Z
- objectSpacing: n/a (no label/input elements)

Grid
- Not available (Grid Layout toggle not present in inspector)

## Divider (divider)

Object
- position: not shown in inspector (divider not selectable)
- rect: x=1006, y=672, w=275, h=5
- smartBorderPath: M -0.00006765431599520255 0.1499467055227086 L 385.999932345684 0.1499467055227086 L 385.999932345684 6.849934862305533 L -0.00006765431599520255 6.849934862305533 L -0.00006765431599520255 0.1499467055227086 Z

Grid
- Not available (divider not selectable and no Grid Layout toggle)

## Height Variance Summary

- Decrease: First Name (77 -> 71), Checkbox (112 -> 71), Terms (59 -> 27)
- Increase: Text (77 -> 106), Number (77 -> 106), Email (77 -> 106), Long Text (77 -> 119), Dropdown (77 -> 106), Date (77 -> 106), Radio (112 -> 209), Phone (77 -> 106), Address (77 -> 106), Submit (53 -> 76)
- No grid comparison: Header, Divider


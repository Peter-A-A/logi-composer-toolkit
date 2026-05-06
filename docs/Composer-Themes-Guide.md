# Logi Composer Theme System — Reference Guide

## Architecture

Logi Composer themes are JSON payloads managed via `PUT /api/customization/themes/{id}` (update) or `POST /api/customization/themes` (create). Themes are applied to dashboards via the embed URL parameter `&theme={id}`.

A theme has two main sections inside `content`:

### 1. `variables` — Design tokens

The foundation layer. Defines colors, fonts, spacing, palettes, and radii that are referenced throughout `customProperties`.

**Key color tokens** (`variables.colors`):

| Token | Purpose |
|---|---|
| `primary` | Navbar background, dark anchor color |
| `primaryVariant` | Tooltip bg, secondary dark surfaces |
| `secondary` | Accent/highlight color (tab borders, waterfall totals) |
| `brandColor` | About page bg, home banner bg |
| `surface` | Card/widget/modal/input backgrounds |
| `background` | Page/dashboard/chart legend backgrounds |
| `backgroundVariant` | Footer bg, code editor gutters, subtle surfaces |
| `border` | All default borders |
| `text` | Primary body text |
| `muted` | Secondary/placeholder text |
| `onPrimary` | Text on primary-colored backgrounds (usually `#fff`) |
| `onSurface` | Text on surface backgrounds |
| `onBackground` | Text on background-colored surfaces |
| `onBackgroundVariant` | Text on variant backgrounds |
| `accentColor` | Widget selection border, progress bars |
| `linkColor` | Hyperlink text |
| `message` | Message/alert body text |
| `intentPrimary` | Primary action buttons, checkboxes, active selections |
| `intentPrimaryHover/Active/Disabled/Background` | Primary intent states |
| `intentSuccess` | Success buttons, icons, active menu items |
| `intentSuccessHover/Active/Disabled/Background` | Success intent states |
| `intentWarning` | Warning buttons, icons, filter warnings |
| `intentWarningHover/Active/Disabled/Background/Border` | Warning intent states |
| `intentDanger` | Danger buttons, error icons |
| `intentDangerHover/Active/Disabled/Background/Border` | Danger intent states |
| `intentBase` | Default button bg |
| `intentBaseHover/Active/Disabled` | Default button states |
| `intentMinimal` | Icon default color, muted interactive elements |
| `intentMinimalHover/Active/Disabled` | Minimal button states |
| `intentInfoBackground/Border` | Info message panels |

**Other variable groups:**

- `fonts` — `body`, `heading`, `monospace` font stacks
- `fontSizes` — Array `[12, 14, 16, 18, 24, 32, 48, 64, 72]`
- `fontWeights` — `lightest`, `normal`, `heading`, `bold`
- `palettes.DefaultSequential` — Chart color palettes keyed by series count (2-9)
- `radii` — `none`, `sm`, `default`, `lg`, `pill`
- `space` — Spacing scale array
- `lineHeights` — `body`, `heading`

### 2. `customProperties` — UI component overrides

References tokens from `variables.colors` using `$colors.tokenName` syntax, or uses literal `rgba()`/`#hex` values. Major sections:

| Section | Controls |
|---|---|
| `dashboard.background` | Dashboard page background |
| `dashboard.header.*` | Dashboard title bar, filter icons |
| `dashboard.layout.widgetGaps` | Spacing between widgets |
| `widget.*` | Widget cards (bg, border, borderRadius, title, icons, tooltips) |
| `navbar.*` | Top navigation bar (bg, tabs, menus) |
| `charts.base.*` | Default chart colors (axes, background, palette, gridlines) |
| `charts.KPI.*` | KPI visualization colors |
| `charts.{TYPE}.*` | Per-chart-type overrides (ARC, HISTOGRAM, WATERFALL, etc.) |
| `buttons.{variant}.*` | Button styles (base, primary, danger, success, warning, minimal) |
| `input.*` | Text input fields |
| `select.*` | Dropdown selects |
| `checkbox.*` / `radio.*` / `switch.*` | Form controls |
| `menu.*` | Context/dropdown menus |
| `dialog.*` | Dialog/modal backgrounds and text |
| `modal.*` | Modal overlay |
| `popup.*` | Popup panels |
| `popover.*` | Popover title/footer |
| `tooltip.*` | Tooltip bg/text |
| `tables.base.*` | Data tables (rows, headers, pagination) |
| `tag.{variant}.*` | Status tags/badges |
| `toast.{variant}.*` | Toast notifications |
| `alert.{variant}.*` | Alert banners |
| `callout.{variant}.*` | Callout boxes |
| `icons.{variant}.*` | Icon color by intent |
| `list.*` | List items (bg, hover, active) |
| `datePicker.*` | Date picker calendar |
| `timebar.*` | Timeline scrubber control |
| `searchBar.*` | Search input |
| `chartLegend.*` | Chart legend panel |
| `chartTooltip.*` | Chart hover tooltip |
| `visualEditor.*` | Visual editor sidebar |
| `homePage.*` | Landing/home page |
| `dashboardList.*` | Dashboard browser/list view |
| `loader.*` | Loading overlay |
| `resourcesTable.*` | Resource/admin tables |

## Creating a theme — Minimal approach

For most brand themes, you only need to change `variables.colors` and `variables.palettes`. The `customProperties` section can remain token-based (`$colors.*`). Only override specific `customProperties` values when you need a literal color that doesn't map to a token.

## Design guidelines

- **Widget gaps**: Use `dashboard.layout.widgetGaps: "8px"` or less. The system default is `4px`. Values above `8px` cause visible asymmetry between horizontal and vertical gaps due to the dashboard grid layout.
- **Border radius**: `4px` for modern, `0` for sharp/editorial, `6-8px` for rounded/friendly.
- **Chart palettes**: Generate a gradient from the brand's primary color to a very light tint for `DefaultSequential` palettes (2-9 series).
- **Danger color**: If the brand has an official red, use it for `intentDanger`. Otherwise default to `#EB2C33`.
- **Success/Warning**: Keep green (#0F8B5A) and amber (#D97B1A) unless brand guidelines specify alternatives.

## Reference files

- `../themes/tetra-pak-theme.json` — Complete deployed example (Tetra Pak brand) — use as the primary reference for all `customProperties` sections
- `../themes/theme-template.json` — Annotated template with BRAND_* placeholders — start here when creating a new theme

## API Examples

**List all themes:**
```
GET /api/customization/themes
```

**Get a theme:**
```
GET /api/customization/themes/{id}
```

**Create a theme:**
```
POST /api/customization/themes
Body: { "name": "my-theme", "content": { "variables": {...}, "customProperties": {...} } }
```

**Update a theme:**
```
PUT /api/customization/themes/{id}
Body: { full theme object }
```

**Apply to embedded dashboard:**
```
/managed/Dashboard/{dashId}?theme={themeId}
```

## System themes available

- `modern` — Default light theme (Source Sans Pro)
- `dark` — Dark mode
- `composer` — Legacy Composer style
- `d+a_light` — D+A light variant
- `__platform__` — Platform base theme

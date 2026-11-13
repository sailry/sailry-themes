# Sailry themes

Official theme packages for [Sailry](https://sailry.dev), maintained independently
from the [application](https://github.com/sailry/sailry-harness). Each package
owns its manifest, artwork and provenance; Sailry owns the reusable importer
and renderer. See [AGENTS.md](AGENTS.md) for repository rules and
[SOURCE.md](SOURCE.md) for the initial source revision.

## Repository and catalog

The application checks out this repository as its `themes/` Git submodule.
Clone both repositories with:

```sh
git clone --recurse-submodules https://github.com/sailry/sailry-harness.git
```

For an existing application checkout, run
`git submodule update --init --recursive`. The parent Gitlink pins one exact
commit; it does not track this repository's latest branch automatically.
When editing a detached submodule, select a working branch, commit here, and
commit the reviewed `themes/` pointer separately in the application repository.
Publish the theme commit before a parent commit that references it. Publishing
one repository does not publish uncommitted or unpublished changes in the other.

`catalog.json` is the generated v1 discovery index. Its `themes` entries contain
the manifest's display metadata, relative package `path`, and canonical package
`digest`. Each entry also lists exact `resources` with relative `path`, encoded
`bytes` and individual SHA-256 `digest`; `theme.json` is included once. `modes`
lists the required light and dark variants. `previews` maps those modes to their
existing `background.window` resource, when present. A preview is artwork, not a
rendered application screenshot.

Optional `market.json` beside a theme manifest contains only
`description_locales`, a map of supported Sailry locales to translated display
text. The generator copies it into the catalog. This presentation metadata is
not installed and does not change the canonical package digest. Keep strict
`theme.json` free of catalog-only fields.

Consumers resolve the official repository ref to one immutable Git commit, then
read the index and every selected resource from that same commit. The official
source is `https://github.com/sailry/sailry-themes`; resources can be acquired from
`https://raw.githubusercontent.com/sailry/sailry-themes/<commit>/<path>/<resource>`.
No release archive is required or advertised. Verify each resource's encoded size
and digest, the complete canonical package digest, and Sailry's strict importer
before installation. Metadata or cached previews alone do not mean package
resources are available offline. The repository supplies data; it does not start
application requests or install themes automatically.

```sh
python3 scripts/catalog.py
python3 scripts/catalog.py --check
python3 -m unittest discover -s scripts/tests -v
```

These commands use Python 3.12 or newer with no dependencies. The check mode is
read-only and rejects a stale index. It validates index metadata, local resource
paths and encoded resource budgets; it does not parse Kit theme fields, decode
images or replace Sailry's strict import validator.

New official packages start at `package_version: "0.1.0"`. Content changes,
including package-local market metadata, increment the semantic version; ordinary
updates increment the patch. Only strictly newer SemVer precedence offers an
update. Same-version content changes, build metadata alone and older versions do
not offer updates. The current manifest and catalog formats use numeric `1`,
independently of each package's release version. A package digest is
SHA-256 over `theme.json` and its distinct referenced resources, sorted by their
relative paths. Hash input starts with `Sailry theme package v1` and a zero byte;
each path and file uses an unsigned 64-bit big-endian byte length followed by
its UTF-8 path or file bytes. Unreferenced artwork, guides and tests are excluded.
Consumers compare semantic version precedence before offering an update and
verify digests when acquiring its immutable resources. An update must preserve
the selected theme ID and appearance mode and retain the previous package on
failure. A digest identifies content; it is not an authorization grant.

## Importing

Each ID-named directory here is a portable v1 theme source. Import a directory or ZIP
from Settings → Appearance → Import. Imported packages are stored under
`<profile>/desktop/themes/<id>/`. Application builds embed the reviewed `themes/`
submodule snapshot through `bundled.go`; that snapshot also supplies offline
catalog resources. Editing a source directory does not replace an installed copy.

Importing a package with an installed ID replaces that theme, regardless of its
release version. Selection and light/dark mode are preserved; an active theme
refreshes immediately. The complete verified snapshot replaces old resources.
Failed replacement restores the previous package when possible; an unsuccessful
restore is reported as uncertain and retains the previous files for recovery.

The theme card's native context menu offers Apply, Details, Homepage, Export and
Uninstall. Export creates a ZIP with `theme.json` at its root and the referenced
assets. ZIP import also accepts one containing folder. A theme's optional
`homepage` must be an HTTP or HTTPS URL; themes without one disable that menu item.

A package contains `theme.json` and local raster resources under `assets/`.
The manifest requires `version: 1`, an ID matching its installed directory,
a name, author/license metadata, and both `light` and `dark` variants.
Optional `description` introduces the theme. Official themes require a valid
SemVer `package_version`; local imports may omit it. `license.name` summarizes
the license without replacing `license.text`.
The numeric `version` remains the manifest format version, not a release version.
Provided descriptions must be nonblank and at most 4 KiB, with ordinary line breaks
and tabs allowed. Release versions and license names must be nonblank, single-line
strings of at most 64 and 160 UTF-8 bytes, respectively.
Colors and sizing in each variant's `theme` use Sailry's `Config` and validation
in `internal/desktop/theme`, rendered through MyGo and Kit. Omitted values inherit
the application's configured defaults.

## Composer and buttons

Each variant may set `composer.border_width` (0–4 logical pixels). The color uses
Kit's `input.border` token; the surface and radius retain their Kit theme tokens.
The default width is zero.

The optional `composer.top_left` and `composer.bottom_right` assets draw fixed-size,
transparent corner ornaments. Their `height` is the square size (16–96 pixels).
Decorations paint behind content without taking input focus or installing actions.

`icon.send` and `icon.stop` replace the two distinct button glyphs.
`button.send` and `button.stop` optionally add image textures beneath them.
By default button colors and gradients use the `button.primary.*` Kit tokens.
Optional `composer.send` and `composer.stop` objects independently define solid
`background`, `foreground`, `hover`, and `active` colors through Kit's custom
button variant. All four colors are required when an object is present. Raster
glyphs keep their original colors; omit the icon asset to use a Kit vector glyph
in the action foreground color. Kit still owns
hover, pressed, disabled, keyboard activation and accessible names. Missing image
resources use the normal controls; the send image never substitutes for Stop.

## Welcome cards

Each variant's `cards` object accepts `explore`, `build`, `review` and `plan`.
Each card may configure solid `background`, `foreground`, `detail`, `icon`,
`hover`, `active` and `border` colors; `border_width` (0–4 pixels); and
`radius` (0–32 pixels). Omitted fields retain the existing Kit-based appearance.
The matching `icon.explore`, `icon.build`, `icon.review` and `icon.plan` assets
replace individual 24-pixel glyphs. Labels, prompt actions and responsive layout
remain application-owned.

Explicit card backgrounds use their configured color and alpha directly;
hover and active colors may also include alpha (`#RRGGBBAA`). Omitted backgrounds
retain Kit's normal tint. Optional `background.card.explore`,
`background.card.build`, `background.card.review` and `background.card.plan`
assets add noninteractive textures, clipped to the card radius behind its content.

## Window backgrounds and sidebar headings

`background.window` draws once behind the entire Shell, including navigation,
the feature rail and title bar. Existing surface transparency settings control
how much of it shows through. `background.content` and `background.sidebar` are
separate optional foreground decorations; omit them for a continuous wallpaper.

Sidebar group headings have default Kit icons. The `icon.group.hosts`,
`icon.group.activity`, `icon.group.unassigned`, `icon.group.projects` and
`icon.group.recent` assets replace their 16-pixel glyphs without changing group
labels, disclosure controls or keyboard interaction.

## Raster decorations

PNG, JPEG, WebP and GIF resources are supported; SVG and remote URLs are rejected.
Use transparent PNG for art shared across light and dark modes. Each variant can
set its own `opacity` (0–1), `alignment` ([horizontal, vertical], each 0–1),
`fit` and `height`. `cover` fills and crops, `contain` preserves the whole image,
and `fill` stretches it. Background slots also accept `tile`, which repeats
without stretching at `tile_size` logical pixels wide (32–1024, default 256),
preserving the image's aspect ratio. Repeating textures must have matching edges.

The Great Sage package uses a transparent gold-and-vermilion landscape as a
window wallpaper with `cover`, and reduces decoration opacity in light mode.
Its translucent cards share a small repeating grain texture and themed icons.
Compress production PNGs and size small ornaments/icons for their displayed size;
large wallpapers should retain enough detail for the window.

## Message surfaces and wordmark

`messages.user` and `messages.assistant` accept optional solid `background`,
`foreground` and `border` colors, `border_width` (0–4 pixels) and `radius`
(0–32 pixels). Omitted values preserve the current Kit message slots. The user
style covers sent and pending prompts, including inline editing; the assistant
style covers the message body, leaving status headers and action footers separate.
Markdown body text follows the configured foreground; links, code and status
colors retain their semantic roles. These refinements do not replace selection,
copy, reference links or editing behavior.

Optional `message.user.top_left`, `message.user.bottom_right`,
`message.assistant.top_left` and `message.assistant.bottom_right` assets add
transparent corner ornaments (16–96 pixels), clipped within the surface.

`wordmark.foreground` and `wordmark.glow` independently color the welcome page's
square particles and their illumination. Defaults follow Kit's foreground.

`button.new_session` overlays an eventless, full-width top-edge ornament on the
sidebar's existing New Conversation button. Its `height` is 4–96 pixels; a thin
transparent PNG preserves the label and Kit's fill and interaction states.
New-session artwork is clipped to the Kit button's outer rounded bounds. Its
configured height is capped at the button height; shorter strips leave the rest
of the overlay transparent. Decoration never creates an inset border or changes
button hit testing.

## Decorative animation

Settings → Appearance → Theme animation controls all theme motion. The choice
is saved locally, applies immediately and survives theme/mode changes. It defaults
to enabled. Kit's reduced-motion state removes these layers; inactive
windows keep a static frame without scheduling decorative redraws.

Each light/dark variant may define `effects`, independently of its static assets:

```json
"effects": {
  "background.content": [
    {
      "kind": "twinkle", "color": "#8DEAFF", "count": 24,
      "opacity": 0.7, "size": 4, "duration": 8, "seed": 61
    }
  ]
}
```

Targets are `background.window`, `background.content`, `background.sidebar`,
`conversation`, `hero.new_session` and the existing `banner.*` slots. Background
and conversation effects also work without an image; hero/banner targets require
their corresponding artwork to establish the region's height. Hero effects paint
behind the illustration. Window effects paint above the wallpaper and beneath
the Shell's translucent surfaces. Conversation effects paint beneath content
and remain clipped to their container. These inert layers do not capture clicks,
focus, scrolling or text selection.

For clearly visible particles, use `background.content` and `background.sidebar`:
they paint after the panel tint and before controls. Reserve `background.window`
for ambient motion behind the glass. Start with 3–5 pixel particles and adjust
their opacity for the artwork; pale particles suit dark variants, while deeper
colors remain visible on light surfaces. Do not brighten the wallpaper to
compensate for particles hidden by a panel tint.

Kinds are `twinkle` (stars), `embers` (rising sparks), `dust` (drifting specks),
`petals` (falling curved petals), `pulse` (soft halo) and `scan` (moving light line).
`color` uses Kit's solid color syntax; `opacity` is 0–1, `size` is 0.5–12 logical
pixels and `duration` is one loop in seconds (3–120). `seed` is an optional unsigned
32-bit value for repeatable placement. Each target accepts 1–4 layers, each layer
1–64 particles, and each variant at most 192 particles. Pulse and scan require
`count: 1`; their extent follows the target bounds. Motion uses Kit's animation
clock, capped at 20 redraws per second, with stable loops across viewport changes.
GIF artwork remains static; these effects do not add a video or script runtime.

Import and export use the application's theme parser. The installed application
must support the declared theme fields. Static artwork remains when theme
animation is disabled.

## Chart colors

Conversation charts use Kit's semantic colors. Set these tokens under
`light.theme.colors` and `dark.theme.colors` independently:

| Token | Use |
| --- | --- |
| `chart.1`–`chart.5` | Category and series palette, including pie slices and Sankey nodes |
| `chart.2` | Default line, bar, area and radar series |
| `chart.bullish`, `chart.bearish` | Rising and falling candlesticks |
| `chart.grid` | Chart grid lines |
| `foreground`, `muted.foreground` | Normal text and subdued axis labels |

Omitted chart tokens inherit Kit defaults. Choose distinct series colors with
enough contrast against each variant's conversation background.

## Global control colors

The theme's `colors` already exposes Kit's global button treatments:
`button.background`, `button.foreground`, `button.hover.background` and
`button.active.background`, plus the same fields under `button.primary`,
`button.secondary`, `button.danger`, `button.info`, `button.success` and
`button.warning`. Background fields accept gradients. Ghost controls use the
semantic secondary foreground, accent hover and button active colors; disabled
states remain Kit-derived.

Tabs use `tab.background`, `tab.foreground`, `tab.active.background`,
`tab.active.foreground`, `tab_bar.background` and
`tab_bar.segmented.background`. Segmented controls draw the selected segment
with `background` over the segmented track, so `tab.active.foreground` must
contrast with both `tab.active.background` and `background`, and the track must
differ visibly from `background`. Underline tabs also draw `tab.active.foreground`
directly on the page surface.

Switches expose `switch.background` for the unchecked track and
`switch.thumb.background` for the thumb. The checked track uses
`primary.background`; `button.primary.background` independently controls
primary buttons.

## Checking packages

Run the catalog and fixture commands in [Repository and catalog](#repository-and-catalog)
for package metadata, local paths and resource budgets. The application owns its
strict manifest parser, raster decoding, import/export behavior and interaction
checks in `internal/desktop/theme` and the Desktop feature packages.

From the application checkout, the theme package's existing tests are:

```sh
unset GOROOT
export GOTOOLCHAIN=go1.27.3 CGO_ENABLED=0
go test ./internal/desktop/theme
```

Use Settings → Appearance → Import in an isolated development profile to check a
specific directory or ZIP with the production parser and inspect both variants.
Theme asset changes can be imported into an existing application binary; changes
to its parser or renderer require a new build. Static catalog checks do not prove
rendered contrast, clipping, native interaction or platform acceptance.

Keep package-specific checks focused on distinctive artwork or design behavior.
Application loader and interaction tests use temporary fixtures and remain in the
application repository.

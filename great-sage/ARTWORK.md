# Great Sage artwork

Original Sun Wukong / Great Sage theme artwork generated with the built-in OpenAI
imagegen tool. The hero and landscape come from an approved AI-generated
full-window concept; the lower-right corner used the generated upper-left
ornament as its edit target. No external game artwork was imported. Package and artwork are
licensed under Apache-2.0, as specified in `theme.json`.

Production assets are compressed indexed PNGs with transparency. The landscape
retains its generated resolution; the hero and corner ornaments are
sized for their display roles. The package shares artwork across variants and
sets background opacity separately for light and dark modes.

## Generation prompts

### hero.png

Generated with gpt-6.1-sol from the approved full-window concept, which was
itself generated from a text description over a screenshot of Sailry's
unthemed layout, with no character or pose reference. Prompt:

From the attached mockup, paint ONLY the Monkey King as a standalone cutout for compositing: the same character, costume, painting style, airborne pose with the golden staff swung overhead in both hands, and his flowing red ink-wash cape, seen from behind at an angle. He has NO tail. Full body including the whole staff and cape, fully inside the frame with margin. No UI, no text, no clouds, no mountains, no palace, no background scenery. Background: a perfectly flat, uniform chroma-key green #00FF00 everywhere around him, with no shadows, glow or gradients on it, and no green anywhere on the character.

The green ground was keyed to alpha with spill removed, then the figure was
trimmed, scaled to 720 pixels high and indexed.

### background.png

Generated with gpt-6.1-sol from the same approved concept. Prompt:

From the attached mockup, paint ONLY its background scenery as a window wallpaper: the same painting style, black/gold/red palette, golden Heavenly Palace on the sea of clouds, waterfalls, layered ink mountains, golden river, gold-outlined auspicious clouds, gold dust and red silk ribbons and crimson ink smoke. NO UI, NO text, NO wordmark, NO people or characters, NO Monkey King and no staff. Keep the centre (where the wordmark, composer and cards sit) darker and calmer; the detail lives at the edges and the top. The left quarter (behind the sidebar) stays dim and quiet.

The painting was scaled to 1600 by 1000 and indexed; its near-black ink is
fully transparent, so the theme background shows there unchanged.

### cloud-top-left.png

Use case: illustration-story. Asset type: reusable transparent auspicious-cloud corner ornament for a black, gold and red Chinese Great Sage desktop theme. Generate ONE square PNG with genuine transparent background. A delicate antique-gold engraved Chinese 祥云 cloud curl ornament occupies the upper-left corner and extends right and down in a loose L shape. Very sparse flowing gold outlines, a tiny muted crimson ink accent, generous fully transparent negative space over the remaining lower-right 75 percent. All strokes inside canvas with comfortable margin. Designed to be shown at 48 pixels, simplified clear cloud curls with moderate stroke width. No text, no monkey, no scene, no black rectangle, no checkerboard painted into image, no frame, no gold-filled panels. Elegant restrained Chinese gold-ink ornament.

### cloud-bottom-right.png

Use case: precise-object-edit. Project asset: transparent lower-right cloud corner decoration. Input image is the edit target. Rotate the entire existing gold and red upper-left L-shaped cloud ornament by exactly 180 degrees to form a lower-right L-shaped ornament. Preserve its gold engraved cloud artwork, red accents, relative proportions and genuine transparent background. Output only the rotated transparent artwork, no black fill, no text, no UI, no new objects.

### Retired send glyph

The raster glyph was removed in favor of Kit vector glyphs that follow the
composer action foreground in each variant. Its original generation prompt is
retained for provenance.

Use case: ui-mockup. Project asset: ONE small transparent PNG send-button glyph for an original Great Sage Sun Wukong theme. Centered square canvas. A clear bold UPWARD ARROW with a straight shaft subtly resembling a red-and-black Ruyi Jingu Bang staff, two tiny ornamental bands. The arrowhead must remain unmistakably an upward send arrow. Flat warm ink black silhouette with a tiny vermilion accent, NOT gold (it will appear on a gold circular button). Very simple graphic designed for legibility at 16px, thick strokes, minimal detail, occupies central 70% of canvas. Genuine transparent background. No button circle, no background, no glow, no shadow, no text, no other objects, no watermark.


### Card and heading icons

Use case: stylized-concept. Generate one small square transparent raster icon per asset for the Great Sage theme. Simple elegant bold silhouettes, antique gold and warm black thick ink outlines, restrained vermilion accents, clear at 24 logical pixels, central 75 percent, very few details, original flat engraved brush art. No photorealism, badge, scene, text or watermark.

- `explore.png`: one golden auspicious cloud with three curled lobes and a flowing red tail, suggesting exploration and travel
- `build.png`: one red-and-gold Ruyi Jingu Bang staff diagonally ascending, gold bands at both ends and a dark vermilion shaft
- `review.png`: one bold gold almond eye with a vermilion pupil and two controlled flame strokes, suggesting inspection
- `plan.png`: one ivory and antique-gold rolled scroll with short black ink marks rather than letters and a small vermilion ribbon

The sidebar reuses these original illustrations at 16 pixels. Production icons are compressed to 96 × 96 pixels.

### grain.png

Use case: stylized-concept. Subtle seamless tileable transparent square PNG texture for small dark-gold-red Chinese mythology cards. Only sparse antique bronze and muted gold dry-brush fibers, fine dust and tiny ink speckles, dispersed with matching edges. Genuine transparent alpha across most pixels, no paper or black rectangle. Delicate irregular grain, low contrast at reduced opacity over brown or ivory panels. No clouds, mountains, scene, shapes, text, icons, frames, broad washes or painted checkerboard.

### Button edge gilding

The rejected inset circlet frame was replaced with broken gold leaf at the actual
button edges. No separate capsule outline is included. The `button.new_session`
slot uses full-width fill at 32 logical pixels and 65% opacity, matching the Kit
button's bounds and corner clip. The texture has no geometric frame to distort,
and its transparent center leaves the live caption untouched. The 768 × 258
indexed PNG retains generated alpha; downsizing and palette compression are the
only postprocessing. The frame resource was removed from the package.

The existing `grain.png` is reused as a content-panel texture as well as on cards.
It tiles at its native 256-pixel size without generating another image. Primary
buttons use solid warm-black fills. Send and Stop use separate high-contrast
solid fills with Kit vector glyphs.

Generated with the built-in OpenAI imagegen tool using this prompt:

Use case: stylized-concept. Asset type: transparent gold-leaf EDGE TEXTURE overlay for a Sun Wukong burgundy lacquer UI button. Generate original gilding texture only, NOT a frame or object. Wide 3:1 canvas, genuine transparent alpha. Fine irregular antique gold leaf fragments and tiny burnished gold engraved streaks MUST TOUCH the actual canvas boundaries: a refined patch along the top-left edge, thinning out along the upper edge; a smaller balanced patch along the bottom-right edge, thinning along the bottom edge. The gold looks fused into worn red lacquer, but DO NOT paint any red or button surface: only the gold pixels are present. Edge zones are at most the outermost 12 percent of canvas height, and the two corner patches cover at most 18 percent of width. Keep the entire central 75 percent completely transparent for live text. Gold leaf has convincing bright micro-highlights, etched grooves, aged bronze shadows and sparse tiny flakes. Flat irregular gilded edge detail with understated luxuriant material finish, no glow. There must be NO enclosed loop, NO complete outline, NO capsule, NO oval, NO rounded rectangle, NO inner rim, NO clouds, NO circlet, NO central flourish, NO text, NO label, NO button background, NO border offset from image edges, NO transparent padding outside the outermost gold. Texture is intended to stretch across a 223x32px button, with corners clipped by the real button's radius, so avoid recognizable shapes that stretching would distort. Only the upper-left and lower-right EDGE gold textures, on transparent background.

### Send glyph refinement

Use case: precise-object-edit. Edit target: supplied small transparent upward send-arrow glyph. Change only the ink-black shaft and arrowhead to bright warm ivory-gold, preserving the same bold simple UP arrow shape, two little red staff bands, centered proportions and genuine transparent alpha. It will appear at 16px on a dark burgundy button. The shaft and arrowhead must be highly legible, thick and flat. No background, glow, shadows, new ornaments or circle.

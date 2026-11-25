# Directing guide: story, camera, light

## Script
- Length: 150 wpm. 30 s = 75 words, 45 s = 110, 60 s = 150. Shorter sentences than you think.
- Beat sheet for 30-60 s: hook (0-3 s: a question, a contradiction or a strange fact) -> setup (who/where/when) ->
  escalation (2-3 beats, each reveals something new) -> turn -> payoff line -> optional loop back to the first image.
- One idea per sentence; one visual per sentence. If you cannot picture a sentence, rewrite it.
- Numbers, dates and names: write them as spoken ("nineteen fifty-three") in `script`.

## Shot list (write it before code)
`t-range | location | what is in frame | camera move | on-screen text | sfx`.
Locations should be physically adjacent in the world so the camera can travel between them in one move
(through a door, down a street, through a window, into a painting frame that is a real object in the world).

## Camera
- One continuous take looks expensive and avoids cut logic. Keys every 2-5 s; let the Catmull-Rom path do the rest.
- fov 35-45 for intimate/dramatic, 50-60 for establishing/travel. Animate fov a little (4-8 degrees) on emphasis lines.
- Eye height 1.4-1.7 for human POV; low (0.4-0.8) for power/menace; high (6+) for map-like overview.
- Move toward the thing being said. Push in on revelations, pull back on consequences.
- Avoid moving faster than about 6 units/s at 30 fps unless it is a whip move; motion blur is not simulated.
- `look` target should lead the position along the path so the camera looks where it is going.

## Light and look
- Three-light rule: one cool or warm key with shadows, one soft fill (hemisphere/ambient, low), warm practical lights
  (lamps, windows) as point lights without shadows. Only one shadow-casting light (performance).
- Fog (`FogExp2`, density 0.02-0.04) hides far geometry, gives depth and lets you place objects out of sight until needed.
- Mood palettes: night = #101626 sky, warm #ffb066 practicals; day = #9ec9ff sky, #fff1d6 key; tension = desaturated, high contrast.
- ACESFilmic tone mapping, exposure 1.0-1.2. Emissive materials (windows, screens) make a scene feel lit and cheap to render.
- Readability: keep the subject lighter or warmer than the background; keep the lower 20% of a 9:16 frame free for captions.

## Characters (stylized 3D, readable)
- Use `createCharacter`: articulated mannequin with face (blink, mouth flap, mood), walk cycle from a `makePath`, gestures per spoken word.
- Give each character a distinct silhouette: height, shirt colour contrasting the background, hair style.
- `lookAt` makes characters turn their heads toward each other: it sells interaction for free.
- Props that matter to the story (a note, a coin, a key) are real meshes (`documentMesh`, `box`, `picture`) with a close-up moment.
- Depth of field follows `focusPoint`: pass the character or prop the narration is about.

## Pacing check before final render
Watch the preview with captions on. Every sentence needs a visual change or camera move within 3 s. If a 4 s stretch has
neither, add a prop reveal, a push-in, or an sfx accent.

/**
 * Lemo-Opuscar <-> 3D-Animator Style & Post-FX Bridge (Version 3)
 * Loads real palette tokens from /plugin/skills/lemo-opuscar/styles/<slug>/STYLE.md + style.json
 * and provides conflict-free single-pass post-processing ('hdr' | 'gtao' | 'crt' | 'none').
 */

const CURATED_FALLBACK_PALETTES = {
  'dark-documentary': { bg: '#05080c', primary: '#b3dbff', accent: '#f2c48d', wall: '#101620', isDark: true },
  'archive-lighttable': { bg: '#161411', primary: '#f4efe4', accent: '#d0312d', wall: '#242019', isDark: true },
  'briefing-board': { bg: '#f2f0eb', primary: '#1e242b', accent: '#d0312d', wall: '#dfe2e6', isDark: false },
  'blueprint': { bg: '#071a45', primary: '#dcebff', accent: '#ff8c78', wall: '#0a2457', isDark: true },
  'circuit-board': { bg: '#06140c', primary: '#5df59b', accent: '#ffd166', wall: '#0c2416', isDark: true },
  'comic-history': { bg: '#f2ead7', primary: '#1e1b18', accent: '#d0312d', wall: '#e4d8bd', isDark: false },
  'chalkboard': { bg: '#131d17', primary: '#f1f5f0', accent: '#f59e0b', wall: '#19261e', isDark: true },
  'ascii-crt': { bg: '#050b07', primary: '#4ade80', accent: '#f97316', wall: '#09120c', isDark: true },
  'watercolor': { bg: '#f3e2c8', primary: '#2d241c', accent: '#c8442a', wall: '#e8dcc6', isDark: false },
  'halftone-dossier': { bg: '#f4ebd9', primary: '#1d2230', accent: '#d0312d', wall: '#e5dac3', isDark: false }
};

const SLUG_ALIASES = {
  'newspaper-clipping': 'caption-news',
  'watercolor-wash': 'watercolor',
  'paper-cutout': 'paper-popup',
  'claymation': 'brick-toy',
  'woodcut-print': 'woodcut',
  'sumi-e-ink': 'ink-wash',
  'vhs-glitch': 'ascii-crt',
  'synthwave': 'neon-tubes',
  'analog-film': 'silent-film',
  'chalkboard-lecture': 'chalkboard',
  'copper-engraving': 'engraving',
  'infrared-surveillance': 'thermal-camera',
  'kinetic-typography': 'text-flash-cuts',
  'oil-impasto': 'impasto',
  'origami-journey': 'paper-popup',
  'sand-art': 'ink-wash',
  'gameboy-pixel': 'pixel-rpg',
  'teletext': 'ascii-crt',
  'cad-wireframe': 'hardcore-info',
  'schematic': 'blueprint'
};

function hexLum(hex) {
  const n = parseInt(hex.slice(1), 16);
  const r = ((n >> 16) & 255) / 255;
  const g = ((n >> 8) & 255) / 255;
  const b = (n & 255) / 255;
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export async function loadLemoStyle(rawSlug) {
  if (!rawSlug || rawSlug === 'none') return null;
  const slug = SLUG_ALIASES[rawSlug] || rawSlug;
  const curated = CURATED_FALLBACK_PALETTES[slug];

  let meta = { slug, en: slug };
  let colors = [];
  let mdText = '';

  let loadedViaMeta = false;
  try {
    const r = await fetch(`/lemo-meta/${encodeURIComponent(slug)}`);
    if (r.ok) {
      const payload = await r.json();
      loadedViaMeta = true;
      if (payload.exists) {
        if (payload.meta) meta = payload.meta;
        if (payload.mdText) {
          mdText = payload.mdText;
          const hexMatches = mdText.match(/#[0-9a-fA-F]{6}\b/g) || [];
          colors = [...new Set(hexMatches)];
        }
      }
    }
  } catch {}

  if (!loadedViaMeta) {
    try {
      const r = await fetch(`/plugin/skills/lemo-opuscar/styles/${encodeURIComponent(slug)}/style.json`);
      if (r.ok) meta = await r.json();
    } catch {}

    try {
      const r = await fetch(`/plugin/skills/lemo-opuscar/styles/${encodeURIComponent(slug)}/STYLE.md`);
      if (r.ok) {
        mdText = await r.text();
        const hexMatches = mdText.match(/#[0-9a-fA-F]{6}\b/g) || [];
        colors = [...new Set(hexMatches)];
      }
    } catch {}
  }

  const sortedByLum = [...colors].sort((a, b) => hexLum(a) - hexLum(b));
  const looksLight = curated
    ? !curated.isDark
    : (/\b(cream|warm paper|white paper|manila|parchment|off-white|pastel|ivory)\b/i.test(mdText) &&
       !/\b(night|near-black|dark lacquer|black lacquer|dark studio)\b/i.test(mdText.slice(0, 500)));

  const defaultLight = { bg: '#f4efe4', primary: '#1e222a', accent: '#d0312d', wall: '#e5ddd0', isDark: false };
  const defaultDark = { bg: '#0c1018', primary: '#eae3d2', accent: '#d0312d', wall: '#1a202c', isDark: true };
  const fallback = curated || (looksLight ? defaultLight : defaultDark);

  let bg = fallback.bg;
  let primary = fallback.primary;
  let accent = fallback.accent;
  let wall = fallback.wall;

  if (!curated && sortedByLum.length >= 2) {
    bg = looksLight ? sortedByLum[sortedByLum.length - 1] : sortedByLum[0];
    primary = looksLight ? sortedByLum[0] : sortedByLum[sortedByLum.length - 1];
    accent = colors.find((c) => c !== bg && c !== primary) || fallback.accent;
    wall = bg;
  }

  return {
    slug: meta.slug || slug,
    title: meta.en || slug,
    bg,
    primary,
    accent,
    wall,
    allColors: colors.length ? colors : [bg, primary, accent, wall],
    isDark: !looksLight
  };
}

/**
 * Single clean post-processing pass ('hdr' | 'gtao' | 'crt' | 'none').
 * When mode === 'crt', Three.js renders onto `glSourceCanvas` and Lemo crt.js draws onto `stageCanvas`
 * so the two WebGL contexts never collide on the same canvas.
 */
export async function createPostController(mode, { renderer, glSourceCanvas, scene, camera, stageCanvas, width, height }) {
  if (mode === 'gtao') {
    const { makePost } = await import('/plugin/skills/lemo-opuscar/core/three/post.js');
    const post = makePost(renderer, scene, camera, width, height, { ssaa: 1, ao: true, aoAmt: 0.65 });
    post.bloom.strength = 0.18;
    return {
      mode: 'gtao',
      render(focusDist = 2.0) {
        post.dof.focus = Math.max(0.2, focusDist);
        post.dof.aper = 3.2;
        post.dof.maxCoc = 12;
        post.composer.render();
      }
    };
  }

  if (mode === 'crt') {
    const crtMod = await import('/plugin/skills/lemo-opuscar/core/post/crt.js');
    const crtPost = crtMod.makePost(stageCanvas);
    return {
      mode: 'crt',
      render(_focusDist = 2.0, t = 0) {
        renderer.render(scene, camera);
        crtPost.render(glSourceCanvas, null, Math.round(t * 30), null, {
          scan: 0.16,
          grille: 0.08,
          bleed: 6,
          rshift: 2,
          power: 1.0,
          track: 0.0
        });
      }
    };
  }

  return { mode: mode || 'hdr', render: null };
}

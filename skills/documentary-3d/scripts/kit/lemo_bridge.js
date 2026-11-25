/**
 * Lemo-Opuscar <-> 3D-Animator Style & Post-FX Bridge (Version 3)
 * Loads real palette tokens from /plugin/skills/lemo-opuscar/styles/<slug>/STYLE.md + style.json
 * and provides conflict-free single-pass post-processing ('hdr' | 'gtao' | 'crt' | 'none').
 */

const CURATED_FALLBACK_PALETTES = {
  'dark-documentary': { bg: '#05080c', primary: '#b3dbff', accent: '#f2c48d', wall: '#101620', isDark: true },
  'archive-lighttable': { bg: '#161411', primary: '#f4efe4', accent: '#d0312d', wall: '#242019', isDark: true },
  'briefing-board': { bg: '#11191d', primary: '#eae3d2', accent: '#d0312d', wall: '#26281c', isDark: true },
  'blueprint': { bg: '#071a45', primary: '#dcebff', accent: '#ff8c78', wall: '#0a2457', isDark: true },
  'circuit-board': { bg: '#06140c', primary: '#5df59b', accent: '#ffd166', wall: '#0c2416', isDark: true },
  'comic-history': { bg: '#f2ead7', primary: '#1e1b18', accent: '#d0312d', wall: '#e4d8bd', isDark: false },
  'chalkboard': { bg: '#131d17', primary: '#f1f5f0', accent: '#f59e0b', wall: '#19261e', isDark: true },
  'ascii-crt': { bg: '#050b07', primary: '#4ade80', accent: '#f97316', wall: '#09120c', isDark: true }
};

export async function loadLemoStyle(slug) {
  if (!slug || slug === 'none') return null;
  const fallback = CURATED_FALLBACK_PALETTES[slug] || {
    bg: '#0c1018',
    primary: '#eae3d2',
    accent: '#d0312d',
    wall: '#1a202c',
    isDark: true
  };

  let meta = { slug, en: slug };
  let colors = [];

  try {
    const r = await fetch(`/plugin/skills/lemo-opuscar/styles/${encodeURIComponent(slug)}/style.json`);
    if (r.ok) meta = await r.json();
  } catch {}

  try {
    const r = await fetch(`/plugin/skills/lemo-opuscar/styles/${encodeURIComponent(slug)}/STYLE.md`);
    if (r.ok) {
      const md = await r.text();
      const hexMatches = md.match(/#[0-9a-fA-F]{6}\b/g) || [];
      colors = [...new Set(hexMatches)];
    }
  } catch {}

  return {
    slug: meta.slug || slug,
    title: meta.en || slug,
    bg: colors[0] || fallback.bg,
    primary: colors[1] || fallback.primary,
    accent: colors[2] || fallback.accent,
    wall: colors[3] || fallback.wall,
    allColors: colors.length ? colors : [fallback.bg, fallback.primary, fallback.accent, fallback.wall],
    isDark: fallback.isDark
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

// Look presets: pick with story.look ("noir" | "warm" | "day" | "clean"); override any key with story.lookOverrides.
export const LOOKS = {
  noir:  { sky: 0x0b1020, fog: 0.035, hemi: [0x5a70b0, 0x120d0a, 0.55], key: { color: 0xaec4ff, i: 0.9, pos: [-8, 14, 6] }, practical: 0xffb066,
           exposure: 1.1, bloom: { strength: 0.5, radius: 0.6, threshold: 0.8 }, dof: { aperture: 0.0005, maxblur: 0.01 }, grain: 0.03, vignette: 0.5 },
  warm:  { sky: 0x2a1a12, fog: 0.03, hemi: [0xffd2a1, 0x2b1a10, 0.7], key: { color: 0xffc78a, i: 1.1, pos: [6, 10, 6] }, practical: 0xffa04d,
           exposure: 1.15, bloom: { strength: 0.45, radius: 0.5, threshold: 0.82 }, dof: { aperture: 0.0005, maxblur: 0.01 }, grain: 0.03, vignette: 0.45 },
  day:   { sky: 0xa9cdf5, fog: 0.012, hemi: [0xdcecff, 0x7a6a58, 0.9], key: { color: 0xfff1d6, i: 2.2, pos: [10, 18, 8] }, practical: 0xffd9a0,
           exposure: 1.0, bloom: { strength: 0.25, radius: 0.5, threshold: 0.9 }, dof: { aperture: 0.0004, maxblur: 0.008 }, grain: 0.015, vignette: 0.3 },
  clean: { sky: 0xeef1f6, fog: 0.006, hemi: [0xffffff, 0xb9c0cc, 1.0], key: { color: 0xffffff, i: 1.6, pos: [6, 12, 8] }, practical: 0xffffff,
           exposure: 1.0, bloom: { strength: 0.1, radius: 0.4, threshold: 0.95 }, dof: { aperture: 0.0003, maxblur: 0.006 }, grain: 0.0, vignette: 0.15 },
};
export const getLook = (name, overrides = {}) => ({ ...(LOOKS[name] || LOOKS.noir), ...overrides });

/**
 * Code-3D-Video Modular Combination Helper (Version 3)
 * Bridges original code-3d-video scenes (`stage.js`, `character.js`, `builders.js`) cleanly with:
 *   1) 3D-Animator 12 shaders (`styles.js`) + WhisperX mid-shot `styleAt` morphing
 *   2) Lemo-Opuscar 99 style palettes & GTAO/DOF / VHS-CRT (`lemo_bridge.js`)
 *   3) p5.brush live CanvasTextures (`p5_brush_texture.js`)
 */

export async function loadShaderBridge() {
  return await import('/plugin/skills/documentary-3d/scripts/kit/styles.js');
}

export async function loadLemoBridge() {
  return await import('/plugin/skills/documentary-3d/scripts/kit/lemo_bridge.js');
}

export async function loadBrushBridge() {
  return await import('/plugin/skills/documentary-3d/scripts/kit/p5_brush_texture.js');
}

export async function attachStyleToStage(stage, styleName = 'paper', mixMap = null) {
  const { setStyle, styleAt } = await loadShaderBridge();
  setStyle(styleName, { scene: stage.scene, key: stage.key, renderer: stage.renderer, mix: mixMap });
  return { setStyle, styleAt };
}

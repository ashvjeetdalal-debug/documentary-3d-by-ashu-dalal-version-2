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

export async function loadGLTFProp({ THREE, scene, url, targetSize = 1.2, pos = [0, 0, 0], rot = [0, 0, 0], preserveReadable = false }) {
  const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
  const gltf = await new GLTFLoader().loadAsync(url);
  const root = gltf.scene;
  root.traverse((o) => {
    if (o.isMesh) {
      o.castShadow = true;
      o.receiveShadow = true;
      if (preserveReadable) o.userData.preserveReadable = true;
    }
  });
  const b = new THREE.Box3().setFromObject(root);
  const s = b.getSize(new THREE.Vector3());
  const mx = Math.max(s.x, s.y, s.z, 0.001);
  root.scale.multiplyScalar(targetSize / mx);
  root.updateMatrixWorld(true);
  const b2 = new THREE.Box3().setFromObject(root);
  const c = b2.getCenter(new THREE.Vector3());
  root.position.set(-c.x, -b2.min.y, -c.z);
  const holder = new THREE.Group();
  holder.add(root);
  holder.position.set(...pos);
  holder.rotation.set(...rot);
  scene.add(holder);
  return holder;
}

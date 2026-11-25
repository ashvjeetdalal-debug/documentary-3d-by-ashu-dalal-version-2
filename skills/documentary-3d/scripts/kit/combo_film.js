/**
 * Glitch-Free 3D-Animator + Lemo-Opuscar Modular Scene Engine (Version 3)
 * Combines cleanly:
 *   - 3D-Animator (12 shader looks + live mid-shot morphing + HDR accumulation)
 *   - Lemo-Opuscar (99 STYLE.md palettes + core/three/post.js GTAO/DOF OR core/post/crt.js CRT)
 *   - Archival Photo Cards (userData.preserveReadable = true so photos stay crisp in all looks)
 *   - Real CC0 .glb / .gltf 3D Models (GLTFLoader with auto-centering & scale normalization)
 */
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { clamp, lerp, easeInOut, halton, hash } from './lib.js';
import { setStyle, styleAt } from './styles.js';
import { loadLemoStyle, createPostController } from './lemo_bridge.js';

function parseStyleSpec(spec) {
  if (!spec.includes(':')) return [[0, spec]];
  return spec.split(',').map((part) => {
    const [ts, look] = part.split(':');
    return [parseFloat(ts) || 0, (look || 'lit').trim()];
  }).sort((a, b) => a[0] - b[0]);
}

function loadTextureAsync(url) {
  return new Promise((resolve) => {
    new THREE.TextureLoader().load(
      url,
      (tex) => { tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8; resolve(tex); },
      undefined,
      () => resolve(null)
    );
  });
}

async function loadModelAsync(url) {
  try {
    return await new GLTFLoader().loadAsync(url);
  } catch (e) {
    console.warn('[combo_film] GLTF/GLB load failed:', url, e?.message || e);
    return null;
  }
}

export async function bootCombo({ W, H, styleSpec, lemoSlug, postMode, photoUrl, modelUrl, totalSec }) {
  const stageCanvas = document.getElementById('stage');
  // Keep stageCanvas free for 2D/WebGL2 blitting whenever HDR accumulation or CRT owns stageCanvas
  const useOffscreenGl = (postMode === 'crt' || postMode === 'hdr' || postMode === 'none');
  const glCanvas = useOffscreenGl ? Object.assign(document.createElement('canvas'), { width: W, height: H }) : stageCanvas;

  const renderer = new THREE.WebGLRenderer({
    canvas: glCanvas,
    antialias: postMode === 'gtao' || postMode === 'crt',
    preserveDrawingBuffer: true,
    powerPreference: 'high-performance'
  });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = postMode === 'gtao' ? THREE.NoToneMapping : THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.08;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const lemo = await loadLemoStyle(lemoSlug);
  const bgHex = lemo ? lemo.bg : '#0c1018';
  const wallHex = lemo ? lemo.wall : '#242c3b';
  const deskHex = lemo ? (lemo.isDark ? '#1a202c' : '#d8cfc0') : '#4c382a';
  const accentHex = lemo ? lemo.accent : '#d0312d';

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(bgHex);
  scene.fog = new THREE.FogExp2(bgHex, 0.045);

  const aspect = W / H;
  const camera = new THREE.PerspectiveCamera(aspect < 1 ? 52 : 42, aspect, 0.1, 40);

  // Studio Three-Point Lighting harmonized with Lemo palette
  const fill = new THREE.HemisphereLight(lemo ? lemo.primary : '#b8d4ff', '#1a1816', 0.85);
  scene.add(fill);

  const key = new THREE.DirectionalLight('#fff2dc', 2.4);
  key.position.set(2.4, 3.8, 2.8);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.bias = -0.0005;
  scene.add(key);

  const rim = new THREE.DirectionalLight(accentHex, 0.9);
  rim.position.set(-2.6, 2.0, -2.0);
  scene.add(rim);

  // Stage Floor & Backdrop
  const deskMat = new THREE.MeshStandardMaterial({ color: deskHex, roughness: 0.68, metalness: 0.05 });
  const desk = new THREE.Mesh(new THREE.BoxGeometry(5.5, 0.08, 3.6), deskMat);
  desk.position.set(0, -0.04, 0);
  desk.receiveShadow = true;
  desk.userData.kind = 'back';
  scene.add(desk);

  const wallMat = new THREE.MeshStandardMaterial({ color: wallHex, roughness: 0.88, metalness: 0.02 });
  const backWall = new THREE.Mesh(new THREE.PlaneGeometry(5.5, 3.6), wallMat);
  backWall.position.set(0, 1.4, -1.2);
  backWall.receiveShadow = true;
  backWall.userData.kind = 'back';
  scene.add(backWall);

  // Hero Procedural 3D Artifacts (respond cleanly to all 12 shaders)
  const heroGroup = new THREE.Group();
  heroGroup.name = 'hero_artifact';
  scene.add(heroGroup);

  const plinth = new THREE.Mesh(
    new THREE.CylinderGeometry(0.32, 0.36, 0.08, 32),
    new THREE.MeshStandardMaterial({ color: lemo ? lemo.primary : '#273040', roughness: 0.42, metalness: 0.55 })
  );
  plinth.position.set(0, 0.04, 0);
  plinth.castShadow = plinth.receiveShadow = true;
  heroGroup.add(plinth);

  const coreObj = new THREE.Mesh(
    new THREE.IcosahedronGeometry(0.24, 1),
    new THREE.MeshStandardMaterial({ color: '#c8d6e5', roughness: 0.28, metalness: 0.78 })
  );
  coreObj.position.set(0, 0.42, 0);
  coreObj.userData.heat = 0.85;
  coreObj.castShadow = true;
  heroGroup.add(coreObj);

  const ringMesh = new THREE.Mesh(
    new THREE.TorusGeometry(0.38, 0.018, 16, 48),
    new THREE.MeshStandardMaterial({ color: accentHex, roughness: 0.3, metalness: 0.5 })
  );
  ringMesh.position.set(0, 0.42, 0);
  ringMesh.castShadow = true;
  heroGroup.add(ringMesh);

  // Optional Downloaded Real 3D Model (.glb / .gltf via --model) replacing default procedural core
  let gltfMixer = null;
  let gltfHolder = null;
  if (modelUrl) {
    const normModel = (modelUrl.startsWith('/') || modelUrl.startsWith('http')) ? modelUrl : '/' + modelUrl;
    const gltf = await loadModelAsync(normModel);
    if (gltf && gltf.scene) {
      coreObj.visible = false;
      ringMesh.visible = false;
      const mdl = gltf.scene;
      mdl.traverse((o) => {
        if (o.isMesh) {
          o.castShadow = true;
          o.receiveShadow = true;
        }
      });
      const b = new THREE.Box3().setFromObject(mdl);
      const sz = b.getSize(new THREE.Vector3());
      const maxDim = Math.max(sz.x, sz.y, sz.z, 0.001);
      const scale = 0.72 / maxDim;
      mdl.scale.multiplyScalar(scale);
      mdl.updateMatrixWorld(true);
      const bScaled = new THREE.Box3().setFromObject(mdl);
      const cScaled = bScaled.getCenter(new THREE.Vector3());
      mdl.position.set(-cScaled.x, 0.08 - bScaled.min.y, -cScaled.z);

      gltfHolder = new THREE.Group();
      gltfHolder.name = 'downloaded_model';
      gltfHolder.add(mdl);
      heroGroup.add(gltfHolder);

      if (gltf.animations && gltf.animations.length) {
        gltfMixer = new THREE.AnimationMixer(mdl);
        gltfMixer.clipAction(gltf.animations[0]).play();
      }
    }
  }

  // Optional Readability-Protected Archival Evidence Card (if --photo supplied)
  if (photoUrl) {
    const normPhoto = (photoUrl.startsWith('/') || photoUrl.startsWith('http')) ? photoUrl : '/' + photoUrl;
    const tex = await loadTextureAsync(normPhoto);
    if (tex) {
      const cardGroup = new THREE.Group();
      cardGroup.name = 'archival_card';
      const frame = new THREE.Mesh(
        new THREE.BoxGeometry(0.88, 0.64, 0.02),
        new THREE.MeshStandardMaterial({ color: '#eae3d2', roughness: 0.85 })
      );
      frame.userData.preserveReadable = true;
      frame.castShadow = true;
      cardGroup.add(frame);

      const photoMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(0.80, 0.56),
        new THREE.MeshStandardMaterial({ map: tex, roughness: 0.4 })
      );
      photoMesh.position.z = 0.012;
      photoMesh.userData.preserveReadable = true;
      cardGroup.add(photoMesh);

      const pin = new THREE.Mesh(
        new THREE.SphereGeometry(0.026, 12, 12),
        new THREE.MeshStandardMaterial({ color: '#d0312d', roughness: 0.25 })
      );
      pin.position.set(0, 0.29, 0.028);
      pin.userData.preserveReadable = true;
      cardGroup.add(pin);

      cardGroup.position.set(aspect < 1 ? 0 : -0.68, 0.52, -0.35);
      cardGroup.rotation.set(-0.08, 0.18, 0.04);
      scene.add(cardGroup);
    }
  }

  // Deterministic Floating Dust Motes
  const dustCount = 80;
  const dustPos = new Float32Array(dustCount * 3);
  for (let i = 0; i < dustCount; i++) {
    dustPos[i * 3] = (hash(i * 3 + 1) - 0.5) * 3.0;
    dustPos[i * 3 + 1] = hash(i * 3 + 2) * 1.8;
    dustPos[i * 3 + 2] = (hash(i * 3 + 3) - 0.5) * 2.2;
  }
  const dustGeo = new THREE.BufferGeometry();
  dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
  const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({ color: '#ffffff', size: 0.014, transparent: true, opacity: 0.35 }));
  scene.add(dust);

  const postCtrl = await createPostController(postMode, {
    renderer, glSourceCanvas: glCanvas, scene, camera, stageCanvas, width: W, height: H
  });

  const styleTimeline = parseStyleSpec(styleSpec);
  const SHUTTER = 0.5 / 30;
  const offCtx = (postMode === 'hdr' || postMode === 'none')
    ? Object.assign(document.createElement('canvas'), { width: W, height: H }).getContext('2d')
    : null;
  const stageCtx2d = useOffscreenGl && postMode !== 'crt' ? stageCanvas.getContext('2d') : null;

  function renderSubframe(tSub) {
    const p = clamp(tSub / totalSec, 0, 1);
    const e = easeInOut(p);

    // Deterministic Hero Animation
    if (gltfHolder) {
      gltfHolder.rotation.y = tSub * 0.45;
      if (gltfMixer) gltfMixer.setTime(tSub);
    } else {
      coreObj.rotation.y = tSub * 0.65;
      coreObj.rotation.x = Math.sin(tSub * 0.4) * 0.25;
      coreObj.position.y = 0.42 + Math.sin(tSub * 1.4) * 0.03;
      ringMesh.rotation.x = Math.PI * 0.35 + tSub * 0.5;
      ringMesh.rotation.y = -tSub * 0.4;
    }

    const activeStyle = styleAt(styleTimeline, tSub, 'lit');
    setStyle(activeStyle, { scene, key, fill, renderer });
    if (scene.fog && scene.background && scene.background.isColor) {
      scene.fog.color.copy(scene.background);
    }

    // Single Eased Camera Curve
    const camZ = lerp(aspect < 1 ? 2.4 : 2.1, aspect < 1 ? 1.65 : 1.35, e);
    const camX = Math.sin(e * Math.PI) * 0.35;
    const camY = lerp(0.55, 0.72, e);
    camera.position.set(camX, camY, camZ);
    camera.lookAt(0, 0.38, -0.1);

    const focusDist = camera.position.distanceTo(new THREE.Vector3(0, 0.38, 0));
    if (postCtrl.render) {
      postCtrl.render(focusDist, tSub);
    } else {
      renderer.render(scene, camera);
    }
  }

  window.total = totalSec;
  window.renderAt = function (t, n = 4) {
    const samples = (postCtrl.mode === 'gtao' || postCtrl.mode === 'crt') ? 1 : Math.max(1, n);
    if (samples === 1 || !offCtx) {
      renderSubframe(t);
      if (stageCtx2d) {
        stageCtx2d.clearRect(0, 0, W, H);
        stageCtx2d.drawImage(glCanvas, 0, 0);
      }
      return;
    }
    const accum = offCtx;
    accum.clearRect(0, 0, W, H);
    for (let s = 0; s < samples; s++) {
      const dt = (halton(s + 1, 2) - 0.5) * SHUTTER;
      renderSubframe(Math.max(0, t + dt));
      accum.globalAlpha = s === 0 ? 1 : 1 / (s + 1);
      accum.drawImage(glCanvas, 0, 0);
    }
    accum.globalAlpha = 1;
    if (stageCtx2d) {
      stageCtx2d.clearRect(0, 0, W, H);
      stageCtx2d.drawImage(accum.canvas, 0, 0);
    }
  };
}

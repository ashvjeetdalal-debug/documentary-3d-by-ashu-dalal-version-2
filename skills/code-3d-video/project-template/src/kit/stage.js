// Stage = renderer + scene + camera + lights + optional post-processing (bloom, depth of field, vignette, grain).
// Post-processing is wrapped in try/catch: if anything about it fails the video still renders (just plainer).
import { getLook } from './looks.js';

export async function createStage({ THREE, canvas, story }) {
  const W = innerWidth, H = innerHeight;
  const look = getLook(story.look, story.lookOverrides);
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = look.exposure;

  const scene = new THREE.Scene();
  scene.background = new THREE.Color(look.sky);
  scene.fog = new THREE.FogExp2(look.sky, look.fog);
  const camera = new THREE.PerspectiveCamera(50, W / H, 0.1, 300);

  scene.add(new THREE.HemisphereLight(look.hemi[0], look.hemi[1], look.hemi[2]));
  const key = new THREE.DirectionalLight(look.key.color, look.key.i);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  const B = story.shadowBounds ?? 14;
  Object.assign(key.shadow.camera, { left: -B, right: B, top: B, bottom: -B, near: 1, far: 70 });
  key.shadow.bias = -0.0004;
  scene.add(key, key.target);

  // ---- optional post-processing ----
  const post = { composer: null, bokeh: null, film: null };
  if (story.post !== false) {
    try {
      const A = 'three/addons/postprocessing/';
      const [{ EffectComposer }, { RenderPass }, { UnrealBloomPass }, { BokehPass }, { ShaderPass }, { OutputPass }] = await Promise.all(
        ['EffectComposer', 'RenderPass', 'UnrealBloomPass', 'BokehPass', 'ShaderPass', 'OutputPass'].map((n) => import(`${A}${n}.js`)));
      const rt = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType, samples: 4 });
      const composer = new EffectComposer(renderer, rt);
      composer.setSize(W, H);
      composer.addPass(new RenderPass(scene, camera));
      if (look.dof && story.dof !== false) {
        post.bokeh = new BokehPass(scene, camera, { focus: 6, aperture: look.dof.aperture, maxblur: look.dof.maxblur });
        composer.addPass(post.bokeh);
      }
      if (look.bloom) composer.addPass(new UnrealBloomPass(new THREE.Vector2(W, H), look.bloom.strength, look.bloom.radius, look.bloom.threshold));
      post.film = new ShaderPass({
        uniforms: { tDiffuse: { value: null }, time: { value: 0 }, grain: { value: look.grain }, vig: { value: look.vignette } },
        vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
        fragmentShader: `uniform sampler2D tDiffuse; uniform float time, grain, vig; varying vec2 vUv;
          float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
          void main(){ vec4 c = texture2D(tDiffuse, vUv); vec2 d = vUv - 0.5; c.rgb *= 1.0 - vig * dot(d, d) * 2.2;
            c.rgb += (h(vUv * 1000.0 + time) - 0.5) * grain; gl_FragColor = c; }`,
      });
      composer.addPass(post.film);
      composer.addPass(new OutputPass());
      post.composer = composer;
    } catch (e) {
      console.warn('post-processing disabled (video still renders without bloom/DOF):', e && e.message);
    }
  }

  const _focus = new THREE.Vector3();
  // Call once per frame. cam = {pos, look, fov}; focusPoint optional [x,y,z] for depth of field (default: camera look target).
  function render(t, cam, focusPoint) {
    camera.fov = cam.fov; camera.updateProjectionMatrix();
    camera.position.set(cam.pos[0], cam.pos[1], cam.pos[2]);
    camera.lookAt(cam.look[0], cam.look[1], cam.look[2]);
    // the shadow-casting key light follows what the camera looks at, so shadows stay sharp anywhere in a long world
    key.target.position.set(cam.look[0], cam.look[1], cam.look[2]);
    key.position.set(cam.look[0] + look.key.pos[0], look.key.pos[1], cam.look[2] + look.key.pos[2]);
    key.target.updateMatrixWorld(); key.updateMatrixWorld();
    if (post.composer) {
      if (post.bokeh) {
        const f = focusPoint || cam.look;
        _focus.set(f[0], f[1], f[2]);
        post.bokeh.uniforms.focus.value = camera.position.distanceTo(_focus);
      }
      if (post.film) post.film.uniforms.time.value = Math.floor(t * 24) % 997;
      post.composer.render();
    } else renderer.render(scene, camera);
  }
  return { THREE, renderer, scene, camera, look, key, render, hasPost: !!post.composer };
}

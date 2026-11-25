// Smoke scene used by `npm run doctor`: exercises the real kit (stage, post-processing, builders, character) in your three.js.
import { createStage } from './kit/stage.js';
import { box, documentMesh } from './kit/builders.js';
import { createCharacter } from './kit/character.js';
import { makePath } from './kit/path.js';

export async function build({ THREE, canvas, story, rng }) {
  const stage = await createStage({ THREE, canvas, story });
  box({ THREE, scene: stage.scene, size: [30, 0.1, 30], color: '#3a3f4a', pos: [0, -0.05, 0] });
  box({ THREE, scene: stage.scene, size: [1, 1, 1], color: '#c0562e', pos: [-1.6, 0.5, -1] });
  documentMesh({ THREE, scene: stage.scene, rng, title: 'CHECK', numbers: true, pos: [1.4, 1.0, -0.5], rot: [0, -0.4, 0] });
  const c = createCharacter({ THREE, scene: stage.scene, name: 'check', path: makePath([{ t: 0, pos: [0, 0, -2] }, { t: 4, pos: [0, 0, 1] }]), mood: 'smile' });
  return { update(t, s) { c.update(t, s); stage.render(t, s.camera); } };
}

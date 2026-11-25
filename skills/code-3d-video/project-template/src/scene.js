// DEMO scene composed from the kit. Copy this file's structure for a new video:
//   1) createStage  2) build the world with builders  3) create characters with paths  4) update(t, s) = set everything from t.
// RULES: every frame is a pure function of t (no Date.now / Math.random / requestAnimationFrame / accumulating state).
import { createStage } from './kit/stage.js';
import { street, box, documentMesh, sign } from './kit/builders.js';
import { createCharacter } from './kit/character.js';
import { makePath } from './kit/path.js';

export async function build({ THREE, canvas, story, rng }) {
  const stage = await createStage({ THREE, canvas, story });
  const { scene } = stage;

  // world
  const st = street({ THREE, scene, rng, length: 80, lamps: 5, look: stage.look });
  sign({ THREE, scene, text: 'MAPLE ST', pos: [-5.2, 3.4, -30], rot: [0, Math.PI / 2, 0], w: 2.2, h: 0.55 });
  box({ THREE, scene, size: [0.9, 0.8, 0.9], color: '#6b4a2f', pos: [-0.6, 0.4, -35.2] });
  documentMesh({ THREE, scene, rng, title: 'NOTE', text: 'IF YOU READ THIS\nTHE LAMP IS NOT\nA LAMP.', pos: [-0.6, 0.81, -35.2], rot: [-Math.PI / 2, 0, 0.3], w: 0.4, h: 0.5 });

  // characters
  const kidPath = makePath([{ t: 0, pos: [0.6, 0, -10] }, { t: 14.5, pos: [0.5, 0, -33] }]);
  const kid = createCharacter({ THREE, scene, name: 'kid', height: 1.35, skin: '#f1c9a5', shirt: '#3f7cff', pants: '#27304a', hair: '#2b1d14',
    path: kidPath, mood: 'worried', lookAt: [-1.4, 1.5, -38] });
  const keeper = createCharacter({ THREE, scene, name: 'keeper', height: 1.8, skin: '#d9a47c', shirt: '#b5472e', pants: '#2a2a2a', hair: '#cfcfcf',
    hairStyle: 'long', pos: [-1.4, 0, -38], yaw: 0, mood: 'smile', lookAt: (t) => kidPath.at(t).pos });

  const speakerAt = (t) => (story.speakers || []).find((s) => t >= s.t0 && t < s.t1)?.who ?? story.speaker ?? 'kid';
  return {
    update(t, s) {
      st.update(t);
      const who = speakerAt(t);
      kid.update(t, { ...s, speaking: s.speaking && who === 'kid' });
      keeper.update(t, { ...s, speaking: s.speaking && who === 'keeper' });
      const kp = kidPath.at(t).pos;
      stage.render(t, s.camera, [kp[0], 1.1, kp[2]]);    // depth-of-field focus follows the kid
    },
  };
}

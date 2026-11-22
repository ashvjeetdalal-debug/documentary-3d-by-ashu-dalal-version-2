/**
 * p5.brush <-> Three.js Bridge Module
 * Allows dynamic, animated p5.brush generative canvases (watercolor, charcoal, hatching)
 * to be projected directly as animated CanvasTextures onto Three.js 3D meshes and objects.
 */

import * as THREE from 'three';
import * as brush from '../../../p5-brush/dist/brush.esm.js';

export class BrushTextureTarget {
  constructor(width = 1024, height = 1024) {
    this.width = width;
    this.height = height;

    // Create offscreen canvas for brush
    this.canvas = document.createElement('canvas');
    this.canvas.width = width;
    this.canvas.height = height;

    // Initialize brush on this canvas
    brush.load(this.canvas);
    brush.scaleBrushes(width / 600);

    // Create Three.js Texture
    this.texture = new THREE.CanvasTexture(this.canvas);
    this.texture.colorSpace = THREE.SRGBColorSpace;
    this.texture.anisotropy = 8;
  }

  /**
   * Render a frame of generative drawing onto the canvas and flag texture for update
   * @param {number} t - normalized time in seconds
   * @param {Function} drawCallback - custom drawing logic accepting (brush, t)
   */
  update(t, drawCallback) {
    brush.load(this.canvas);
    brush.seed(Math.floor(t * 1000) % 100000);
    
    if (drawCallback) {
      drawCallback(brush, t);
    }
    
    // Flush standalone brush canvas
    brush.render();
    
    // Notify Three.js to re-upload to GPU
    this.texture.needsUpdate = true;
  }

  /**
   * Returns a ready-to-use Three.js Standard Material
   */
  createMaterial(options = {}) {
    return new THREE.MeshStandardMaterial({
      map: this.texture,
      roughness: options.roughness ?? 0.85,
      metalness: options.metalness ?? 0.0,
      ...options
    });
  }
}

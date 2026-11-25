// Word-synced captions: shows short chunks, highlights the word being spoken right now.
export class Captions {
  constructor(el, words, opts = {}) {
    this.el = el;
    const max = opts.chunk || 3;
    this.chunks = [];
    let cur = [];
    const flush = () => { if (cur.length) { this.chunks.push({ t0: cur[0].t0, t1: cur[cur.length - 1].t1, items: cur }); cur = []; } };
    words.forEach((w, i) => {
      cur.push(w);
      const gap = i + 1 < words.length ? words[i + 1].t0 - w.t1 : 9;
      if (cur.length >= max || /[.,!?;:]$/.test(w.w) || gap > 0.45) flush();
    });
    flush();
    this.idx = -1;
    this.spans = [];
  }
  // Returns the word being spoken at time t (or null).
  update(t) {
    let ci = -1;
    for (let i = 0; i < this.chunks.length; i++) {
      const c = this.chunks[i], next = this.chunks[i + 1];
      const end = next ? Math.min(c.t1 + 0.35, next.t0) : c.t1 + 0.35;
      if (t >= c.t0 - 0.04 && t < end) { ci = i; break; }
    }
    if (ci !== this.idx) {
      this.idx = ci;
      this.el.textContent = '';
      this.spans = [];
      if (ci >= 0) {
        for (const w of this.chunks[ci].items) {
          const s = document.createElement('span');
          s.className = 'w'; s.textContent = w.w;
          this.el.appendChild(s); this.spans.push(s);
        }
      }
    }
    let active = null;
    if (ci >= 0) {
      this.chunks[ci].items.forEach((w, j) => {
        const on = t >= w.t0 && t < w.t1;
        this.spans[j].classList.toggle('on', on);
        if (on) active = w;
      });
    }
    return active;
  }
}

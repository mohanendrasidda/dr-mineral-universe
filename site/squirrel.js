/* Free-roaming Dr. Mineral — wanders the page: walks components, leaps
   between them, peek-a-boos, and stays glued to elements as you scroll.
   Self-contained; include on any page with <script src="squirrel.js" defer></script>.
   Frames live in <scriptDir>/sprites/. */
(function () {
  if (window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var scriptURL = (document.currentScript && document.currentScript.src) || location.href;
  var F = function (n) { return new URL('sprites/' + n + '.png', scriptURL).href; };
  var FR = { idle: F('idle'), walkA: F('walk-a'), walkB: F('walk-b'), run: F('run'), boo: F('boo') };
  Object.keys(FR).forEach(function (k) { var i = new Image(); i.src = FR[k]; });

  var SIZE = 104;
  var el = document.createElement('img');
  el.alt = '';
  Object.assign(el.style, {
    position: 'fixed', left: '0', top: '0', width: SIZE + 'px', height: 'auto',
    zIndex: 60, pointerEvents: 'none', opacity: '0', transition: 'opacity .6s',
    willChange: 'transform', filter: 'drop-shadow(0 10px 14px rgba(0,0,0,.45))'
  });
  el.src = FR.idle;
  function add() { document.body.appendChild(el); }
  if (document.body) add(); else addEventListener('DOMContentLoaded', add);

  var SEL = 'h1,h2,h3,.cta,.chip,.perch';
  var plat = null, recent = [], X = 0, facing = 1, mode = 'idle', timer = 1.2;
  var hopY = 0, squash = 0, last = performance.now(), shown = false, started = false;
  var leap = null, peekSteps = null, pp = 0, frameT = 0, walkDir = 1;

  var clamp = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var ease = function (t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
  var rnd = function (a, b) { return a + Math.random() * (b - a); };

  function visible() {
    var out = [];
    document.querySelectorAll(SEL).forEach(function (e) {
      var r = e.getBoundingClientRect();
      if (r.top > 96 && r.top < innerHeight - 36 && r.width > 48) out.push(e);
    });
    return out;
  }
  function setFrame(n) { if (FR[n]) el.src = FR[n]; }
  function pushRecent(e) { recent.push(e); while (recent.length > 3) recent.shift(); }
  function pick() {
    var v = visible().filter(function (e) { return e !== plat && recent.indexOf(e) < 0; });
    if (!v.length) v = visible().filter(function (e) { return e !== plat; });
    if (!v.length) return null;
    return v[(Math.random() * Math.min(4, v.length)) | 0];
  }

  function topFor(r) { return r.top - SIZE + 12; }
  function place() {
    var sx = facing * (1 + 0.14 * squash), sy = 1 - 0.16 * squash;
    if (mode === 'leap' && leap) {
      var rr = leap.to.getBoundingClientRect();
      var x1 = clamp(leap.fromX, rr.left, rr.right - SIZE * 0.55);
      var y1 = topFor(rr), t = ease(Math.min(1, leap.t));
      var x = lerp(leap.fromX, rr.left + Math.min(rr.width * 0.3, 30), t);
      var y = lerp(leap.fromY, y1, t) - leap.h * 4 * t * (1 - t);
      el.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0) scale(' + sx + ',' + sy + ')';
      return;
    }
    if (!plat) return;
    var r = plat.getBoundingClientRect();
    X = clamp(X, r.left + 2, Math.max(r.left + 2, r.right - SIZE * 0.55));
    var y2 = topFor(r) + hopY;
    el.style.transform = 'translate3d(' + X + 'px,' + y2 + 'px,0) scale(' + sx + ',' + sy + ')';
  }

  function chooseNext() {
    var roll = Math.random();
    if (roll < 0.42) { mode = 'walk'; timer = rnd(1.3, 2.8); walkDir = Math.random() < .5 ? 1 : -1; facing = walkDir; }
    else if (roll < 0.72) { mode = 'peek'; pp = 0; peekSteps = [['idle', SIZE * 0.5, .34], ['boo', -2, .5], ['idle', SIZE * 0.5, .3], ['boo', -2, .5], ['idle', 0, .35]]; applyPeek(); }
    else { startLeap(); }
  }
  function applyPeek() {
    if (pp >= peekSteps.length) { mode = 'idle'; hopY = 0; timer = rnd(.6, 1.4); return; }
    var s = peekSteps[pp]; setFrame(s[0]); hopY = s[1]; timer = s[2];
    if (s[0] === 'boo') squash = 1;
  }
  function startLeap() {
    var tgt = pick();
    if (!tgt) { mode = 'walk'; timer = rnd(1, 2); return; }
    var r = plat ? plat.getBoundingClientRect() : { left: X, top: innerHeight / 2 };
    leap = { fromX: X, fromY: topFor(r) + hopY, to: tgt, t: 0, dur: rnd(.55, .82), h: rnd(60, 115) };
    var tr = tgt.getBoundingClientRect();
    facing = (tr.left + tr.width / 2 > X) ? 1 : -1;
    setFrame('run'); mode = 'leap'; hopY = 0;
  }

  function show() { if (!shown) { shown = true; el.style.opacity = '1'; } }

  function loop(now) {
    requestAnimationFrame(loop);
    var dt = Math.min(.05, (now - last) / 1000); last = now;
    try {
      if (squash > 0) squash = Math.max(0, squash - dt * 3.2);
      if (!plat || !document.body.contains(plat)) { plat = visible()[0] || null; X = plat ? plat.getBoundingClientRect().left + 14 : X; }
      if (!plat) { place(); return; }

      // if current platform scrolled out of comfortable range, hop to a fresh one
      var pr = plat.getBoundingClientRect();
      if (mode !== 'leap' && (pr.top < 70 || pr.top > innerHeight - 28)) { var v = visible(); if (v.length) { plat = v[0]; X = plat.getBoundingClientRect().left + 14; mode = 'idle'; timer = .4; } }

      timer -= dt; frameT += dt;

      if (mode === 'leap') {
        leap.t += dt / leap.dur;
        if (leap.t >= 1) { plat = leap.to; pushRecent(plat); var rr = plat.getBoundingClientRect(); X = rr.left + Math.min(rr.width * 0.3, 30); mode = 'land'; squash = 1; setFrame('idle'); timer = .22; }
      } else if (mode === 'land') {
        if (timer <= 0) { mode = 'idle'; timer = rnd(.5, 1.2); }
      } else if (mode === 'peek') {
        if (timer <= 0) { pp++; applyPeek(); }
      } else if (mode === 'walk') {
        var r = plat.getBoundingClientRect();
        X += walkDir * 34 * dt;
        if (X < r.left + 2) { walkDir = 1; facing = 1; } else if (X > r.right - SIZE * 0.55) { walkDir = -1; facing = -1; }
        setFrame((frameT % .34 < .17) ? 'walkA' : 'walkB');
        if (timer <= 0) { mode = 'idle'; setFrame('idle'); timer = rnd(.4, 1); }
      } else { // idle
        setFrame('idle');
        if (timer <= 0) chooseNext();
      }
      place();
    } catch (e) { /* keep the loop alive */ }
  }

  function start() {
    if (started) return; started = true;
    plat = pick() || visible()[0] || null;
    if (plat) { var r = plat.getBoundingClientRect(); X = r.left + 14; pushRecent(plat); }
    setFrame('idle'); requestAnimationFrame(loop);
    if (scrollY > 40) show();
  }

  addEventListener('scroll', function () { if (scrollY > 110) show(); }, { passive: true });
  addEventListener('load', function () { setTimeout(start, 800); });
  setTimeout(function () { start(); show(); }, 2400);
})();

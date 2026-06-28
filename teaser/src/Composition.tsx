import React from "react";
import {
  AbsoluteFill,
  Sequence,
  Img,
  OffthreadVideo,
  Audio,
  staticFile,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";

// ---- palette / type ----
const BG = "#0a0807";
const INK = "#efe3cf";
const GOLD = "#e7b765";
const SERIF = "'Cormorant Garamond', Georgia, serif";
const MONO = "'IBM Plex Mono', ui-monospace, monospace";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const WARM = "saturate(1.18) sepia(0.12) brightness(0.98) contrast(1.04)";

const fadeIO = (f: number, inE: number, outS: number, outE: number) =>
  interpolate(f, [0, inE, outS, outE], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

const Grade: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(78% 72% at 50% 42%, transparent 38%, rgba(6,5,4,.74) 100%)",
      pointerEvents: "none",
    }}
  />
);

// Ken Burns still
const KB: React.FC<{
  src: string;
  from?: number;
  to?: number;
  panX?: number;
  panY?: number;
  inE?: number;
  outS: number;
  outE: number;
  total: number;
}> = ({ src, from = 1.05, to = 1.16, panX = 0, panY = 0, inE = 22, outS, outE, total }) => {
  const f = useCurrentFrame();
  const s = interpolate(f, [0, total], [from, to], { extrapolateRight: "clamp" });
  const px = interpolate(f, [0, total], [0, panX], { extrapolateRight: "clamp" });
  const py = interpolate(f, [0, total], [0, panY], { extrapolateRight: "clamp" });
  const op = fadeIO(f, inE, outS, outE);
  return (
    <Img
      src={staticFile(src)}
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        objectFit: "cover",
        transform: `scale(${s}) translate(${px}px, ${py}px)`,
        opacity: op,
        filter: WARM,
      }}
    />
  );
};

const Caption: React.FC<{
  children: React.ReactNode;
  top: string;
  size?: number;
  italic?: boolean;
  inE?: number;
  outS: number;
  outE: number;
}> = ({ children, top, size = 44, italic = false, inE = 24, outS, outE }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, inE, outS, outE);
  const rise = interpolate(f, [0, 40], [14, 0], { extrapolateRight: "clamp", easing: ease });
  return (
    <div
      style={{
        position: "absolute",
        width: "100%",
        top,
        textAlign: "center",
        color: INK,
        fontFamily: SERIF,
        fontWeight: 500,
        fontSize: size,
        fontStyle: italic ? "italic" : "normal",
        letterSpacing: 0.5,
        opacity: op,
        transform: `translateY(${rise}px)`,
        textShadow: "0 2px 30px #000d",
        padding: "0 8%",
      }}
    >
      {children}
    </div>
  );
};

const Kicker: React.FC<{ children: React.ReactNode; outE: number }> = ({ children, outE }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, 20, outE - 40, outE);
  return (
    <div
      style={{
        position: "absolute",
        width: "100%",
        top: "12%",
        textAlign: "center",
        color: "rgba(231,183,101,.82)",
        fontFamily: MONO,
        fontSize: 15,
        letterSpacing: "0.36em",
        opacity: op,
      }}
    >
      {children}
    </div>
  );
};

// full-frame stock clip (graded warm)
const ClipScene: React.FC<{
  src: string;
  rate?: number;
  total: number;
  inE?: number;
  outS: number;
  outE: number;
  filter?: string;
  fromScale?: number;
  toScale?: number;
}> = ({ src, rate = 0.8, total, inE = 18, outS, outE, filter = WARM, fromScale = 1.02, toScale = 1.1 }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, inE, outS, outE);
  const z = interpolate(f, [0, total], [fromScale, toScale], { extrapolateRight: "clamp" });
  return (
    <OffthreadVideo
      src={staticFile(src)}
      playbackRate={rate}
      muted
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        objectFit: "cover",
        opacity: op,
        transform: `scale(${z})`,
        filter,
      }}
    />
  );
};

// screen-blended motion overlay (embers / dust / sparks on black) — brings stills alive
const Overlay: React.FC<{
  src: string;
  opacity?: number;
  blend?: string;
  rate?: number;
  total: number;
  fadeOut?: number;
}> = ({ src, opacity = 0.5, blend = "screen", rate = 1, total, fadeOut = 18 }) => {
  const f = useCurrentFrame();
  const op = interpolate(f, [0, 14, total - fadeOut, total], [0, opacity, opacity, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <OffthreadVideo
      src={staticFile(src)}
      muted
      playbackRate={rate}
      style={{
        position: "absolute",
        inset: 0,
        width: "100%",
        height: "100%",
        objectFit: "cover",
        mixBlendMode: blend as React.CSSProperties["mixBlendMode"],
        opacity: op,
        pointerEvents: "none",
      }}
    />
  );
};

const SubLabel: React.FC<{ tag: string; line: string; outS: number; outE: number }> = ({
  tag,
  line,
  outS,
  outE,
}) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, 14, outS, outE);
  return (
    <div style={{ position: "absolute", left: "8%", bottom: "16%", opacity: op }}>
      <div style={{ fontFamily: MONO, fontSize: 14, letterSpacing: "0.22em", color: GOLD }}>
        {tag}
      </div>
      <div
        style={{
          fontFamily: SERIF,
          fontWeight: 500,
          fontSize: 40,
          color: INK,
          marginTop: 6,
          textShadow: "0 2px 24px #000d",
        }}
      >
        {line}
      </div>
    </div>
  );
};

type Dist = { img: string; clip?: string; tag: string; line: string; d: number; sfx?: string };
const Districts: React.FC = () => {
  const items: Dist[] = [
    { img: "mines.png", clip: "district-mines.mp4", tag: "01 · MINE", line: "Do the security work.", d: 78 },
    { img: "foundry.png", clip: "district-foundry.mp4", tag: "02 · FORGE", line: "Mint the reward onto the chain.", d: 84, sfx: "foundry-sfx.m4a" },
    { img: "ledger.png", tag: "03 · RECORD", line: "Logged on-chain, forever.", d: 60 },
    { img: "vault.png", tag: "04 · VAULT", line: "The treasury it controls.", d: 60 },
    { img: "watch.png", clip: "district-watch.mp4", tag: "05 · GUARD", line: "Audited. Monitored. Secured.", d: 70 },
  ];
  let acc = 0;
  return (
    <AbsoluteFill style={{ background: BG }}>
      {items.map((it, i) => {
        const from = acc;
        acc += it.d;
        const total = it.d + 16;
        return (
          <Sequence key={it.img} from={from} durationInFrames={total}>
            <AbsoluteFill style={{ background: BG }}>
              {it.clip ? (
                <ClipScene src={it.clip} rate={0.95} total={total} outS={it.d - 4} outE={total} fromScale={1.0} toScale={1.06} />
              ) : (
                <>
                  <KB src={it.img} from={1.07} to={1.2} panX={i % 2 ? -20 : 20} outS={it.d - 4} outE={total} total={total} />
                  <Overlay src="fx-dust.mp4" opacity={0.45} rate={0.9} total={total} />
                </>
              )}
              {it.sfx && <Audio src={staticFile(it.sfx)} volume={0.5} playbackRate={0.95} />}
              <Grade />
              <SubLabel tag={it.tag} line={it.line} outS={it.d - 6} outE={total - 2} />
            </AbsoluteFill>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const TheLine: React.FC = () => {
  const f = useCurrentFrame();
  const op = fadeIO(f, 28, 115, 150);
  const heroR = interpolate(f, [0, 55], [26, 0], { extrapolateRight: "clamp", easing: ease });
  return (
    <div
      style={{
        opacity: op,
        display: "flex",
        alignItems: "center",
        gap: 40,
        maxWidth: 1120,
        padding: "0 60px",
      }}
    >
      <Img
        src={staticFile("drmineral.png")}
        style={{
          height: 380,
          transform: `translateY(${heroR}px)`,
          filter: "drop-shadow(0 18px 50px rgba(231,183,101,.22))",
        }}
      />
      <div
        style={{
          color: INK,
          fontFamily: SERIF,
          fontWeight: 500,
          fontSize: 46,
          fontStyle: "italic",
          maxWidth: 540,
          lineHeight: 1.3,
        }}
      >
        “I don’t collect treasure.
        <br />I collect discoveries.”
      </div>
    </div>
  );
};

const CTA: React.FC = () => {
  const f = useCurrentFrame();
  const op = interpolate(f, [0, 26], [0, 1], { extrapolateRight: "clamp", easing: ease });
  const sub = fadeIO(f, 40, 200, 240);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(90% 80% at 50% 42%, #16120e 0%, ${BG} 80%)`,
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        opacity: op,
      }}
    >
      <div style={{ fontFamily: MONO, fontSize: 14, letterSpacing: "0.34em", color: "rgba(231,183,101,.8)" }}>
        UNIVERSITY OF NEBRASKA
      </div>
      <div
        style={{
          fontFamily: SERIF,
          fontWeight: 700,
          fontSize: 70,
          color: "#f6e9d0",
          marginTop: 12,
          letterSpacing: 1,
          textShadow: "0 0 50px rgba(245,196,107,.35)",
        }}
      >
        The Lab Reward Coin
      </div>
      <div
        style={{
          fontFamily: SERIF,
          fontStyle: "italic",
          fontSize: 26,
          color: "rgba(214,199,170,.85)",
          marginTop: 16,
          opacity: sub,
        }}
      >
        a coin for real security work
      </div>
    </AbsoluteFill>
  );
};

// ---- master ----
export const Teaser: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: BG }}>
      <Audio
        src={staticFile("score.mp3")}
        volume={(f) =>
          interpolate(
            f,
            [0, 45, durationInFrames - 90, durationInFrames - 4],
            [0, 0.62, 0.62, 0],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          )
        }
      />

      {/* 1 — Lincoln at dusk */}
      <Sequence from={0} durationInFrames={150}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene src="clip-lincoln.mp4" rate={0.85} total={150} outS={126} outE={150} />
          <Grade />
          <Kicker outE={150}>UNIVERSITY OF NEBRASKA · LINCOLN</Kicker>
          <Caption top="72%" size={42} outS={100} outE={140}>
            An ordinary city.
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 2 — the campus */}
      <Sequence from={135} durationInFrames={150}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene src="clip-campus.mp4" rate={0.85} total={150} outS={126} outE={150} />
          <Grade />
          <Caption top="72%" size={40} italic outS={106} outE={146}>
            A quiet campus. Nobody looks twice.
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 3 — golden-hour surface (real forest god-rays) */}
      <Sequence from={270} durationInFrames={135}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene src="fx-forest.mp4" rate={0.7} total={135} outS={112} outE={135} fromScale={1.06} toScale={1.14} />
          <Grade />
          <Caption top="72%" size={40} italic outS={92} outE={130}>
            The world above.
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 4 — the descent (LTX clip) + dust */}
      <Sequence from={390} durationInFrames={165}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene src="clip-descent.mp4" rate={0.72} total={165} outS={140} outE={165} />
          <Overlay src="fx-dust.mp4" opacity={0.32} rate={0.8} total={165} />
          <Grade />
          <Caption top="72%" size={42} italic outS={116} outE={156}>
            But beneath it,
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 5 — the reveal + dust motes drifting in the shaft */}
      <Sequence from={540} durationInFrames={175}>
        <AbsoluteFill style={{ background: BG }}>
          <KB src="central-cavern.png" from={1.04} to={1.15} outS={150} outE={175} total={175} />
          <Overlay src="fx-dust.mp4" opacity={0.6} rate={0.8} total={175} />
          <Grade />
          <Caption top="44%" size={52} outS={132} outE={170}>
            a lab has worked for ages.
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 6 — mineral cutaway (real crystal macro, warm-graded) */}
      <Sequence from={700} durationInFrames={100}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene
            src="fx-crystal.mp4"
            rate={0.7}
            total={100}
            outS={78}
            outE={100}
            fromScale={1.05}
            toScale={1.16}
            filter="sepia(0.55) saturate(1.5) hue-rotate(-12deg) brightness(0.82) contrast(1.08)"
          />
          <Overlay src="fx-sparks.mp4" opacity={0.4} total={100} />
          <Grade />
          <Caption top="74%" size={38} italic outS={62} outE={96}>
            carved from the rock —
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 7 — the core loop across the five districts */}
      <Sequence from={785} durationInFrames={366}>
        <Districts />
      </Sequence>

      {/* 8 — the line */}
      <Sequence from={1136} durationInFrames={155}>
        <AbsoluteFill
          style={{
            background: `radial-gradient(80% 80% at 50% 45%, #15110c 0%, ${BG} 78%)`,
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <TheLine />
        </AbsoluteFill>
      </Sequence>

      {/* 9 — title card / CTA (overlaps the line to crossfade, no dead gap) */}
      <Sequence from={1266} durationInFrames={durationInFrames - 1266}>
        <CTA />
      </Sequence>
    </AbsoluteFill>
  );
};

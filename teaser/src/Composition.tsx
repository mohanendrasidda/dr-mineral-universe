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

const fadeIO = (f: number, inE: number, outS: number, outE: number) =>
  interpolate(f, [0, inE, outS, outE], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

// cinematic vignette
const Grade: React.FC = () => (
  <AbsoluteFill
    style={{
      background:
        "radial-gradient(78% 72% at 50% 42%, transparent 38%, rgba(6,5,4,.72) 100%)",
      pointerEvents: "none",
    }}
  />
);

// Ken Burns still: slow scale + drift, with fade in/out
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

const ClipScene: React.FC<{
  src: string;
  rate?: number;
  total: number;
  inE?: number;
  outS: number;
  outE: number;
}> = ({ src, rate = 0.8, total, inE = 18, outS, outE }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, inE, outS, outE);
  const z = interpolate(f, [0, total], [1.02, 1.1], { extrapolateRight: "clamp" });
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

const Districts: React.FC = () => {
  const items: [string, string, string][] = [
    ["mines.png", "01 · MINE", "Do the security work."],
    ["foundry.png", "02 · FORGE", "Mint the reward onto the chain."],
    ["ledger.png", "03 · RECORD", "Logged on-chain, forever."],
    ["vault.png", "04 · VAULT", "The treasury it controls."],
    ["watch.png", "05 · GUARD", "Audited. Monitored. Secured."],
  ];
  const D = 60;
  return (
    <AbsoluteFill style={{ background: BG }}>
      {items.map(([img, tag, line], i) => (
        <Sequence key={img} from={i * D} durationInFrames={D + 14}>
          <AbsoluteFill>
            <KB
              src={img}
              from={1.06}
              to={1.18}
              panX={i % 2 ? -18 : 18}
              outS={D - 6}
              outE={D + 12}
              total={D + 14}
            />
            <Grade />
            <SubLabel tag={tag} line={line} outS={D - 8} outE={D + 10} />
          </AbsoluteFill>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

const TheLine: React.FC = () => {
  const f = useCurrentFrame();
  const op = fadeIO(f, 28, 110, 148);
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
  const op = interpolate(f, [0, 30], [0, 1], { extrapolateRight: "clamp", easing: ease });
  const sub = fadeIO(f, 45, 200, 240);
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
            [0, 45, durationInFrames - 80, durationInFrames - 4],
            [0, 0.62, 0.62, 0],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          )
        }
      />

      {/* 1 — Lincoln at dusk (real Nebraska aerial) */}
      <Sequence from={0} durationInFrames={150}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene src="clip-lincoln.mp4" rate={0.85} total={150} outS={125} outE={150} />
          <Grade />
          <Kicker outE={150}>UNIVERSITY OF NEBRASKA · LINCOLN</Kicker>
          <Caption top="72%" size={42} outS={100} outE={140}>
            An ordinary city.
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 2 — the campus */}
      <Sequence from={135} durationInFrames={155}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene src="clip-campus.mp4" rate={0.85} total={155} outS={130} outE={155} />
          <Grade />
          <Caption top="72%" size={40} italic outS={110} outE={150}>
            A quiet campus. Nobody looks twice.
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 3 — the descent (LTX clip) */}
      <Sequence from={275} durationInFrames={165}>
        <AbsoluteFill style={{ background: "#000" }}>
          <ClipScene src="clip-descent.mp4" rate={0.75} total={165} outS={140} outE={165} />
          <Grade />
          <Caption top="72%" size={42} italic outS={115} outE={155}>
            But beneath it,
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 4 — the reveal */}
      <Sequence from={425} durationInFrames={195}>
        <AbsoluteFill style={{ background: BG }}>
          <KB src="central-cavern.png" from={1.04} to={1.16} outS={170} outE={195} total={195} />
          <Grade />
          <Caption top="44%" size={52} outS={150} outE={188}>
            a lab has worked for ages.
          </Caption>
        </AbsoluteFill>
      </Sequence>

      {/* 5 — the core loop across the five districts */}
      <Sequence from={605} durationInFrames={320}>
        <Districts />
      </Sequence>

      {/* 6 — the line */}
      <Sequence from={920} durationInFrames={150}>
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

      {/* 7 — title card / CTA */}
      <Sequence from={1060} durationInFrames={durationInFrames - 1060}>
        <CTA />
      </Sequence>
    </AbsoluteFill>
  );
};

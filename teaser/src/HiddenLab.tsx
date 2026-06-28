import React from "react";
import {
  AbsoluteFill,
  Sequence,
  OffthreadVideo,
  Audio,
  staticFile,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";

const SERIF = "'Cormorant Garamond', Georgia, serif";
const MONO = "'IBM Plex Mono', ui-monospace, monospace";
const GOLD = "linear-gradient(180deg,#fdeecb 0%,#f0c878 38%,#caa052 60%,#9a6a3a 78%,#e9c07f 100%)";
const ease = Easing.bezier(0.16, 1, 0.3, 1);

const goldText: React.CSSProperties = {
  backgroundImage: GOLD,
  WebkitBackgroundClip: "text",
  backgroundClip: "text",
  WebkitTextFillColor: "transparent",
  color: "transparent",
  filter: "drop-shadow(0 2px 2px rgba(0,0,0,.55)) drop-shadow(0 0 40px rgba(231,183,101,.55))",
};

const fadeIO = (f: number, inE: number, outS: number, outE: number) =>
  interpolate(f, [0, inE, outS, outE], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

const Beat: React.FC<{
  src: string;
  total: number;
  outS: number;
  trim?: number;
  punchIn?: boolean;
  inE?: number;
  children?: React.ReactNode;
}> = ({ src, total, outS, trim = 0, punchIn = false, inE = 12, children }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, inE, outS, total);
  const scale = punchIn ? interpolate(f, [0, 22], [1.16, 1.0], { extrapolateRight: "clamp", easing: ease }) : 1;
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center" }}>
      <OffthreadVideo src={staticFile(src)} muted startFrom={trim} style={{ width: "100%", height: "100%", objectFit: "contain", opacity: op, transform: `scale(${scale})` }} />
      {children}
    </AbsoluteFill>
  );
};

const Kicker: React.FC<{ children: React.ReactNode; outE: number }> = ({ children, outE }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, 16, outE - 26, outE);
  return (
    <div style={{ position: "absolute", width: "100%", top: "15%", textAlign: "center", color: "rgba(231,183,101,.85)", fontFamily: MONO, fontSize: 18, letterSpacing: "0.4em", opacity: op }}>
      {children}
    </div>
  );
};

// title gets its OWN beat on black, then we cut clean to the cavern
const TitleCard: React.FC<{ total: number }> = ({ total }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, 12, total - 8, total);
  const spread = interpolate(f, [10, total], [0.16, 0.32], { extrapolateRight: "clamp", easing: ease });
  const glint = interpolate(f, [14, total - 6], [-30, 130], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ background: "#040303", justifyContent: "center", alignItems: "center" }}>
      <div style={{ position: "relative", opacity: op }}>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 108, letterSpacing: `${spread}em`, paddingLeft: `${spread}em`, ...goldText }}>THE HIDDEN LAB</div>
        <div style={{ position: "absolute", inset: 0, background: `linear-gradient(105deg, transparent ${glint - 12}%, rgba(255,255,255,.9) ${glint}%, transparent ${glint + 12}%)`, mixBlendMode: "overlay", pointerEvents: "none" }} />
      </div>
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const title = interpolate(f, [6, 32], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const l1 = interpolate(f, [40, 58], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const l2 = interpolate(f, [60, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const tag = interpolate(f, [92, 112], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return (
    <AbsoluteFill style={{ background: "radial-gradient(90% 80% at 50% 42%, #16120e 0%, #050403 82%)", justifyContent: "center", alignItems: "center", flexDirection: "column" }}>
      <div style={{ fontFamily: MONO, fontSize: 13, letterSpacing: "0.34em", color: "rgba(231,183,101,.8)", opacity: title }}>UNIVERSITY OF NEBRASKA</div>
      <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 82, marginTop: 14, letterSpacing: 1, opacity: title, ...goldText }}>The Lab Reward Coin</div>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 30, color: "#d6c7aa", marginTop: 28, opacity: l1, letterSpacing: 1 }}>Not mined — <span style={{ color: "#e7b765" }}>earned.</span></div>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 30, color: "#d6c7aa", marginTop: 6, opacity: l2, letterSpacing: 1 }}>Not purchased — <span style={{ color: "#e7b765" }}>proven.</span></div>
      <div style={{ fontFamily: MONO, fontSize: 13, letterSpacing: "0.26em", color: "rgba(214,199,170,.78)", marginTop: 30, opacity: tag }}>THE FUTURE OF CYBERSECURITY STARTS HERE</div>
      <div style={{ fontFamily: MONO, fontSize: 10, letterSpacing: "0.2em", color: "rgba(150,140,120,.5)", marginTop: 18, opacity: tag }}>MUSIC: “THE DESCENT” — KEVIN MACLEOD (CC BY 4.0)</div>
    </AbsoluteFill>
  );
};

type Seg = { id: string; dur: number; lead: number; kind: "clip" | "title" | "end"; kicker?: string; trim?: number; punchIn?: boolean };
const SEG: Seg[] = [
  { id: "S1", dur: 132, lead: 0, kind: "clip", kicker: "UNIVERSITY OF NEBRASKA" },
  { id: "S3", dur: 120, lead: 12, kind: "clip" },
  { id: "S6", dur: 120, lead: 12, kind: "clip" },
  { id: "TITLE", dur: 50, lead: 0, kind: "title" }, // own beat on black; hard cut from S6 (fades to black) and to S7
  { id: "S7", dur: 150, lead: 4, kind: "clip", punchIn: true },
  { id: "S10", dur: 100, lead: 12, kind: "clip" },
  { id: "S13", dur: 100, lead: 12, kind: "clip" },
  { id: "S14", dur: 88, lead: 12, kind: "clip", trim: 8 },
  { id: "S15", dur: 116, lead: 12, kind: "clip" },
  { id: "S17", dur: 100, lead: 12, kind: "clip", trim: 40 }, // climax — trimmed to land on the symbol + teal orbit
  { id: "END", dur: 132, lead: 12, kind: "end" },
];
const OV = 12;
const START: Record<string, number> = {};
{
  let acc = 0;
  for (const s of SEG) {
    acc = acc === 0 ? 0 : acc - s.lead;
    START[s.id] = acc;
    acc += s.dur;
  }
}
const TITLE_F = START["TITLE"];

// scene-relative sound design
const SFX: { sc: string; off: number; src: string; vol: number; dur: number }[] = [
  { sc: "S1", off: 0, src: "sfx-rain.mp3", vol: 0.34, dur: 250 },
  { sc: "S1", off: 0, src: "sfx-wind.mp3", vol: 0.3, dur: 250 },
  { sc: "S1", off: 30, src: "sfx-thunder.mp3", vol: 0.7, dur: 170 },
  { sc: "S3", off: 0, src: "sfx-leaves.mp3", vol: 0.4, dur: 110 },
  { sc: "S3", off: 58, src: "sfx-thunder.mp3", vol: 0.45, dur: 140 },
  // descent — all cues END before the silence window
  { sc: "S6", off: 0, src: "sfx-drone.mp3", vol: 0.3, dur: 112 },
  { sc: "S6", off: 14, src: "sfx-drips.mp3", vol: 0.5, dur: 40 },
  { sc: "S6", off: 40, src: "sfx-gear.mp3", vol: 0.55, dur: 46 },
  { sc: "S6", off: 66, src: "sfx-drips.mp3", vol: 0.45, dur: 40 },
  // TITLE — the BOOM lands here after the dead silence
  { sc: "TITLE", off: 12, src: "sfx-impact.mp3", vol: 0.95, dur: 170 },
  { sc: "TITLE", off: 16, src: "sfx-shimmer.mp3", vol: 0.5, dur: 40 },
  // S7 reveal (clean) + the lab ambience bed
  { sc: "S7", off: 4, src: "sfx-crowd.mp3", vol: 0.16, dur: 520 },
  { sc: "S7", off: 4, src: "sfx-drone.mp3", vol: 0.18, dur: 520 },
  { sc: "S10", off: 6, src: "sfx-shimmer.mp3", vol: 0.35, dur: 40 },
  { sc: "S13", off: 30, src: "sfx-forgehammer.mp3", vol: 0.35, dur: 40 },
  { sc: "S14", off: 14, src: "sfx-hammer.mp3", vol: 1.0, dur: 40 },
  { sc: "S14", off: 14, src: "sfx-impact.mp3", vol: 0.5, dur: 120 },
  { sc: "S14", off: 24, src: "sfx-shimmer.mp3", vol: 0.6, dur: 40 },
  { sc: "S15", off: 10, src: "sfx-shimmer.mp3", vol: 0.22, dur: 40 },
  { sc: "S17", off: 8, src: "sfx-shimmer.mp3", vol: 0.4, dur: 40 },
  { sc: "S17", off: 8, src: "sfx-coin.mp3", vol: 0.72, dur: 60 },
];

export const HiddenLab: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {/* music: build -> DEAD SILENCE (~0.7s) -> SLAM on the title -> sustain -> swell on the coin */}
      <Audio
        src={staticFile("v2-music-full.mp3")}
        volume={(f) =>
          interpolate(
            f,
            [0, 24, TITLE_F - 26, TITLE_F - 12, TITLE_F + 8, TITLE_F + 18, START["S15"], START["S15"] + 16, START["S15"] + 70, START["S17"] + 20, durationInFrames - 70, durationInFrames - 4],
            [0, 0.48, 0.55, 0.02, 0.02, 0.8, 0.66, 0.44, 0.62, 0.76, 0.62, 0],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          )
        }
      />

      {SFX.map((s, i) => {
        const from = Math.max(0, START[s.sc] + s.off);
        return (
          <Sequence key={`sfx${i}`} from={from} durationInFrames={s.dur}>
            <Audio src={staticFile(s.src)} volume={(f) => interpolate(f, [0, 6, s.dur - 10, s.dur], [0, s.vol, s.vol, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} />
          </Sequence>
        );
      })}

      {SEG.map((s) => (
        <Sequence key={s.id} from={START[s.id]} durationInFrames={s.dur + 4}>
          {s.kind === "clip" ? (
            <Beat src={`v2-${s.id}.mp4`} total={s.dur} outS={s.dur - OV} trim={s.trim} punchIn={s.punchIn} inE={s.punchIn ? 4 : 12}>
              {s.kicker && <Kicker outE={s.dur}>{s.kicker}</Kicker>}
            </Beat>
          ) : s.kind === "title" ? (
            <TitleCard total={s.dur} />
          ) : (
            <EndCard />
          )}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

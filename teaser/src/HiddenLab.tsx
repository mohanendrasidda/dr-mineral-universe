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
  filter: "drop-shadow(0 2px 2px rgba(0,0,0,.55)) drop-shadow(0 0 36px rgba(231,183,101,.5))",
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
  const scale = punchIn
    ? interpolate(f, [0, 20], [1.14, 1.0], { extrapolateRight: "clamp", easing: ease })
    : 1;
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center" }}>
      <OffthreadVideo
        src={staticFile(src)}
        muted
        startFrom={trim}
        style={{ width: "100%", height: "100%", objectFit: "contain", opacity: op, transform: `scale(${scale})` }}
      />
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

const TitleReveal: React.FC = () => {
  const f = useCurrentFrame();
  const op = interpolate(f, [34, 60], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const spread = interpolate(f, [34, 130], [0.18, 0.34], { extrapolateRight: "clamp", easing: ease });
  const out = fadeIO(f, 34, 128, 150);
  // moving specular glint sweeping the letters
  const glint = interpolate(f, [40, 100], [-30, 130], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ position: "relative", opacity: Math.min(op, out) }}>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 104, letterSpacing: `${spread}em`, paddingLeft: `${spread}em`, ...goldText }}>
          THE HIDDEN LAB
        </div>
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(105deg, transparent ${glint - 12}%, rgba(255,255,255,.85) ${glint}%, transparent ${glint + 12}%)`,
            mixBlendMode: "overlay",
            pointerEvents: "none",
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const title = interpolate(f, [6, 32], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const l1 = interpolate(f, [40, 58], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const l2 = interpolate(f, [60, 80], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const tag = interpolate(f, [90, 110], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return (
    <AbsoluteFill style={{ background: "radial-gradient(90% 80% at 50% 42%, #16120e 0%, #050403 82%)", justifyContent: "center", alignItems: "center", flexDirection: "column" }}>
      <div style={{ fontFamily: MONO, fontSize: 13, letterSpacing: "0.34em", color: "rgba(231,183,101,.8)", opacity: title }}>UNIVERSITY OF NEBRASKA</div>
      <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 82, marginTop: 14, letterSpacing: 1, opacity: title, ...goldText }}>The Lab Reward Coin</div>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 30, color: "#d6c7aa", marginTop: 28, opacity: l1, letterSpacing: 1 }}>
        Not mined — <span style={{ color: "#e7b765" }}>earned.</span>
      </div>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 30, color: "#d6c7aa", marginTop: 6, opacity: l2, letterSpacing: 1 }}>
        Not purchased — <span style={{ color: "#e7b765" }}>proven.</span>
      </div>
      <div style={{ fontFamily: MONO, fontSize: 13, letterSpacing: "0.26em", color: "rgba(214,199,170,.78)", marginTop: 30, opacity: tag }}>THE FUTURE OF CYBERSECURITY STARTS HERE</div>
      <div style={{ fontFamily: MONO, fontSize: 10, letterSpacing: "0.2em", color: "rgba(150,140,120,.5)", marginTop: 18, opacity: tag }}>MUSIC: “THE DESCENT” — KEVIN MACLEOD (CC BY 4.0)</div>
    </AbsoluteFill>
  );
};

type Clip = { id: string; dur: number; kicker?: string; title?: boolean; trim?: number; punchIn?: boolean };
const CLIPS: Clip[] = [
  { id: "S1", dur: 132, kicker: "UNIVERSITY OF NEBRASKA" },
  { id: "S3", dur: 120 },
  { id: "S6", dur: 120 },
  { id: "S7", dur: 150, title: true, punchIn: true },
  { id: "S10", dur: 100 },
  { id: "S13", dur: 100 },
  { id: "S14", dur: 88, trim: 8 },
  { id: "S15", dur: 116 },
  { id: "S17", dur: 100 },
  { id: "S20", dur: 132, trim: 18 },
];
const OV = 12;
const START: Record<string, number> = {};
{
  let acc = 0;
  for (const c of CLIPS) {
    START[c.id] = acc;
    acc += c.dur - OV;
  }
}
const END_FROM = START["S20"] + CLIPS[CLIPS.length - 1].dur - OV;

// scene-relative sound design (off can be negative to pre-roll a cue)
const SFX: { sc: string; off: number; src: string; vol: number; dur: number }[] = [
  { sc: "S1", off: 0, src: "sfx-rain.mp3", vol: 0.34, dur: 250 },
  { sc: "S1", off: 0, src: "sfx-wind.mp3", vol: 0.3, dur: 250 },
  { sc: "S1", off: 30, src: "sfx-thunder.mp3", vol: 0.7, dur: 170 },
  { sc: "S3", off: 0, src: "sfx-leaves.mp3", vol: 0.4, dur: 110 },
  { sc: "S3", off: 58, src: "sfx-thunder.mp3", vol: 0.45, dur: 140 },
  { sc: "S6", off: 0, src: "sfx-drone.mp3", vol: 0.3, dur: 720 },
  { sc: "S6", off: 14, src: "sfx-drips.mp3", vol: 0.5, dur: 50 },
  { sc: "S6", off: 46, src: "sfx-gear.mp3", vol: 0.55, dur: 50 },
  { sc: "S6", off: 78, src: "sfx-drips.mp3", vol: 0.45, dur: 50 },
  { sc: "S7", off: -46, src: "sfx-shortriser.mp3", vol: 0.7, dur: 62 },
  { sc: "S7", off: 0, src: "sfx-impact.mp3", vol: 0.85, dur: 170 },
  { sc: "S7", off: 6, src: "sfx-shimmer.mp3", vol: 0.55, dur: 40 },
  { sc: "S7", off: 16, src: "sfx-crowd.mp3", vol: 0.15, dur: 520 },
  { sc: "S10", off: 6, src: "sfx-shimmer.mp3", vol: 0.35, dur: 40 },
  { sc: "S13", off: 30, src: "sfx-forgehammer.mp3", vol: 0.35, dur: 40 },
  { sc: "S14", off: 14, src: "sfx-hammer.mp3", vol: 1.0, dur: 40 },
  { sc: "S14", off: 14, src: "sfx-impact.mp3", vol: 0.5, dur: 120 },
  { sc: "S14", off: 24, src: "sfx-shimmer.mp3", vol: 0.6, dur: 40 },
  { sc: "S15", off: 10, src: "sfx-shimmer.mp3", vol: 0.22, dur: 40 },
  { sc: "S17", off: 6, src: "sfx-drone.mp3", vol: 0.2, dur: 150 },
  { sc: "S17", off: 12, src: "sfx-coin.mp3", vol: 0.72, dur: 60 },
  { sc: "S17", off: 6, src: "sfx-shimmer.mp3", vol: 0.4, dur: 40 },
  { sc: "S20", off: 0, src: "sfx-wind.mp3", vol: 0.22, dur: 140 },
  { sc: "S20", off: 34, src: "sfx-shimmer.mp3", vol: 0.4, dur: 40 },
  { sc: "S20", off: 40, src: "sfx-coin.mp3", vol: 0.55, dur: 60 },
];

export const HiddenLab: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  const rv = START["S7"]; // reveal frame
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {/* music with Nolan-style dynamics: build -> dip to near-silence before the reveal -> SLAM -> swell on the coin */}
      <Audio
        src={staticFile("v2-music-full.mp3")}
        volume={(f) =>
          interpolate(
            f,
            [0, 24, rv - 36, rv - 6, rv + 8, START["S15"], START["S15"] + 16, START["S15"] + 70, START["S17"] + 24, durationInFrames - 80, durationInFrames - 4],
            [0, 0.48, 0.55, 0.12, 0.78, 0.66, 0.44, 0.62, 0.74, 0.6, 0],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          )
        }
      />

      {SFX.map((s, i) => {
        const from = Math.max(0, START[s.sc] + s.off);
        return (
          <Sequence key={`sfx${i}`} from={from} durationInFrames={s.dur}>
            <Audio
              src={staticFile(s.src)}
              volume={(f) => interpolate(f, [0, 6, s.dur - 10, s.dur], [0, s.vol, s.vol, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
            />
          </Sequence>
        );
      })}

      {CLIPS.map((c) => (
        <Sequence key={c.id} from={START[c.id]} durationInFrames={c.dur + 4}>
          <Beat src={`v2-${c.id}.mp4`} total={c.dur} outS={c.dur - OV} trim={c.trim} punchIn={c.punchIn}>
            {c.kicker && <Kicker outE={c.dur}>{c.kicker}</Kicker>}
            {c.title && <TitleReveal />}
          </Beat>
        </Sequence>
      ))}

      <Sequence from={END_FROM} durationInFrames={durationInFrames - END_FROM}>
        <EndCard />
      </Sequence>
    </AbsoluteFill>
  );
};

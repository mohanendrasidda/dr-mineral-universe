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
const ease = Easing.bezier(0.16, 1, 0.3, 1);

const fadeIO = (f: number, inE: number, outS: number, outE: number) =>
  interpolate(f, [0, inE, outS, outE], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

const Beat: React.FC<{
  src: string;
  total: number;
  inE?: number;
  outS: number;
  outE: number;
  children?: React.ReactNode;
}> = ({ src, total, inE = 14, outS, outE, children }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, inE, outS, outE);
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center" }}>
      <OffthreadVideo
        src={staticFile(src)}
        muted
        style={{ width: "100%", height: "100%", objectFit: "contain", opacity: op }}
      />
      {children}
    </AbsoluteFill>
  );
};

const Kicker: React.FC<{ children: React.ReactNode; outE: number }> = ({ children, outE }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, 16, outE - 28, outE);
  return (
    <div
      style={{
        position: "absolute",
        width: "100%",
        top: "15%",
        textAlign: "center",
        color: "rgba(231,183,101,.85)",
        fontFamily: MONO,
        fontSize: 18,
        letterSpacing: "0.4em",
        opacity: op,
      }}
    >
      {children}
    </div>
  );
};

const TitleReveal: React.FC = () => {
  const f = useCurrentFrame();
  const op = interpolate(f, [38, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const spread = interpolate(f, [38, 120], [0.26, 0.4], { extrapolateRight: "clamp", easing: ease });
  const out = fadeIO(f, 38, 120, 150);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div
        style={{
          fontFamily: SERIF,
          fontWeight: 700,
          fontSize: 96,
          color: "#f6e9d0",
          letterSpacing: `${spread}em`,
          paddingLeft: `${spread}em`,
          opacity: Math.min(op, out),
          textShadow: "0 0 60px rgba(245,196,107,.45)",
        }}
      >
        THE HIDDEN LAB
      </div>
    </AbsoluteFill>
  );
};

const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const title = interpolate(f, [6, 34], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const l1 = fadeIO(f, 44, 999, 9999);
  const l2 = interpolate(f, [62, 84], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const tag = interpolate(f, [92, 112], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(90% 80% at 50% 42%, #16120e 0%, #050403 82%)",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <div style={{ fontFamily: MONO, fontSize: 14, letterSpacing: "0.34em", color: "rgba(231,183,101,.8)", opacity: title }}>
        UNIVERSITY OF NEBRASKA
      </div>
      <div
        style={{
          fontFamily: SERIF,
          fontWeight: 700,
          fontSize: 76,
          color: "#f6e9d0",
          marginTop: 14,
          letterSpacing: 1,
          opacity: title,
          textShadow: "0 0 50px rgba(245,196,107,.35)",
        }}
      >
        The Lab Reward Coin
      </div>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 30, color: "#d6c7aa", marginTop: 26, opacity: l1, letterSpacing: 1 }}>
        Not mined — <span style={{ color: "#e7b765", opacity: l2 }}>earned.</span>
      </div>
      <div style={{ fontFamily: SERIF, fontStyle: "italic", fontSize: 30, color: "#d6c7aa", marginTop: 6, opacity: l2, letterSpacing: 1 }}>
        Not purchased — <span style={{ color: "#e7b765" }}>proven.</span>
      </div>
      <div style={{ fontFamily: MONO, fontSize: 14, letterSpacing: "0.28em", color: "rgba(214,199,170,.8)", marginTop: 30, opacity: tag }}>
        THE FUTURE OF CYBERSECURITY STARTS HERE
      </div>
    </AbsoluteFill>
  );
};

// one sound cue with a soft in/out envelope
const Snd: React.FC<{ src: string; vol: number; dur: number }> = ({ src, vol, dur }) => (
  <Audio
    src={staticFile(src)}
    volume={(f) =>
      interpolate(f, [0, 8, dur - 12, dur], [0, vol, vol, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    }
  />
);

// per-scene diegetic sound design (frames @24fps; scenes start at i*126)
const SFX: { src: string; from: number; vol: number; dur: number }[] = [
  // S1/S3 — surface storm
  { src: "sfx-rain.mp3", from: 0, vol: 0.34, dur: 280 },
  { src: "sfx-wind.mp3", from: 0, vol: 0.3, dur: 280 },
  { src: "sfx-thunder.mp3", from: 34, vol: 0.55, dur: 200 },
  { src: "sfx-thunder.mp3", from: 196, vol: 0.42, dur: 180 },
  { src: "sfx-leaves.mp3", from: 128, vol: 0.4, dur: 132 },
  // S6 — descent
  { src: "sfx-drone.mp3", from: 250, vol: 0.3, dur: 900 },
  { src: "sfx-drips.mp3", from: 262, vol: 0.5, dur: 50 },
  { src: "sfx-drips.mp3", from: 322, vol: 0.45, dur: 50 },
  { src: "sfx-gear.mp3", from: 292, vol: 0.55, dur: 50 },
  // S7 — the reveal
  { src: "sfx-shortriser.mp3", from: 330, vol: 0.6, dur: 62 },
  { src: "sfx-impact.mp3", from: 378, vol: 0.6, dur: 190 },
  { src: "sfx-shimmer.mp3", from: 384, vol: 0.5, dur: 40 },
  { src: "sfx-crowd.mp3", from: 392, vol: 0.15, dur: 760 },
  // core loop
  { src: "sfx-shimmer.mp3", from: 512, vol: 0.32, dur: 40 }, // S10 screen
  { src: "sfx-forgehammer.mp3", from: 658, vol: 0.32, dur: 40 }, // S13 forge
  { src: "sfx-hammer.mp3", from: 782, vol: 0.9, dur: 40 }, // S14 strike
  { src: "sfx-impact.mp3", from: 784, vol: 0.4, dur: 120 },
  { src: "sfx-shimmer.mp3", from: 792, vol: 0.55, dur: 40 }, // chain ignites
  { src: "sfx-shimmer.mp3", from: 892, vol: 0.22, dur: 40 }, // S15
  { src: "sfx-shimmer.mp3", from: 1010, vol: 0.4, dur: 40 }, // S17
  { src: "sfx-coin.mp3", from: 1016, vol: 0.6, dur: 60 },
  // S20 — bookend
  { src: "sfx-wind.mp3", from: 1134, vol: 0.22, dur: 150 },
  { src: "sfx-shimmer.mp3", from: 1158, vol: 0.4, dur: 40 },
  { src: "sfx-coin.mp3", from: 1164, vol: 0.5, dur: 60 },
];

const CLIPS: { id: string; kicker?: string; title?: boolean }[] = [
  { id: "S1", kicker: "UNIVERSITY OF NEBRASKA" },
  { id: "S3" },
  { id: "S6" },
  { id: "S7", title: true },
  { id: "S10" },
  { id: "S13" },
  { id: "S14" },
  { id: "S15" },
  { id: "S17" },
  { id: "S20" },
];

export const HiddenLab: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  const D = 138;
  const OV = 12;
  const step = D - OV;
  const endFrom = CLIPS.length * step - OV + 8;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Audio
        src={staticFile("v2-music-full.mp3")}
        volume={(f) =>
          interpolate(f, [0, 24, durationInFrames - 60, durationInFrames - 4], [0, 0.6, 0.6, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        }
      />

      {SFX.map((s, i) => (
        <Sequence key={`sfx${i}`} from={s.from} durationInFrames={s.dur}>
          <Snd src={s.src} vol={s.vol} dur={s.dur} />
        </Sequence>
      ))}

      {CLIPS.map((c, i) => {
        const from = i * step;
        const total = D;
        return (
          <Sequence key={c.id} from={from} durationInFrames={total + 4}>
            <Beat src={`v2-${c.id}.mp4`} total={total} outS={total - OV} outE={total}>
              {c.kicker && <Kicker outE={total}>{c.kicker}</Kicker>}
              {c.title && <TitleReveal />}
            </Beat>
          </Sequence>
        );
      })}

      <Sequence from={endFrom} durationInFrames={durationInFrames - endFrom}>
        <EndCard />
      </Sequence>
    </AbsoluteFill>
  );
};

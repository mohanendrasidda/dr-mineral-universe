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

const INK = "#efe3cf";
const SERIF = "'Cormorant Garamond', Georgia, serif";
const MONO = "'IBM Plex Mono', ui-monospace, monospace";
const ease = Easing.bezier(0.16, 1, 0.3, 1);

const fadeIO = (f: number, inE: number, outS: number, outE: number) =>
  interpolate(f, [0, inE, outS, outE], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

// one clip beat: letterboxed 2.39 video + its VO, with fade in/out
const Beat: React.FC<{
  src: string;
  vo?: string;
  voDelay?: number;
  total: number;
  inE?: number;
  outS: number;
  outE: number;
  children?: React.ReactNode;
}> = ({ src, vo, voDelay = 8, total, inE = 16, outS, outE, children }) => {
  const f = useCurrentFrame();
  const op = fadeIO(f, inE, outS, outE);
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center" }}>
      <OffthreadVideo
        src={staticFile(src)}
        muted
        style={{ width: "100%", height: "100%", objectFit: "contain", opacity: op }}
      />
      {vo && (
        <Sequence from={voDelay}>
          <Audio src={staticFile(vo)} volume={1} />
        </Sequence>
      )}
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
        top: "16%",
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
  const op = interpolate(f, [40, 70], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: ease });
  const spread = interpolate(f, [40, 110], [0.28, 0.42], { extrapolateRight: "clamp", easing: ease });
  const sub = fadeIO(f, 95, 130, 150);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", flexDirection: "column" }}>
      <div
        style={{
          fontFamily: SERIF,
          fontWeight: 700,
          fontSize: 96,
          color: "#f6e9d0",
          letterSpacing: `${spread}em`,
          opacity: op,
          textShadow: "0 0 60px rgba(245,196,107,.4)",
          paddingLeft: `${spread}em`,
        }}
      >
        THE HIDDEN LAB
      </div>
      <div
        style={{
          fontFamily: MONO,
          fontSize: 18,
          letterSpacing: "0.34em",
          color: "rgba(214,199,170,.85)",
          marginTop: 22,
          opacity: sub,
        }}
      >
        THE LAB REWARD COIN
      </div>
    </AbsoluteFill>
  );
};

export const HiddenLab: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  const D = 140; // ~5.8s per clip at 24fps
  const OV = 12; // crossfade overlap
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {/* music bed (builds) */}
      <Audio
        src={staticFile("score.mp3")}
        volume={(f) =>
          interpolate(f, [0, 60, 300, durationInFrames - 60, durationInFrames - 4], [0, 0.3, 0.4, 0.5, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          })
        }
      />

      {/* S1 — surface */}
      <Sequence from={0} durationInFrames={D}>
        <Beat src="v2-S1.mp4" vo="v2-vo-S1.m4a" total={D} outS={D - OV} outE={D}>
          <Kicker outE={D}>UNIVERSITY OF NEBRASKA</Kicker>
        </Beat>
      </Sequence>

      {/* S3 — stays behind */}
      <Sequence from={D - OV} durationInFrames={D}>
        <Beat src="v2-S3.mp4" vo="v2-vo-S3.m4a" total={D} outS={D - OV} outE={D} />
      </Sequence>

      {/* S6 — descent */}
      <Sequence from={2 * (D - OV)} durationInFrames={D}>
        <Beat src="v2-S6.mp4" vo="v2-vo-S6.m4a" total={D} outS={D - OV} outE={D} />
      </Sequence>

      {/* S7 — the reveal + title */}
      <Sequence from={3 * (D - OV)} durationInFrames={D + 24}>
        <Beat src="v2-S7.mp4" vo="v2-vo-S7.m4a" voDelay={20} total={D + 24} outS={D + 6} outE={D + 24}>
          <TitleReveal />
        </Beat>
      </Sequence>
    </AbsoluteFill>
  );
};

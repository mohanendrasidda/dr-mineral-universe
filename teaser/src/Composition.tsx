import React from "react";
import {
  AbsoluteFill,
  Sequence,
  Img,
  staticFile,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  Easing,
} from "remotion";

// ---- palette ----
const BG = "#0b0d12";
const INK = "#eae3d2";
const GOLD = "#e7b765";
const GOLD2 = "#9a6a3a";
const SERIF = "Georgia, 'Times New Roman', serif";

const ease = Easing.bezier(0.16, 1, 0.3, 1);

// fade-in then fade-out helper based on a local frame
const fadeInOut = (
  f: number,
  inEnd: number,
  outStart: number,
  outEnd: number
) =>
  interpolate(f, [0, inEnd, outStart, outEnd], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });

// ---------- reusable art ----------
const Stars: React.FC<{ count?: number; warm?: boolean }> = ({
  count = 90,
  warm = false,
}) => {
  const frame = useCurrentFrame();
  const dots = new Array(count).fill(0).map((_, i) => {
    const x = (i * 97.13) % 100;
    const y = (i * 53.71) % 60;
    const tw = 0.35 + 0.65 * Math.abs(Math.sin(frame * 0.04 + i));
    const s = 1 + (i % 3);
    return (
      <div
        key={i}
        style={{
          position: "absolute",
          left: `${x}%`,
          top: `${y}%`,
          width: s,
          height: s,
          borderRadius: "50%",
          background: warm ? GOLD : "#ffffff",
          opacity: tw * (warm ? 0.5 : 0.7),
        }}
      />
    );
  });
  return <>{dots}</>;
};

const AcornSVG: React.FC<{ size?: number; color?: string }> = ({
  size = 60,
  color = GOLD,
}) => (
  <svg width={size} height={size * 1.2} viewBox="0 0 100 120">
    <ellipse cx="50" cy="78" rx="30" ry="34" fill={color} />
    <path d="M16 44 Q50 26 84 44 Q84 56 50 58 Q16 56 16 44 Z" fill={GOLD2} />
    <rect x="46" y="20" width="8" height="16" rx="4" fill={GOLD2} />
  </svg>
);

// a small stylized squirrel silhouette
const Squirrel: React.FC<{ color?: string; size?: number }> = ({
  color = "#05070b",
  size = 150,
}) => (
  <svg width={size} height={size} viewBox="0 0 200 200">
    <path d="M150 170 C 210 150 205 60 150 60 C 185 80 175 140 130 150 Z" fill={color} />
    <path d="M70 175 C 55 120 70 95 105 100 C 140 105 140 165 110 178 Z" fill={color} />
    <circle cx="92" cy="92" r="26" fill={color} />
    <path d="M78 70 L82 50 L96 66 Z" fill={color} />
    <circle cx="100" cy="135" r="9" fill={GOLD2} />
  </svg>
);

// ---------- scenes ----------
const SurfaceNight: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const titleOp = fadeInOut(frame, 30, 95, 130);
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(120% 90% at 50% 120%, #1a2230 0%, ${BG} 60%)`,
      }}
    >
      <Stars />
      {[...Array(7)].map((_, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            bottom: height * 0.16,
            left: `${6 + i * 13}%`,
            width: `${7 + (i % 3) * 3}%`,
            height: `${10 + (i % 4) * 7}%`,
            background: "#0c1119",
            borderTop: "2px solid #161d28",
          }}
        />
      ))}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          width,
          height: height * 0.16,
          background: "#070a0e",
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: height * 0.16 - 4,
          left: width * 0.5 - 75,
        }}
      >
        <Squirrel />
      </div>
      <div
        style={{
          position: "absolute",
          width,
          top: height * 0.22,
          textAlign: "center",
          color: INK,
          fontFamily: SERIF,
          fontSize: 52,
          letterSpacing: 1,
          opacity: titleOp,
        }}
      >
        An ordinary campus.
        <div
          style={{
            fontSize: 24,
            color: "#9aa0ab",
            marginTop: 14,
            fontStyle: "italic",
          }}
        >
          Nobody ever looks twice.
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Descent: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const seam = interpolate(frame, [0, 70], [0, height * 1.4], {
    extrapolateRight: "clamp",
    easing: ease,
  });
  const warmth = interpolate(frame, [0, 90], [0, 1], {
    extrapolateRight: "clamp",
  });
  const txt = fadeInOut(frame, 25, 70, 100);
  const imgOp = interpolate(frame, [38, 95], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: ease,
  });
  const imgZoom = interpolate(frame, [38, 110], [1.12, 1.0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ background: BG }}>
      <AbsoluteFill
        style={{
          opacity: warmth,
          background: `radial-gradient(60% 60% at 50% 50%, ${GOLD2}55, ${BG} 70%)`,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: width * 0.5 - seam / 2,
          top: height * 0.5 - seam / 2,
          width: seam,
          height: seam,
          borderRadius: "50%",
          background: `radial-gradient(circle, ${GOLD} 0%, ${GOLD2} 35%, transparent 70%)`,
          filter: "blur(6px)",
        }}
      />
      <Img
        src={staticFile("env-first-descent.png")}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: imgOp,
          transform: `scale(${imgZoom})`,
        }}
      />
      <div
        style={{
          position: "absolute",
          width,
          top: height * 0.78,
          textAlign: "center",
          color: INK,
          fontFamily: SERIF,
          fontSize: 34,
          fontStyle: "italic",
          opacity: txt,
        }}
      >
        …until the morning the ground answered.
      </div>
    </AbsoluteFill>
  );
};

const Cavern: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const reveal = interpolate(frame, [0, 45], [0, 1], {
    extrapolateRight: "clamp",
    easing: ease,
  });
  const zoom = interpolate(frame, [0, 190], [1.04, 1.15], {
    extrapolateRight: "clamp",
  });
  const titleOp = fadeInOut(frame, 50, 135, 180);
  return (
    <AbsoluteFill style={{ background: "#0e0a10" }}>
      <Img
        src={staticFile("env-central-cavern.png")}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
          opacity: reveal,
          transform: `scale(${zoom})`,
        }}
      />
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(80% 70% at 50% 32%, transparent, rgba(8,6,5,.55) 78%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          width,
          top: height * 0.42,
          textAlign: "center",
          color: INK,
          fontFamily: SERIF,
          fontSize: 50,
          letterSpacing: 1,
          opacity: titleOp,
          textShadow: "0 2px 30px #000c",
        }}
      >
        A civilization beneath it.
      </div>
    </AbsoluteFill>
  );
};

const Line: React.FC = () => {
  const frame = useCurrentFrame();
  const { width } = useVideoConfig();
  const op = fadeInOut(frame, 35, 80, 115);
  const rise = interpolate(frame, [0, 50], [16, 0], {
    extrapolateRight: "clamp",
    easing: ease,
  });
  const heroRise = interpolate(frame, [0, 55], [30, 0], {
    extrapolateRight: "clamp",
    easing: ease,
  });
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(80% 80% at 50% 50%, #16120f 0%, ${BG} 75%)`,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          opacity: op,
          display: "flex",
          alignItems: "center",
          gap: 48,
          maxWidth: 1120,
          padding: "0 48px",
        }}
      >
        <Img
          src={staticFile("drmineral-hero.png")}
          style={{
            height: 430,
            transform: `translateY(${heroRise}px)`,
            filter: "drop-shadow(0 18px 50px rgba(231,183,101,.22))",
          }}
        />
        <div style={{ textAlign: "left", transform: `translateY(${rise}px)` }}>
          <div style={{ marginBottom: 16 }}>
            <AcornSVG size={44} />
          </div>
          <div
            style={{
              color: INK,
              fontFamily: SERIF,
              fontSize: 44,
              fontStyle: "italic",
              maxWidth: 520,
              lineHeight: 1.32,
            }}
          >
            “I don't collect treasure.
            <br />I collect discoveries.”
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const ChainGrows: React.FC = () => {
  const frame = useCurrentFrame();
  const links = 9;
  const op = fadeInOut(frame, 25, 90, 115);
  const versions = ["v1", "v8", "v25"];
  const vIdx = Math.min(
    2,
    Math.floor(
      interpolate(frame, [20, 95], [0, 3], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    )
  );
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(90% 80% at 50% 40%, #1a1410 0%, ${BG} 75%)`,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ opacity: op, textAlign: "center" }}>
        <div
          style={{
            display: "flex",
            gap: 10,
            justifyContent: "center",
            marginBottom: 36,
          }}
        >
          {[...Array(links)].map((_, i) => {
            const appear = interpolate(
              frame,
              [i * 7, i * 7 + 22],
              [0, 1],
              {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: ease,
              }
            );
            return (
              <div
                key={i}
                style={{
                  width: 34,
                  height: 34,
                  borderRadius: "50%",
                  border: `4px solid ${GOLD}`,
                  opacity: appear,
                  transform: `scale(${0.6 + appear * 0.4})`,
                  boxShadow: `0 0 18px ${GOLD2}`,
                }}
              />
            );
          })}
        </div>
        <div
          style={{ color: INK, fontFamily: SERIF, fontSize: 44, letterSpacing: 1 }}
        >
          The lab keeps growing.
        </div>
        <div
          style={{
            color: GOLD,
            fontFamily: SERIF,
            fontSize: 30,
            marginTop: 14,
            letterSpacing: 4,
          }}
        >
          {versions[vIdx]} →
        </div>
      </div>
    </AbsoluteFill>
  );
};

const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const op = interpolate(frame, [0, 40], [0, 1], {
    extrapolateRight: "clamp",
    easing: ease,
  });
  const spread = interpolate(frame, [0, 60], [16, 7], {
    extrapolateRight: "clamp",
    easing: ease,
  });
  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(70% 70% at 50% 45%, #1c1510 0%, ${BG} 80%)`,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div style={{ opacity: op, textAlign: "center" }}>
        <div
          style={{ display: "flex", justifyContent: "center", marginBottom: 22 }}
        >
          <AcornSVG size={64} />
        </div>
        <div
          style={{
            color: INK,
            fontFamily: SERIF,
            fontWeight: 700,
            fontSize: 60,
            letterSpacing: spread,
          }}
        >
          THE DR. MINERAL
        </div>
        <div
          style={{
            color: GOLD,
            fontFamily: SERIF,
            fontWeight: 700,
            fontSize: 60,
            letterSpacing: spread + 6,
            marginTop: 4,
          }}
        >
          UNIVERSE
        </div>
        <div
          style={{
            color: "#9aa0ab",
            fontFamily: SERIF,
            fontStyle: "italic",
            fontSize: 26,
            marginTop: 22,
          }}
        >
          an underground civilization of curious minds
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- main ----------
export const Teaser: React.FC = () => {
  return (
    <AbsoluteFill style={{ background: BG }}>
      <Sequence durationInFrames={150}>
        <SurfaceNight />
      </Sequence>
      <Sequence from={150} durationInFrames={110}>
        <Descent />
      </Sequence>
      <Sequence from={260} durationInFrames={190}>
        <Cavern />
      </Sequence>
      <Sequence from={450} durationInFrames={120}>
        <Line />
      </Sequence>
      <Sequence from={570} durationInFrames={120}>
        <ChainGrows />
      </Sequence>
      <Sequence from={690} durationInFrames={90}>
        <TitleCard />
      </Sequence>
    </AbsoluteFill>
  );
};

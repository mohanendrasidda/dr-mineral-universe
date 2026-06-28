import "./index.css";
import { Composition } from "remotion";
import { Teaser } from "./Composition";
import { HiddenLab } from "./HiddenLab";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="DrMineralTeaser"
        component={Teaser}
        durationInFrames={1366}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="HiddenLabTeaser"
        component={HiddenLab}
        durationInFrames={550}
        fps={24}
        width={1920}
        height={1080}
      />
    </>
  );
};

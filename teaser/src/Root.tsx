import "./index.css";
import { Composition } from "remotion";
import { Teaser } from "./Composition";

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
    </>
  );
};

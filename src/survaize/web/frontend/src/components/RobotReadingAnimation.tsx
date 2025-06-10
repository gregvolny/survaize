import React from "react";
import RobotReadingGraphic, {
  RobotReadingGraphicProps,
} from "./RobotReadingGraphic";

const RobotReadingAnimation: React.FC<RobotReadingGraphicProps> = (props) => {
  return <RobotReadingGraphic {...props} />;
};

export default RobotReadingAnimation;

import React from 'react';

export const RobotReadingAnimation: React.FC = () => (
  <svg
    className="robot-animation"
    width="120"
    height="120"
    viewBox="0 0 120 120"
    aria-hidden="true"
  >
    <rect x="50" y="10" width="20" height="10" rx="2" className="robot-antenna" />
    <rect x="30" y="20" width="60" height="50" rx="8" className="robot-head" />
    <g className="robot-eye" transform="translate(50,40)">
      <circle cx="0" cy="0" r="8" fill="#fff" />
      <circle cx="0" cy="0" r="4" className="robot-eye-pupil" />
    </g>
    <g className="robot-eye" transform="translate(70,40)">
      <circle cx="0" cy="0" r="8" fill="#fff" />
      <circle cx="0" cy="0" r="4" className="robot-eye-pupil" />
    </g>
    <rect x="45" y="65" width="30" height="35" rx="2" className="robot-paper" />
  </svg>
);

export default RobotReadingAnimation;

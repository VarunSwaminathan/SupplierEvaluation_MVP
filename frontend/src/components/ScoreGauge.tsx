import { useEffect, useState } from "react";

interface ScoreGaugeProps {
  score: number;
  maxScore?: number;
}

export const ScoreGauge = ({ score, maxScore = 100 }: ScoreGaugeProps) => {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedScore(score);
    }, 100);
    return () => clearTimeout(timer);
  }, [score]);

  const percentage = (animatedScore / maxScore) * 100;
  const rotation = (percentage / 100) * 180;

  const getColor = (pct: number) => {
    if (pct >= 80) return "hsl(var(--success))";
    if (pct >= 60) return "hsl(var(--primary))";
    if (pct >= 40) return "hsl(var(--warning))";
    return "hsl(var(--destructive))";
  };

  return (
    <div className="relative w-full max-w-xs mx-auto">
      <svg viewBox="0 0 200 120" className="w-full">
        {/* Background arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="hsl(var(--muted))"
          strokeWidth="20"
          strokeLinecap="round"
        />
        {/* Animated arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={getColor(percentage)}
          strokeWidth="20"
          strokeLinecap="round"
          strokeDasharray="251.2"
          strokeDashoffset={251.2 - (251.2 * percentage) / 100}
          style={{
            transition: "stroke-dashoffset 1.5s ease-out, stroke 0.5s ease",
          }}
        />
        {/* Center text */}
        <text
          x="100"
          y="85"
          textAnchor="middle"
          className="text-4xl font-bold fill-foreground"
        >
          {animatedScore.toFixed(0)}
        </text>
        <text
          x="100"
          y="105"
          textAnchor="middle"
          className="text-sm fill-muted-foreground"
        >
          Overall Score
        </text>
      </svg>
    </div>
  );
};

import { cn } from "@/lib/utils";

interface GradeBadgeProps {
  grade: string;
  className?: string;
}

const gradeConfig: Record<string, { bg: string; text: string; border: string }> = {
  A: { bg: "bg-success/10", text: "text-success", border: "border-success/30" },
  B: { bg: "bg-primary/10", text: "text-primary", border: "border-primary/30" },
  C: { bg: "bg-warning/10", text: "text-warning", border: "border-warning/30" },
  D: { bg: "bg-destructive/10", text: "text-destructive", border: "border-destructive/30" },
  F: { bg: "bg-destructive/20", text: "text-destructive", border: "border-destructive/50" },
};

export const GradeBadge = ({ grade, className }: GradeBadgeProps) => {
  const config = gradeConfig[grade] || gradeConfig.C;

  return (
    <div
      className={cn(
        "inline-flex items-center justify-center w-24 h-24 rounded-2xl border-2 font-bold text-5xl shadow-soft transition-all duration-300 hover:scale-105",
        config.bg,
        config.text,
        config.border,
        className
      )}
    >
      {grade}
    </div>
  );
};

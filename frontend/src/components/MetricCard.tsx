import { Card } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  icon: LucideIcon;
  label: string;
  value: string | number;
  suffix?: string;
  trend?: "up" | "down" | "neutral";
}

export const MetricCard = ({ icon: Icon, label, value, suffix, trend }: MetricCardProps) => {
  const trendColor = trend === "up" ? "text-success" : trend === "down" ? "text-destructive" : "text-muted-foreground";

  return (
    <Card className="p-6 shadow-card bg-gradient-card hover:shadow-soft transition-shadow duration-300">
      <div className="flex items-start justify-between">
        <div className="space-y-2 flex-1">
          <p className="text-sm font-medium text-muted-foreground">{label}</p>
          <div className="flex items-baseline gap-1">
            <span className="text-3xl font-bold text-foreground">{value}</span>
            {suffix && <span className="text-lg text-muted-foreground">{suffix}</span>}
          </div>
        </div>
        <div className="p-3 bg-accent rounded-xl">
          <Icon className="w-5 h-5 text-accent-foreground" />
        </div>
      </div>
    </Card>
  );
};

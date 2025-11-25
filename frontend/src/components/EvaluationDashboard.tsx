import { Card } from "@/components/ui/card";
import { GradeBadge } from "./GradeBadge";
import { ScoreGauge } from "./ScoreGauge";
import { MetricCard } from "./MetricCard";
import { TrendingUp, DollarSign, Clock, AlertTriangle, CheckCircle2 } from "lucide-react";

interface EvaluationData {
  supplier_grade: string;
  overall_score: number;
  rationale: string;
  lender_concerns: string[];
  strengths: string[];
  details: {
    operational_metrics: {
      on_time_delivery_rate: number;
      invoice_paid_rate: number;
    };
    financial_ratios: {
      current_ratio: number;
      debt_to_equity: number;
    };
  };
}

interface EvaluationDashboardProps {
  data: EvaluationData | null;
}

export const EvaluationDashboard = ({ data }: EvaluationDashboardProps) => {
  if (!data) {
    return (
      <Card className="p-12 shadow-card bg-gradient-card">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center mx-auto">
            <TrendingUp className="w-8 h-8 text-accent-foreground" />
          </div>
          <h3 className="text-xl font-semibold text-foreground">No Data Yet</h3>
          <p className="text-muted-foreground">Upload documents to see the evaluation results</p>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Header with Grade and Score */}
      <Card className="p-8 shadow-card bg-gradient-card">
        <div className="grid md:grid-cols-2 gap-8 items-center">
          <div className="flex flex-col items-center space-y-4">
            <h3 className="text-sm font-medium text-muted-foreground uppercase tracking-wider">
              Supplier Grade
            </h3>
            <GradeBadge grade={data.supplier_grade} />
          </div>
          <div className="flex flex-col items-center">
            <ScoreGauge score={data.overall_score} />
          </div>
        </div>
      </Card>

      {/* Analysis Rationale */}
      <Card className="p-6 shadow-card bg-gradient-card">
        <h3 className="text-lg font-semibold text-foreground mb-3">Analysis</h3>
        <p className="text-muted-foreground leading-relaxed">{data.rationale}</p>
      </Card>

      {/* Metrics Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={Clock}
          label="On-Time Delivery"
          value={data.details.operational_metrics.on_time_delivery_rate.toFixed(1)}
          suffix="%"
        />
        <MetricCard
          icon={DollarSign}
          label="Invoice Paid Rate"
          value={data.details.operational_metrics.invoice_paid_rate.toFixed(1)}
          suffix="%"
        />
        <MetricCard
          icon={TrendingUp}
          label="Current Ratio"
          value={data.details.financial_ratios.current_ratio.toFixed(2)}
        />
        <MetricCard
          icon={DollarSign}
          label="Debt-to-Equity"
          value={data.details.financial_ratios.debt_to_equity.toFixed(2)}
        />
      </div>

      {/* Risks and Strengths */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="p-6 shadow-card bg-gradient-card">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="w-5 h-5 text-destructive" />
            <h3 className="text-lg font-semibold text-foreground">Lender Concerns</h3>
          </div>
          <ul className="space-y-3">
            {data.lender_concerns.map((concern, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-muted-foreground">
                <span className="w-1.5 h-1.5 bg-destructive rounded-full mt-2 flex-shrink-0" />
                <span>{concern}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-6 shadow-card bg-gradient-card">
          <div className="flex items-center gap-2 mb-4">
            <CheckCircle2 className="w-5 h-5 text-success" />
            <h3 className="text-lg font-semibold text-foreground">Strengths</h3>
          </div>
          <ul className="space-y-3">
            {data.strengths.map((strength, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-muted-foreground">
                <span className="w-1.5 h-1.5 bg-success rounded-full mt-2 flex-shrink-0" />
                <span>{strength}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
};

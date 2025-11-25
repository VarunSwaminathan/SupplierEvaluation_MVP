import { useState } from "react";
import { FileUpload } from "@/components/FileUpload";
import { EvaluationDashboard } from "@/components/EvaluationDashboard";

const Index = () => {
  const [evaluationData, setEvaluationData] = useState(null);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card shadow-soft">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Supplier Evaluation Platform
          </h1>
          <p className="text-muted-foreground mt-1">
            Comprehensive financial and operational analysis
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 space-y-8">
        <FileUpload onUploadComplete={setEvaluationData} />
        <EvaluationDashboard data={evaluationData} />
      </main>
    </div>
  );
};

export default Index;

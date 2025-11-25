import { useState, useCallback } from "react";
import { Upload, FileText, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";

interface FileUploadProps {
  onUploadComplete: (data: any) => void;
}

interface FileCategory {
  key: string;
  label: string;
  files: File[];
}

export const FileUpload = ({ onUploadComplete }: FileUploadProps) => {
  const { toast } = useToast();
  const [isUploading, setIsUploading] = useState(false);
  const [categories] = useState<FileCategory[]>([
    { key: "po_files", label: "Purchase Orders", files: [] },
    { key: "inv_files", label: "Invoices", files: [] },
    { key: "financial_files", label: "Financial Statements (PDF)", files: [] },
  ]);
  const [filesByCategory, setFilesByCategory] = useState<Record<string, File[]>>({
    po_files: [],
    inv_files: [],
    financial_files: [],
  });

  const handleDrop = useCallback((e: React.DragEvent, categoryKey: string) => {
    e.preventDefault();
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFilesByCategory((prev) => ({
      ...prev,
      [categoryKey]: [...prev[categoryKey], ...droppedFiles],
    }));
  }, []);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>, categoryKey: string) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      setFilesByCategory((prev) => ({
        ...prev,
        [categoryKey]: [...prev[categoryKey], ...selectedFiles],
      }));
    }
  }, []);

  const removeFile = useCallback((categoryKey: string, index: number) => {
    setFilesByCategory((prev) => ({
      ...prev,
      [categoryKey]: prev[categoryKey].filter((_, i) => i !== index),
    }));
  }, []);

  const handleUpload = async () => {
    const totalFiles = Object.values(filesByCategory).flat().length;
    if (totalFiles === 0) {
      toast({
        title: "No files selected",
        description: "Please add files to upload",
        variant: "destructive",
      });
      return;
    }

    setIsUploading(true);
    const formData = new FormData();

    Object.entries(filesByCategory).forEach(([key, files]) => {
      files.forEach((file) => {
        formData.append(key, file);
      });
    });

    try {
      console.log("Starting upload to backend...");
      const response = await fetch("https://c5269af321bf.ngrok-free.app/upload/full_evaluation", {
        method: "POST",
        headers: {
          "ngrok-skip-browser-warning": "69420",
        },
        body: formData,
      });

      console.log("Response status:", response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Server error response:", errorText);
        throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Upload successful, received data:", data);
      onUploadComplete(data);
      
      toast({
        title: "Upload successful",
        description: "Files analyzed successfully",
      });

      // Clear files after successful upload
      setFilesByCategory({
        po_files: [],
        inv_files: [],
        financial_files: [],
      });
    } catch (error) {
      console.error("Upload error details:", error);
      
      let errorMessage = "An error occurred";
      if (error instanceof TypeError && error.message.includes("fetch")) {
        errorMessage = "Cannot connect to backend. Check if: 1) Backend is running 2) CORS is configured 3) Ngrok tunnel is active";
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      toast({
        title: "Upload failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card className="p-6 space-y-6 shadow-card bg-gradient-card">
      <div className="space-y-1">
        <h2 className="text-2xl font-bold text-foreground">Upload Documents</h2>
        <p className="text-sm text-muted-foreground">
          Upload purchase orders, invoices, and financial statements for evaluation
        </p>
      </div>

      <div className="space-y-4">
        {categories.map((category) => (
          <div key={category.key} className="space-y-2">
            <label className="text-sm font-medium text-foreground">{category.label}</label>
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => handleDrop(e, category.key)}
              className="border-2 border-dashed border-border rounded-lg p-6 transition-colors hover:border-primary/50 hover:bg-accent/5"
            >
              <div className="flex flex-col items-center gap-2 text-center">
                <Upload className="w-8 h-8 text-muted-foreground" />
                <div className="text-sm text-muted-foreground">
                  Drag & drop files or{" "}
                  <label className="text-primary cursor-pointer hover:underline">
                    browse
                    <input
                      type="file"
                      multiple
                      className="hidden"
                      onChange={(e) => handleFileInput(e, category.key)}
                      accept={category.key === "financial_files" ? ".pdf" : "*"}
                    />
                  </label>
                </div>
              </div>

              {filesByCategory[category.key].length > 0 && (
                <div className="mt-4 space-y-2">
                  {filesByCategory[category.key].map((file, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between p-2 bg-accent rounded-md"
                    >
                      <div className="flex items-center gap-2">
                        <FileText className="w-4 h-4 text-accent-foreground" />
                        <span className="text-sm text-accent-foreground truncate">{file.name}</span>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(category.key, index)}
                        className="h-6 w-6 p-0"
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <Button
        onClick={handleUpload}
        disabled={isUploading}
        className="w-full bg-gradient-primary hover:opacity-90 transition-opacity"
        size="lg"
      >
        {isUploading ? "Analyzing..." : "Upload & Analyze"}
      </Button>
    </Card>
  );
};

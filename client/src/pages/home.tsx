import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useToast } from "@/hooks/use-toast";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";
import { apiRequest } from "@/lib/queryClient";

export default function Home() {
    const [file, setFile] = useState<File | null>(null);
    const [title, setTitle] = useState("");
    const { toast } = useToast();

    const uploadMutation = useMutation({
        mutationFn: async (formData: FormData) => {
            // The API endpoint is absolute to avoid path issues
            const res = await fetch("http://localhost:8000/pipeline/upload", {
                method: "POST",
                body: formData,
                // Do not set Content-Type header manually for FormData, fetch does it automatically with boundary
            });

            if (!res.ok) {
                const text = await res.text();
                throw new Error(`Upload failed: ${res.status} ${text}`);
            }

            return res.json();
        },
        onSuccess: (data) => {
            toast({
                title: "Success",
                description: `Podcast uploaded! ID: ${data.podcast_id}`,
            });
            // Reset form
            setFile(null);
            setTitle("");
        },
        onError: (error) => {
            toast({
                title: "Error",
                description: error.message,
                variant: "destructive",
            });
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!file || !title) {
            toast({
                title: "Error",
                description: "Please select a file and enter a title",
                variant: "destructive",
            });
            return;
        }

        const formData = new FormData();
        formData.append("file", file);
        formData.append("title", title);

        uploadMutation.mutate(formData);
    };

    return (
        <div className="container mx-auto p-8 max-w-2xl text-center">
            <h1 className="text-4xl font-extrabold mb-8 bg-gradient-to-r from-purple-600 to-blue-500 bg-clip-text text-transparent">
                PodC Summarizer
            </h1>

            <Card className="w-full text-left">
                <CardHeader>
                    <CardTitle>Upload Podcast</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="space-y-2">
                            <Label htmlFor="title">Podcast Title</Label>
                            <Input
                                id="title"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                placeholder="Enter podcast title"
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="file">Audio File</Label>
                            <Input
                                id="file"
                                type="file"
                                accept="audio/*"
                                onChange={(e) => setFile(e.target.files?.[0] || null)}
                            />
                        </div>

                        <Button
                            type="submit"
                            className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                            disabled={uploadMutation.isPending}
                        >
                            {uploadMutation.isPending ? (
                                <>
                                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                    Uploading & Processing...
                                </>
                            ) : (
                                "Start Summarization"
                            )}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}

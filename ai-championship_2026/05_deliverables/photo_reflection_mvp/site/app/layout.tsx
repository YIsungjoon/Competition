import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "사진이 묻는 하루",
  description: "사진과 대화하며 오늘을 더 깊이 돌아보는 AI 기억 인터뷰",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased">{children}</body>
    </html>
  );
}

import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Trial Lesson Booking",
  description: "Telegram × Notion CRM — Education enrollment system",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

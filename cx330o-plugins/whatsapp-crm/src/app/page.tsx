"use client";
import { useState, useEffect } from "react";

const TRANSLATIONS: Record<string, Record<string, string>> = {
  en: {
    title: "Reserve a Table",
    date: "Date & Time",
    guests: "Number of Guests",
    seating: "Seating Preference",
    indoor: "Indoor",
    outdoor: "Outdoor",
    private: "Private Room",
    request: "Special Requests (allergies, birthday, etc.)",
    submit: "Confirm Reservation",
    submitting: "Submitting...",
    success: "Reservation confirmed! You'll receive a WhatsApp confirmation shortly.",
    error: "Something went wrong. Please try again.",
  },
  th: {
    title: "จองโต๊ะ",
    date: "วันที่และเวลา",
    guests: "จำนวนผู้เข้าพัก",
    seating: "ประเภทที่นั่ง",
    indoor: "ในร่ม",
    outdoor: "กลางแจ้ง",
    private: "ห้องส่วนตัว",
    request: "คำขอพิเศษ (แพ้อาหาร, วันเกิด ฯลฯ)",
    submit: "ยืนยันการจอง",
    submitting: "กำลังส่ง...",
    success: "จองสำเร็จ! คุณจะได้รับข้อความยืนยันทาง WhatsApp",
    error: "เกิดข้อผิดพลาด กรุณาลองอีกครั้ง",
  },
  ar: {
    title: "حجز طاولة",
    date: "التاريخ والوقت",
    guests: "عدد الضيوف",
    seating: "تفضيل الجلوس",
    indoor: "داخلي",
    outdoor: "خارجي",
    private: "غرفة خاصة",
    request: "طلبات خاصة (حساسية، عيد ميلاد، إلخ)",
    submit: "تأكيد الحجز",
    submitting: "جاري الإرسال...",
    success: "تم تأكيد الحجز! ستتلقى رسالة تأكيد عبر واتساب",
    error: "حدث خطأ. يرجى المحاولة مرة أخرى",
  },
  zh: {
    title: "预约餐位",
    date: "日期和时间",
    guests: "用餐人数",
    seating: "座位偏好",
    indoor: "室内",
    outdoor: "户外",
    private: "包间",
    request: "特殊要求（过敏、生日等）",
    submit: "确认预约",
    submitting: "提交中...",
    success: "预约成功！您将通过 WhatsApp 收到确认消息。",
    error: "出错了，请重试。",
  },
};

export default function ReservationForm() {
  const [lang, setLang] = useState("en");
  const [phone, setPhone] = useState("");
  const [form, setForm] = useState({ date: "", guests: 2, seating: "indoor", request: "" });
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");

  const t = TRANSLATIONS[lang] || TRANSLATIONS.en;

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setPhone(params.get("phone") || "");
    setLang(params.get("lang") || "en");
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("submitting");
    try {
      const webhookUrl = process.env.NEXT_PUBLIC_WEBHOOK_URL;
      if (!webhookUrl) throw new Error("Webhook URL not configured");
      const res = await fetch(webhookUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ phone, lang, ...form }),
      });
      setStatus(res.ok ? "success" : "error");
    } catch {
      setStatus("error");
    }
  };

  if (status === "success") {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#ECE5DD]">
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md text-center">
          <div className="text-5xl mb-4">✅</div>
          <p className="text-lg text-gray-700">{t.success}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-[#ECE5DD]" dir={lang === "ar" ? "rtl" : "ltr"}>
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md space-y-5">
        <h1 className="text-2xl font-bold text-[#075E54] text-center">{t.title}</h1>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">{t.date}</label>
          <input
            type="datetime-local"
            required
            value={form.date}
            onChange={(e) => setForm({ ...form, date: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#25D366] focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">{t.guests}</label>
          <input
            type="number"
            min={1}
            max={20}
            required
            value={form.guests}
            onChange={(e) => setForm({ ...form, guests: Number(e.target.value) })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#25D366] focus:outline-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">{t.seating}</label>
          <select
            value={form.seating}
            onChange={(e) => setForm({ ...form, seating: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#25D366] focus:outline-none"
          >
            <option value="indoor">{t.indoor}</option>
            <option value="outdoor">{t.outdoor}</option>
            <option value="private">{t.private}</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">{t.request}</label>
          <textarea
            rows={3}
            value={form.request}
            onChange={(e) => setForm({ ...form, request: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#25D366] focus:outline-none"
          />
        </div>

        <button
          type="submit"
          disabled={status === "submitting"}
          className="w-full bg-[#25D366] hover:bg-[#128C7E] text-white font-semibold py-3 rounded-lg transition disabled:opacity-50"
        >
          {status === "submitting" ? t.submitting : t.submit}
        </button>

        {status === "error" && <p className="text-red-500 text-center text-sm">{t.error}</p>}
      </form>
    </div>
  );
}

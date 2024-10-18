"use client";
import { useState, useEffect } from "react";

const TRANSLATIONS: Record<string, Record<string, string>> = {
  en: {
    title: "Book a Trial Lesson",
    name: "Full Name",
    email: "Email",
    phone: "Phone Number",
    course: "Course Interest",
    level: "Current Level",
    beginner: "Beginner",
    intermediate: "Intermediate",
    advanced: "Advanced",
    format: "Preferred Format",
    online: "Online",
    offline: "In-person",
    date: "Preferred Date & Time",
    notes: "Questions or Notes",
    submit: "Book Trial Lesson",
    submitting: "Submitting...",
    success: "You're all set! Check Telegram for your confirmation.",
    error: "Something went wrong. Please try again.",
  },
  ru: {
    title: "Записаться на пробный урок",
    name: "ФИО",
    email: "Электронная почта",
    phone: "Телефон",
    course: "Интересующий курс",
    level: "Текущий уровень",
    beginner: "Начинающий",
    intermediate: "Средний",
    advanced: "Продвинутый",
    format: "Формат",
    online: "Онлайн",
    offline: "Очно",
    date: "Желаемая дата и время",
    notes: "Вопросы или примечания",
    submit: "Записаться",
    submitting: "Отправка...",
    success: "Готово! Проверьте Telegram для подтверждения.",
    error: "Произошла ошибка. Попробуйте ещё раз.",
  },
  vi: {
    title: "Đăng ký học thử",
    name: "Họ và tên",
    email: "Email",
    phone: "Số điện thoại",
    course: "Khóa học quan tâm",
    level: "Trình độ hiện tại",
    beginner: "Mới bắt đầu",
    intermediate: "Trung cấp",
    advanced: "Nâng cao",
    format: "Hình thức",
    online: "Trực tuyến",
    offline: "Trực tiếp",
    date: "Ngày giờ mong muốn",
    notes: "Câu hỏi hoặc ghi chú",
    submit: "Đăng ký học thử",
    submitting: "Đang gửi...",
    success: "Đăng ký thành công! Kiểm tra Telegram để xác nhận.",
    error: "Đã xảy ra lỗi. Vui lòng thử lại.",
  },
};

const COURSES = [
  { id: "english", label: "🇬🇧 English" },
  { id: "japanese", label: "🇯🇵 Japanese" },
  { id: "chinese", label: "🇨🇳 Chinese" },
  { id: "programming", label: "💻 Programming" },
  { id: "design", label: "🎨 Design" },
];

export default function TrialLessonForm() {
  const [lang, setLang] = useState("en");
  const [chatId, setChatId] = useState("");
  const [form, setForm] = useState({
    name: "", email: "", phone: "", course: "", level: "beginner", format: "online", date: "", notes: "",
  });
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");

  const t = TRANSLATIONS[lang] || TRANSLATIONS.en;

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setChatId(params.get("chat_id") || "");
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
        body: JSON.stringify({ chat_id: chatId, lang, ...form }),
      });
      setStatus(res.ok ? "success" : "error");
    } catch {
      setStatus("error");
    }
  };

  if (status === "success") {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50">
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md text-center">
          <div className="text-5xl mb-4">🎓</div>
          <p className="text-lg text-gray-700">{t.success}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-cyan-50 p-4">
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md space-y-4">
        <h1 className="text-2xl font-bold text-center text-[#0088cc]">{t.title}</h1>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">{t.name}</label>
          <input type="text" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#0088cc] focus:outline-none" />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">{t.email}</label>
            <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#0088cc] focus:outline-none" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">{t.phone}</label>
            <input type="tel" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#0088cc] focus:outline-none" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-2">{t.course}</label>
          <div className="grid grid-cols-2 gap-2">
            {COURSES.map((c) => (
              <label key={c.id} className={`flex items-center gap-2 p-2 rounded-lg border cursor-pointer transition text-sm ${
                form.course === c.id ? "border-[#0088cc] bg-blue-50" : "border-gray-200 hover:border-blue-300"
              }`}>
                <input type="radio" name="course" value={c.id} checked={form.course === c.id}
                  onChange={(e) => setForm({ ...form, course: e.target.value })} className="accent-[#0088cc]" />
                {c.label}
              </label>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">{t.level}</label>
            <select value={form.level} onChange={(e) => setForm({ ...form, level: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#0088cc] focus:outline-none">
              <option value="beginner">{t.beginner}</option>
              <option value="intermediate">{t.intermediate}</option>
              <option value="advanced">{t.advanced}</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">{t.format}</label>
            <select value={form.format} onChange={(e) => setForm({ ...form, format: e.target.value })}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#0088cc] focus:outline-none">
              <option value="online">{t.online}</option>
              <option value="offline">{t.offline}</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">{t.date}</label>
          <input type="datetime-local" required value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#0088cc] focus:outline-none" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">{t.notes}</label>
          <textarea rows={2} value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#0088cc] focus:outline-none" />
        </div>

        <button type="submit" disabled={status === "submitting" || !form.course}
          className="w-full bg-[#0088cc] hover:bg-[#006699] text-white font-semibold py-3 rounded-lg transition disabled:opacity-50">
          {status === "submitting" ? t.submitting : t.submit}
        </button>

        {status === "error" && <p className="text-red-500 text-center text-sm">{t.error}</p>}
      </form>
    </div>
  );
}

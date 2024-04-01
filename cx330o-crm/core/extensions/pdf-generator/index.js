/**
 * cx330o PDF Invoice/Quote Generator
 * 
 * Standalone microservice for generating PDF invoices and quotes.
 * Supports multi-currency, custom templates, and company logos.
 * Called via REST API from cx330o CRM.
 */

const express = require("express");
const PDFDocument = require("pdfkit");

const app = express();
app.use(express.json());

// 生成发票 PDF
app.post("/api/invoice", (req, res) => {
  const { invoice_number, date, due_date, company, client, items, notes, currency = "USD" } = req.body;

  const doc = new PDFDocument({ margin: 50 });
  res.setHeader("Content-Type", "application/pdf");
  res.setHeader("Content-Disposition", `attachment; filename=invoice-${invoice_number}.pdf`);
  doc.pipe(res);

  // Header
  doc.fontSize(20).text(company?.name || "Company Name", 50, 50);
  doc.fontSize(10).text(company?.address || "", 50, 75);
  doc.fontSize(10).text(company?.email || "", 50, 90);

  // Invoice info
  doc.fontSize(16).text("INVOICE", 400, 50, { align: "right" });
  doc.fontSize(10).text(`#${invoice_number}`, 400, 75, { align: "right" });
  doc.text(`Date: ${date}`, 400, 90, { align: "right" });
  doc.text(`Due: ${due_date}`, 400, 105, { align: "right" });

  // Client info
  doc.fontSize(12).text("Bill To:", 50, 140);
  doc.fontSize(10).text(client?.name || "", 50, 158);
  doc.text(client?.address || "", 50, 173);
  doc.text(client?.email || "", 50, 188);

  // Items table
  let y = 230;
  doc.fontSize(10).font("Helvetica-Bold");
  doc.text("Item", 50, y);
  doc.text("Qty", 280, y, { width: 60, align: "right" });
  doc.text("Price", 350, y, { width: 80, align: "right" });
  doc.text("Total", 440, y, { width: 80, align: "right" });
  doc.moveTo(50, y + 15).lineTo(520, y + 15).stroke();

  y += 25;
  doc.font("Helvetica");
  let subtotal = 0;
  for (const item of items || []) {
    const total = (item.quantity || 0) * (item.price || 0);
    subtotal += total;
    doc.text(item.description || "", 50, y, { width: 220 });
    doc.text(String(item.quantity || 0), 280, y, { width: 60, align: "right" });
    doc.text(`${currency} ${(item.price || 0).toFixed(2)}`, 350, y, { width: 80, align: "right" });
    doc.text(`${currency} ${total.toFixed(2)}`, 440, y, { width: 80, align: "right" });
    y += 20;
  }

  // Total
  doc.moveTo(350, y + 5).lineTo(520, y + 5).stroke();
  y += 15;
  doc.font("Helvetica-Bold");
  doc.text("Total:", 350, y, { width: 80, align: "right" });
  doc.text(`${currency} ${subtotal.toFixed(2)}`, 440, y, { width: 80, align: "right" });

  // Notes
  if (notes) {
    y += 40;
    doc.font("Helvetica").fontSize(9).text("Notes:", 50, y);
    doc.text(notes, 50, y + 15, { width: 470 });
  }

  doc.end();
});

// 生成报价单 PDF
app.post("/api/quote", (req, res) => {
  const { quote_number, date, valid_until, company, client, items, terms, currency = "USD" } = req.body;

  const doc = new PDFDocument({ margin: 50 });
  res.setHeader("Content-Type", "application/pdf");
  res.setHeader("Content-Disposition", `attachment; filename=quote-${quote_number}.pdf`);
  doc.pipe(res);

  doc.fontSize(20).text(company?.name || "Company Name", 50, 50);
  doc.fontSize(16).text("QUOTATION", 400, 50, { align: "right" });
  doc.fontSize(10).text(`#${quote_number}`, 400, 75, { align: "right" });
  doc.text(`Date: ${date}`, 400, 90, { align: "right" });
  doc.text(`Valid Until: ${valid_until}`, 400, 105, { align: "right" });

  doc.fontSize(12).text("To:", 50, 140);
  doc.fontSize(10).text(client?.name || "", 50, 158);
  doc.text(client?.company || "", 50, 173);

  let y = 210;
  let subtotal = 0;
  doc.font("Helvetica-Bold").fontSize(10);
  doc.text("Description", 50, y);
  doc.text("Amount", 440, y, { width: 80, align: "right" });
  doc.moveTo(50, y + 15).lineTo(520, y + 15).stroke();
  y += 25;

  doc.font("Helvetica");
  for (const item of items || []) {
    const total = (item.quantity || 1) * (item.price || 0);
    subtotal += total;
    doc.text(item.description || "", 50, y, { width: 380 });
    doc.text(`${currency} ${total.toFixed(2)}`, 440, y, { width: 80, align: "right" });
    y += 20;
  }

  doc.moveTo(350, y + 5).lineTo(520, y + 5).stroke();
  y += 15;
  doc.font("Helvetica-Bold");
  doc.text("Total:", 350, y, { width: 80, align: "right" });
  doc.text(`${currency} ${subtotal.toFixed(2)}`, 440, y, { width: 80, align: "right" });

  if (terms) {
    y += 40;
    doc.font("Helvetica").fontSize(9).text("Terms & Conditions:", 50, y);
    doc.text(terms, 50, y + 15, { width: 470 });
  }

  doc.end();
});

app.get("/health", (_, res) => res.json({ status: "ok" }));

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => console.log(`PDF Generator running on port ${PORT}`));

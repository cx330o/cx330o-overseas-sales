"""
统一输出层 — 整合多种输出方式：
- CSV 写入
- Google Sheets 集成
- 新增 JSON 和数据库输出
"""

import csv
import json
import logging
from pathlib import Path

from .models import Lead, Review

logger = logging.getLogger(__name__)


class OutputManager:
    """统一输出管理器"""

    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def to_csv(self, leads: list[Lead], filename: str = "leads.csv"):
        path = self.output_dir / filename
        if not leads:
            logger.warning("No leads to export")
            return

        fieldnames = [
            "business_name", "category", "address", "phone", "website",
            "email", "rating", "review_count", "domain", "emails_found",
            "ai_summary", "ai_personalized_message", "source", "source_url", "scraped_at",
        ]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for lead in leads:
                row = lead.model_dump(include=set(fieldnames))
                row["emails_found"] = "; ".join(row.get("emails_found", []))
                row["scraped_at"] = str(row.get("scraped_at", ""))
                writer.writerow(row)

        logger.info(f"✅ Exported {len(leads)} leads to {path}")

    def to_json(self, leads: list[Lead], filename: str = "leads.json"):
        path = self.output_dir / filename
        data = [lead.model_dump(mode="json") for lead in leads]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"✅ Exported {len(leads)} leads to {path}")

    def reviews_to_csv(self, reviews: list[Review], filename: str = "reviews.csv"):
        path = self.output_dir / filename
        if not reviews:
            return
        fieldnames = [
            "lead_dedup_key", "reviewer_name", "rating", "text",
            "translated_text", "relative_date", "owner_response", "scraped_at",
        ]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in reviews:
                row = r.model_dump(include=set(fieldnames))
                row["scraped_at"] = str(row.get("scraped_at", ""))
                writer.writerow(row)
        logger.info(f"✅ Exported {len(reviews)} reviews to {path}")

    async def to_google_sheets(self, leads: list[Lead], spreadsheet_id: str = None):
        """Google Sheets 输出"""
        import os
        sid = spreadsheet_id or os.getenv("SPREADSHEET_ID")
        if not sid:
            logger.warning("No SPREADSHEET_ID configured, skipping Sheets export")
            return

        try:
            import gspread
            from google.oauth2.service_account import Credentials

            creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE", "credentials.json")
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]
            creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
            gc = gspread.authorize(creds)
            sheet = gc.open_by_key(sid).sheet1

            # 写入表头
            headers = [
                "Business Name", "Category", "Address", "Phone", "Website",
                "Email", "Rating", "Reviews", "Domain", "AI Summary", "Source",
            ]
            existing = sheet.get_all_values()
            if not existing:
                sheet.append_row(headers)

            # 去重写入
            existing_names = {row[0] for row in existing[1:]} if len(existing) > 1 else set()
            new_rows = []
            for lead in leads:
                if lead.business_name not in existing_names:
                    new_rows.append([
                        lead.business_name, lead.category, lead.address, lead.phone,
                        lead.website, lead.email, str(lead.rating or ""),
                        str(lead.review_count or ""), lead.domain,
                        lead.ai_summary, lead.source,
                    ])

            if new_rows:
                sheet.append_rows(new_rows)
                logger.info(f"✅ Added {len(new_rows)} leads to Google Sheets")
            else:
                logger.info("No new leads to add to Sheets")

        except Exception as e:
            logger.error(f"Google Sheets export error: {e}")

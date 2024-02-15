"""
核心管线 — 状态机工作流

完整流程：加载线索 → 研究 → 评分 → 生成邮件 → 发送 → 更新 CRM
"""

import asyncio
import logging

from .models import LeadData
from .research import research_lead
from .scoring import score_lead
from .email_generator import generate_cold_email, generate_interview_script
from .email_sender import EmailSender
from .crm import get_crm, CRMBase

logger = logging.getLogger(__name__)


class OutreachPipeline:
    """
    AI 外联管线 — 状态机工作流

    基于图结构的状态机，
    简化为线性管线 + 条件分支（合格/不合格）。
    """

    def __init__(
        self,
        crm_source: str = "csv",
        crm_kwargs: dict = None,
        company_info: dict = None,
        auto_send: bool = False,
        min_score: float = 50.0,
    ):
        self.crm: CRMBase = get_crm(crm_source, **(crm_kwargs or {}))
        self.company_info = company_info
        self.auto_send = auto_send
        self.min_score = min_score
        self.sender = EmailSender() if auto_send else None
        self.results = {"total": 0, "qualified": 0, "emailed": 0, "sent": 0}

    async def run(self, lead_ids: list[str] = None) -> list[LeadData]:
        """执行完整外联管线"""
        logger.info("🚀 Starting Outreach AI pipeline")

        # Step 1: 加载线索
        leads = self.crm.fetch_leads(status="new")
        if lead_ids:
            leads = [l for l in leads if l.id in lead_ids]
        self.results["total"] = len(leads)
        logger.info(f"📋 Loaded {len(leads)} leads")

        # Step 2-5: 逐个处理（循环处理模式）
        processed = []
        for i, lead in enumerate(leads):
            logger.info(f"\n--- [{i+1}/{len(leads)}] Processing: {lead.name} ---")

            # Step 2: 研究
            lead.status = "researching"
            lead, reports = await research_lead(lead)
            logger.info(f"  📊 Research complete ({len(reports)} reports)")

            # Step 3: 评分（条件路由）
            lead = await score_lead(lead)
            logger.info(f"  📈 Score: {lead.score}/100 — {lead.status}")

            # 条件分支：不合格的跳过
            if lead.score < self.min_score:
                logger.info(f"  ⏭️ Skipping (score below {self.min_score})")
                self.crm.update_lead(lead)
                processed.append(lead)
                continue

            self.results["qualified"] += 1

            # Step 4: 生成邮件
            lead = await generate_cold_email(lead, self.company_info)
            if lead.personalized_email:
                self.results["emailed"] += 1
                logger.info(f"  ✉️ Email generated: {lead.email_subject}")

            # Step 4b: 生成面试脚本
            await generate_interview_script(lead)

            # Step 5: 发送（可选）
            if self.auto_send and self.sender and lead.email:
                success = self.sender.send(lead)
                if success:
                    self.results["sent"] += 1

            # Step 6: 更新 CRM
            self.crm.update_lead(lead)
            processed.append(lead)

        # 汇总
        logger.info(f"\n✅ Pipeline complete:")
        logger.info(f"   Total: {self.results['total']}")
        logger.info(f"   Qualified: {self.results['qualified']}")
        logger.info(f"   Emails generated: {self.results['emailed']}")
        logger.info(f"   Emails sent: {self.results['sent']}")

        return processed

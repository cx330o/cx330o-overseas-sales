"""
OSINT 引擎 — 多源异步聚合架构

从域名出发，聚合多个公开数据源获取邮箱、子域名等信息。
简化版实现，保留核心架构模式，支持 Hunter.io 和 crt.sh 等免费源。
"""

import asyncio
import logging
import re

from .base import BaseEngine
from ..models import Lead

logger = logging.getLogger(__name__)


class OSINTEngine(BaseEngine):
    """OSINT 情报聚合引擎 — 从域名获取邮箱和子域名"""

    async def run(self) -> list[Lead]:
        """
        对 config.query 作为域名进行 OSINT 查询。
        并行查询多个数据源（异步聚合模式）。
        """
        domain = self.config.query
        logger.info(f"[OSINT] Gathering intelligence for domain: {domain}")

        # 并行执行所有数据源查询
        tasks = [
            self._search_crtsh(domain),
            self._search_hunter(domain),
            self._search_hackertarget(domain),
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 聚合结果
        all_emails = set()
        all_subdomains = set()

        for result in results:
            if isinstance(result, Exception):
                logger.error(f"[OSINT] Source error: {result}")
                continue
            emails, subdomains = result
            all_emails.update(emails)
            all_subdomains.update(subdomains)

        # 构建统一 Lead 对象
        if all_emails or all_subdomains:
            lead = Lead(
                business_name=domain,
                domain=domain,
                emails_found=sorted(all_emails),
                subdomains=sorted(all_subdomains),
                source="osint",
            )
            self.leads.append(lead)
            logger.info(
                f"[OSINT] Found {len(all_emails)} emails, {len(all_subdomains)} subdomains"
            )

        return self.leads

    async def _search_crtsh(self, domain: str) -> tuple[set, set]:
        """crt.sh 证书透明度查询 — 免费，无需 API key"""
        emails, subdomains = set(), set()
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        try:
            data = await self._fetch_json(url)
            if isinstance(data, list):
                for entry in data:
                    name = entry.get("name_value", "")
                    for line in name.split("\n"):
                        line = line.strip().lower()
                        if line and "*" not in line and line.endswith(domain):
                            subdomains.add(line)
        except Exception as e:
            logger.debug(f"[crt.sh] Error: {e}")
        return emails, subdomains

    async def _search_hunter(self, domain: str) -> tuple[set, set]:
        """Hunter.io 邮箱查询"""
        import os
        emails, subdomains = set(), set()
        api_key = os.getenv("HUNTER_API_KEY")
        if not api_key:
            logger.debug("[Hunter] No API key, skipping")
            return emails, subdomains

        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}&limit=10"
        try:
            data = await self._fetch_json(url)
            if "data" in data and "emails" in data["data"]:
                for entry in data["data"]["emails"]:
                    emails.add(entry["value"])
                    for source in entry.get("sources", []):
                        src_domain = source.get("domain", "")
                        if domain in src_domain:
                            subdomains.add(src_domain)
        except Exception as e:
            logger.debug(f"[Hunter] Error: {e}")
        return emails, subdomains

    async def _search_hackertarget(self, domain: str) -> tuple[set, set]:
        """HackerTarget 子域名查询 — 免费"""
        emails, subdomains = set(), set()
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        try:
            text = await self._fetch(url)
            if text and "error" not in text.lower():
                for line in text.strip().split("\n"):
                    parts = line.split(",")
                    if parts:
                        subdomain = parts[0].strip().lower()
                        if subdomain.endswith(domain):
                            subdomains.add(subdomain)
        except Exception as e:
            logger.debug(f"[HackerTarget] Error: {e}")
        return emails, subdomains

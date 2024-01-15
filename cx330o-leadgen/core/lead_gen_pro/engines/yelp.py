"""
Yelp 引擎 — 异步抓取实现
增强：统一数据模型输出、错误处理、速率控制
"""

import logging
import re
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from .base import BaseEngine
from ..models import Lead

logger = logging.getLogger(__name__)


class YelpEngine(BaseEngine):
    """Yelp 商家信息抓取引擎"""

    BASE_URL = "https://www.yelp.com/search"

    async def run(self) -> list[Lead]:
        logger.info(f"[Yelp] Searching: {self.config.query} in {self.config.location}")

        offset = 0
        page_size = 10

        while len(self.leads) < self.config.max_results:
            url = (
                f"{self.BASE_URL}?find_desc={quote_plus(self.config.query)}"
                f"&find_loc={quote_plus(self.config.location)}"
                f"&start={offset}"
            )
            html = await self._fetch(url)
            if not html:
                break

            new_leads = self._parse_search_results(html)
            if not new_leads:
                break

            self.leads.extend(new_leads)
            offset += page_size
            logger.info(f"[Yelp] Collected {len(self.leads)} leads so far")

        self.leads = self.leads[:self.config.max_results]
        return self.leads

    def _parse_search_results(self, html: str) -> list[Lead]:
        """解析 Yelp 搜索结果页"""
        soup = BeautifulSoup(html, "lxml")
        leads = []

        # Yelp 搜索结果容器
        containers = soup.select('[data-testid="serp-ia-card"]') or soup.select("li .container__09f24__FeTO6")
        if not containers:
            # 备用选择器
            containers = soup.select("div.businessName__09f24__EYSZE")

        for container in containers:
            try:
                lead = Lead(source="yelp")

                # 商家名称
                name_el = container.select_one("a[href*='/biz/'] h3, a[href*='/biz/'] span")
                if name_el:
                    lead.business_name = name_el.get_text(strip=True)

                # 链接
                link_el = container.select_one("a[href*='/biz/']")
                if link_el:
                    href = link_el.get("href", "")
                    lead.source_url = f"https://www.yelp.com{href}" if href.startswith("/") else href

                # 评分
                rating_el = container.select_one('[aria-label*="star rating"]')
                if rating_el:
                    label = rating_el.get("aria-label", "")
                    match = re.search(r"([\d.]+)", label)
                    if match:
                        lead.rating = float(match.group(1))

                # 评论数
                review_el = container.select_one('span[class*="reviewCount"]')
                if review_el:
                    match = re.search(r"(\d+)", review_el.get_text())
                    if match:
                        lead.review_count = int(match.group(1))

                # 分类
                cat_els = container.select('a[href*="/search?cflt="]')
                if cat_els:
                    lead.category = ", ".join(el.get_text(strip=True) for el in cat_els)

                # 地址和电话（通常在详情页，这里取摘要）
                addr_el = container.select_one("address, span[class*='secondaryAttributes']")
                if addr_el:
                    lead.address = addr_el.get_text(strip=True)

                if lead.business_name:
                    leads.append(lead)
            except Exception as e:
                logger.debug(f"Error parsing Yelp result: {e}")

        return leads

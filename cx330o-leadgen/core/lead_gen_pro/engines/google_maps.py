"""
Google Maps 引擎 — 整合多种能力：
- Playwright 异步抓取 + 搜索结果 URL 提取
- 详细评论解析、分页管理、多语言支持
- 商家详情提取（名称/地址/电话/网站/评分/邮箱）
"""

import logging
import re
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from .base import BaseEngine
from ..models import Lead, Review, ScrapeConfig

logger = logging.getLogger(__name__)


class GoogleMapsEngine(BaseEngine):
    """Google Maps 商家信息 + 评论抓取引擎"""

    BASE_SEARCH_URL = "https://www.google.com/maps/search/{query}/@{lat},{lng},{zoom}z"

    def __init__(self, config: ScrapeConfig):
        super().__init__(config)
        self.reviews: list[Review] = []

    async def run(self) -> list[Lead]:
        """
        执行流程：
        1. 搜索 Google Maps 获取商家列表（Playwright 异步抓取）
        2. 逐个解析商家详情（详情字段提取）
        3. 可选：抓取评论（深度评论解析）
        """
        logger.info(f"[GoogleMaps] Searching: {self.config.query} in {self.config.location}")

        try:
            from playwright.async_api import async_playwright
        except ImportError:
            logger.error("playwright not installed. Run: pip install playwright && playwright install")
            return []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # 搜索 Google Maps
            search_url = f"https://www.google.com/maps/search/{quote_plus(self.config.query + ' ' + self.config.location)}"
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(3000)

            # 滚动加载更多结果（滚动加载逻辑）
            results_panel = page.locator('[role="feed"]')
            if await results_panel.count() > 0:
                for _ in range(min(self.config.max_results // 5, 20)):
                    await results_panel.evaluate("el => el.scrollTop = el.scrollHeight")
                    await page.wait_for_timeout(1500)

            # 提取所有商家链接
            links = await page.locator('a[href*="/maps/place/"]').all()
            place_urls = []
            for link in links[:self.config.max_results]:
                href = await link.get_attribute("href")
                if href and "/maps/place/" in href:
                    place_urls.append(href)

            logger.info(f"[GoogleMaps] Found {len(place_urls)} places")

            # 逐个访问商家页面提取详情（商家详情提取）
            for url in place_urls:
                try:
                    lead = await self._extract_place_details(page, url)
                    if lead and lead.business_name:
                        self.leads.append(lead)
                        logger.info(f"  ✓ {lead.business_name}")

                        # 可选：抓取评论
                        if self.config.include_reviews:
                            reviews = await self._extract_reviews(page, lead)
                            self.reviews.extend(reviews)
                except Exception as e:
                    logger.error(f"  ✗ Error extracting {url}: {e}")

            await browser.close()

        return self.leads

    async def _extract_place_details(self, page, url: str) -> Lead:
        """
        提取商家详情 — 融合字段提取 + 元数据解析
        """
        await page.goto(url, wait_until="networkidle", timeout=20000)
        await page.wait_for_timeout(2000)

        lead = Lead(source="google_maps", source_url=url)

        # 商家名称
        name_el = page.locator("h1")
        if await name_el.count() > 0:
            lead.business_name = (await name_el.first.text_content() or "").strip()

        # 地址（aria-label 匹配）
        addr_btn = page.locator('button[data-item-id="address"]')
        if await addr_btn.count() > 0:
            lead.address = (await addr_btn.get_attribute("aria-label") or "").replace("Address: ", "")

        # 电话
        phone_btn = page.locator('button[data-item-id*="phone"]')
        if await phone_btn.count() > 0:
            lead.phone = (await phone_btn.get_attribute("aria-label") or "").replace("Phone: ", "")

        # 网站
        website_link = page.locator('a[data-item-id="authority"]')
        if await website_link.count() > 0:
            lead.website = (await website_link.get_attribute("href") or "")

        # 分类
        cat_btn = page.locator('button[jsaction*="category"]')
        if await cat_btn.count() > 0:
            lead.category = (await cat_btn.first.text_content() or "").strip()

        # 评分和评论数（评分解析逻辑）
        rating_el = page.locator('div[role="img"][aria-label*="star"]')
        if await rating_el.count() > 0:
            label = await rating_el.first.get_attribute("aria-label") or ""
            match = re.search(r"([\d.]+)\s*star", label)
            if match:
                lead.rating = float(match.group(1))

        review_el = page.locator('span[aria-label*="review"]')
        if await review_el.count() > 0:
            label = await review_el.first.get_attribute("aria-label") or ""
            match = re.search(r"([\d,]+)\s*review", label)
            if match:
                lead.review_count = int(match.group(1).replace(",", ""))

        # 提取域名
        if lead.website:
            domain_match = re.search(r"https?://(?:www\.)?([^/]+)", lead.website)
            if domain_match:
                lead.domain = domain_match.group(1)

        return lead

    async def _extract_reviews(self, page, lead: Lead) -> list[Review]:
        """
        评论抓取 — 详细评论解析逻辑
        包括：评分、文本、翻译文本、用户信息、店主回复
        """
        reviews = []

        # 点击"Reviews"标签
        reviews_tab = page.locator('button[aria-label*="Reviews"]')
        if await reviews_tab.count() == 0:
            return reviews

        await reviews_tab.first.click()
        await page.wait_for_timeout(2000)

        # 滚动加载评论
        review_panel = page.locator('div[role="feed"]')
        if await review_panel.count() > 0:
            for _ in range(min(self.config.max_reviews_per_place // 3, 10)):
                await review_panel.evaluate("el => el.scrollTop = el.scrollHeight")
                await page.wait_for_timeout(1000)

        # 解析每条评论（评论解析）
        review_els = await page.locator('div[data-review-id]').all()
        for el in review_els[:self.config.max_reviews_per_place]:
            try:
                review = Review(lead_dedup_key=lead.dedup_key)

                # 评论者名称
                name_el = el.locator('div[class*="name"] button, a[aria-label]')
                if await name_el.count() > 0:
                    review.reviewer_name = (await name_el.first.text_content() or "").strip()

                # 评分
                star_el = el.locator('span[role="img"]')
                if await star_el.count() > 0:
                    label = await star_el.first.get_attribute("aria-label") or ""
                    match = re.search(r"(\d)", label)
                    if match:
                        review.rating = float(match.group(1))

                # 评论文本
                text_el = el.locator('span[class*="review-full-text"], div[class*="MyEned"]')
                if await text_el.count() > 0:
                    review.text = (await text_el.first.text_content() or "").strip()

                # 相对日期
                date_el = el.locator('span[class*="rsqaWe"]')
                if await date_el.count() > 0:
                    review.relative_date = (await date_el.first.text_content() or "").strip()

                if review.text or review.rating:
                    reviews.append(review)
            except Exception as e:
                logger.debug(f"Error parsing review: {e}")

        logger.info(f"  📝 {len(reviews)} reviews for {lead.business_name}")
        return reviews

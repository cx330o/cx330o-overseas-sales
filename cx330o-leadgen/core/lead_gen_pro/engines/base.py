"""
基础引擎抽象类 — 插件架构 + 引擎抽象

所有数据源引擎都继承此类，实现统一的 async run() 接口。
"""

import asyncio
import logging
import random
from abc import ABC, abstractmethod
from typing import Optional

import aiohttp

from ..models import Lead, ScrapeConfig

logger = logging.getLogger(__name__)

# User-Agent 随机化
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
]


class BaseEngine(ABC):
    """所有线索获取引擎的基类"""

    def __init__(self, config: ScrapeConfig):
        self.config = config
        self.leads: list[Lead] = []
        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def _get_headers(self) -> dict:
        ua = self.config.user_agent or random.choice(USER_AGENTS)
        return {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=10, ssl=False)
            self._session = aiohttp.ClientSession(
                connector=connector,
                headers=self._get_headers(),
            )
        return self._session

    async def _fetch(self, url: str, **kwargs) -> str:
        """带重试和速率控制的 HTTP 请求"""
        session = await self._get_session()
        for attempt in range(self.config.max_retries):
            try:
                await asyncio.sleep(self.config.request_delay)
                proxy = self.config.proxy
                async with session.get(url, proxy=proxy, **kwargs) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    elif resp.status == 429:
                        wait = (attempt + 1) * 5
                        logger.warning(f"[{self.name}] Rate limited, waiting {wait}s...")
                        await asyncio.sleep(wait)
                    else:
                        logger.warning(f"[{self.name}] HTTP {resp.status} for {url}")
            except Exception as e:
                logger.error(f"[{self.name}] Request error (attempt {attempt+1}): {e}")
                await asyncio.sleep(2)
        return ""

    async def _fetch_json(self, url: str, **kwargs) -> dict:
        session = await self._get_session()
        for attempt in range(self.config.max_retries):
            try:
                await asyncio.sleep(self.config.request_delay)
                async with session.get(url, proxy=self.config.proxy, **kwargs) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    elif resp.status == 429:
                        await asyncio.sleep((attempt + 1) * 5)
            except Exception as e:
                logger.error(f"[{self.name}] JSON fetch error: {e}")
                await asyncio.sleep(2)
        return {}

    @abstractmethod
    async def run(self) -> list[Lead]:
        """执行抓取，返回线索列表。子类必须实现。"""
        ...

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

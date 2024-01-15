"""统一数据模型 — 所有引擎的输出都归一化到这些模型"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Lead(BaseModel):
    """核心线索模型，统一所有数据源的输出格式"""
    # 基本信息
    business_name: str = ""
    category: str = ""
    address: str = ""
    phone: str = ""
    website: str = ""
    email: str = ""

    # 评分与评论（深度解析）
    rating: Optional[float] = None
    review_count: Optional[int] = None
    
    # 社交与在线信息（OSINT 情报聚合）
    domain: str = ""
    subdomains: list[str] = Field(default_factory=list)
    emails_found: list[str] = Field(default_factory=list)
    
    # AI 丰富数据（ChatGPT 管线）
    ai_summary: str = ""
    ai_personalized_message: str = ""
    
    # 元数据
    source: str = ""  # google_maps / yelp / osint / enriched
    source_url: str = ""
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 去重标识
    @property
    def dedup_key(self) -> str:
        """用于去重的唯一标识"""
        return f"{self.business_name}|{self.address}|{self.phone}".lower().strip()


class Review(BaseModel):
    """评论模型，详细评论解析"""
    lead_dedup_key: str = ""
    reviewer_name: str = ""
    rating: float = 0
    text: str = ""
    translated_text: str = ""
    relative_date: str = ""
    reviewer_reviews_count: int = 0
    reviewer_photos_count: int = 0
    owner_response: str = ""
    scraped_at: datetime = Field(default_factory=datetime.utcnow)


class ScrapeConfig(BaseModel):
    """抓取配置"""
    query: str
    location: str = ""
    max_results: int = 50
    include_reviews: bool = False
    max_reviews_per_place: int = 10
    ai_enrich: bool = False
    sources: list[str] = Field(default_factory=lambda: ["google_maps"])
    # 反爬配置
    request_delay: float = 0.5
    max_retries: int = 3
    proxy: Optional[str] = None
    user_agent: Optional[str] = None

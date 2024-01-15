"""CLI 入口 — python -m lead_gen_pro"""

import argparse
import asyncio
import logging
import sys

from dotenv import load_dotenv

from .models import ScrapeConfig
from .pipeline import LeadGenPipeline

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="LeadGen Pro — 统一线索获取引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Google Maps 搜索
  python -m lead_gen_pro --source google_maps --query "restaurants" --location "New York"

  # 多源搜索 + AI 丰富
  python -m lead_gen_pro --source google_maps yelp --query "dentist" --location "London" --ai-enrich

  # OSINT 域名情报
  python -m lead_gen_pro --source osint --query "example.com"

  # 包含评论
  python -m lead_gen_pro --source google_maps --query "hotels" --location "Paris" --reviews --max-reviews 20
        """,
    )
    parser.add_argument("--query", "-q", required=True, help="搜索关键词或域名")
    parser.add_argument("--location", "-l", default="", help="地理位置")
    parser.add_argument("--source", "-s", nargs="+", default=["google_maps"],
                        choices=["google_maps", "yelp", "osint"],
                        help="数据源（可多选）")
    parser.add_argument("--max-results", "-n", type=int, default=50, help="最大结果数")
    parser.add_argument("--reviews", action="store_true", help="是否抓取评论")
    parser.add_argument("--max-reviews", type=int, default=10, help="每个商家最大评论数")
    parser.add_argument("--ai-enrich", action="store_true", help="启用 AI 数据丰富")
    parser.add_argument("--output", "-o", default="./output", help="输出目录")
    parser.add_argument("--delay", type=float, default=0.5, help="请求间隔（秒）")
    parser.add_argument("--proxy", default=None, help="代理地址")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细日志")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    config = ScrapeConfig(
        query=args.query,
        location=args.location,
        max_results=args.max_results,
        include_reviews=args.reviews,
        max_reviews_per_place=args.max_reviews,
        ai_enrich=args.ai_enrich,
        sources=args.source,
        request_delay=args.delay,
        proxy=args.proxy,
    )

    pipeline = LeadGenPipeline(config, output_dir=args.output)

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(pipeline.run())


if __name__ == "__main__":
    main()

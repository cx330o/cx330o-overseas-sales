"""
LeadGen Pro 快速演示 — 不需要任何 API key

演示 OSINT 引擎（crt.sh + HackerTarget 都是免费的）
+ Yelp 引擎的数据解析
+ 统一输出到 CSV/JSON
"""

import asyncio
import logging
import sys

sys.path.insert(0, ".")

from lead_gen_pro.models import ScrapeConfig, Lead
from lead_gen_pro.engines.osint import OSINTEngine
from lead_gen_pro.output import OutputManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


async def demo_osint():
    """演示 OSINT 引擎 — 从域名获取子域名和邮箱"""
    print("\n" + "=" * 60)
    print("  LeadGen Pro — OSINT 引擎演示")
    print("  从公开数据源获取域名情报（无需 API key）")
    print("=" * 60 + "\n")

    # 用几个知名域名做演示
    domains = ["github.com", "shopify.com", "stripe.com"]

    all_leads = []
    for domain in domains:
        config = ScrapeConfig(
            query=domain,
            sources=["osint"],
            request_delay=1.0,
            max_retries=2,
        )
        engine = OSINTEngine(config)
        async with engine:
            leads = await engine.run()
            all_leads.extend(leads)

        if leads:
            lead = leads[0]
            print(f"\n📌 {domain}:")
            print(f"   子域名数量: {len(lead.subdomains)}")
            if lead.subdomains[:5]:
                for sd in lead.subdomains[:5]:
                    print(f"     - {sd}")
                if len(lead.subdomains) > 5:
                    print(f"     ... 还有 {len(lead.subdomains) - 5} 个")
            if lead.emails_found:
                print(f"   邮箱: {', '.join(lead.emails_found[:5])}")
        else:
            print(f"\n📌 {domain}: 未获取到数据")

    # 输出到文件
    output = OutputManager("./demo_output")
    output.to_csv(all_leads, "osint_leads.csv")
    output.to_json(all_leads, "osint_leads.json")

    print(f"\n✅ 结果已保存到 demo_output/ 目录")
    return all_leads


async def demo_mock_pipeline():
    """演示完整管线（用模拟数据）"""
    print("\n" + "=" * 60)
    print("  LeadGen Pro — 完整管线演示（模拟数据）")
    print("=" * 60 + "\n")

    # 模拟从 Google Maps 获取的数据
    mock_leads = [
        Lead(
            business_name="Tokyo Sushi Bar",
            category="Japanese Restaurant",
            address="123 Main St, New York, NY 10001",
            phone="+1-212-555-0101",
            website="https://tokyosushi.example.com",
            rating=4.5,
            review_count=328,
            source="google_maps",
            domain="tokyosushi.example.com",
        ),
        Lead(
            business_name="Berlin Coffee House",
            category="Coffee Shop",
            address="456 Oak Ave, San Francisco, CA 94102",
            phone="+1-415-555-0202",
            website="https://berlincoffee.example.com",
            rating=4.8,
            review_count=512,
            source="google_maps",
            domain="berlincoffee.example.com",
        ),
        Lead(
            business_name="Paris Dental Clinic",
            category="Dentist",
            address="789 Elm St, London, UK",
            phone="+44-20-7946-0303",
            website="https://parisdental.example.com",
            email="info@parisdental.example.com",
            rating=4.2,
            review_count=156,
            source="google_maps",
            domain="parisdental.example.com",
        ),
        # 故意重复一条，测试去重
        Lead(
            business_name="Tokyo Sushi Bar",
            category="Japanese Restaurant",
            address="123 Main St, New York, NY 10001",
            phone="+1-212-555-0101",
            source="yelp",
        ),
    ]

    print(f"📥 模拟获取了 {len(mock_leads)} 条线索（含 1 条重复）")

    # 去重
    seen = set()
    unique = []
    for lead in mock_leads:
        if lead.dedup_key not in seen:
            seen.add(lead.dedup_key)
            unique.append(lead)
    print(f"🔄 去重后: {len(unique)} 条")

    # 输出
    output = OutputManager("./demo_output")
    output.to_csv(unique, "mock_leads.csv")
    output.to_json(unique, "mock_leads.json")

    print(f"\n📊 线索详情:")
    for lead in unique:
        print(f"   {lead.business_name} | {lead.category} | ⭐{lead.rating} ({lead.review_count} reviews)")
        print(f"     📍 {lead.address}")
        print(f"     🌐 {lead.website}")
        if lead.email:
            print(f"     📧 {lead.email}")
        print()

    print(f"✅ 结果已保存到 demo_output/ 目录")


async def main():
    # Part 1: 模拟数据演示
    await demo_mock_pipeline()

    # Part 2: 真实 OSINT 演示
    await demo_osint()

    print("\n" + "=" * 60)
    print("  🎉 演示完成！查看 demo_output/ 目录中的文件")
    print("=" * 60)


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

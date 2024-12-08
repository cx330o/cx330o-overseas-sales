# cx330o Payments — 统一支付网关

Hyperswitch 集成，Rust 编写的高性能支付路由。

## 功能

- 50+ 支付商统一接入（Stripe / PayPal / Adyen / Klarna）
- 智能路由（基于成功率、费率、地区）
- 多币种支持（135+ 货币）
- 订阅计费 + 用量计费
- 退款管理 + 争议处理
- 3DS 认证 + PCI DSS 合规
- 可视化控制台

## 启动

```bash
docker compose --profile payments up -d
# 控制台: http://localhost:85
# API:    http://localhost:8180
```

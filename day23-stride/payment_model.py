#!/usr/bin/env python3
"""
Day 23 STRIDE 演練 —— 電商付款流程威脅模型
使用 OWASP pytm（threat-modeling-as-code）建模，跑出真實產生的威脅清單與 DFD。

用法：
  python3 payment_model.py --dfd | dot -Tpng -o dfd.png      # 產生資料流圖
  python3 payment_model.py                                    # 印出威脅清單（不安全版）
"""

from pytm import TM, Boundary, Actor, Server, Datastore, Dataflow, Data, Classification

tm = TM("電商付款流程 STRIDE 威脅模型")
tm.description = "Day 23 動手做：對一個最小化的線上支付流程跑一次自動化威脅建模"

internet = Boundary("Internet")
internal = Boundary("Internal Network")

user = Actor("手機 App 使用者")
user.inBoundary = internet

payment_api = Server("Payment API")
payment_api.inBoundary = internal
payment_api.OS = "Linux"
# ⚠️ 刻意先不設任何 controls，模擬「還沒做威脅建模」的原始架構

orders_db = Datastore("Orders DB")
orders_db.inBoundary = internal
orders_db.isSQL = True

card_data = Data(
    name="付款資料",
    description="信用卡卡號、金額、收件地址",
    classification=Classification.RESTRICTED,
)

req = Dataflow(user, payment_api, "送出付款請求")
req.protocol = "HTTPS"
req.data = card_data

query = Dataflow(payment_api, orders_db, "查詢／寫入訂單")
query.protocol = "SQL"
query.data = card_data

if __name__ == "__main__":
    tm.process()

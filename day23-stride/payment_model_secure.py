#!/usr/bin/env python3
"""Day 23 STRIDE 演練 —— 套用防守設計後的版本，對照 payment_model.py 的落差。"""

from pytm import TM, Boundary, Actor, Server, Datastore, Dataflow, Data, Classification
from pytm.enums import TLSVersion

tm = TM("電商付款流程 STRIDE 威脅模型（已加固版）")
tm.description = "Day 23 動手做：套用信任邊界檢核／最小攻擊面／故障安全對應的控制後重新掃描"

internet = Boundary("Internet")
internal = Boundary("Internal Network")

user = Actor("手機 App 使用者")
user.inBoundary = internet

payment_api = Server("Payment API")
payment_api.inBoundary = internal
payment_api.OS = "Linux"
payment_api.controls.hasAccessControl = True
payment_api.controls.authorizesSource = True
payment_api.controls.authenticatesSource = True
payment_api.controls.implementsAuthenticationScheme = True
payment_api.controls.implementsPOLP = True
payment_api.controls.sanitizesInput = True
payment_api.controls.validatesInput = True
payment_api.controls.handlesResourceConsumption = True
payment_api.controls.definesConnectionTimeout = True
payment_api.controls.isResilient = True

orders_db = Datastore("Orders DB")
orders_db.inBoundary = internal
orders_db.isSQL = True
orders_db.controls.hasAccessControl = True
orders_db.controls.authorizesSource = True
orders_db.controls.implementsPOLP = True
orders_db.controls.validatesInput = True
orders_db.controls.isEncryptedAtRest = True

card_data = Data(
    name="付款資料",
    description="信用卡卡號、金額、收件地址",
    classification=Classification.RESTRICTED,
)

req = Dataflow(user, payment_api, "送出付款請求")
req.protocol = "HTTPS"
req.data = card_data
req.tlsVersion = TLSVersion.TLSv13
req.controls.isEncrypted = True
req.controls.authenticatesDestination = True
req.controls.implementsAuthenticationScheme = True
req.controls.authorizesSource = True

query = Dataflow(payment_api, orders_db, "查詢／寫入訂單")
query.protocol = "SQL"
query.data = card_data
query.controls.isEncrypted = True
query.controls.authenticatesDestination = True
query.controls.implementsAuthenticationScheme = True
query.controls.authorizesSource = True

if __name__ == "__main__":
    tm.process()

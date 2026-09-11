# Day 23 動手做：pytm 威脅建模範例

對應文章：Day-23.md

## 環境需求

* Python 3.9 以上
* Graphviz（提供 `dot` 指令，用來把威脅模型畫成 DFD）

## 安裝

```bash
pip install pytm
# Ubuntu / Debian：
sudo apt-get install graphviz
# macOS：
brew install graphviz
```

## 檔案

* `payment_model.py`　——　原始（未加固）版本，跑出 62 筆威脅
* `payment_model_secure.py`　——　套用七項基本控制後的版本，跑出 35 筆威脅

## 指令

```bash
# 產生資料流圖（DFD）
python3 payment_model.py --dfd | dot -Tpng -Gdpi=192 -o dfd.png

# 列出威脅比對庫裡全部規則名稱
python3 payment_model.py --list

# 印出威脅清單摘要（依 STRIDE 六類各挑一筆的做法見文章內文）
python3 - <<'EOF'
from payment_model import tm
tm.resolve()
print("total findings:", len(tm.findings))
for f in tm.findings:
    print(f.threat_id, f.target, f.description, f.severity)
EOF
```

把 `payment_model` 換成 `payment_model_secure` 就能看到加固後的比對結果（62 → 35 筆）。

> ⚠️ **兩個模型請分開用獨立的 Python 行程執行，不要在同一支腳本裡先後 `import` 兩者。** pytm 用 class 層級的全域清單追蹤所有已建立的元件，同一行程內先後匯入兩份模型會讓元件被算在一起，`len(tm.findings)` 就不會是乾淨的 62 或 35。

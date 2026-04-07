import re

with open('domain_generator_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_tlds = """    "商业/购物 (Business)": [
        "co", "store", "club", "vip", "biz", "trade", "pro", "shop"
    ],
    "国家/地区 (ccTLD)": ["""

new_tlds = """    "商业/购物 (Business)": [
        "co", "store", "club", "vip", "biz", "trade", "pro", "shop"
    ],
    "Web3/Crypto": [
        "eth", "crypto", "io", "xyz", "network", "coin", "wallet", "exchange", "nft", "dao"
    ],
    "教育/学术 (Education)": [
        "edu", "academy", "institute", "school", "college", "university", "degree", "study"
    ],
    "医疗/健康 (Health)": [
        "health", "care", "clinic", "hospital", "medical", "fitness", "diet", "yoga"
    ],
    "金融/投资 (Finance)": [
        "finance", "fund", "capital", "cash", "invest", "money", "credit", "loans"
    ],
    "国家/地区 (ccTLD)": ["""

content = content.replace(old_tlds, new_tlds)

with open('domain_generator_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("TLDs updated.")

import itertools
import os
import string

# 真实的 2 字符顶级域名 (ccTLD) 列表（部分常用列表，可根据需要扩充）
REAL_2_CHAR_TLDS = [
    "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar", "as", "at", "au", "aw", "ax", "az",
    "ba", "bb", "bd", "be", "bf", "bg", "bh", "bi", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", "bz",
    "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", "co", "cr", "cu", "cv", "cw", "cx", "cy", "cz",
    "de", "dj", "dk", "dm", "do", "dz", "ec", "ee", "eg", "er", "es", "et", "eu",
    "fi", "fj", "fk", "fm", "fo", "fr",
    "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi", "gl", "gm", "gn", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy",
    "hk", "hm", "hn", "hr", "ht", "hu",
    "id", "ie", "il", "im", "in", "io", "iq", "ir", "is", "it",
    "je", "jm", "jo", "jp",
    "ke", "kg", "kh", "ki", "km", "kn", "kp", "kr", "kw", "ky", "kz",
    "la", "lb", "lc", "li", "lk", "lr", "ls", "lt", "lu", "lv", "ly",
    "ma", "mc", "md", "me", "mg", "mh", "mk", "ml", "mm", "mn", "mo", "mp", "mq", "mr", "ms", "mt", "mu", "mv", "mw", "mx", "my", "mz",
    "na", "nc", "ne", "nf", "ng", "ni", "nl", "no", "np", "nr", "nu", "nz",
    "om",
    "pa", "pe", "pf", "pg", "ph", "pk", "pl", "pm", "pn", "pr", "ps", "pt", "pw", "py",
    "qa",
    "re", "ro", "rs", "ru", "rw",
    "sa", "sb", "sc", "sd", "se", "sg", "sh", "si", "sj", "sk", "sl", "sm", "sn", "so", "sr", "ss", "st", "su", "sv", "sx", "sy", "sz",
    "tc", "td", "tf", "tg", "th", "tj", "tk", "tl", "tm", "tn", "to", "tr", "tt", "tv", "tw", "tz",
    "ua", "ug", "uk", "us", "uy", "uz",
    "va", "vc", "ve", "vg", "vi", "vn", "vu",
    "wf", "ws",
    "ye", "yt",
    "za", "zm", "zw"
]

def generate_prefixes(min_len, max_len, charset, exclude_chars=""):
    """生成域名前缀组合"""
    valid_chars = [c for c in charset if c not in exclude_chars]
    prefixes = []
    for length in range(min_len, max_len + 1):
        for combo in itertools.product(valid_chars, repeat=length):
            prefixes.append("".join(combo))
    return prefixes

def generate_domains(prefixes, tlds):
    """组合前缀和后缀生成域名"""
    for tld in tlds:
        for prefix in prefixes:
            yield f"{prefix}.{tld}"

def save_domains_in_batches(domain_generator, batch_size=5000, output_dir="output"):
    """分批保存域名到TXT文件"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    batch = []
    file_index = 1
    
    for domain in domain_generator:
        batch.append(domain)
        if len(batch) >= batch_size:
            _write_batch(batch, file_index, output_dir)
            batch = []
            file_index += 1
            
    # 写入剩余的
    if batch:
        _write_batch(batch, file_index, output_dir)
        
def _write_batch(batch, file_index, output_dir):
    filename = os.path.join(output_dir, f"domains_part_{file_index}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(",".join(batch))
    print(f"已生成: {filename} (共 {len(batch)} 个域名)")

if __name__ == "__main__":
    # === 配置区域 ===
    
    # 1. 前缀长度设置
    PREFIX_MIN_LEN = 1
    PREFIX_MAX_LEN = 2
    
    # 2. 字符集设置 (默认小写字母 + 数字)
    CHARSET = string.ascii_lowercase + string.digits
    
    # 3. 排除字符 (例如排除容易混淆的 0, o, 1, l)
    EXCLUDE_CHARS = ""
    
    # 4. 目标后缀列表 (可以限制为特定的几个，或者使用全部2字符TLD)
    # TARGET_TLDS = ["cc", "so", "io", "co"] 
    TARGET_TLDS = REAL_2_CHAR_TLDS
    
    # 5. 每批输出数量
    BATCH_SIZE = 5000
    
    # === 执行区域 ===
    print("开始生成域名前缀...")
    prefixes = generate_prefixes(PREFIX_MIN_LEN, PREFIX_MAX_LEN, CHARSET, EXCLUDE_CHARS)
    print(f"共生成 {len(prefixes)} 种前缀组合。")
    
    print("开始组合域名并写入文件...")
    domain_gen = generate_domains(prefixes, TARGET_TLDS)
    save_domains_in_batches(domain_gen, batch_size=BATCH_SIZE)
    
    print("域名生成完毕！")

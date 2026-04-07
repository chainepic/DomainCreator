import sys
import os
import itertools
import string
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QSpinBox, QCheckBox, QLineEdit,
                             QPushButton, QListWidget, QFileDialog, QMessageBox,
                             QAbstractItemView, QGroupBox, QGridLayout, QRadioButton,
                             QButtonGroup, QTabWidget, QStackedWidget)
from PyQt6.QtCore import QThread, pyqtSignal, Qt

# Categorized TLDs

TRANSLATIONS = {
    "zh": {
        "title": "Domain Generator V2 (域名生成器)",
        "status_ready": "准备就绪",
        "btn_generate": "开始生成",
        "tab_mode": "1. 生成模式",
        "tab_tld": "2. 后缀选择",
        "tab_output": "3. 输出与执行",
        "group_mode": "选择生成模式",
        "radio_brute": "字符穷举",
        "radio_words": "英文单词",
        "radio_pattern": "Pattern 模式",
        "radio_hacks": "创意拼词 (Hacks)",
        "brute_min": "最小长度:",
        "brute_max": "最大长度:",
        "brute_charset": "包含字符:",
        "brute_exclude": "排除字符:",
        "cb_lower": "小写字母 (a-z)",
        "cb_num": "数字 (0-9)",
        "exclude_ph": "如: 0o1l",
        "words_len": "内置词库长度:",
        "words_to": "到",
        "words_custom": "自定义单词\n(无视长度限制):",
        "words_custom_ph": "用逗号分隔，如: watch,spell,super",
        "pattern_label": "输入模式公式 (如 CVC, LVN):",
        "pattern_ph": "C=辅音, V=元音, L=任意字母, N=任意数字",
        "pattern_ex": "示例:\nCVC -> bat, cat (辅音+元音+辅音)\nLVN -> a1, z9 (字母+元音+数字)",
        "hacks_label": "创意拼词模式 (Domain Hacks):",
        "hacks_desc": "程序会自动将单词与后缀进行匹配。如 internet + net -> inter.net",
        "hacks_ph": "输入自定义单词 (逗号分隔)，留空则使用内置词库",
        "tld_len_label": "<b>按长度批量选择:</b>",
        "btn_len2": "+ 选中 2位后缀",
        "btn_len3": "+ 选中 3位后缀",
        "btn_len4": "+ 选中 4位及以上",
        "tld_cat_label": "<b>按类型批量选择:</b>",
        "btn_clear_all": "清空所有选择",
        "group_output": "输出设置",
        "batch_label": "每批输出数量:",
        "out_dir_label": "输出目录:",
        "btn_browse": "浏览...",
        "btn_lang": "English",
        "copyright": "Copyright © Chainepic Ltd. | X: @chainepic",
        "msg_gen_combo": "正在生成组合...",
        "msg_gen_prefix": "共生成 {} 种前缀，开始组合域名...",
        "msg_gen_count": "已生成 {} 个域名...",
        "msg_done": "完成！共生成 {} 个域名。",
        "msg_err": "发生错误: {}",
        "err_no_words": "没有找到符合条件的单词，请调整长度或输入自定义单词！",
        "err_pattern_empty": "Pattern 模式生成的组合为空，请检查输入！",
        "err_charset": "请至少选择一种字符集！",
        "err_len": "最小长度不能大于最大长度！",
        "err_pattern": "请输入 Pattern 公式！",
        "err_tld": "请至少选择一个目标后缀！",
        "status_generating": "正在生成，请稍候...",
        "box_success": "成功",
        "box_success_msg": "域名生成完毕！\n共生成 {} 个域名。\n保存在: {}",
        "box_err": "错误",
        "box_err_msg": "生成过程中发生错误:\n{}"
    },
    "en": {
        "title": "Domain Generator V2",
        "status_ready": "Ready",
        "btn_generate": "Start Generating",
        "tab_mode": "1. Generation Mode",
        "tab_tld": "2. TLD Selection",
        "tab_output": "3. Output & Execute",
        "group_mode": "Select Generation Mode",
        "radio_brute": "Brute Force",
        "radio_words": "English Words",
        "radio_pattern": "Pattern Mode",
        "radio_hacks": "Domain Hacks",
        "brute_min": "Min Length:",
        "brute_max": "Max Length:",
        "brute_charset": "Include Chars:",
        "brute_exclude": "Exclude Chars:",
        "cb_lower": "Lowercase (a-z)",
        "cb_num": "Numbers (0-9)",
        "exclude_ph": "e.g.: 0o1l",
        "words_len": "Built-in Word Length:",
        "words_to": "to",
        "words_custom": "Custom Words\n(Ignores length):",
        "words_custom_ph": "Comma separated, e.g.: watch,spell,super",
        "pattern_label": "Enter Pattern Formula (e.g. CVC, LVN):",
        "pattern_ph": "C=Consonant, V=Vowel, L=Any Letter, N=Any Number",
        "pattern_ex": "Example:\nCVC -> bat, cat (Consonant+Vowel+Consonant)\nLVN -> a1, z9 (Letter+Vowel+Number)",
        "hacks_label": "Domain Hacks Mode:",
        "hacks_desc": "Automatically matches words with TLDs. e.g. internet + net -> inter.net",
        "hacks_ph": "Enter custom words (comma separated), leave empty for built-in words",
        "tld_len_label": "<b>Select by Length:</b>",
        "btn_len2": "+ Select 2-char TLDs",
        "btn_len3": "+ Select 3-char TLDs",
        "btn_len4": "+ Select 4+ char TLDs",
        "tld_cat_label": "<b>Select by Category:</b>",
        "btn_clear_all": "Clear All Selections",
        "group_output": "Output Settings",
        "batch_label": "Output per Batch:",
        "out_dir_label": "Output Directory:",
        "btn_browse": "Browse...",
        "btn_lang": "中文",
        "copyright": "Copyright © Chainepic Ltd. | X: @chainepic",
        "msg_gen_combo": "Generating combinations...",
        "msg_gen_prefix": "Generated {} prefixes, starting to combine domains...",
        "msg_gen_count": "Generated {} domains...",
        "msg_done": "Done! Generated {} domains.",
        "msg_err": "Error occurred: {}",
        "err_no_words": "No matching words found, please adjust length or enter custom words!",
        "err_pattern_empty": "Pattern mode generated empty combinations, please check input!",
        "err_charset": "Please select at least one character set!",
        "err_len": "Minimum length cannot be greater than maximum length!",
        "err_pattern": "Please enter a Pattern formula!",
        "err_tld": "Please select at least one target TLD!",
        "status_generating": "Generating, please wait...",
        "box_success": "Success",
        "box_success_msg": "Domain generation complete!\nGenerated {} domains.\nSaved in: {}",
        "box_err": "Error",
        "box_err_msg": "An error occurred during generation:\n{}"
    }
}

CATEGORIZED_TLDS = {
    "通用/基础 (Generic)": [
        "com", "net", "org", "info", "biz", "xyz", "online", "site", "top", "icu", 
        "pro", "name", "wang", "win", "ren", "bid", "loan", "men", "date", "trade", 
        "party", "science", "faith", "review", "racing", "webcam", "download", 
        "accountant", "cricket"
    ],
    "科技/AI (Tech/AI)": [
        "io", "ai", "dev", "app", "tech", "me", "tv", "cc", "so", "ws", "xyz", 
        "site", "online", "pw"
    ],
    "商业/购物 (Business)": [
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
    "国家/地区 (ccTLD)": [
        "ac", "ad", "ae", "af", "ag", "ai", "al", "am", "an", "ao", "aq", "ar", 
        "as", "at", "au", "aw", "ax", "az", "ba", "bb", "bd", "be", "bf", "bg", 
        "bh", "bi", "bj", "bm", "bn", "bo", "br", "bs", "bt", "bv", "bw", "by", 
        "bz", "ca", "cc", "cd", "cf", "cg", "ch", "ci", "ck", "cl", "cm", "cn", 
        "co", "cr", "cu", "cv", "cw", "cx", "cy", "cz", "de", "dj", "dk", "dm", 
        "do", "dz", "ec", "ee", "eg", "er", "es", "et", "eu", "fi", "fj", "fk", 
        "fm", "fo", "fr", "ga", "gb", "gd", "ge", "gf", "gg", "gh", "gi", "gl", 
        "gm", "gn", "gp", "gq", "gr", "gs", "gt", "gu", "gw", "gy", "hk", "hm", 
        "hn", "hr", "ht", "hu", "id", "ie", "il", "im", "in", "io", "iq", "ir", 
        "is", "it", "je", "jm", "jo", "jp", "ke", "kg", "kh", "ki", "km", "kn", 
        "kp", "kr", "kw", "ky", "kz", "la", "lb", "lc", "li", "lk", "lr", "ls", 
        "lt", "lu", "lv", "ly", "ma", "mc", "md", "me", "mg", "mh", "mk", "ml", 
        "mm", "mn", "mo", "mp", "mq", "mr", "ms", "mt", "mu", "mv", "mw", "mx", 
        "my", "mz", "na", "nc", "ne", "nf", "ng", "ni", "nl", "no", "np", "nr", 
        "nu", "nz", "om", "pa", "pe", "pf", "pg", "ph", "pk", "pl", "pm", "pn", 
        "pr", "ps", "pt", "pw", "py", "qa", "re", "ro", "rs", "ru", "rw", "sa", 
        "sb", "sc", "sd", "se", "sg", "sh", "si", "sj", "sk", "sl", "sm", "sn", 
        "so", "sr", "ss", "st", "su", "sv", "sx", "sy", "sz", "tc", "td", "tf", 
        "tg", "th", "tj", "tk", "tl", "tm", "tn", "to", "tr", "tt", "tv", "tw", 
        "tz", "ua", "ug", "uk", "us", "uy", "uz", "va", "vc", "ve", "vg", "vi", 
        "vn", "vu", "wf", "ws", "ye", "yt", "za", "zm", "zw"
    ]
}

ALL_TLDS = sorted(list(set(tld for tlds in CATEGORIZED_TLDS.values() for tld in tlds)))

WORDS_2 = ['aa', 'ab', 'ac', 'ad', 'ae', 'af', 'ag', 'ah', 'ai', 'aj', 'ak', 'al', 'am', 'an', 'ao', 'ap', 'aq', 'ar', 'as', 'at', 'au', 'av', 'aw', 'ax', 'ay', 'az', 'ba', 'bb', 'bc', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bk', 'bl', 'bm', 'bn', 'bo', 'bp', 'br', 'bs', 'bt', 'bu', 'bv', 'bw', 'bx', 'by', 'ca', 'cb', 'cc', 'cd', 'ce', 'cf', 'cg', 'ch', 'ci', 'cj', 'ck', 'cl', 'cm', 'cn', 'co', 'cp', 'cq', 'cr', 'cs', 'ct', 'cu', 'cv', 'cw', 'cx', 'cy', 'cz', 'da', 'db', 'dc', 'dd', 'de', 'df', 'dg', 'dh', 'di', 'dj', 'dk', 'dl', 'dm', 'dn', 'do', 'dp', 'dq', 'dr', 'ds', 'dt', 'du', 'dv', 'dw', 'dx', 'dy', 'dz', 'ea', 'eb', 'ec', 'ed', 'ee', 'ef', 'eg', 'eh', 'ei', 'ej', 'ek', 'el', 'em', 'en', 'eo', 'ep', 'eq', 'er', 'es', 'et', 'eu', 'ev', 'ew', 'ex', 'ez', 'fa', 'fb', 'fc', 'fd', 'fe', 'ff', 'fg', 'fh', 'fi', 'fj', 'fl', 'fm', 'fn', 'fo', 'fp', 'fr', 'fs', 'ft', 'fu', 'fw', 'fx', 'fy', 'ga', 'gb', 'gc', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gj', 'gk', 'gl', 'gm', 'gn', 'go', 'gp', 'gr', 'gs', 'gt', 'gu', 'gv', 'gw', 'gx', 'gz', 'ha', 'hb', 'hc', 'hd', 'he', 'hf', 'hg', 'hh', 'hi', 'hj', 'hk', 'hl', 'hm', 'hn', 'ho', 'hp', 'hq', 'hr', 'hs', 'ht', 'hu', 'hv', 'hw', 'hx', 'hy', 'hz', 'ia', 'ib', 'ic', 'id', 'ie', 'if', 'ig', 'ih', 'ii', 'ij', 'ik', 'il', 'im', 'in', 'io', 'ip', 'iq', 'ir', 'is', 'it', 'iu', 'iv', 'ix', 'iz', 'ja', 'jb', 'jc', 'jd', 'je', 'jf', 'jg', 'jh', 'ji', 'jj', 'jk', 'jl', 'jm', 'jn', 'jo', 'jp', 'jr', 'js', 'jt', 'ju', 'jv', 'jw', 'ka', 'kb', 'kc', 'kd', 'ke', 'kg', 'kh', 'ki', 'kj', 'kk', 'kl', 'km', 'kn', 'ko', 'kp', 'kr', 'ks', 'kt', 'ku', 'kv', 'kw', 'kx', 'ky', 'kz', 'la', 'lb', 'lc', 'ld', 'le', 'lf', 'lg', 'lh', 'li', 'lj', 'lk', 'll', 'lm', 'ln', 'lo', 'lp', 'lq', 'lr', 'ls', 'lt', 'lu', 'lv', 'lw', 'lx', 'ly', 'ma', 'mb', 'mc', 'md', 'me', 'mf', 'mg', 'mh', 'mi', 'mj', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'na', 'nb', 'nc', 'nd', 'ne', 'nf', 'ng', 'nh', 'ni', 'nj', 'nk', 'nl', 'nm', 'nn', 'no', 'np', 'nr', 'ns', 'nt', 'nu', 'nv', 'nw', 'nx', 'ny', 'nz', 'oa', 'ob', 'oc', 'od', 'oe', 'of', 'og', 'oh', 'oi', 'oj', 'ok', 'ol', 'om', 'on', 'oo', 'op', 'or', 'os', 'ot', 'ou', 'ov', 'ow', 'ox', 'oz', 'pa', 'pb', 'pc', 'pd', 'pe', 'pf', 'pg', 'ph', 'pi', 'pj', 'pk', 'pl', 'pm', 'pn', 'po', 'pp', 'pq', 'pr', 'ps', 'pt', 'pu', 'pv', 'pw', 'px', 'py', 'qa', 'qb', 'qc', 'qd', 'qi', 'qq', 'qr', 'qt', 'ra', 'rb', 'rc', 'rd', 're', 'rf', 'rg', 'rh', 'ri', 'rj', 'rk', 'rl', 'rm', 'rn', 'ro', 'rp', 'rr', 'rs', 'rt', 'ru', 'rv', 'rw', 'rx', 'ry', 'sa', 'sb', 'sc', 'sd', 'se', 'sf', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sp', 'sq', 'sr', 'ss', 'st', 'su', 'sv', 'sw', 'sx', 'sy', 'sz', 'ta', 'tb', 'tc', 'td', 'te', 'tf', 'tg', 'th', 'ti', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tp', 'tr', 'ts', 'tt', 'tu', 'tv', 'tw', 'tx', 'ty', 'tz', 'ua', 'ub', 'uc', 'ud', 'ue', 'uf', 'ug', 'uh', 'ui', 'uk', 'ul', 'um', 'un', 'up', 'ur', 'us', 'ut', 'uu', 'uv', 'uw', 'ux', 'va', 'vb', 'vc', 've', 'vf', 'vg', 'vi', 'vl', 'vm', 'vn', 'vo', 'vp', 'vr', 'vs', 'vt', 'vu', 'vv', 'vw', 'vx', 'wa', 'wb', 'wc', 'wd', 'we', 'wf', 'wg', 'wh', 'wi', 'wj', 'wk', 'wl', 'wm', 'wn', 'wo', 'wp', 'wr', 'ws', 'wt', 'wu', 'wv', 'ww', 'wx', 'wy', 'xa', 'xb', 'xc', 'xd', 'xe', 'xf', 'xi', 'xl', 'xm', 'xp', 'xr', 'xs', 'xt', 'xu', 'xv', 'xx', 'xy', 'ya', 'yd', 'ye', 'yi', 'yn', 'yo', 'yr', 'yu', 'yy', 'za', 'zh', 'zu', 'zz']
WORDS_3 = ['aaa', 'aac', 'aba', 'abc', 'abe', 'abi', 'abn', 'abs', 'abt', 'abu', 'aca', 'acc', 'ace', 'ack', 'acl', 'acm', 'acp', 'acs', 'act', 'ada', 'adc', 'add', 'adj', 'adm', 'adp', 'adr', 'ads', 'adv', 'aes', 'afb', 'afc', 'aff', 'afl', 'afp', 'aft', 'age', 'ago', 'agp', 'aid', 'aim', 'air', 'aix', 'aka', 'ala', 'ale', 'ali', 'all', 'alr', 'als', 'alt', 'ama', 'amc', 'amd', 'amg', 'ami', 'amp', 'ams', 'amt', 'amy', 'ana', 'and', 'ang', 'ann', 'ans', 'ant', 'any', 'aol', 'apa', 'apc', 'ape', 'api', 'apo', 'app', 'apr', 'aps', 'apt', 'arc', 'are', 'arg', 'ari', 'ark', 'arm', 'arp', 'arr', 'ars', 'art', 'asa', 'asc', 'asf', 'ash', 'asi', 'ask', 'asm', 'asn', 'asp', 'ass', 'ast', 'asu', 'ata', 'atc', 'ate', 'ati', 'atk', 'atl', 'atm', 'atp', 'ats', 'att', 'atv', 'atx', 'aud', 'auf', 'aug', 'aus', 'aut', 'aux', 'ave', 'avg', 'avi', 'avr', 'avs', 'awe', 'axe', 'aye', 'bac', 'bad', 'bag', 'bal', 'bam', 'ban', 'bar', 'bas', 'bat', 'bay', 'bbb', 'bbc', 'bbq', 'bbs', 'bbw', 'bdd', 'bea', 'bed', 'bee', 'beg', 'bei', 'bel', 'ben', 'ber', 'bet', 'bhd', 'bib', 'bid', 'big', 'bin', 'bio', 'bis', 'bit', 'biz', 'blk', 'blu', 'bmc', 'bmg', 'bmi', 'bmp', 'bmw', 'bmx', 'boa', 'bob', 'boc', 'bod', 'bon', 'boo', 'bop', 'bos', 'bot', 'bow', 'box', 'boy', 'bpm', 'bra', 'bro', 'bsc', 'bsd', 'bse', 'bst', 'btw', 'bud', 'buf', 'bug', 'bur', 'bus', 'but', 'buy', 'bye', 'caa', 'cab', 'cac', 'cad', 'cal', 'cam', 'can', 'cao', 'cap', 'car', 'cas', 'cat', 'cbc', 'cbd', 'cbs', 'cca', 'ccc', 'ccd', 'ccm', 'cdc', 'cdn', 'cdp', 'cdr', 'cds', 'cdt', 'cen', 'ceo', 'ces', 'cet', 'cfa', 'cfo', 'cfr', 'cfs', 'cgi', 'cha', 'che', 'chf', 'chi', 'cho', 'chr', 'chu', 'cia', 'cid', 'cio', 'cir', 'cis', 'cit', 'cle', 'cli', 'clr', 'cmd', 'cme', 'cmp', 'cms', 'cnc', 'cnn', 'cns', 'coa', 'cod', 'coe', 'col', 'com', 'con', 'cop', 'cor', 'cos', 'cot', 'cow', 'cox', 'cpa', 'cpc', 'cpe', 'cpg', 'cpi', 'cpl', 'cpm', 'cpp', 'cpr', 'cps', 'cpt', 'cpu', 'crc', 'cre', 'crm', 'crn', 'crs', 'crt', 'cry', 'csa', 'csc', 'csi', 'csr', 'css', 'cst', 'csu', 'csv', 'ctr', 'cts', 'ctx', 'cub', 'cue', 'cum', 'cup', 'cur', 'cut', 'cuz', 'cvs', 'dab', 'dac', 'dad', 'dag', 'dal', 'dam', 'dan', 'dar', 'das', 'dat', 'dau', 'day', 'dba', 'dbz', 'dcp', 'dcr', 'dcs', 'ddr', 'dds', 'dea', 'deb', 'dec', 'dee', 'def', 'deg', 'dei', 'del', 'dem', 'den', 'dep', 'der', 'des', 'det', 'dev', 'dew', 'dex', 'dhs', 'dia', 'did', 'die', 'dig', 'dim', 'din', 'dip', 'dir', 'dis', 'dit', 'div', 'diy', 'djs', 'dll', 'dlp', 'dma', 'dmc', 'dmx', 'dna', 'dns', 'doc', 'dod', 'doe', 'dog', 'doi', 'dom', 'don', 'doo', 'dos', 'dot', 'dow', 'dpi', 'drm', 'dry', 'dsa', 'dsc', 'dsl', 'dsm', 'dsp', 'dss', 'dst', 'dtd', 'dts', 'dub', 'due', 'dug', 'dui', 'dun', 'duo', 'dvb', 'dvd', 'dvi', 'dvr', 'dwi', 'dye', 'ean', 'ear', 'eas', 'eat', 'eau', 'ecc', 'eco', 'ecs', 'ect', 'edi', 'eds', 'edt', 'edu', 'een', 'eff', 'egg', 'ego', 'eia', 'ein', 'eis', 'elf', 'eli', 'elk', 'elm', 'emc', 'emi', 'emo', 'emp', 'ems', 'emu', 'enb', 'end', 'eng', 'ent', 'env', 'eos', 'epa', 'eps', 'era', 'erp', 'err', 'ers', 'esa', 'esc', 'esd', 'esl', 'esp', 'esq', 'ess', 'est', 'eta', 'etc', 'eur', 'eva', 'eve', 'evo', 'exc', 'exe', 'exp', 'ext', 'eye', 'faa', 'fab', 'fac', 'fam', 'fan', 'fao', 'faq', 'far', 'fas', 'fat', 'fav', 'fax', 'fbi', 'fcc', 'fda', 'feb', 'fed', 'fee', 'few', 'ffi', 'ffl', 'fha', 'fig', 'fin', 'fir', 'fit', 'fix', 'fla', 'flu', 'fly', 'fno', 'fob', 'fog', 'foo', 'for', 'fox', 'fpo', 'fps', 'fra', 'fre', 'fri', 'fry', 'fsa', 'fsb', 'fta', 'ftc', 'ftd', 'fte', 'ftp', 'fun', 'fur', 'fwd', 'fyi', 'gag', 'gal', 'gam', 'gan', 'gao', 'gap', 'gas', 'gay', 'gba', 'gbp', 'gcc', 'gdb', 'gdp', 'ged', 'gee', 'gel', 'gem', 'gen', 'geo', 'ger', 'get', 'gev', 'ghz', 'gia', 'gif', 'gig', 'gil', 'gin', 'gis', 'gln', 'glu', 'gly', 'gmc', 'gmt', 'gnd', 'gnu', 'goa', 'god', 'goo', 'gop', 'got', 'gov', 'gpa', 'gpl', 'gpo', 'gps', 'gre', 'gsa', 'gsm', 'gst', 'gta', 'gtk', 'gui', 'gum', 'gun', 'gus', 'gut', 'guy', 'gym', 'had', 'hai', 'hal', 'ham', 'han', 'har', 'has', 'hat', 'hay', 'hbo', 'hcl', 'hdd', 'hee', 'heh', 'hem', 'hen', 'hep', 'her', 'hes', 'het', 'hex', 'hey', 'hgh', 'hhs', 'hid', 'him', 'hip', 'his', 'hit', 'hiv', 'hmm', 'hms', 'hoc', 'hog', 'hon', 'hop', 'hot', 'how', 'hpa', 'hrs', 'hsn', 'htm', 'hua', 'hub', 'hud', 'hug', 'huh', 'hum', 'hun', 'hut', 'hwy', 'ian', 'ibm', 'ibn', 'icc', 'ice', 'ich', 'icq', 'ics', 'ict', 'ida', 'idc', 'ide', 'idg', 'ids', 'iec', 'ies', 'ifs', 'ign', 'iii', 'iis', 'ile', 'ill', 'ilo', 'imc', 'imf', 'img', 'imo', 'imp', 'ims', 'inc', 'ind', 'inf', 'ing', 'ink', 'inn', 'ins', 'int', 'ion', 'ios', 'ipb', 'ipc', 'ipo', 'ips', 'ira', 'irc', 'ire', 'irq', 'irs', 'isa', 'isd', 'ish', 'isl', 'iso', 'isp', 'iss', 'ist', 'ita', 'itc', 'itk', 'its', 'itu', 'ity', 'ive', 'ivy', 'jam', 'jan', 'jar', 'jaw', 'jay', 'jbl', 'jen', 'jet', 'jew', 'jfk', 'jim', 'jin', 'job', 'joe', 'jon', 'joy', 'jpg', 'jpy', 'jsp', 'jul', 'jun', 'jvc', 'kai', 'kan', 'kat', 'kay', 'kde', 'ken', 'kev', 'key', 'khz', 'kia', 'kid', 'kim', 'kin', 'kit', 'kms', 'koh', 'kos', 'kpx', 'kvm', 'lab', 'lac', 'lad', 'lag', 'lai', 'lam', 'lan', 'lao', 'lap', 'las', 'lat', 'law', 'lax', 'lay', 'lbs', 'lcd', 'lds', 'lea', 'lec', 'led', 'lee', 'leg', 'lei', 'len', 'leo', 'les', 'let', 'leu', 'lev', 'lex', 'lib', 'lic', 'lid', 'lie', 'lil', 'lim', 'lin', 'lip', 'lis', 'lit', 'liu', 'liz', 'llc', 'llp', 'lob', 'loc', 'log', 'lol', 'lon', 'los', 'lot', 'lou', 'low', 'lps', 'lsu', 'ltd', 'luc', 'lug', 'luv', 'lux', 'lys', 'mac', 'mad', 'mae', 'mag', 'mah', 'mai', 'mal', 'man', 'mao', 'map', 'mar', 'mas', 'mat', 'max', 'may', 'mba', 'mca', 'mci', 'mda', 'mds', 'mdt', 'med', 'meg', 'mel', 'mem', 'men', 'mer', 'mes', 'met', 'mev', 'mfc', 'mfg', 'mfr', 'mft', 'mgm', 'mhz', 'mia', 'mib', 'mic', 'mid', 'mil', 'min', 'mio', 'mir', 'mis', 'mit', 'mix', 'mla', 'mlb', 'mlm', 'mls', 'mmc', 'mmf', 'mmm', 'mms', 'mnt', 'mob', 'moc', 'mod', 'moe', 'moi', 'mol', 'mom', 'mon', 'moo', 'mop', 'mos', 'mot', 'mov', 'mpa', 'mpc', 'mpg', 'mph', 'mpi', 'mps', 'mri', 'mrs', 'msa', 'msc', 'msg', 'msi', 'msm', 'msn', 'mso', 'mst', 'msu', 'mta', 'mtv', 'mud', 'mug', 'mum', 'mus', 'mvc', 'mvp', 'myr', 'nad', 'nam', 'nan', 'nap', 'nas', 'nat', 'nav', 'nay', 'nba', 'nbc', 'ncr', 'nec', 'ned', 'nel', 'neo', 'nes', 'net', 'neu', 'new', 'nfl', 'nfs', 'ngc', 'ngo', 'nhl', 'nhs', 'nib', 'nic', 'nie', 'nih', 'nil', 'nip', 'nis', 'nmr', 'nod', 'nok', 'nom', 'non', 'nor', 'nos', 'not', 'nov', 'now', 'nox', 'npr', 'nrc', 'nrs', 'nsa', 'nsf', 'nsu', 'nsw', 'ntp', 'num', 'nur', 'nut', 'nws', 'nwt', 'nyc', 'nyt', 'oak', 'obj', 'obs', 'occ', 'och', 'ocr', 'oct', 'odd', 'ode', 'oem', 'off', 'ogg', 'ohm', 'oil', 'oki', 'old', 'ole', 'omb', 'omg', 'one', 'ons', 'ont', 'ooh', 'ooo', 'opp', 'ops', 'opt', 'ora', 'orb', 'ord', 'ore', 'orf', 'org', 'oro', 'ors', 'oss', 'osu', 'osx', 'otc', 'our', 'out', 'owe', 'owl', 'own', 'pac', 'pad', 'pak', 'pal', 'pam', 'pan', 'pap', 'par', 'pas', 'pat', 'paw', 'pax', 'pay', 'paz', 'pbs', 'pcb', 'pcg', 'pci', 'pcm', 'pcr', 'pcs', 'pct', 'pda', 'pdb', 'pdf', 'pdp', 'pdt', 'pea', 'pee', 'peg', 'pei', 'pen', 'pep', 'per', 'pet', 'pfc', 'pga', 'pgp', 'phd', 'phe', 'phi', 'php', 'phs', 'pic', 'pid', 'pie', 'pig', 'pim', 'pin', 'pit', 'pix', 'pkg', 'plc', 'pls', 'ply', 'plz', 'pmc', 'pms', 'png', 'pod', 'poe', 'pol', 'pop', 'por', 'pos', 'pot', 'pow', 'poy', 'ppc', 'ppl', 'ppm', 'ppp', 'pps', 'ppt', 'prc', 'pre', 'pri', 'pro', 'psa', 'psc', 'psi', 'psp', 'pst', 'psu', 'psy', 'pta', 'pte', 'ptr', 'pts', 'pty', 'pub', 'put', 'pvc', 'pvt', 'qld', 'qos', 'qtr', 'qty', 'que', 'qui', 'quo', 'rac', 'rad', 'rae', 'raf', 'rag', 'rai', 'ram', 'ran', 'rao', 'rap', 'ras', 'rat', 'raw', 'ray', 'rbi', 'rca', 'rcs', 'rcw', 'rdf', 'rea', 'rec', 'red', 'ref', 'reg', 'rei', 'rel', 'rem', 'ren', 'rep', 'req', 'res', 'ret', 'rev', 'rex', 'rey', 'rfc', 'rfp', 'rgb', 'rib', 'ric', 'rid', 'rig', 'rim', 'rio', 'rip', 'rms', 'rna', 'rob', 'roc', 'rod', 'roe', 'roi', 'rom', 'ron', 'ros', 'rot', 'row', 'roy', 'rpc', 'rpg', 'rpm', 'rrp', 'rsa', 'rss', 'rtf', 'rts', 'rub', 'rue', 'rug', 'rum', 'run', 'rus', 'rye', 'sac', 'sad', 'sal', 'sam', 'san', 'sao', 'sap', 'sar', 'sas', 'sat', 'saw', 'sax', 'say', 'sba', 'sbc', 'sbs', 'sca', 'sch', 'sci', 'scm', 'sco', 'scr', 'sdk', 'sdl', 'sdn', 'sds', 'sea', 'sec', 'sed', 'see', 'sek', 'sem', 'sen', 'seo', 'sep', 'seq', 'ser', 'ses', 'set', 'sew', 'sex', 'sgd', 'sgh', 'sgi', 'sgt', 'sha', 'she', 'shi', 'shy', 'sic', 'sid', 'sie', 'sig', 'sim', 'sin', 'sip', 'sir', 'sis', 'sit', 'six', 'ska', 'ski', 'sku', 'sky', 'sle', 'sli', 'slr', 'smb', 'smc', 'sme', 'smf', 'smp', 'sms', 'snp', 'snr', 'soa', 'soc', 'sol', 'som', 'son', 'soo', 'sos', 'sox', 'soy', 'spa', 'spc', 'spd', 'spf', 'spi', 'spp', 'spy', 'sql', 'src', 'sri', 'srl', 'srs', 'ssa', 'ssh', 'ssi', 'ssk', 'ssl', 'sst', 'sta', 'std', 'ste', 'sti', 'stl', 'sto', 'stp', 'str', 'sts', 'stu', 'sub', 'sue', 'sum', 'sun', 'sup', 'sur', 'sus', 'suv', 'svc', 'svg', 'svn', 'swf', 'syn', 'sys', 'tab', 'tac', 'tad', 'tag', 'tai', 'taj', 'tal', 'tam', 'tan', 'tao', 'tap', 'tar', 'tas', 'tau', 'tax', 'tba', 'tbd', 'tcl', 'tcm', 'tcp', 'tdk', 'tds', 'tea', 'tec', 'ted', 'tee', 'teh', 'tek', 'tel', 'tem', 'ten', 'ter', 'tes', 'tex', 'tft', 'tgp', 'tha', 'thb', 'the', 'thn', 'tho', 'thr', 'ths', 'thu', 'thx', 'thy', 'tia', 'tic', 'tie', 'til', 'tim', 'tin', 'tip', 'tis', 'tit', 'tlc', 'tls', 'tmp', 'tnt', 'toc', 'toe', 'tom', 'ton', 'too', 'top', 'tor', 'tos', 'tot', 'tow', 'toy', 'tra', 'tri', 'try', 'tsn', 'tsp', 'ttf', 'ttl', 'tty', 'tub', 'tue', 'tvs', 'two', 'twp', 'txt', 'tyr', 'uae', 'ubc', 'udp', 'ufo', 'uid', 'uma', 'umd', 'uml', 'una', 'unc', 'und', 'une', 'uni', 'uno', 'upc', 'ups', 'uri', 'url', 'urn', 'urw', 'usa', 'usb', 'usc', 'usd', 'use', 'usr', 'uss', 'utc', 'utf', 'utp', 'vac', 'val', 'van', 'var', 'vat', 'vcd', 'vcr', 'vel', 'ver', 'vet', 'vga', 'vhf', 'vhs', 'via', 'vic', 'vid', 'vie', 'vii', 'vin', 'vip', 'vis', 'viz', 'voc', 'vol', 'von', 'vor', 'vos', 'vox', 'vpn', 'wac', 'wai', 'wal', 'wan', 'wap', 'war', 'was', 'wat', 'wav', 'wax', 'way', 'web', 'wed', 'wee', 'wei', 'wen', 'wes', 'wet', 'who', 'why', 'wie', 'wig', 'wil', 'win', 'wit', 'wks', 'wma', 'wmd', 'wmv', 'won', 'woo', 'wow', 'wtf', 'wto', 'wwe', 'wwf', 'www', 'xda', 'xii', 'xiv', 'xml', 'xsl', 'xtc', 'xvi', 'xxl', 'xxx', 'yan', 'yay', 'yds', 'yea', 'yen', 'yep', 'yer', 'yes', 'yet', 'yin', 'you', 'yrs', 'yum', 'yup', 'zen', 'zip', 'zoe', 'zoo', 'zum', 'zur', 'zus']
WORDS_4 = ['abba', 'abby', 'abit', 'able', 'acad', 'acct', 'acer', 'aces', 'acid', 'aclu', 'acme', 'acne', 'acre', 'acta', 'acts', 'adam', 'addr', 'adds', 'adhd', 'adsl', 'aero', 'aest', 'afro', 'aged', 'ages', 'agri', 'aide', 'aids', 'aims', 'ajax', 'akin', 'akon', 'alan', 'alas', 'alba', 'alec', 'alex', 'alfa', 'alla', 'alle', 'ally', 'alma', 'aloe', 'alot', 'alps', 'also', 'alta', 'alto', 'amen', 'amer', 'ames', 'amex', 'amid', 'ammo', 'amor', 'amos', 'amps', 'anal', 'andy', 'anna', 'anne', 'anon', 'ansi', 'ante', 'anti', 'ants', 'apex', 'apis', 'appl', 'apps', 'aqua', 'arab', 'arch', 'area', 'ares', 'args', 'argv', 'aria', 'arid', 'arin', 'arms', 'army', 'arte', 'arts', 'asap', 'asia', 'asin', 'asks', 'asst', 'astm', 'asus', 'atom', 'attn', 'attr', 'auch', 'audi', 'aunt', 'aura', 'aust', 'auth', 'auto', 'avec', 'avid', 'avis', 'aviv', 'avon', 'away', 'axel', 'axes', 'axis', 'axle', 'babe', 'baby', 'bach', 'back', 'bags', 'baht', 'bail', 'bait', 'baja', 'bake', 'bald', 'bali', 'ball', 'balm', 'band', 'bang', 'bank', 'bans', 'barb', 'bard', 'bare', 'bark', 'barn', 'barr', 'bars', 'bart', 'base', 'bash', 'bass', 'bath', 'bats', 'bays', 'bdsm', 'bead', 'beam', 'bean', 'bear', 'beat', 'beau', 'beck', 'beds', 'beef', 'been', 'beer', 'bees', 'bell', 'belt', 'bend', 'benq', 'bent', 'benz', 'berg', 'bern', 'bert', 'best', 'beta', 'beth', 'bets', 'bias', 'bids', 'bien', 'bike', 'bild', 'bill', 'bind', 'bins', 'biol', 'bios', 'bird', 'bite', 'bits', 'blah', 'bldg', 'blew', 'bloc', 'blog', 'blow', 'blue', 'blur', 'blvd', 'bnet', 'boat', 'boca', 'body', 'boil', 'bold', 'bolt', 'bomb', 'bond', 'bone', 'bonn', 'bono', 'boob', 'book', 'bool', 'boom', 'boot', 'bore', 'born', 'bose', 'boss', 'both', 'bots', 'bout', 'bowl', 'bows', 'boyd', 'boys', 'boyz', 'brad', 'bras', 'bred', 'brew', 'brit', 'bros', 'buck', 'buds', 'buff', 'bugs', 'bulb', 'bulk', 'bull', 'bump', 'bunk', 'burn', 'burr', 'burt', 'bury', 'bush', 'bust', 'busy', 'butt', 'buys', 'buzz', 'byrd', 'byte', 'cabo', 'cafe', 'cage', 'cain', 'cake', 'calc', 'calf', 'call', 'calm', 'came', 'camp', 'cams', 'cane', 'cans', 'cant', 'cape', 'caps', 'carb', 'card', 'care', 'carl', 'carp', 'carr', 'cars', 'cart', 'cary', 'casa', 'case', 'cash', 'cass', 'cast', 'cats', 'cave', 'cctv', 'cdma', 'cdna', 'cdrw', 'cell', 'cent', 'cern', 'cert', 'cest', 'chad', 'chan', 'chap', 'char', 'chat', 'chef', 'chem', 'chen', 'cher', 'chew', 'chic', 'chin', 'chip', 'chit', 'chop', 'chow', 'ciao', 'cite', 'city', 'clad', 'clam', 'clan', 'claw', 'clay', 'clic', 'clin', 'clip', 'clit', 'club', 'clue', 'cmos', 'cnet', 'coal', 'coat', 'cobb', 'coca', 'cock', 'coco', 'code', 'cody', 'coed', 'coil', 'coin', 'coke', 'cola', 'cold', 'cole', 'coli', 'coll', 'colt', 'coma', 'comb', 'come', 'comm', 'como', 'comp', 'cond', 'cone', 'conf', 'conn', 'cons', 'cont', 'cook', 'cool', 'coop', 'cope', 'cops', 'copy', 'cord', 'core', 'cork', 'corn', 'corp', 'corr', 'cory', 'cost', 'cote', 'coup', 'cove', 'cows', 'cozy', 'cpan', 'cpus', 'crab', 'crap', 'crew', 'crib', 'cron', 'crop', 'crow', 'cruz', 'ctrl', 'cuba', 'cube', 'cubs', 'cues', 'cuff', 'cult', 'cunt', 'cups', 'curb', 'cure', 'curl', 'cute', 'cuts', 'cyan', 'dade', 'dads', 'dale', 'daly', 'dame', 'damn', 'damp', 'dams', 'dana', 'dane', 'dans', 'dare', 'dark', 'darn', 'dart', 'dash', 'data', 'date', 'dave', 'dawn', 'days', 'dblp', 'dead', 'deaf', 'deal', 'dean', 'dear', 'debt', 'deck', 'deco', 'deed', 'deep', 'deer', 'deli', 'dell', 'demi', 'demo', 'dems', 'dent', 'deny', 'dept', 'desc', 'desk', 'dhcp', 'dial', 'diaz', 'dice', 'dick', 'died', 'dies', 'diet', 'diff', 'digg', 'digi', 'dime', 'dimm', 'dine', 'ding', 'dino', 'dion', 'dior', 'dire', 'dirk', 'dirt', 'disc', 'dish', 'disk', 'dist', 'diva', 'dive', 'divx', 'dmoz', 'dock', 'docs', 'does', 'dogg', 'dogs', 'doll', 'dome', 'done', 'dong', 'dont', 'doom', 'door', 'dora', 'dorm', 'dose', 'dots', 'doug', 'dove', 'down', 'drag', 'dram', 'draw', 'drew', 'drip', 'drop', 'drug', 'drum', 'dual', 'duck', 'duct', 'dude', 'duel', 'dues', 'duff', 'duke', 'dull', 'duly', 'dumb', 'dump', 'dune', 'dunn', 'dusk', 'dust', 'duty', 'dvds', 'dyer', 'dyes', 'dyke', 'each', 'earl', 'earn', 'ears', 'ease', 'east', 'easy', 'eats', 'ebay', 'echo', 'econ', 'eddy', 'eden', 'edge', 'edit', 'educ', 'eggs', 'eine', 'elec', 'elem', 'ella', 'elle', 'else', 'embl', 'emma', 'ends', 'engl', 'enom', 'enum', 'envy', 'enya', 'epic', 'eric', 'erie', 'erik', 'erin', 'espn', 'esta', 'este', 'euro', 'eval', 'evan', 'even', 'ever', 'evil', 'exam', 'excl', 'exec', 'exif', 'exim', 'exit', 'expo', 'eyed', 'eyes', 'ezra', 'face', 'fact', 'fade', 'fail', 'fair', 'fake', 'fall', 'fame', 'fans', 'faqs', 'fare', 'farm', 'faso', 'fast', 'fate', 'fats', 'faux', 'fave', 'fear', 'feat', 'feed', 'feel', 'fees', 'feet', 'fell', 'felt', 'fema', 'feng', 'feof', 'fern', 'fest', 'fiat', 'fifa', 'fife', 'figs', 'fiji', 'file', 'fill', 'film', 'find', 'fine', 'finn', 'fins', 'fire', 'firm', 'fish', 'fist', 'fits', 'five', 'flag', 'flap', 'flat', 'flaw', 'flea', 'fled', 'flee', 'flew', 'flex', 'flip', 'flop', 'flow', 'flux', 'foam', 'foia', 'foil', 'fold', 'folk', 'fond', 'font', 'food', 'fool', 'foot', 'ford', 'fore', 'fork', 'form', 'fort', 'foto', 'foul', 'four', 'fran', 'frau', 'fred', 'free', 'freq', 'frey', 'frog', 'from', 'fuck', 'fuel', 'fuji', 'full', 'func', 'fund', 'funk', 'fury', 'fuse', 'gage', 'gail', 'gain', 'gala', 'gale', 'gals', 'game', 'gang', 'gaps', 'gary', 'gate', 'gave', 'gays', 'gaza', 'gaze', 'gcse', 'gear', 'geek', 'gems', 'gene', 'gets', 'gifs', 'gift', 'gigs', 'gill', 'gimp', 'gina', 'girl', 'give', 'glad', 'glen', 'glow', 'glue', 'gmbh', 'goal', 'goat', 'gods', 'goes', 'goin', 'gold', 'golf', 'gone', 'gong', 'good', 'gore', 'goth', 'goto', 'govt', 'gown', 'gprs', 'grab', 'grad', 'gram', 'gran', 'gras', 'gray', 'greg', 'grep', 'grew', 'grey', 'grid', 'grim', 'grin', 'grip', 'grow', 'guam', 'gulf', 'gull', 'guns', 'guru', 'guts', 'guys', 'gwen', 'gyms', 'gzip', 'haas', 'hack', 'haha', 'hahn', 'hail', 'hair', 'hale', 'half', 'hall', 'halo', 'halt', 'hama', 'hand', 'hang', 'hank', 'hans', 'hard', 'hare', 'harm', 'harp', 'hart', 'hash', 'hast', 'hate', 'hath', 'hats', 'haul', 'have', 'hawk', 'hays', 'haze', 'hdtv', 'head', 'heal', 'heap', 'hear', 'heat', 'heck', 'heel', 'hehe', 'held', 'hell', 'helm', 'help', 'hemp', 'herb', 'herd', 'here', 'hero', 'hers', 'hess', 'hide', 'hier', 'hifi', 'high', 'hike', 'hill', 'hint', 'hips', 'hire', 'hist', 'hits', 'hklm', 'hmmm', 'hold', 'hole', 'holt', 'holy', 'home', 'homo', 'hong', 'hood', 'hook', 'hoop', 'hope', 'horn', 'hose', 'host', 'hour', 'howe', 'href', 'hsbc', 'html', 'http', 'hubs', 'huge', 'hugh', 'hugo', 'hugs', 'hulk', 'hull', 'hung', 'hunk', 'huns', 'hunt', 'hurt', 'hush', 'hvac', 'hyde', 'hymn', 'hype', 'ibid', 'ibis', 'icon', 'idea', 'idle', 'idol', 'ieee', 'ietf', 'igor', 'ilug', 'imac', 'imap', 'imdb', 'inch', 'incl', 'indi', 'indo', 'indy', 'info', 'init', 'inks', 'inns', 'inst', 'intl', 'into', 'ions', 'iowa', 'ipaq', 'ipod', 'iran', 'iraq', 'iris', 'iron', 'isbn', 'isdn', 'isis', 'isle', 'isnt', 'isps', 'issn', 'item', 'ivan', 'jack', 'jade', 'jail', 'jake', 'jams', 'jane', 'jars', 'java', 'jaws', 'jays', 'jazz', 'jdbc', 'jean', 'jedi', 'jeep', 'jeff', 'jerk', 'jess', 'jets', 'jeux', 'jews', 'jill', 'jimi', 'jira', 'jive', 'joan', 'jobs', 'joel', 'joey', 'john', 'join', 'jojo', 'joke', 'jong', 'jose', 'josh', 'jour', 'jovi', 'jpeg', 'juan', 'judd', 'jude', 'judy', 'july', 'jump', 'june', 'jung', 'junk', 'jury', 'just', 'kane', 'kara', 'karl', 'kart', 'kate', 'katy', 'katz', 'kbps', 'keen', 'keep', 'keno', 'kent', 'kept', 'kern', 'kerr', 'keys', 'khan', 'kick', 'kids', 'kiev', 'kill', 'kind', 'king', 'kirk', 'kiss', 'kite', 'kits', 'kiwi', 'knee', 'knew', 'knit', 'knob', 'knot', 'know', 'knox', 'kobe', 'koch', 'kona', 'kong', 'kool', 'korn', 'kris', 'kung', 'kurt', 'kyle', 'labs', 'lace', 'lack', 'lady', 'laid', 'lake', 'lama', 'lamb', 'lame', 'lamp', 'land', 'lane', 'lang', 'laos', 'laps', 'lara', 'lars', 'last', 'late', 'lava', 'lawn', 'laws', 'lays', 'lazy', 'ldap', 'lead', 'leaf', 'leah', 'leak', 'lean', 'leap', 'leds', 'left', 'lego', 'legs', 'lena', 'lend', 'lens', 'lent', 'leon', 'less', 'lest', 'lets', 'lett', 'levi', 'levy', 'liam', 'liar', 'libc', 'libs', 'lick', 'lied', 'lien', 'lies', 'lieu', 'life', 'lift', 'like', 'lily', 'lima', 'limb', 'lime', 'limo', 'limp', 'line', 'ling', 'link', 'linn', 'lion', 'lips', 'lira', 'lisa', 'lisp', 'list', 'lite', 'live', 'load', 'loan', 'loch', 'lock', 'loft', 'logo', 'logs', 'lois', 'lola', 'lone', 'long', 'look', 'loop', 'lord', 'lore', 'lori', 'lose', 'loss', 'lost', 'lots', 'loud', 'love', 'lowe', 'lows', 'luck', 'lucy', 'luis', 'luke', 'lulu', 'lump', 'luna', 'lund', 'lung', 'lure', 'lush', 'lust', 'lyme', 'lynn', 'lynx', 'lyon', 'mach', 'mack', 'macs', 'macy', 'made', 'mage', 'mags', 'maid', 'mail', 'main', 'mais', 'make', 'male', 'mali', 'mall', 'mama', 'mana', 'mann', 'mans', 'many', 'maps', 'mara', 'marc', 'mare', 'mark', 'mars', 'mart', 'marx', 'mary', 'mask', 'mass', 'mast', 'mate', 'math', 'mats', 'matt', 'maui', 'maxi', 'maya', 'mayo', 'maze', 'mbps', 'mcse', 'mcsg', 'mead', 'meal', 'mean', 'meat', 'meds', 'meet', 'mega', 'mehr', 'melt', 'memo', 'mens', 'ment', 'menu', 'mere', 'mesa', 'mesh', 'mess', 'meta', 'meth', 'mets', 'mgmt', 'mice', 'mick', 'midi', 'mike', 'mild', 'mile', 'milf', 'milk', 'mill', 'mime', 'mimi', 'mind', 'mine', 'ming', 'minh', 'mini', 'mins', 'mint', 'mips', 'mira', 'misc', 'miss', 'mist', 'moby', 'mock', 'mode', 'mods', 'mojo', 'mold', 'mole', 'moms', 'mona', 'monk', 'mono', 'mont', 'mood', 'moon', 'more', 'moss', 'most', 'moto', 'move', 'mpeg', 'mpls', 'mrna', 'msdn', 'msds', 'msie', 'msrp', 'much', 'mugs', 'mule', 'muse', 'must', 'mute', 'muze', 'myth', 'nach', 'nadu', 'nail', 'name', 'nano', 'napa', 'nasa', 'nash', 'nate', 'natl', 'nato', 'navy', 'nazi', 'ncaa', 'ncbi', 'neal', 'near', 'neat', 'neck', 'need', 'neil', 'nemo', 'neon', 'nerd', 'nero', 'ness', 'nest', 'nets', 'news', 'next', 'ngos', 'nice', 'nick', 'nike', 'nile', 'nimh', 'nina', 'nine', 'nist', 'nite', 'niue', 'noaa', 'noah', 'node', 'noel', 'noir', 'none', 'noon', 'nope', 'nora', 'nord', 'norm', 'nose', 'note', 'noun', 'nous', 'nova', 'novo', 'ntsc', 'nude', 'nuke', 'null', 'nuts', 'nyse', 'oahu', 'oaks', 'oath', 'obey', 'oclc', 'odbc', 'odds', 'oder', 'odor', 'oecd', 'offs', 'ohio', 'oils', 'okay', 'olds', 'oman', 'omar', 'omit', 'omni', 'once', 'ones', 'only', 'onto', 'onyx', 'oops', 'opal', 'open', 'opus', 'oral', 'orgy', 'orig', 'osha', 'oslo', 'ostg', 'otis', 'otto', 'ours', 'outs', 'oval', 'oven', 'over', 'owed', 'owen', 'owls', 'owns', 'pace', 'pack', 'pact', 'pads', 'page', 'paid', 'pain', 'pair', 'pale', 'palm', 'palo', 'pals', 'pane', 'pans', 'pant', 'papa', 'para', 'park', 'part', 'paso', 'pass', 'past', 'path', 'paul', 'pays', 'pcos', 'pdas', 'pdfs', 'peak', 'pear', 'peas', 'peck', 'peek', 'peel', 'peer', 'penn', 'pens', 'perl', 'pers', 'peru', 'peso', 'pest', 'pete', 'pets', 'phat', 'phil', 'phys', 'pick', 'pics', 'pier', 'pies', 'pigs', 'pike', 'pile', 'pill', 'pimp', 'pine', 'ping', 'pink', 'pins', 'pint', 'pipe', 'piss', 'pits', 'pitt', 'pity', 'plan', 'plat', 'play', 'plea', 'plot', 'plug', 'plum', 'plus', 'pmid', 'poem', 'poet', 'pogo', 'pole', 'polk', 'poll', 'polo', 'poly', 'pond', 'pong', 'pony', 'pooh', 'pool', 'poor', 'pope', 'pops', 'pork', 'porn', 'port', 'pose', 'post', 'pots', 'pour', 'prac', 'pray', 'prep', 'pres', 'prev', 'prey', 'prix', 'prob', 'proc', 'prod', 'prof', 'prog', 'prom', 'prop', 'pros', 'prot', 'prov', 'publ', 'pubs', 'puff', 'pull', 'pulp', 'puma', 'pump', 'punk', 'punt', 'pure', 'push', 'puts', 'quad', 'quan', 'quay', 'quit', 'quiz', 'quot', 'race', 'rack', 'rage', 'raid', 'rail', 'rain', 'rake', 'rama', 'ramp', 'rams', 'rand', 'rang', 'rank', 'rant', 'rape', 'rare', 'rash', 'rate', 'rats', 'rave', 'rays', 'razr', 'read', 'real', 'reap', 'rear', 'reds', 'reed', 'reef', 'reel', 'regs', 'reid', 'rely', 'rene', 'reno', 'rent', 'reps', 'resp', 'rest', 'rfid', 'ribs', 'rica', 'rice', 'rich', 'rick', 'rico', 'ride', 'rims', 'ring', 'riot', 'ripe', 'rise', 'risk', 'rita', 'rite', 'ritz', 'road', 'robe', 'rock', 'rode', 'rods', 'role', 'roll', 'roma', 'rome', 'roms', 'roof', 'room', 'root', 'rope', 'rosa', 'rose', 'ross', 'roth', 'rove', 'rowe', 'rows', 'roxy', 'rsvp', 'ruby', 'rude', 'rudy', 'rugs', 'ruin', 'rule', 'runs', 'rush', 'russ', 'rust', 'ruth', 'ryan', 'saab', 'sack', 'safe', 'saga', 'sage', 'said', 'sail', 'sake', 'sale', 'salt', 'same', 'sand', 'sane', 'sang', 'sans', 'sara', 'sars', 'sata', 'saul', 'save', 'saws', 'says', 'sbin', 'scam', 'scan', 'scar', 'scat', 'scsi', 'seal', 'seam', 'sean', 'seas', 'seat', 'secs', 'sect', 'seed', 'seek', 'seem', 'seen', 'sees', 'sega', 'self', 'sell', 'semi', 'send', 'sent', 'sept', 'serv', 'seth', 'sets', 'sexe', 'sexo', 'sexy', 'sgml', 'shah', 'shaw', 'shea', 'shed', 'shin', 'ship', 'shit', 'shoe', 'shop', 'shot', 'show', 'shui', 'shut', 'siam', 'sich', 'sick', 'side', 'sigh', 'sign', 'silk', 'sims', 'sind', 'sing', 'sink', 'sins', 'sion', 'sire', 'site', 'sith', 'sits', 'situ', 'size', 'skin', 'skip', 'skis', 'skye', 'slab', 'slac', 'slam', 'slap', 'slim', 'slip', 'slot', 'slow', 'slug', 'slut', 'smes', 'smtp', 'snap', 'snmp', 'snow', 'soak', 'soap', 'soar', 'sock', 'soda', 'sofa', 'soft', 'soho', 'soil', 'sold', 'sole', 'solo', 'soma', 'some', 'song', 'sons', 'sont', 'sony', 'soon', 'sore', 'sort', 'soul', 'soup', 'sour', 'spam', 'span', 'spas', 'spec', 'spin', 'spit', 'spot', 'spun', 'spur', 'sqrt', 'staa', 'stab', 'stag', 'stan', 'star', 'stat', 'stay', 'stem', 'step', 'stew', 'stir', 'stop', 'stub', 'stud', 'subs', 'such', 'suck', 'sued', 'suit', 'sums', 'sung', 'suns', 'suny', 'supp', 'sure', 'surf', 'suse', 'suvs', 'svcd', 'sven', 'swan', 'swap', 'swim', 'sync', 'tabs', 'tack', 'taco', 'tags', 'tail', 'take', 'tale', 'talk', 'tall', 'tang', 'tank', 'tape', 'taps', 'tara', 'task', 'tata', 'tate', 'taxi', 'teak', 'teal', 'team', 'tear', 'teas', 'tech', 'teen', 'tees', 'tele', 'tell', 'temp', 'tend', 'tens', 'tent', 'term', 'test', 'text', 'thai', 'than', 'that', 'thee', 'them', 'then', 'theo', 'ther', 'they', 'thin', 'this', 'thor', 'thou', 'thru', 'thug', 'thus', 'tick', 'tide', 'tidy', 'tied', 'tier', 'ties', 'tiff', 'tiki', 'tile', 'till', 'tilt', 'time', 'tina', 'tiny', 'tion', 'tips', 'tire', 'tits', 'tive', 'tivo', 'toby', 'todd', 'todo', 'toes', 'togo', 'told', 'toll', 'tomb', 'tome', 'tone', 'toni', 'tons', 'tony', 'took', 'tool', 'toon', 'tops', 'tori', 'torn', 'tort', 'tory', 'toss', 'tote', 'tour', 'tous', 'tout', 'town', 'toys', 'trac', 'tran', 'trap', 'tray', 'tree', 'trek', 'treo', 'tres', 'trim', 'trio', 'trip', 'troy', 'true', 'tube', 'tubs', 'tuck', 'tues', 'tuna', 'tune', 'turf', 'turn', 'twin', 'tyne', 'type', 'typo', 'tyre', 'uber', 'ucla', 'uefa', 'ugly', 'undo', 'undp', 'unit', 'univ', 'unix', 'unto', 'upon', 'upto', 'urge', 'urls', 'usda', 'used', 'user', 'uses', 'usgs', 'usps', 'ussr', 'utah', 'util', 'vail', 'vain', 'vaio', 'vale', 'vans', 'vary', 'vase', 'vast', 'vega', 'veil', 'vein', 'vent', 'vera', 'verb', 'very', 'vest', 'veto', 'vets', 'vibe', 'vice', 'vida', 'vids', 'viet', 'view', 'viii', 'vine', 'visa', 'vita', 'viva', 'vivo', 'vlan', 'void', 'voip', 'vols', 'volt', 'voor', 'vote', 'vous', 'vows', 'waco', 'wade', 'wage', 'wait', 'wake', 'walk', 'wall', 'walt', 'wand', 'wang', 'want', 'ward', 'ware', 'warm', 'warn', 'warp', 'wars', 'wash', 'watt', 'wave', 'ways', 'weak', 'wear', 'webb', 'webs', 'weed', 'week', 'weir', 'weld', 'well', 'went', 'were', 'west', 'what', 'when', 'whip', 'whom', 'wide', 'wien', 'wife', 'wifi', 'wigs', 'wiki', 'wild', 'will', 'wind', 'wine', 'wing', 'wink', 'wins', 'wipe', 'wire', 'wise', 'wish', 'with', 'wlan', 'wnba', 'woes', 'woke', 'wolf', 'wong', 'wont', 'wood', 'wool', 'word', 'wore', 'work', 'worm', 'worn', 'wrap', 'writ', 'wsop', 'wwii', 'xbox', 'xeon', 'xiii', 'xmas', 'xnxx', 'xslt', 'xvid', 'xxxx', 'yale', 'yang', 'yard', 'yarn', 'yeah', 'year', 'yell', 'ymca', 'yoga', 'york', 'your', 'yuan', 'yves', 'yyyy', 'zach', 'zero', 'zeta', 'ziff', 'zinc', 'zine', 'zion', 'zone', 'zoom', 'zope']

WORDS_5 = ['aaron', 'abbey', 'abdul', 'abide', 'about', 'above', 'abuse', 'acids', 'acorn', 'acres', 'acted', 'actor', 'acura', 'acute', 'adams', 'adapt', 'added', 'adler', 'admin', 'admit', 'adobe', 'adopt', 'adult', 'after', 'again', 'agent', 'agile', 'aging', 'agnes', 'agree', 'ahead', 'ahmad', 'ahmed', 'aided', 'aides', 'aimed', 'aired', 'aires', 'aisle', 'akron', 'alain', 'alamo', 'alarm', 'album', 'alert', 'alexa', 'algae', 'alias', 'alice', 'alien', 'align', 'alike', 'alito', 'alive', 'allah', 'allan', 'allen', 'alley', 'allow', 'alloy', 'aloha', 'alone', 'along', 'aloud', 'alpha', 'altar', 'alter', 'alton', 'alvin', 'amber', 'amend', 'amiga', 'amino', 'among', 'ample', 'andre', 'angel', 'anger', 'angie', 'angle', 'anglo', 'angry', 'angus', 'anime', 'anita', 'ankle', 'annex', 'annie', 'annum', 'anton', 'apart', 'apnic', 'apple', 'apply', 'april', 'apron', 'arabs', 'arbor', 'arden', 'areas', 'arena', 'argos', 'argue', 'argus', 'arial', 'ariel', 'aries', 'arise', 'armed', 'armor', 'aroma', 'arose', 'array', 'arrow', 'aruba', 'arxiv', 'ascii', 'asean', 'ashes', 'asian', 'aside', 'asked', 'aspen', 'assay', 'asses', 'asset', 'assoc', 'aston', 'astra', 'astro', 'atari', 'atlas', 'atoms', 'attic', 'audio', 'audit', 'autos', 'avail', 'avant', 'avaya', 'avery', 'avian', 'avoid', 'avril', 'await', 'awake', 'award', 'aware', 'awful', 'axial', 'babes', 'backs', 'bacon', 'badge', 'badly', 'baked', 'baker', 'balls', 'bands', 'banff', 'banjo', 'banks', 'baron', 'barre', 'barry', 'basal', 'based', 'basel', 'bases', 'basic', 'basil', 'basin', 'basis', 'batch', 'bates', 'baths', 'baton', 'bauer', 'bayer', 'beach', 'beads', 'beams', 'beans', 'beard', 'bears', 'beast', 'beats', 'becky', 'beech', 'beers', 'began', 'begin', 'begun', 'beige', 'being', 'bella', 'belle', 'bells', 'belly', 'below', 'belts', 'bench', 'benin', 'benny', 'berry', 'betsy', 'betty', 'bezel', 'bible', 'biker', 'bikes', 'bills', 'billy', 'binds', 'bingo', 'birch', 'birds', 'birth', 'bison', 'bitch', 'bites', 'black', 'blade', 'blair', 'blake', 'blame', 'blanc', 'bland', 'blank', 'blast', 'blaze', 'bleed', 'blend', 'bless', 'blind', 'bling', 'blink', 'bliss', 'blitz', 'block', 'blogs', 'blond', 'blood', 'bloom', 'blown', 'blows', 'blues', 'bluff', 'blunt', 'blush', 'board', 'boats', 'bobby', 'bogus', 'boing', 'boise', 'bolts', 'bombs', 'bonds', 'bones', 'bonus', 'boobs', 'books', 'boone', 'boost', 'booth', 'boots', 'booty', 'bored', 'boris', 'borne', 'bosch', 'bound', 'bowel', 'bowen', 'bowie', 'bowls', 'boxed', 'boxer', 'boxes', 'boyle', 'brace', 'brady', 'brain', 'brake', 'brand', 'brass', 'braun', 'brave', 'bravo', 'bread', 'break', 'breed', 'brent', 'brett', 'brian', 'brick', 'bride', 'brief', 'bring', 'broad', 'brock', 'broke', 'bronx', 'brook', 'brown', 'bruce', 'bruno', 'brush', 'bryan', 'bryce', 'bucks', 'buddy', 'buena', 'buffy', 'buggy', 'buick', 'build', 'built', 'bulbs', 'bulls', 'bunch', 'bunny', 'burke', 'burma', 'burns', 'burnt', 'burst', 'busch', 'buses', 'busty', 'butte', 'butts', 'buyer', 'byrne', 'byron', 'bytes', 'cabin', 'cable', 'cache', 'cadet', 'cafes', 'cages', 'cairo', 'cajun', 'cakes', 'calls', 'camel', 'camps', 'canal', 'candy', 'canoe', 'canon', 'capri', 'carat', 'carbs', 'cards', 'cared', 'cares', 'carey', 'cargo', 'carla', 'carlo', 'carol', 'carry', 'carte', 'carts', 'cases', 'casey', 'casio', 'casts', 'catch', 'cater', 'cathy', 'cause', 'caves', 'cdrom', 'cease', 'cecil', 'cedar', 'celeb', 'cello', 'cells', 'cents', 'cette', 'chain', 'chair', 'chalk', 'champ', 'chang', 'chaos', 'charm', 'chars', 'chart', 'chase', 'chats', 'cheap', 'cheat', 'check', 'cheek', 'cheer', 'chefs', 'cheng', 'chess', 'chest', 'chevy', 'chick', 'chico', 'chief', 'child', 'chile', 'chili', 'chill', 'china', 'ching', 'chips', 'chloe', 'choir', 'chord', 'chose', 'chris', 'chuck', 'chung', 'chunk', 'ciara', 'cider', 'cigar', 'cimel', 'cindy', 'circa', 'cisco', 'cited', 'cites', 'civic', 'civil', 'claim', 'clair', 'clamp', 'clara', 'clare', 'clark', 'clash', 'class', 'claus', 'clean', 'clear', 'clerk', 'click', 'cliff', 'climb', 'clint', 'clips', 'clive', 'clock', 'clone', 'close', 'cloth', 'cloud', 'clown', 'clubs', 'clues', 'clyde', 'coach', 'coast', 'coats', 'cobra', 'cocks', 'cocoa', 'cocos', 'codec', 'coded', 'codes', 'cohen', 'coins', 'colin', 'colon', 'color', 'colts', 'combo', 'comes', 'comet', 'comic', 'comma', 'conan', 'condo', 'congo', 'const', 'cooke', 'cooks', 'coral', 'corba', 'cords', 'corel', 'cores', 'corey', 'corps', 'costa', 'costs', 'couch', 'cough', 'could', 'count', 'coupe', 'court', 'cover', 'crack', 'craft', 'craig', 'crane', 'crank', 'craps', 'crash', 'crate', 'crawl', 'crazy', 'cream', 'creed', 'creek', 'creep', 'creme', 'crest', 'crete', 'crews', 'cried', 'cries', 'crime', 'crisp', 'croix', 'crops', 'cross', 'crowd', 'crown', 'crude', 'cruel', 'crush', 'crust', 'crypt', 'cuban', 'cubes', 'cubic', 'cured', 'curly', 'curry', 'curse', 'curve', 'cutie', 'cyber', 'cycle', 'cymru', 'cyrus', 'czech', 'daddy', 'daily', 'dairy', 'daisy', 'damon', 'dance', 'danny', 'dansk', 'dante', 'darby', 'darth', 'darts', 'dated', 'dates', 'datum', 'david', 'davis', 'deals', 'dealt', 'death', 'debit', 'debra', 'debts', 'debug', 'debut', 'decal', 'decay', 'decks', 'decor', 'deeds', 'deere', 'delay', 'delhi', 'della', 'delle', 'delta', 'demon', 'demos', 'demux', 'denim', 'denis', 'denny', 'denon', 'dense', 'depot', 'depth', 'derby', 'derek', 'desks', 'deter', 'detox', 'devel', 'devil', 'devon', 'dewey', 'dhtml', 'diana', 'diane', 'diary', 'dicke', 'dicks', 'didnt', 'diego', 'diets', 'diffs', 'diggs', 'digit', 'dildo', 'dinar', 'diner', 'diode', 'dirty', 'disco', 'discs', 'disks', 'ditch', 'diver', 'dixie', 'dixon', 'dodge', 'doing', 'dolby', 'dolce', 'dolls', 'dolly', 'donna', 'donor', 'doors', 'doris', 'doses', 'doubt', 'dough', 'dover', 'downs', 'doyle', 'dozen', 'draft', 'drain', 'drake', 'drama', 'drank', 'drawn', 'draws', 'dread', 'dream', 'dress', 'dried', 'drift', 'drill', 'drink', 'drive', 'drops', 'drove', 'drugs', 'drums', 'drunk', 'dryer', 'duane', 'dubai', 'ducks', 'dukes', 'dummy', 'dunes', 'dunno', 'dusty', 'dutch', 'dwarf', 'dwell', 'dying', 'dylan', 'dyson', 'eager', 'eagle', 'early', 'earns', 'earth', 'eaten', 'eater', 'eaton', 'ebony', 'ebook', 'ecard', 'econo', 'eddie', 'edgar', 'edges', 'edith', 'edits', 'edwin', 'egypt', 'eight', 'elbow', 'elder', 'elect', 'elena', 'elgin', 'eliot', 'elisa', 'elite', 'eliza', 'ellen', 'ellis', 'elton', 'elvis', 'emacs', 'email', 'emily', 'emory', 'empty', 'emule', 'ended', 'endif', 'enemy', 'enjoy', 'enron', 'enter', 'entre', 'entry', 'epoch', 'epoxy', 'epson', 'equal', 'equip', 'erase', 'erect', 'erica', 'ernie', 'ernst', 'error', 'essay', 'essex', 'ethan', 'ether', 'euros', 'evans', 'event', 'every', 'evite', 'exact', 'exams', 'excel', 'exile', 'exist', 'exits', 'expat', 'extra', 'ezine', 'fable', 'faced', 'faces', 'facts', 'faded', 'fails', 'faint', 'faire', 'fairs', 'fairy', 'faith', 'fakes', 'falls', 'false', 'fancy', 'fares', 'fargo', 'farms', 'faroe', 'fatal', 'fatty', 'fault', 'fauna', 'favor', 'faxes', 'fears', 'feast', 'fedex', 'feeds', 'feels', 'felix', 'femme', 'fence', 'ferry', 'fetal', 'fetch', 'fetus', 'fever', 'fewer', 'fgets', 'fiber', 'fibre', 'field', 'fiery', 'fifth', 'fifty', 'fight', 'filed', 'files', 'fills', 'filme', 'films', 'filth', 'final', 'finch', 'finds', 'fined', 'fines', 'fiona', 'fired', 'fires', 'firms', 'first', 'fixed', 'fixes', 'flags', 'flair', 'flame', 'flare', 'flash', 'flats', 'flaws', 'fleet', 'flesh', 'flick', 'flies', 'flint', 'flirt', 'float', 'flock', 'flood', 'floor', 'flora', 'flour', 'flown', 'flows', 'floyd', 'fluid', 'flush', 'flute', 'flyer', 'flynn', 'focal', 'focus', 'folds', 'foley', 'folio', 'folks', 'fomit', 'fonts', 'foods', 'fools', 'force', 'forex', 'forge', 'forks', 'forma', 'forms', 'forte', 'forth', 'forty', 'forum', 'fotos', 'found', 'frame', 'franc', 'frank', 'franz', 'fraud', 'fread', 'freak', 'freed', 'fresh', 'fried', 'fries', 'fritz', 'frogs', 'front', 'frost', 'fruit', 'fucks', 'fudge', 'fuels', 'fully', 'funds', 'fungi', 'funky', 'funny', 'furry', 'fuzzy', 'gabon', 'gains', 'gamer', 'games', 'gamma', 'gangs', 'garde', 'garth', 'gases', 'gates', 'gauge', 'gavin', 'gears', 'geeks', 'geile', 'genes', 'genie', 'genre', 'genus', 'geoff', 'georg', 'gerry', 'getty', 'ghana', 'ghost', 'giant', 'gibbs', 'gifts', 'giles', 'girls', 'given', 'gives', 'gland', 'glass', 'glenn', 'glibc', 'glide', 'globe', 'glory', 'gloss', 'glove', 'gmail', 'gnome', 'goals', 'goats', 'going', 'gomez', 'gonna', 'goods', 'goose', 'gorge', 'gotta', 'gould', 'gowns', 'grabs', 'grace', 'grade', 'grain', 'grams', 'grand', 'grant', 'grape', 'graph', 'grasp', 'grass', 'grave', 'great', 'greed', 'greek', 'green', 'greet', 'gregg', 'grief', 'grill', 'grind', 'grips', 'groom', 'gross', 'group', 'grove', 'grown', 'grows', 'guard', 'gucci', 'guess', 'guest', 'guide', 'guild', 'guilt', 'gupta', 'gypsy', 'habit', 'hacks', 'hague', 'hairy', 'haiti', 'halls', 'hamas', 'hands', 'handy', 'hangs', 'hanna', 'hanoi', 'happy', 'hardy', 'harry', 'harsh', 'hatch', 'hated', 'hates', 'haute', 'haven', 'havoc', 'hawks', 'hayes', 'hazel', 'heads', 'heard', 'hears', 'heart', 'heath', 'heavy', 'hedge', 'heels', 'heidi', 'heinz', 'helen', 'helix', 'hello', 'helps', 'hence', 'henri', 'henry', 'herbs', 'hertz', 'hicks', 'hides', 'highs', 'hills', 'hindi', 'hindu', 'hinge', 'hints', 'hipaa', 'hired', 'hires', 'hitch', 'hobbs', 'hobby', 'hogan', 'holds', 'holes', 'holly', 'homer', 'homes', 'homme', 'honda', 'honey', 'honor', 'hoods', 'hooks', 'hoops', 'hoped', 'hopes', 'horde', 'horns', 'horny', 'horse', 'hosts', 'hotel', 'hound', 'hours', 'house', 'howto', 'httpd', 'https', 'huang', 'human', 'humor', 'hunks', 'huron', 'hurry', 'hurts', 'husky', 'hyatt', 'hydro', 'hyper', 'ibiza', 'ibook', 'icann', 'icons', 'idaho', 'ideal', 'ideas', 'idiot', 'ifdef', 'image', 'imply', 'inbox', 'incur', 'index', 'india', 'indie', 'infos', 'inlet', 'inlog', 'inner', 'input', 'intel', 'inter', 'intra', 'intro', 'ionic', 'ipods', 'ipsec', 'iraqi', 'irene', 'irish', 'irons', 'irony', 'irwin', 'isaac', 'islam', 'isles', 'issue', 'isuzu', 'italy', 'items', 'ivory', 'jacks', 'jacob', 'james', 'jamie', 'janet', 'janis', 'japan', 'jared', 'jason', 'jboss', 'jeans', 'jelly', 'jenna', 'jenny', 'jerry', 'jesse', 'jesus', 'jewel', 'jihad', 'jimmy', 'johan', 'johns', 'joins', 'joint', 'jokes', 'jolie', 'jolla', 'jolly', 'jonah', 'jonas', 'jones', 'jorge', 'josef', 'joyce', 'judge', 'juice', 'juicy', 'jules', 'julia', 'julie', 'julio', 'jumbo', 'jumps', 'kanye', 'kappa', 'karen', 'karma', 'kathy', 'katie', 'kauai', 'kayak', 'kazaa', 'keeps', 'keith', 'kelly', 'kenny', 'kenya', 'kerry', 'kevin', 'kicks', 'kills', 'kinda', 'kinds', 'kings', 'kinky', 'kiosk', 'kirby', 'kitts', 'kitty', 'klaus', 'klein', 'knees', 'knife', 'knobs', 'knock', 'knots', 'known', 'knows', 'kodak', 'korea', 'kraft', 'kuala', 'kudoz', 'kumar', 'kylie', 'kyoto', 'label', 'labor', 'lacks', 'laden', 'lakes', 'lamar', 'lamps', 'lance', 'lands', 'lanes', 'lange', 'lanka', 'large', 'largo', 'larry', 'laser', 'lasik', 'lasts', 'latch', 'later', 'latex', 'latin', 'laugh', 'laura', 'layer', 'layup', 'leads', 'leaks', 'learn', 'lease', 'least', 'leave', 'leeds', 'legal', 'leica', 'leigh', 'lemma', 'lemon', 'lenny', 'lenox', 'leone', 'leroy', 'lesbo', 'level', 'lever', 'levin', 'lewis', 'lexar', 'lexus', 'libby', 'libya', 'liens', 'lifts', 'light', 'liked', 'likes', 'lilac', 'lilly', 'limbs', 'limit', 'linda', 'lined', 'linen', 'liner', 'lines', 'links', 'linus', 'linux', 'lions', 'lipid', 'lists', 'liter', 'litre', 'lived', 'liver', 'lives', 'lloyd', 'loads', 'loans', 'lobby', 'local', 'locke', 'locks', 'locus', 'lodge', 'logan', 'logic', 'login', 'logon', 'logos', 'lohan', 'looks', 'loops', 'loose', 'lopez', 'lords', 'loren', 'loser', 'loses', 'lotto', 'lotus', 'louis', 'loved', 'lover', 'loves', 'lower', 'loyal', 'lucas', 'lucia', 'lucky', 'lunar', 'lunch', 'lungs', 'luton', 'lycos', 'lydia', 'lying', 'lymph', 'lynch', 'lynne', 'lyons', 'lyric', 'macau', 'macon', 'macos', 'macro', 'madam', 'mafia', 'magic', 'magna', 'mails', 'maine', 'mains', 'maize', 'major', 'maker', 'makes', 'malay', 'males', 'malls', 'malta', 'mambo', 'mandy', 'manga', 'mango', 'mania', 'manor', 'maori', 'maple', 'march', 'marco', 'mardi', 'maria', 'marie', 'marin', 'mario', 'marks', 'marry', 'marsh', 'marty', 'masks', 'mason', 'match', 'mateo', 'mates', 'maths', 'matte', 'maven', 'maxim', 'maybe', 'mayen', 'mayer', 'mayor', 'mazda', 'mccoy', 'mcgee', 'meade', 'meals', 'means', 'meant', 'meats', 'medal', 'media', 'meets', 'megan', 'ments', 'menus', 'merck', 'mercy', 'merge', 'merit', 'merry', 'messy', 'metal', 'meter', 'metre', 'metro', 'meyer', 'miami', 'micah', 'micro', 'midst', 'might', 'mikes', 'milan', 'miles', 'milfs', 'mills', 'minds', 'miner', 'mines', 'minor', 'minus', 'missy', 'misty', 'mitch', 'mixed', 'mixer', 'mixes', 'mobil', 'modal', 'model', 'modem', 'modes', 'moist', 'molly', 'momma', 'mommy', 'monde', 'mondo', 'money', 'monks', 'monte', 'month', 'monty', 'moody', 'moore', 'moose', 'moral', 'moran', 'morse', 'moses', 'motel', 'motif', 'motor', 'motto', 'mound', 'mount', 'mouse', 'mouth', 'moved', 'mover', 'moves', 'movie', 'mpegs', 'msgid', 'msnbc', 'muddy', 'multi', 'mummy', 'mundo', 'music', 'musik', 'myers', 'mysql', 'myths', 'nails', 'naive', 'naked', 'named', 'names', 'nancy', 'nanny', 'naomi', 'nasal', 'nasty', 'natal', 'nauru', 'naval', 'nazis', 'needs', 'needy', 'negro', 'nelly', 'nepal', 'nerve', 'never', 'nevis', 'newer', 'newly', 'nexus', 'niche', 'nicht', 'nifty', 'nigel', 'niger', 'night', 'nikki', 'nikon', 'ninja', 'ninth', 'nitro', 'nixon', 'nobel', 'noble', 'nodes', 'noise', 'noisy', 'nokia', 'nolan', 'norma', 'norms', 'north', 'notch', 'noted', 'notes', 'notre', 'novel', 'nudes', 'nuevo', 'nurse', 'nylon', 'oasis', 'obese', 'occur', 'ocean', 'octet', 'offer', 'often', 'ogden', 'older', 'olive', 'olsen', 'olson', 'omaha', 'omega', 'onion', 'onset', 'opens', 'opera', 'oprah', 'opted', 'optic', 'orbit', 'order', 'organ', 'orion', 'ortho', 'osaka', 'osama', 'oscar', 'other', 'otter', 'ought', 'ounce', 'outer', 'ovens', 'owens', 'owing', 'owned', 'owner', 'oxide', 'oxley', 'ozone', 'pablo', 'paced', 'packs', 'paddy', 'pagan', 'pager', 'pages', 'paige', 'pains', 'paint', 'pairs', 'palau', 'palma', 'palms', 'panda', 'panel', 'panic', 'pants', 'panty', 'paolo', 'paper', 'papua', 'param', 'paris', 'parks', 'parse', 'parts', 'party', 'pasta', 'paste', 'patch', 'paths', 'patio', 'patti', 'patty', 'paula', 'paulo', 'pause', 'paved', 'paxil', 'payne', 'peace', 'peach', 'peaks', 'pearl', 'pedal', 'pedro', 'peers', 'peggy', 'penis', 'penny', 'pepsi', 'percy', 'perez', 'perry', 'perth', 'pesos', 'pests', 'peter', 'petit', 'petty', 'pgsql', 'phase', 'phone', 'photo', 'phpbb', 'piano', 'picks', 'piece', 'piles', 'pills', 'pilot', 'pinch', 'pines', 'piper', 'pipes', 'pitch', 'pivot', 'pixar', 'pixel', 'pizza', 'place', 'plaid', 'plain', 'plane', 'plano', 'plans', 'plant', 'plate', 'plato', 'playa', 'plays', 'plaza', 'plone', 'plots', 'plugs', 'plump', 'plush', 'pluto', 'poems', 'poets', 'point', 'poker', 'polar', 'poles', 'polls', 'polly', 'ponds', 'poole', 'pools', 'poppy', 'popup', 'porch', 'porno', 'porto', 'ports', 'posed', 'poses', 'posix', 'posts', 'pouch', 'pound', 'power', 'prada', 'pratt', 'press', 'price', 'pride', 'prima', 'prime', 'print', 'prior', 'prism', 'prize', 'probe', 'promo', 'prone', 'proof', 'props', 'prose', 'proto', 'proud', 'prove', 'proxy', 'prweb', 'psalm', 'puffy', 'pulls', 'pulse', 'pumps', 'punch', 'punta', 'pupil', 'puppy', 'purse', 'pussy', 'putin', 'qaeda', 'qatar', 'quake', 'quark', 'quart', 'quasi', 'queen', 'queer', 'query', 'quest', 'queue', 'quick', 'quiet', 'quilt', 'quinn', 'quite', 'quota', 'quote', 'qwest', 'rabbi', 'racer', 'races', 'racks', 'radar', 'radio', 'rails', 'rains', 'rainy', 'raise', 'rally', 'ralph', 'ramon', 'ramps', 'ranch', 'randy', 'range', 'ranks', 'rants', 'raped', 'rapid', 'rated', 'rates', 'ratio', 'raton', 'raven', 'razor', 'reach', 'react', 'reads', 'ready', 'realm', 'rebel', 'recap', 'recon', 'reels', 'reese', 'refer', 'regal', 'reged', 'regis', 'rehab', 'reich', 'reign', 'reiki', 'reits', 'relax', 'relay', 'remix', 'renal', 'renee', 'renew', 'rents', 'repay', 'repec', 'reply', 'reset', 'resin', 'rests', 'retro', 'reuse', 'reyes', 'rhino', 'rhode', 'rican', 'ricky', 'ricoh', 'rider', 'rides', 'ridge', 'rifle', 'right', 'rigid', 'riley', 'rings', 'rinse', 'risen', 'rises', 'risks', 'risky', 'rival', 'river', 'roach', 'roads', 'roast', 'robin', 'robot', 'roche', 'rocks', 'rocky', 'rodeo', 'roger', 'rogue', 'roles', 'rolex', 'rolls', 'roman', 'romeo', 'rooms', 'roots', 'ropes', 'rosen', 'roses', 'rosie', 'rossi', 'rotor', 'rouge', 'rough', 'round', 'route', 'rover', 'rowan', 'royal', 'royce', 'rubin', 'rugby', 'ruins', 'ruled', 'ruler', 'rules', 'rumor', 'rupee', 'rural', 'rusty', 'ryder', 'sacks', 'sadly', 'safer', 'sagem', 'saint', 'sakai', 'salad', 'salem', 'sales', 'sally', 'salon', 'salsa', 'salts', 'samba', 'sammy', 'samoa', 'sands', 'sandy', 'santa', 'santo', 'sanyo', 'sarah', 'sassy', 'satan', 'satin', 'sauce', 'saudi', 'sauna', 'saved', 'saver', 'saves', 'savvy', 'saxon', 'sbjct', 'scale', 'scams', 'scans', 'scare', 'scarf', 'scars', 'scary', 'scene', 'scent', 'scion', 'scoop', 'scope', 'score', 'scots', 'scott', 'scout', 'scrap', 'screw', 'scrub', 'scuba', 'sdram', 'seals', 'sears', 'seats', 'secsg', 'sedan', 'seeds', 'seeks', 'seems', 'seiko', 'seite', 'seize', 'sells', 'sendo', 'sends', 'sense', 'seoul', 'serie', 'serif', 'serum', 'serve', 'sesso', 'setup', 'seven', 'sewer', 'sexes', 'shack', 'shade', 'shady', 'shaft', 'shake', 'shall', 'shalt', 'shame', 'shane', 'shape', 'share', 'shark', 'sharp', 'shaun', 'shave', 'shawn', 'shear', 'sheds', 'sheep', 'sheer', 'sheet', 'shelf', 'shell', 'shift', 'shine', 'shiny', 'ships', 'shire', 'shirt', 'shock', 'shoes', 'shook', 'shoot', 'shops', 'shore', 'short', 'shots', 'shout', 'shown', 'shows', 'shrek', 'sided', 'sides', 'siege', 'siena', 'sight', 'sigma', 'signs', 'silky', 'silly', 'silva', 'simon', 'since', 'singh', 'sings', 'sinks', 'sinus', 'sioux', 'sites', 'sixth', 'sixty', 'sized', 'sizes', 'skate', 'skies', 'skill', 'skins', 'skirt', 'skull', 'skype', 'slack', 'slang', 'slash', 'slate', 'slave', 'sleek', 'sleep', 'slept', 'slice', 'slick', 'slide', 'sling', 'slips', 'sloan', 'slope', 'slots', 'sluts', 'small', 'smart', 'smash', 'smell', 'smile', 'smith', 'smoke', 'smoky', 'snack', 'snake', 'sneak', 'snoop', 'snowy', 'soaps', 'sober', 'sobre', 'socio', 'socks', 'sofas', 'sofia', 'soils', 'solar', 'solid', 'solve', 'songs', 'sonia', 'sonic', 'sonny', 'sorry', 'sorts', 'souls', 'sound', 'soups', 'south', 'space', 'spain', 'spank', 'spans', 'sparc', 'spare', 'spark', 'spawn', 'speak', 'spear', 'specs', 'speed', 'spell', 'spend', 'spent', 'sperm', 'spice', 'spicy', 'spies', 'spike', 'spill', 'spine', 'spite', 'split', 'spoke', 'spoon', 'sport', 'spots', 'spray', 'spurs', 'squad', 'squid', 'stack', 'stacy', 'staff', 'stage', 'stain', 'stair', 'stake', 'stall', 'stamp', 'stand', 'stare', 'stark', 'starr', 'stars', 'start', 'state', 'stats', 'stays', 'steak', 'steal', 'steam', 'steel', 'steep', 'steer', 'stein', 'stems', 'steps', 'stern', 'steve', 'stick', 'stiff', 'still', 'sting', 'stock', 'stoke', 'stole', 'stone', 'stony', 'stood', 'stool', 'stops', 'store', 'storm', 'story', 'stout', 'stove', 'strap', 'straw', 'stray', 'strip', 'stuck', 'studs', 'study', 'stuff', 'stunt', 'style', 'suche', 'sucks', 'sudan', 'suede', 'sugar', 'suite', 'suits', 'sunny', 'super', 'suppl', 'supra', 'surge', 'susan', 'sushi', 'susie', 'swamp', 'swear', 'sweat', 'sweep', 'sweet', 'swell', 'swept', 'swift', 'swing', 'swiss', 'sword', 'sworn', 'synth', 'syria', 'syrup', 'table', 'taboo', 'tahoe', 'tails', 'taken', 'takes', 'tales', 'talks', 'tally', 'tamil', 'tammy', 'tampa', 'tango', 'tanks', 'tanya', 'tapes', 'tarot', 'tasks', 'taste', 'tasty', 'taxes', 'taxis', 'teach', 'teams', 'tears', 'tease', 'techs', 'teddy', 'teens', 'teeth', 'tells', 'tempe', 'tempo', 'temps', 'tends', 'tenor', 'tense', 'tenth', 'tents', 'terms', 'terra', 'terre', 'terri', 'terry', 'tesco', 'tests', 'texas', 'texts', 'thank', 'thanx', 'thats', 'theft', 'their', 'theme', 'there', 'these', 'theta', 'thick', 'thief', 'thigh', 'thing', 'think', 'third', 'thong', 'those', 'three', 'threw', 'throw', 'thumb', 'thurs', 'tiava', 'tibet', 'tidal', 'tides', 'tiger', 'tight', 'tiles', 'timed', 'timer', 'times', 'timor', 'tions', 'tired', 'tires', 'titan', 'title', 'titus', 'toast', 'today', 'todos', 'token', 'tokyo', 'tommy', 'toner', 'tones', 'tonga', 'tools', 'toons', 'tooth', 'topaz', 'topic', 'topps', 'torah', 'torch', 'torso', 'total', 'touch', 'tough', 'tours', 'towel', 'tower', 'towns', 'toxic', 'trace', 'track', 'tract', 'tracy', 'trade', 'trail', 'train', 'trait', 'trans', 'traps', 'trash', 'trays', 'tread', 'treat', 'trees', 'trend', 'trent', 'trial', 'tribe', 'trick', 'tried', 'tries', 'trina', 'trips', 'trish', 'troll', 'trong', 'troop', 'trout', 'truck', 'truly', 'trump', 'trunk', 'trust', 'truth', 'tubes', 'tulip', 'tulsa', 'tummy', 'tumor', 'tuned', 'tuner', 'tunes', 'turbo', 'turin', 'turks', 'turns', 'tutor', 'twain', 'tweak', 'tweed', 'twice', 'twiki', 'twink', 'twins', 'twist', 'tying', 'tyler', 'typed', 'types', 'tyres', 'tyson', 'ultra', 'uncle', 'uncut', 'undef', 'under', 'union', 'unite', 'units', 'unity', 'until', 'upper', 'upset', 'urban', 'urged', 'urges', 'urine', 'usage', 'usaid', 'users', 'usher', 'using', 'usual', 'utils', 'utter', 'vague', 'valet', 'valid', 'value', 'valve', 'vance', 'vapor', 'vases', 'vault', 'vdata', 'vegan', 'vegas', 'veins', 'venom', 'venue', 'venus', 'verbs', 'verde', 'versa', 'verse', 'vests', 'vicki', 'video', 'views', 'villa', 'ville', 'vince', 'vinci', 'vines', 'vinyl', 'viola', 'vioxx', 'viper', 'viral', 'virus', 'visas', 'visit', 'visor', 'vista', 'vitae', 'vital', 'vitro', 'vivid', 'vocal', 'vodka', 'vogue', 'voice', 'volts', 'volvo', 'voted', 'voter', 'votes', 'voyer', 'vsnet', 'wacky', 'wages', 'wagon', 'waist', 'waits', 'waive', 'wales', 'walks', 'walls', 'walsh', 'waltz', 'wanna', 'wants', 'wards', 'warez', 'warns', 'waste', 'watch', 'water', 'watts', 'waves', 'wayne', 'wears', 'weary', 'weave', 'weber', 'webmd', 'wedge', 'weeds', 'weeks', 'weigh', 'weird', 'weiss', 'welch', 'wells', 'welsh', 'wendy', 'whale', 'wharf', 'whats', 'wheat', 'wheel', 'where', 'which', 'while', 'white', 'whois', 'whole', 'whore', 'whose', 'wider', 'widow', 'width', 'wigan', 'wight', 'wilde', 'wiley', 'wills', 'willy', 'winds', 'windy', 'wines', 'wings', 'winme', 'winnt', 'winxp', 'wired', 'wires', 'witch', 'witty', 'wives', 'wolfe', 'woman', 'women', 'woods', 'woody', 'words', 'works', 'world', 'worms', 'worry', 'worse', 'worst', 'worth', 'would', 'wound', 'woven', 'wraps', 'wrath', 'wreck', 'wrist', 'write', 'wrong', 'wrote', 'wyatt', 'xanax', 'xerox', 'xhtml', 'xlibs', 'xoops', 'yacht', 'yahoo', 'yards', 'yates', 'years', 'yeast', 'yemen', 'yield', 'young', 'yours', 'youth', 'yukon', 'yummy', 'zaire', 'zdnet', 'zebra', 'zelda', 'zhang', 'zones', 'zyban']
WORDS_6 = ['abbott', 'aboard', 'abroad', 'absent', 'absorb', 'absurd', 'abused', 'abuses', 'accent', 'accept', 'access', 'accord', 'across', 'acting', 'action', 'active', 'actors', 'actual', 'acxiom', 'addict', 'adding', 'adhere', 'adidas', 'adipex', 'adjust', 'admins', 'admire', 'admits', 'adrian', 'adults', 'advent', 'advert', 'advice', 'advise', 'adware', 'aerial', 'affair', 'affect', 'affirm', 'afford', 'afghan', 'afraid', 'africa', 'ageing', 'agency', 'agenda', 'agents', 'agreed', 'agrees', 'aiming', 'alarms', 'alaska', 'albany', 'albeit', 'albert', 'albion', 'albums', 'alerts', 'alexis', 'alfred', 'alicia', 'aliens', 'alison', 'allied', 'allies', 'allows', 'alloys', 'almond', 'almost', 'alpine', 'alumni', 'always', 'amanda', 'amazed', 'amazon', 'ambien', 'amelia', 'amount', 'analog', 'anchor', 'andale', 'anders', 'andrea', 'andrew', 'anemia', 'angela', 'angelo', 'angels', 'angles', 'angola', 'animal', 'annals', 'annual', 'answer', 'anthem', 'antony', 'anyone', 'anyway', 'apache', 'apollo', 'appeal', 'appear', 'append', 'apples', 'applet', 'approx', 'arabia', 'arabic', 'arafat', 'arcade', 'archer', 'arctic', 'argued', 'argues', 'arises', 'armada', 'armani', 'armies', 'armour', 'arnold', 'around', 'arrays', 'arrest', 'arrive', 'arrows', 'artery', 'arthur', 'artist', 'ashlee', 'ashley', 'ashton', 'asians', 'asking', 'asleep', 'aspect', 'aspire', 'assays', 'assert', 'assess', 'assets', 'assign', 'assist', 'assume', 'assure', 'asthma', 'astros', 'asylum', 'athena', 'athens', 'athlon', 'ativan', 'atkins', 'atomic', 'atreyu', 'attach', 'attack', 'attain', 'attend', 'auburn', 'audits', 'audrey', 'august', 'aurora', 'aussie', 'austin', 'author', 'autism', 'autumn', 'avalon', 'avatar', 'avenue', 'avoids', 'awards', 'awhile', 'babies', 'backed', 'backup', 'badger', 'badges', 'bailey', 'bakery', 'baking', 'ballad', 'ballet', 'ballot', 'baltic', 'bamboo', 'banana', 'bangor', 'banker', 'banned', 'banner', 'barber', 'barbie', 'barely', 'barker', 'barley', 'barnes', 'barney', 'barred', 'barrel', 'barrie', 'barron', 'barrow', 'barton', 'basics', 'basins', 'basket', 'basque', 'batman', 'batter', 'battle', 'baxter', 'baylor', 'bazaar', 'beacon', 'beaded', 'beanie', 'beasts', 'beaten', 'beauty', 'beaver', 'became', 'becker', 'become', 'beetle', 'before', 'begins', 'behalf', 'behave', 'behind', 'behold', 'beings', 'beirut', 'belief', 'belize', 'belkin', 'belong', 'bender', 'bengal', 'benign', 'benson', 'benton', 'bergen', 'berger', 'berlin', 'bernie', 'beside', 'bethel', 'better', 'beware', 'beyond', 'bhutan', 'biased', 'bibles', 'bibtex', 'bidder', 'bigger', 'biking', 'bikini', 'bilder', 'billed', 'billie', 'biloxi', 'binary', 'binder', 'biopsy', 'births', 'bishop', 'bissau', 'bistro', 'biting', 'bitmap', 'bitter', 'bizkit', 'blacks', 'blades', 'blamed', 'blanca', 'blanco', 'blanks', 'blazer', 'blends', 'blinds', 'blocks', 'blonde', 'bloody', 'blooms', 'blower', 'boards', 'boasts', 'bodies', 'bodily', 'boeing', 'boiled', 'boiler', 'bolton', 'bombay', 'bomber', 'bonded', 'bonnie', 'bonsai', 'boogie', 'booked', 'border', 'boring', 'borrow', 'bosnia', 'bosses', 'boston', 'botany', 'bother', 'bottle', 'bottom', 'bought', 'bounce', 'bounds', 'bounty', 'bouvet', 'bovine', 'bowman', 'boxing', 'braces', 'brains', 'brakes', 'branch', 'brands', 'brandy', 'brasil', 'braves', 'brazil', 'breach', 'breaks', 'breast', 'breath', 'breeds', 'breeze', 'bremen', 'brenda', 'brewer', 'bricks', 'bridal', 'brides', 'bridge', 'briefs', 'briggs', 'bright', 'brings', 'broken', 'broker', 'bronze', 'brooke', 'brooks', 'browne', 'browns', 'browse', 'bruins', 'brunch', 'brunei', 'brutal', 'bryant', 'bubble', 'bucket', 'buckle', 'buddha', 'budget', 'buenos', 'buffer', 'buffet', 'bufing', 'builds', 'bullet', 'bumper', 'bundle', 'bunker', 'burden', 'bureau', 'burger', 'burial', 'buried', 'burned', 'burner', 'burton', 'busted', 'buster', 'butler', 'butter', 'button', 'buyers', 'buying', 'bylaws', 'bypass', 'cabins', 'cables', 'cached', 'cactus', 'caesar', 'caicos', 'cairns', 'called', 'caller', 'calvin', 'camaro', 'camden', 'camera', 'camino', 'camper', 'campus', 'canada', 'canary', 'cancel', 'cancer', 'cancun', 'candid', 'candle', 'canine', 'canned', 'cannes', 'cannon', 'canopy', 'canton', 'canvas', 'canyon', 'capita', 'capped', 'carbon', 'cardio', 'career', 'carers', 'caring', 'carlos', 'carmel', 'carmen', 'carole', 'carpet', 'carrie', 'carrot', 'carson', 'carter', 'carton', 'carved', 'carver', 'casino', 'casper', 'castle', 'castro', 'casual', 'cation', 'cattle', 'caucus', 'caught', 'causal', 'caused', 'causes', 'cavity', 'cayman', 'ceased', 'celebs', 'celexa', 'celine', 'cellar', 'celtic', 'cement', 'census', 'center', 'centre', 'centro', 'cereal', 'chains', 'chairs', 'chalet', 'champs', 'chance', 'chanel', 'change', 'chapel', 'charge', 'charms', 'charts', 'chaser', 'chavez', 'cheats', 'checks', 'cheeks', 'cheers', 'cheese', 'cheney', 'cheque', 'cherry', 'cheryl', 'chiang', 'chicks', 'chiefs', 'childs', 'choice', 'choose', 'choral', 'chords', 'chorus', 'chosen', 'christ', 'chrome', 'chubby', 'church', 'cialis', 'cigars', 'cinema', 'circle', 'circus', 'cities', 'citing', 'citrix', 'citrus', 'claims', 'claire', 'clamps', 'clancy', 'clarke', 'classy', 'claude', 'clause', 'clears', 'clergy', 'clerks', 'clever', 'clicks', 'client', 'cliffs', 'climax', 'clinic', 'clocks', 'clones', 'closed', 'closer', 'closes', 'closet', 'clouds', 'cloudy', 'clover', 'clutch', 'coarse', 'coated', 'cobalt', 'coding', 'coffee', 'coffin', 'cohort', 'collar', 'colony', 'colors', 'colour', 'column', 'combat', 'comedy', 'comics', 'coming', 'commit', 'common', 'compaq', 'comply', 'condom', 'condos', 'config', 'connie', 'connor', 'conrad', 'constr', 'contra', 'convex', 'convey', 'conway', 'cooked', 'cooker', 'cookie', 'cooled', 'cooler', 'cooper', 'copied', 'copier', 'copies', 'coping', 'copper', 'corner', 'corona', 'corpse', 'corpus', 'cortex', 'cosmic', 'cosmos', 'costly', 'cotton', 'counts', 'county', 'couple', 'coupon', 'course', 'courts', 'cousin', 'covers', 'covert', 'coward', 'cowboy', 'coyote', 'cracks', 'cradle', 'crafts', 'cramer', 'crater', 'creamy', 'create', 'credit', 'creepy', 'creole', 'crimes', 'crises', 'crisis', 'critic', 'crosby', 'crosse', 'crowds', 'crowne', 'cruise', 'crunch', 'crying', 'crypto', 'cursed', 'cursor', 'curtis', 'curved', 'curves', 'custom', 'cutter', 'cycles', 'cyclic', 'cygwin', 'cyprus', 'daemon', 'daewoo', 'dakota', 'dallas', 'dalton', 'damage', 'damien', 'damned', 'dancer', 'dances', 'danger', 'daniel', 'danish', 'darfur', 'daring', 'darker', 'darren', 'darwin', 'dashed', 'dating', 'davies', 'dawson', 'dayton', 'deadly', 'dealer', 'deaths', 'debate', 'debbie', 'debian', 'debris', 'debtor', 'decade', 'decals', 'decent', 'decide', 'decker', 'decree', 'deemed', 'deeper', 'deeply', 'defeat', 'defect', 'defend', 'define', 'degree', 'delays', 'delete', 'delphi', 'deluxe', 'demand', 'demons', 'denial', 'denied', 'denies', 'denise', 'dennis', 'denote', 'dental', 'denton', 'denver', 'depart', 'depend', 'deploy', 'depths', 'deputy', 'derive', 'desert', 'design', 'desire', 'detail', 'detect', 'device', 'devils', 'dewalt', 'dexter', 'diablo', 'dialog', 'dialup', 'diaper', 'didrex', 'diesel', 'differ', 'digest', 'digits', 'dildos', 'dillon', 'dimage', 'diners', 'dining', 'dinner', 'direct', 'dishes', 'disney', 'divers', 'divide', 'divine', 'diving', 'docket', 'doctor', 'docume', 'doesnt', 'dollar', 'domain', 'domino', 'donald', 'donate', 'donkey', 'donors', 'doomed', 'dooyoo', 'dorado', 'dorset', 'dosage', 'dotted', 'double', 'doubts', 'dozens', 'drafts', 'dragon', 'dramas', 'draper', 'drawer', 'dreams', 'dreamy', 'drills', 'drinks', 'driven', 'driver', 'drives', 'drupal', 'dryers', 'drying', 'dubbed', 'dublin', 'dudley', 'duluth', 'dumped', 'duncan', 'dundee', 'dunlop', 'duplex', 'dupont', 'durban', 'durham', 'during', 'dustin', 'duties', 'dwight', 'eagles', 'earned', 'easier', 'easily', 'easter', 'easton', 'eating', 'ebooks', 'ecards', 'echoes', 'edible', 'edison', 'edited', 'editor', 'edmund', 'edward', 'effect', 'effort', 'eighth', 'eighty', 'eileen', 'either', 'elaine', 'elders', 'eleven', 'elijah', 'elliot', 'emails', 'emblem', 'embryo', 'emerge', 'eminem', 'empire', 'employ', 'enable', 'enamel', 'encode', 'encore', 'ending', 'endure', 'energy', 'engage', 'engine', 'enjoys', 'enough', 'enroll', 'ensure', 'enters', 'entire', 'entity', 'enzyme', 'equals', 'equine', 'equity', 'ernest', 'erotic', 'erotik', 'errors', 'escape', 'escort', 'escrow', 'essays', 'estate', 'esteem', 'esther', 'ethics', 'ethnic', 'eugene', 'eureka', 'europa', 'europe', 'evelyn', 'evenly', 'events', 'evolve', 'exceed', 'except', 'excess', 'excise', 'excite', 'excuse', 'exempt', 'exeter', 'exists', 'exodus', 'exotic', 'expand', 'expasy', 'expect', 'expert', 'expire', 'expiry', 'export', 'expose', 'extend', 'extent', 'extern', 'extras', 'fabric', 'facial', 'facing', 'factor', 'fading', 'failed', 'fairly', 'falcon', 'fallen', 'family', 'famous', 'faqfaq', 'farmer', 'faster', 'father', 'faucet', 'faults', 'faulty', 'favors', 'favour', 'feared', 'fedora', 'feeder', 'fellow', 'felony', 'female', 'femdom', 'fences', 'fender', 'ferris', 'fetish', 'fibers', 'fiddle', 'fields', 'fierce', 'fiesta', 'fights', 'figure', 'filing', 'filled', 'filler', 'filmed', 'filter', 'filthy', 'finale', 'finals', 'finder', 'finely', 'finest', 'finger', 'finish', 'finite', 'firing', 'firmly', 'fiscal', 'fisher', 'fishes', 'fitted', 'fixing', 'flames', 'flavor', 'flawed', 'fleece', 'flickr', 'flight', 'floods', 'floors', 'floppy', 'floral', 'flores', 'flower', 'fluffy', 'fluids', 'flyers', 'flying', 'folded', 'folder', 'follow', 'footer', 'forbes', 'forced', 'forces', 'forest', 'forged', 'forget', 'forgot', 'formal', 'format', 'formed', 'former', 'forums', 'fossil', 'foster', 'fought', 'fourth', 'fowler', 'framed', 'frames', 'france', 'franco', 'francs', 'fraser', 'frauen', 'freaks', 'freely', 'freeze', 'french', 'frenzy', 'fresno', 'friday', 'fridge', 'friend', 'fringe', 'fronts', 'frozen', 'fruits', 'fucked', 'fuckin', 'fulfil', 'fuller', 'fulton', 'funded', 'fungal', 'fusion', 'futuna', 'future', 'gadget', 'gaelic', 'gagged', 'gained', 'galaxy', 'gallon', 'galore', 'galway', 'gambia', 'gamble', 'gamers', 'gaming', 'gandhi', 'garage', 'garcia', 'garden', 'garlic', 'garmin', 'garner', 'garnet', 'gasket', 'gather', 'gauges', 'geared', 'geisha', 'gemini', 'gender', 'geneva', 'genius', 'genome', 'genres', 'gentle', 'gently', 'gentoo', 'george', 'gerald', 'gerard', 'german', 'ghetto', 'ghosts', 'giants', 'gibson', 'giclee', 'gifted', 'ginger', 'giving', 'gladly', 'glance', 'glazed', 'global', 'globes', 'gloria', 'glossy', 'gloves', 'goblet', 'golden', 'google', 'gordon', 'gospel', 'gossip', 'gothic', 'gotten', 'govern', 'graded', 'grades', 'graham', 'grains', 'grande', 'grange', 'granny', 'grants', 'grapes', 'graphs', 'gratis', 'gravel', 'graves', 'grease', 'greece', 'greedy', 'greeks', 'greene', 'greens', 'grille', 'grills', 'groove', 'groovy', 'ground', 'groups', 'grower', 'growth', 'guards', 'guests', 'guiana', 'guided', 'guides', 'guilty', 'guinea', 'guitar', 'gundam', 'guyana', 'habits', 'hacked', 'hacker', 'haired', 'hamlet', 'hammer', 'handed', 'handel', 'handle', 'hanger', 'hannah', 'hansen', 'hanson', 'happen', 'harbor', 'harder', 'hardly', 'harlem', 'harley', 'harman', 'harold', 'harper', 'harris', 'harvey', 'hasbro', 'hassle', 'hatred', 'havana', 'having', 'hawaii', 'hayden', 'haynes', 'hazard', 'headed', 'header', 'health', 'hearts', 'heated', 'heater', 'heaven', 'hebrew', 'hector', 'height', 'helena', 'helium', 'helmet', 'helped', 'helper', 'hentai', 'herald', 'herbal', 'hereby', 'herein', 'herman', 'heroes', 'heroic', 'heroin', 'herpes', 'hewitt', 'hidden', 'hiding', 'higher', 'highly', 'hiking', 'hilary', 'hilton', 'hinges', 'hiring', 'hitler', 'hobart', 'hockey', 'holdem', 'holden', 'holder', 'hollow', 'holmes', 'honest', 'honors', 'honour', 'hooded', 'hoodia', 'hoodie', 'hooked', 'hooker', 'hoover', 'hoping', 'hopper', 'horror', 'horses', 'horton', 'hosted', 'hostel', 'hotels', 'hottie', 'hourly', 'housed', 'houses', 'howard', 'howell', 'htdocs', 'hudson', 'hughes', 'humane', 'humans', 'humble', 'hummer', 'humour', 'hunger', 'hungry', 'hunter', 'hurley', 'hustle', 'hybrid', 'ideals', 'idiots', 'ignore', 'images', 'immune', 'impact', 'import', 'impose', 'incest', 'inches', 'income', 'indeed', 'indian', 'indies', 'indigo', 'indoor', 'induce', 'infant', 'infect', 'inform', 'ingram', 'injury', 'inkjet', 'inland', 'inline', 'inmate', 'inning', 'inputs', 'insane', 'insect', 'insert', 'insest', 'inside', 'insist', 'insult', 'insure', 'intact', 'intake', 'intend', 'intent', 'intern', 'invest', 'invite', 'invoke', 'inward', 'iomega', 'iraqis', 'iriver', 'ironic', 'irvine', 'irving', 'isabel', 'isaiah', 'island', 'israel', 'issued', 'issuer', 'issues', 'italia', 'italic', 'ithaca', 'itself', 'itunes', 'ivoire', 'jabber', 'jacket', 'jackie', 'jacobs', 'jaguar', 'janice', 'jargon', 'jarvis', 'jasper', 'jeanne', 'jeeves', 'jensen', 'jeremy', 'jerome', 'jersey', 'jessie', 'jewels', 'jewish', 'jigsaw', 'jingle', 'joanna', 'joanne', 'jockey', 'johann', 'johnny', 'joined', 'joints', 'joomla', 'joplin', 'jordan', 'joseph', 'joshua', 'judged', 'judges', 'judith', 'juices', 'julian', 'juliet', 'julius', 'jumped', 'jumper', 'jungle', 'junior', 'justin', 'kaiser', 'kansas', 'kaplan', 'karate', 'kbytes', 'keeper', 'kelkoo', 'keller', 'kelley', 'kennel', 'kerala', 'kernel', 'kettle', 'keygen', 'keynes', 'keypad', 'kicked', 'kidney', 'kijiji', 'killed', 'killer', 'kinase', 'kindly', 'kissed', 'kisses', 'kitten', 'knight', 'knives', 'konica', 'korean', 'kosher', 'kosovo', 'kramer', 'kruger', 'kuwait', 'labels', 'labour', 'lacked', 'ladder', 'ladies', 'lagoon', 'laguna', 'lakers', 'lambda', 'landed', 'laptop', 'larger', 'larsen', 'larson', 'larvae', 'lasers', 'lasted', 'lastly', 'lately', 'latent', 'latest', 'latina', 'latino', 'latter', 'latvia', 'laughs', 'launch', 'laurel', 'lauren', 'laurie', 'lawful', 'lawson', 'lawyer', 'layers', 'laying', 'layout', 'leader', 'league', 'learns', 'learnt', 'leased', 'leases', 'leaves', 'ledger', 'legacy', 'legend', 'legion', 'lehigh', 'lender', 'length', 'lennon', 'lenses', 'lesbos', 'leslie', 'lesser', 'lesson', 'lester', 'lethal', 'letras', 'letter', 'levels', 'levine', 'liable', 'libyan', 'lifted', 'ligand', 'lights', 'likely', 'liking', 'lilies', 'limits', 'linden', 'linear', 'linens', 'liners', 'lineup', 'lining', 'linked', 'linker', 'linkin', 'lionel', 'liquid', 'liquor', 'lisbon', 'listed', 'listen', 'lister', 'litres', 'litter', 'little', 'lively', 'living', 'lizard', 'loaded', 'loader', 'locale', 'locals', 'locate', 'locked', 'locker', 'lodged', 'lodges', 'logged', 'logger', 'logout', 'lolita', 'london', 'lonely', 'longer', 'looked', 'lookup', 'lortab', 'losers', 'losing', 'losses', 'lotion', 'louise', 'lounge', 'lovely', 'lovers', 'loving', 'lowell', 'lowest', 'loyola', 'lucent', 'ludwig', 'lumber', 'lumpur', 'luther', 'luxury', 'lyrics', 'mackay', 'macros', 'madame', 'madden', 'madrid', 'maggie', 'magnet', 'magnum', 'maiden', 'mailed', 'mailer', 'mailto', 'mainly', 'majors', 'makers', 'makeup', 'making', 'malaga', 'malawi', 'malibu', 'malone', 'manage', 'manila', 'manner', 'manson', 'mantle', 'manual', 'manuel', 'manure', 'mapped', 'marble', 'marcel', 'marcia', 'marcos', 'marcus', 'margin', 'mariah', 'marian', 'marina', 'marine', 'marino', 'marion', 'marked', 'marker', 'market', 'markup', 'markus', 'marley', 'marlin', 'maroon', 'marrow', 'martha', 'martin', 'marvel', 'marvin', 'masses', 'massey', 'master', 'mating', 'matlab', 'matrix', 'matter', 'mature', 'maxtor', 'mayhem', 'mcafee', 'mccain', 'mcgill', 'mcgraw', 'mclean', 'meadow', 'medals', 'median', 'medina', 'medium', 'medley', 'meetup', 'mellon', 'melody', 'melted', 'melvin', 'member', 'memoir', 'memory', 'menace', 'mental', 'mentor', 'mercer', 'merely', 'merged', 'merger', 'merits', 'merlin', 'metals', 'meters', 'method', 'methyl', 'metres', 'metric', 'mexico', 'michel', 'mickey', 'micron', 'middle', 'middot', 'midget', 'midway', 'mighty', 'miguel', 'milano', 'miller', 'milton', 'minded', 'miners', 'mining', 'minnie', 'minors', 'minute', 'mirage', 'miriam', 'mirror', 'misery', 'missed', 'misses', 'mister', 'misuse', 'mixers', 'mixing', 'mobile', 'models', 'modems', 'modern', 'modest', 'modify', 'module', 'moines', 'molded', 'moment', 'monaco', 'monday', 'monica', 'monies', 'monkey', 'monroe', 'months', 'morale', 'morgan', 'mormon', 'morris', 'morrow', 'mortal', 'mortar', 'morton', 'mosaic', 'moscow', 'mosque', 'mostly', 'motels', 'mother', 'motion', 'motive', 'motley', 'motors', 'mounts', 'movers', 'movies', 'moving', 'mozart', 'msgstr', 'muller', 'mumbai', 'munich', 'murder', 'murphy', 'murray', 'muscle', 'museum', 'musica', 'muslim', 'mutant', 'mutual', 'myriad', 'myrtle', 'myself', 'mystic', 'nabble', 'namely', 'naming', 'naples', 'narnia', 'narrow', 'nascar', 'nasdaq', 'nassau', 'nathan', 'nation', 'native', 'nature', 'nausea', 'navajo', 'nearby', 'nearly', 'needed', 'needle', 'nelson', 'nephew', 'nerves', 'nested', 'netbsd', 'neural', 'nevada', 'newark', 'newbie', 'newest', 'newman', 'newton', 'nextag', 'nextel', 'nguyen', 'nicely', 'nickel', 'nicole', 'nights', 'ninety', 'nipple', 'nissan', 'nobody', 'nodded', 'nordic', 'normal', 'norman', 'norris', 'nortel', 'norton', 'norway', 'notice', 'notify', 'noting', 'notion', 'novell', 'novels', 'novice', 'nozzle', 'nuclei', 'nudist', 'nudity', 'number', 'nurses', 'nutten', 'nvidia', 'nylons', 'oakley', 'object', 'obtain', 'occult', 'occupy', 'occurs', 'oceans', 'octave', 'odessa', 'offers', 'office', 'offset', 'oldest', 'oldham', 'oldies', 'oliver', 'olivia', 'onions', 'online', 'onsite', 'opaque', 'opened', 'opener', 'opengl', 'openid', 'openly', 'oppose', 'optics', 'option', 'oracle', 'orange', 'orbitz', 'orchid', 'orders', 'oregon', 'organs', 'orgasm', 'orgies', 'orient', 'origin', 'orphan', 'others', 'ottawa', 'ounces', 'outfit', 'outing', 'outlaw', 'outlet', 'output', 'overly', 'owners', 'owning', 'oxford', 'oxygen', 'oyster', 'packed', 'packet', 'padded', 'paddle', 'padres', 'pagina', 'paging', 'paints', 'paired', 'palace', 'pallet', 'palmer', 'pamela', 'panama', 'panels', 'pantie', 'papers', 'parade', 'parcel', 'pardon', 'parent', 'parfum', 'parish', 'parity', 'parked', 'parker', 'parody', 'parole', 'parrot', 'parser', 'partly', 'pascal', 'passed', 'passes', 'pastel', 'pastor', 'pastry', 'patent', 'patrol', 'patron', 'patton', 'paving', 'payday', 'paying', 'payout', 'paypal', 'pcmcia', 'peanut', 'pearce', 'pearls', 'pedals', 'peeing', 'pencil', 'pentax', 'people', 'peoria', 'pepper', 'period', 'permit', 'persia', 'person', 'peters', 'petite', 'petrol', 'pewter', 'pfizer', 'pharma', 'phases', 'phelps', 'philip', 'philly', 'phones', 'photon', 'photos', 'phrase', 'phuket', 'piazza', 'picked', 'pickup', 'picnic', 'pieces', 'pierce', 'pierre', 'pigeon', 'pillar', 'pillow', 'pilots', 'piping', 'piracy', 'pirate', 'pissed', 'pistol', 'piston', 'pixels', 'placed', 'places', 'plague', 'plains', 'planar', 'planes', 'planet', 'plants', 'plaque', 'plasma', 'plated', 'plates', 'played', 'player', 'please', 'pledge', 'plenty', 'plugin', 'plunge', 'plural', 'pocket', 'poetic', 'poetry', 'pointe', 'points', 'poised', 'poison', 'poland', 'police', 'policy', 'polish', 'polite', 'pollen', 'polski', 'poorly', 'popped', 'portal', 'porter', 'posing', 'postal', 'posted', 'poster', 'potato', 'potent', 'potter', 'pounds', 'poured', 'powder', 'powell', 'powers', 'prague', 'praise', 'prayer', 'prefer', 'prefix', 'preset', 'pretty', 'priced', 'prices', 'priest', 'primer', 'prince', 'printf', 'prints', 'prison', 'privat', 'prizes', 'probes', 'profit', 'prompt', 'proofs', 'proper', 'proton', 'proved', 'proven', 'proves', 'prozac', 'psalms', 'pseudo', 'psycho', 'public', 'pubmed', 'pueblo', 'puerto', 'pulled', 'pulses', 'pumped', 'pundit', 'punish', 'punjab', 'pupils', 'puppet', 'purdue', 'purely', 'purity', 'purple', 'purses', 'pursue', 'pushed', 'pushes', 'putnam', 'puzzle', 'python', 'quarry', 'quartz', 'quebec', 'queens', 'quilts', 'quincy', 'quinta', 'quorum', 'quoted', 'quotes', 'rabbit', 'rachel', 'racial', 'racing', 'racism', 'racist', 'radeon', 'radial', 'radios', 'radius', 'rafael', 'raging', 'raider', 'raised', 'raises', 'ramada', 'ramsey', 'rancho', 'random', 'ranged', 'ranger', 'ranges', 'ranked', 'rapids', 'rarely', 'rather', 'rating', 'ratios', 'ravens', 'reader', 'readme', 'reagan', 'really', 'realms', 'realty', 'reason', 'rebate', 'rebels', 'reboot', 'recall', 'recent', 'recess', 'recipe', 'record', 'rectal', 'redeem', 'redhat', 'reduce', 'reebok', 'reeves', 'refers', 'refill', 'refine', 'reflex', 'reform', 'refuge', 'refund', 'refuse', 'regain', 'regard', 'regent', 'reggae', 'regime', 'regina', 'region', 'regret', 'reilly', 'reject', 'relate', 'relays', 'relied', 'relief', 'relies', 'reload', 'remain', 'remake', 'remark', 'remedy', 'remind', 'remote', 'remove', 'rename', 'render', 'rental', 'rented', 'repair', 'repeal', 'repeat', 'replay', 'report', 'resale', 'rescue', 'resets', 'reside', 'resign', 'resist', 'resize', 'resort', 'result', 'resume', 'retail', 'retain', 'retire', 'return', 'reveal', 'review', 'revise', 'revolt', 'reward', 'rhodes', 'rhymes', 'rhythm', 'ribbon', 'richer', 'riches', 'richie', 'riddle', 'riders', 'riding', 'rifles', 'rights', 'ringer', 'ripley', 'ripped', 'ripper', 'rising', 'ritual', 'rivals', 'rivera', 'rivers', 'robbie', 'robert', 'robots', 'robust', 'rocker', 'rocket', 'rockin', 'rodney', 'rogers', 'roland', 'rolled', 'roller', 'romans', 'ronald', 'ronnie', 'rookie', 'rooted', 'roster', 'rotary', 'rotate', 'rotten', 'rounds', 'routed', 'router', 'routes', 'rowing', 'royale', 'royals', 'rubber', 'rugged', 'ruined', 'rulers', 'ruling', 'rumble', 'rumors', 'runner', 'runoff', 'runway', 'rupert', 'rushed', 'russia', 'rustic', 'rwanda', 'sacred', 'saddam', 'saddle', 'safari', 'safely', 'safety', 'sahara', 'sailor', 'saints', 'salads', 'salary', 'saline', 'salmon', 'salons', 'saloon', 'salute', 'sample', 'samson', 'samuel', 'sandal', 'sander', 'sandra', 'sanity', 'santos', 'satire', 'saturn', 'sauces', 'savage', 'savers', 'saving', 'savior', 'sawyer', 'saying', 'scalar', 'scaled', 'scales', 'scarce', 'scared', 'scenes', 'scenic', 'schema', 'scheme', 'school', 'scooby', 'scopes', 'scored', 'scores', 'scotch', 'scotia', 'scouts', 'scraps', 'scream', 'screen', 'screws', 'script', 'scroll', 'sealed', 'search', 'season', 'seated', 'second', 'secret', 'sector', 'secure', 'sedona', 'seeing', 'seeker', 'seemed', 'seized', 'seldom', 'select', 'seller', 'senate', 'sender', 'seneca', 'senior', 'senses', 'sensor', 'septic', 'sequel', 'serbia', 'serena', 'sergio', 'serial', 'series', 'sermon', 'served', 'server', 'serves', 'sesame', 'settle', 'severe', 'sewage', 'sewing', 'sexcam', 'sexual', 'shaded', 'shades', 'shadow', 'shaker', 'shakes', 'shania', 'shaped', 'shapes', 'shared', 'shares', 'sharks', 'sharon', 'shaved', 'sheets', 'sheikh', 'sheila', 'shelby', 'shells', 'sherry', 'shield', 'shifts', 'shines', 'shirts', 'shocks', 'shoots', 'shoppe', 'shoppy', 'shores', 'shorts', 'should', 'shouts', 'showed', 'shower', 'shrimp', 'shrine', 'shrink', 'shrubs', 'sicily', 'siding', 'sidney', 'sierra', 'sights', 'signal', 'signed', 'signup', 'silent', 'silica', 'silver', 'simone', 'simple', 'simply', 'singer', 'single', 'sirius', 'sister', 'sizeof', 'sizing', 'skates', 'sketch', 'skiing', 'skills', 'skinny', 'skirts', 'slater', 'slaves', 'slayer', 'sleeps', 'sleepy', 'sleeve', 'sliced', 'slices', 'slider', 'slides', 'slight', 'slogan', 'slopes', 'slovak', 'slowed', 'slower', 'slowly', 'sludge', 'smells', 'smiled', 'smiles', 'smiley', 'smoked', 'smoker', 'smooth', 'snacks', 'snakes', 'snatch', 'sniper', 'snyder', 'soccer', 'social', 'socket', 'sodium', 'softly', 'solder', 'soleil', 'solely', 'solids', 'solved', 'sonata', 'sonoma', 'sooner', 'sophia', 'sophie', 'sorrow', 'sorted', 'sought', 'sounds', 'source', 'soviet', 'spaced', 'spaces', 'spades', 'spares', 'sparks', 'sparse', 'speaks', 'spears', 'speech', 'speeds', 'speedy', 'spells', 'spends', 'sphere', 'spices', 'spider', 'spikes', 'spinal', 'spiral', 'spires', 'spirit', 'splash', 'splits', 'spoken', 'sponge', 'sports', 'spouse', 'spread', 'spring', 'sprint', 'spruce', 'spying', 'square', 'squash', 'squirt', 'stable', 'stacey', 'stacks', 'staged', 'stages', 'staind', 'stains', 'stairs', 'stakes', 'stalls', 'stamps', 'stance', 'stands', 'staple', 'starch', 'stared', 'starts', 'stated', 'staten', 'states', 'static', 'statue', 'status', 'stayed', 'stderr', 'steady', 'steaks', 'steals', 'steele', 'stefan', 'stella', 'stereo', 'steven', 'stevie', 'sticks', 'sticky', 'stills', 'stitch', 'stocks', 'stokes', 'stolen', 'stones', 'stools', 'stored', 'stores', 'storey', 'storms', 'stoves', 'strain', 'strait', 'strand', 'straps', 'streak', 'stream', 'street', 'stress', 'strict', 'strike', 'string', 'stripe', 'strips', 'strive', 'stroke', 'stroll', 'strong', 'struck', 'struct', 'struts', 'stuart', 'studio', 'stupid', 'sturdy', 'styled', 'styles', 'stylus', 'subaru', 'submit', 'subset', 'subtle', 'suburb', 'subway', 'sucked', 'sudden', 'sudoku', 'suffer', 'suffix', 'suited', 'suites', 'sulfur', 'summer', 'summit', 'sunday', 'sunset', 'superb', 'supper', 'supply', 'surely', 'surfer', 'surrey', 'survey', 'sussex', 'sutton', 'suzuki', 'sweden', 'sweets', 'swings', 'switch', 'swivel', 'swords', 'sybase', 'sydney', 'sylvia', 'symbol', 'syntax', 'syrian', 'system', 'tables', 'tablet', 'tackle', 'tacoma', 'tactic', 'tagged', 'tahiti', 'tailed', 'tailor', 'taipei', 'taiwan', 'taking', 'talbot', 'talent', 'talked', 'tandem', 'tanned', 'tanner', 'tapped', 'target', 'targus', 'tariff', 'tastes', 'tattoo', 'taught', 'taurus', 'tavern', 'tawnee', 'taylor', 'teamed', 'techno', 'tehran', 'teller', 'telnet', 'temper', 'temple', 'tenant', 'tended', 'tender', 'tennis', 'tenure', 'teresa', 'termed', 'terror', 'tested', 'tester', 'tetris', 'texans', 'thames', 'thanks', 'thehun', 'theirs', 'themed', 'themes', 'thence', 'theory', 'theres', 'theses', 'thesis', 'thighs', 'things', 'thinks', 'thirds', 'thirty', 'thomas', 'thongs', 'though', 'thread', 'threat', 'thrice', 'thrill', 'thrive', 'throat', 'throne', 'thrown', 'throws', 'thrust', 'thumbs', 'ticker', 'ticket', 'tigers', 'tights', 'timber', 'timely', 'timers', 'timing', 'tional', 'tissue', 'titans', 'titled', 'titles', 'titten', 'tivoli', 'tobago', 'todays', 'toggle', 'toilet', 'tokens', 'toledo', 'tomato', 'tomcat', 'tomtom', 'tongue', 'tonnes', 'topeka', 'topics', 'topped', 'torino', 'torque', 'torres', 'tossed', 'totals', 'toward', 'towels', 'towers', 'towing', 'toxins', 'toyota', 'traced', 'traces', 'tracey', 'tracks', 'traded', 'trader', 'trades', 'tragic', 'trails', 'trains', 'traits', 'trance', 'tranny', 'trauma', 'travel', 'travis', 'treats', 'treaty', 'trembl', 'trench', 'trends', 'trendy', 'trevor', 'trials', 'tribal', 'tribes', 'tricks', 'tricky', 'triple', 'tripod', 'trivia', 'trojan', 'troops', 'trophy', 'trucks', 'truman', 'truste', 'trusts', 'truths', 'trying', 'tubing', 'tucker', 'tucson', 'tumble', 'tumors', 'tuners', 'tuning', 'tunnel', 'turkey', 'turned', 'turner', 'turtle', 'tutors', 'tuvalu', 'twelve', 'twenty', 'twinks', 'tycoon', 'typing', 'ubuntu', 'uganda', 'ulster', 'ultima', 'ultram', 'unable', 'unesco', 'unfair', 'unicef', 'unions', 'unique', 'unisex', 'united', 'unless', 'unlike', 'unlock', 'unpaid', 'unread', 'unreal', 'unsafe', 'unseen', 'unsure', 'unused', 'unwrap', 'update', 'upload', 'upside', 'uptake', 'uptime', 'uptown', 'upward', 'urbana', 'urgent', 'urging', 'usable', 'useful', 'usenet', 'utmost', 'utopia', 'vacant', 'vacuum', 'vagina', 'valium', 'valley', 'valued', 'values', 'valves', 'vanity', 'varied', 'varies', 'vaughn', 'vaults', 'vector', 'velcro', 'velvet', 'vendor', 'venice', 'venues', 'verbal', 'verify', 'verlag', 'vernon', 'verona', 'verses', 'versus', 'vertex', 'vessel', 'vested', 'vgroup', 'viable', 'viagra', 'victim', 'victor', 'videos', 'vienna', 'viewed', 'viewer', 'viking', 'villas', 'violet', 'violin', 'virgin', 'virtue', 'vision', 'visits', 'visual', 'vivian', 'vocals', 'voices', 'volume', 'vonage', 'voodoo', 'vortex', 'voters', 'voting', 'voyage', 'voyeur', 'voyuer', 'wagner', 'waited', 'waived', 'waiver', 'waking', 'walden', 'walked', 'walker', 'wallet', 'wallis', 'walnut', 'walter', 'walton', 'wander', 'wanted', 'warmer', 'warmth', 'warned', 'warner', 'warren', 'warsaw', 'washed', 'washer', 'wasted', 'wastes', 'waters', 'watson', 'weaker', 'wealth', 'weapon', 'weaver', 'webcam', 'weblog', 'webmin', 'weekly', 'weezer', 'weighs', 'weight', 'werner', 'wesley', 'westin', 'weston', 'whales', 'wheels', 'whilst', 'whisky', 'whites', 'wholly', 'whores', 'wicked', 'wicker', 'widely', 'widest', 'widget', 'wilcox', 'wilder', 'wilkes', 'willie', 'willis', 'willow', 'wilson', 'wilton', 'winamp', 'window', 'winery', 'winged', 'winner', 'winnie', 'winter', 'wiring', 'wisdom', 'wisely', 'wished', 'wishes', 'within', 'wizard', 'wolves', 'womens', 'wonder', 'wooden', 'worked', 'worker', 'worlds', 'worthy', 'wounds', 'wrench', 'wretch', 'wright', 'writer', 'writes', 'xavier', 'xemacs', 'xpress', 'xtreme', 'yachts', 'yakima', 'yamaha', 'yankee', 'yearly', 'yellow', 'yields', 'yogurt', 'yorker', 'youths', 'zambia', 'zenith', 'zipper', 'zodiac', 'zoloft', 'zombie', 'zoning', 'zshops', 'zurich']

def generate_brute_prefixes(min_len, max_len, charset, exclude_chars=""):
    valid_chars = [c for c in charset if c not in exclude_chars]
    prefixes = []
    for length in range(min_len, max_len + 1):
        for combo in itertools.product(valid_chars, repeat=length):
            prefixes.append("".join(combo))
    return prefixes

def generate_pattern_prefixes(pattern_str):
    mapping = {
        'C': "bcdfghjklmnpqrstvwxyz",
        'V': "aeiou",
        'L': string.ascii_lowercase,
        'N': string.digits
    }
    pools = []
    for char in pattern_str.upper():
        if char in mapping:
            pools.append(mapping[char])
        else:
            pools.append(char)
            
    prefixes = []
    for combo in itertools.product(*pools):
        prefixes.append("".join(combo))
    return prefixes

def generate_domains(prefixes, tlds):
    for tld in tlds:
        for prefix in prefixes:
            yield f"{prefix}.{tld}"

def generate_hacks(words, tlds):
    for word in words:
        for tld in tlds:
            if word.endswith(tld) and len(word) > len(tld):
                prefix = word[:-len(tld)]
                yield f"{prefix}.{tld}"

class GeneratorThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(int, str)
    error = pyqtSignal(str)

    def __init__(self, mode, min_len, max_len, charset, exclude, custom_words, pattern_str, tlds, batch_size, out_dir, lang="zh"):
        super().__init__()
        self.mode = mode
        self.min_len = min_len
        self.max_len = max_len
        self.charset = charset
        self.exclude = exclude
        self.custom_words = custom_words
        self.pattern_str = pattern_str
        self.tlds = tlds
        self.batch_size = batch_size
        self.out_dir = out_dir
        self.lang = lang

    def run(self):
        try:
            t = TRANSLATIONS[self.lang]
            if not os.path.exists(self.out_dir):
                os.makedirs(self.out_dir)

            self.progress.emit(t["msg_gen_combo"])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if self.mode == "hacks":
                words = []
                words.extend(WORDS_2 + WORDS_3 + WORDS_4 + WORDS_5 + WORDS_6)
                if self.custom_words:
                    cw_list = [w.strip().lower() for w in self.custom_words.split(',') if w.strip()]
                    words.extend(cw_list)
                words = list(set(words))
                domain_gen = generate_hacks(words, self.tlds)
                
            else:
                prefixes = []
                if self.mode == "brute":
                    prefixes = generate_brute_prefixes(self.min_len, self.max_len, self.charset, self.exclude)
                elif self.mode == "words":
                    if self.min_len <= 2 <= self.max_len:
                        prefixes.extend(WORDS_2)
                    if self.min_len <= 3 <= self.max_len:
                        prefixes.extend(WORDS_3)
                    if self.min_len <= 4 <= self.max_len:
                        prefixes.extend(WORDS_4)
                    if self.min_len <= 5 <= self.max_len:
                        prefixes.extend(WORDS_5)
                    if self.min_len <= 6 <= self.max_len:
                        prefixes.extend(WORDS_6)
                    
                    if self.custom_words:
                        cw_list = [w.strip().lower() for w in self.custom_words.split(',') if w.strip()]
                        prefixes.extend(cw_list)
                        
                    prefixes = list(set(prefixes))
                    if not prefixes:
                        self.error.emit(t["err_no_words"])
                        return
                elif self.mode == "pattern":
                    prefixes = generate_pattern_prefixes(self.pattern_str)
                    if not prefixes:
                        self.error.emit(t["err_pattern_empty"])
                        return
                
                self.progress.emit(t["msg_gen_prefix"].format(len(prefixes)))
                domain_gen = generate_domains(prefixes, self.tlds)

            batch = []
            file_index = 1
            total_generated = 0

            for domain in domain_gen:
                batch.append(domain)
                if len(batch) >= self.batch_size:
                    self._write_batch(batch, file_index, self.out_dir, timestamp)
                    total_generated += len(batch)
                    batch = []
                    file_index += 1
                    self.progress.emit(t["msg_gen_count"].format(total_generated))

            if batch:
                self._write_batch(batch, file_index, self.out_dir, timestamp)
                total_generated += len(batch)

            self.finished.emit(total_generated, self.out_dir)

        except Exception as e:
            self.error.emit(str(e))

    def _write_batch(self, batch, file_index, output_dir, timestamp):
        filename = os.path.join(output_dir, f"domains_{timestamp}_part_{file_index}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            for domain in batch:
                f.write(f"{domain},\n")

class DomainGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = "zh"
        self.setWindowTitle(TRANSLATIONS[self.lang]["title"])
        self.resize(750, 650)

        QApplication.instance().setStyle("Fusion")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dcdde1;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #00a8ff;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0097e6;
            }
            QPushButton:pressed {
                background-color: #0086d3;
            }
            QLineEdit, QSpinBox {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
            QTabWidget::pane {
                border: 1px solid #dcdde1;
                border-radius: 4px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f6fa;
                border: 1px solid #dcdde1;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
                font-weight: bold;
            }
        """)


        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Top layout for language switch
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.btn_lang = QPushButton(TRANSLATIONS[self.lang]["btn_lang"])
        self.btn_lang.clicked.connect(self.toggle_language)
        top_layout.addWidget(self.btn_lang)
        main_layout.addLayout(top_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.init_mode_tab()
        self.init_tld_tab()
        self.init_output_tab()

        # Status & Generate (Global at bottom)
        bottom_layout = QVBoxLayout()
        self.status_label = QLabel(TRANSLATIONS[self.lang]["status_ready"])
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        bottom_layout.addWidget(self.status_label)

        self.btn_generate = QPushButton(TRANSLATIONS[self.lang]["btn_generate"])
        self.btn_generate.setMinimumHeight(40)
        self.btn_generate.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.btn_generate.clicked.connect(self.start_generation)
        bottom_layout.addWidget(self.btn_generate)
        
        # Copyright
        self.copyright_label = QLabel(TRANSLATIONS[self.lang]["copyright"])
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setStyleSheet("color: gray; font-size: 12px; margin-top: 10px;")
        bottom_layout.addWidget(self.copyright_label)

        main_layout.addLayout(bottom_layout)
        self.update_ui_language()

    def toggle_language(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self.update_ui_language()

    def update_ui_language(self):
        t = TRANSLATIONS[self.lang]
        self.setWindowTitle(t["title"])
        self.btn_lang.setText(t["btn_lang"])
        
        self.tabs.setTabText(0, t["tab_mode"])
        self.tabs.setTabText(1, t["tab_tld"])
        self.tabs.setTabText(2, t["tab_output"])
        
        self.mode_group.setTitle(t["group_mode"])
        self.radio_brute.setText(t["radio_brute"])
        self.radio_words.setText(t["radio_words"])
        self.radio_pattern.setText(t["radio_pattern"])
        self.radio_hacks.setText(t["radio_hacks"])
        
        self.lbl_brute_min.setText(t["brute_min"])
        self.lbl_brute_max.setText(t["brute_max"])
        self.lbl_brute_charset.setText(t["brute_charset"])
        self.lbl_brute_exclude.setText(t["brute_exclude"])
        self.cb_lowercase.setText(t["cb_lower"])
        self.cb_numbers.setText(t["cb_num"])
        self.exclude_edit.setPlaceholderText(t["exclude_ph"])
        
        self.lbl_words_len.setText(t["words_len"])
        self.lbl_words_to.setText(t["words_to"])
        self.lbl_words_custom.setText(t["words_custom"])
        self.custom_words_edit.setPlaceholderText(t["words_custom_ph"])
        
        self.lbl_pattern.setText(t["pattern_label"])
        self.pattern_edit.setPlaceholderText(t["pattern_ph"])
        self.lbl_pattern_ex.setText(t["pattern_ex"])
        
        self.lbl_hacks.setText(t["hacks_label"])
        self.lbl_hacks_desc.setText(t["hacks_desc"])
        self.hacks_custom_edit.setPlaceholderText(t["hacks_ph"])
        
        self.lbl_tld_len.setText(t["tld_len_label"])
        self.btn_len2.setText(t["btn_len2"])
        self.btn_len3.setText(t["btn_len3"])
        self.btn_len4.setText(t["btn_len4"])
        self.lbl_tld_cat.setText(t["tld_cat_label"])
        self.btn_clear_all.setText(t["btn_clear_all"])
        
        for btn, cat in self.cat_buttons:
            btn.setText(f"+ {cat}")
            
        self.group_output.setTitle(t["group_output"])
        self.lbl_batch.setText(t["batch_label"])
        self.lbl_out_dir.setText(t["out_dir_label"])
        self.btn_browse.setText(t["btn_browse"])
        
        self.btn_generate.setText(t["btn_generate"])
        self.copyright_label.setText(t["copyright"])
        if self.btn_generate.isEnabled():
            self.status_label.setText(t["status_ready"])

    def init_mode_tab(self):
        mode_tab = QWidget()
        layout = QVBoxLayout(mode_tab)

        self.mode_group = QGroupBox()
        mode_h_layout = QHBoxLayout()
        
        self.radio_brute = QRadioButton()
        self.radio_words = QRadioButton()
        self.radio_pattern = QRadioButton()
        self.radio_hacks = QRadioButton()
        
        self.radio_brute.setChecked(True)
        
        self.mode_btn_group = QButtonGroup()
        self.mode_btn_group.addButton(self.radio_brute, 0)
        self.mode_btn_group.addButton(self.radio_words, 1)
        self.mode_btn_group.addButton(self.radio_pattern, 2)
        self.mode_btn_group.addButton(self.radio_hacks, 3)
        
        mode_h_layout.addWidget(self.radio_brute)
        mode_h_layout.addWidget(self.radio_words)
        mode_h_layout.addWidget(self.radio_pattern)
        mode_h_layout.addWidget(self.radio_hacks)
        self.mode_group.setLayout(mode_h_layout)
        layout.addWidget(self.mode_group)

        self.settings_stack = QStackedWidget()
        
        # 1. Brute Settings
        brute_widget = QWidget()
        brute_layout = QGridLayout(brute_widget)
        self.lbl_brute_min = QLabel()
        brute_layout.addWidget(self.lbl_brute_min, 0, 0)
        self.brute_min_spin = QSpinBox()
        self.brute_min_spin.setRange(1, 20)
        self.brute_min_spin.setValue(1)
        brute_layout.addWidget(self.brute_min_spin, 0, 1)
        
        self.lbl_brute_max = QLabel()
        brute_layout.addWidget(self.lbl_brute_max, 1, 0)
        self.brute_max_spin = QSpinBox()
        self.brute_max_spin.setRange(1, 20)
        self.brute_max_spin.setValue(2)
        brute_layout.addWidget(self.brute_max_spin, 1, 1)
        
        self.lbl_brute_charset = QLabel()
        brute_layout.addWidget(self.lbl_brute_charset, 2, 0)
        charset_layout = QHBoxLayout()
        self.cb_lowercase = QCheckBox()
        self.cb_lowercase.setChecked(True)
        self.cb_numbers = QCheckBox()
        self.cb_numbers.setChecked(True)
        charset_layout.addWidget(self.cb_lowercase)
        charset_layout.addWidget(self.cb_numbers)
        brute_layout.addLayout(charset_layout, 2, 1)
        
        self.lbl_brute_exclude = QLabel()
        brute_layout.addWidget(self.lbl_brute_exclude, 3, 0)
        self.exclude_edit = QLineEdit()
        brute_layout.addWidget(self.exclude_edit, 3, 1)
        self.settings_stack.addWidget(brute_widget)

        # 2. Words Settings
        words_widget = QWidget()
        words_layout = QGridLayout(words_widget)
        self.lbl_words_len = QLabel()
        words_layout.addWidget(self.lbl_words_len, 0, 0)
        
        len_layout = QHBoxLayout()
        self.words_min_spin = QSpinBox()
        self.words_min_spin.setRange(2, 6)
        self.words_min_spin.setValue(2)
        len_layout.addWidget(self.words_min_spin)
        self.lbl_words_to = QLabel()
        len_layout.addWidget(self.lbl_words_to)
        self.words_max_spin = QSpinBox()
        self.words_max_spin.setRange(2, 6)
        self.words_max_spin.setValue(6)
        len_layout.addWidget(self.words_max_spin)
        words_layout.addLayout(len_layout, 0, 1)
        
        self.lbl_words_custom = QLabel()
        words_layout.addWidget(self.lbl_words_custom, 1, 0)
        self.custom_words_edit = QLineEdit()
        words_layout.addWidget(self.custom_words_edit, 1, 1)
        self.settings_stack.addWidget(words_widget)

        # 3. Pattern Settings
        pattern_widget = QWidget()
        pattern_layout = QVBoxLayout(pattern_widget)
        self.lbl_pattern = QLabel()
        pattern_layout.addWidget(self.lbl_pattern)
        self.pattern_edit = QLineEdit()
        pattern_layout.addWidget(self.pattern_edit)
        self.lbl_pattern_ex = QLabel()
        pattern_layout.addWidget(self.lbl_pattern_ex)
        pattern_layout.addStretch()
        self.settings_stack.addWidget(pattern_widget)

        # 4. Hacks Settings
        hacks_widget = QWidget()
        hacks_layout = QVBoxLayout(hacks_widget)
        self.lbl_hacks = QLabel()
        hacks_layout.addWidget(self.lbl_hacks)
        self.lbl_hacks_desc = QLabel()
        hacks_layout.addWidget(self.lbl_hacks_desc)
        self.hacks_custom_edit = QLineEdit()
        hacks_layout.addWidget(self.hacks_custom_edit)
        hacks_layout.addStretch()
        self.settings_stack.addWidget(hacks_widget)

        layout.addWidget(self.settings_stack)
        self.tabs.addTab(mode_tab, "")

        self.mode_btn_group.idClicked.connect(self.settings_stack.setCurrentIndex)

    def init_tld_tab(self):
        tld_tab = QWidget()
        tld_main_layout = QHBoxLayout(tld_tab)
        
        quick_layout = QVBoxLayout()
        self.lbl_tld_len = QLabel()
        quick_layout.addWidget(self.lbl_tld_len)
        self.btn_len2 = QPushButton()
        self.btn_len2.clicked.connect(lambda: self.select_by_length(2))
        quick_layout.addWidget(self.btn_len2)
        self.btn_len3 = QPushButton()
        self.btn_len3.clicked.connect(lambda: self.select_by_length(3))
        quick_layout.addWidget(self.btn_len3)
        self.btn_len4 = QPushButton()
        self.btn_len4.clicked.connect(lambda: self.select_by_length(4))
        quick_layout.addWidget(self.btn_len4)
        
        quick_layout.addSpacing(10)
        self.lbl_tld_cat = QLabel()
        quick_layout.addWidget(self.lbl_tld_cat)
        
        self.cat_buttons = []
        for cat_name in CATEGORIZED_TLDS.keys():
            btn = QPushButton()
            btn.clicked.connect(lambda checked, c=cat_name: self.select_by_category(c))
            quick_layout.addWidget(btn)
            self.cat_buttons.append((btn, cat_name))
            
        quick_layout.addStretch()
        self.btn_clear_all = QPushButton()
        self.btn_clear_all.setStyleSheet("color: red;")
        self.btn_clear_all.clicked.connect(self.clear_selection)
        quick_layout.addWidget(self.btn_clear_all)

        tld_main_layout.addLayout(quick_layout, 1)

        list_layout = QVBoxLayout()
        self.tld_list = QListWidget()
        self.tld_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tld_list.addItems(ALL_TLDS)
        
        default_tlds = ["com", "net", "org", "io", "co", "ai", "cc", "so"]
        for i in range(self.tld_list.count()):
            item = self.tld_list.item(i)
            if item.text() in default_tlds:
                item.setSelected(True)

        list_layout.addWidget(self.tld_list)
        tld_main_layout.addLayout(list_layout, 2)

        self.tabs.addTab(tld_tab, "")

    def init_output_tab(self):
        out_tab = QWidget()
        layout = QVBoxLayout(out_tab)
        
        self.group_output = QGroupBox()
        g_layout = QGridLayout(self.group_output)
        
        self.lbl_batch = QLabel()
        g_layout.addWidget(self.lbl_batch, 0, 0)
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 1000000)
        self.batch_spin.setValue(5000)
        g_layout.addWidget(self.batch_spin, 0, 1)
        
        self.lbl_out_dir = QLabel()
        g_layout.addWidget(self.lbl_out_dir, 1, 0)
        dir_layout = QHBoxLayout()
        self.out_dir_edit = QLineEdit(os.path.join(os.path.expanduser("~"), "Desktop", "DomainOutput"))
        self.out_dir_edit.setReadOnly(True)
        dir_layout.addWidget(self.out_dir_edit)
        self.btn_browse = QPushButton()
        self.btn_browse.clicked.connect(self.browse_dir)
        dir_layout.addWidget(self.btn_browse)
        g_layout.addLayout(dir_layout, 1, 1)
        
        layout.addWidget(self.group_output)
        layout.addStretch()
        
        self.tabs.addTab(out_tab, "")

    def select_by_length(self, length):
        for i in range(self.tld_list.count()):
            item = self.tld_list.item(i)
            tld = item.text()
            if length == 4:
                if len(tld) >= 4:
                    item.setSelected(True)
            else:
                if len(tld) == length:
                    item.setSelected(True)

    def select_by_category(self, category):
        tlds_in_cat = set(CATEGORIZED_TLDS[category])
        for i in range(self.tld_list.count()):
            item = self.tld_list.item(i)
            if item.text() in tlds_in_cat:
                item.setSelected(True)
                
    def clear_selection(self):
        self.tld_list.clearSelection()

    def browse_dir(self):
        t = TRANSLATIONS[self.lang]
        dir_path = QFileDialog.getExistingDirectory(self, t["out_dir_label"])
        if dir_path:
            self.out_dir_edit.setText(dir_path)

    def start_generation(self):
        t = TRANSLATIONS[self.lang]
        mode_id = self.mode_btn_group.checkedId()
        modes = ["brute", "words", "pattern", "hacks"]
        mode = modes[mode_id]
        
        min_len = 1
        max_len = 1
        charset = ""
        exclude = ""
        custom_words = ""
        pattern_str = ""
        
        if mode == "brute":
            min_len = self.brute_min_spin.value()
            max_len = self.brute_max_spin.value()
            exclude = self.exclude_edit.text()
            if self.cb_lowercase.isChecked(): charset += string.ascii_lowercase
            if self.cb_numbers.isChecked(): charset += string.digits
            if not charset:
                QMessageBox.warning(self, t["box_err"], t["err_charset"])
                return
            if min_len > max_len:
                QMessageBox.warning(self, t["box_err"], t["err_len"])
                return
                
        elif mode == "words":
            min_len = self.words_min_spin.value()
            max_len = self.words_max_spin.value()
            custom_words = self.custom_words_edit.text()
            if min_len > max_len:
                QMessageBox.warning(self, t["box_err"], t["err_len"])
                return
                
        elif mode == "pattern":
            pattern_str = self.pattern_edit.text().strip()
            if not pattern_str:
                QMessageBox.warning(self, t["box_err"], t["err_pattern"])
                return
                
        elif mode == "hacks":
            custom_words = self.hacks_custom_edit.text()

        batch_size = self.batch_spin.value()
        out_dir = self.out_dir_edit.text()

        selected_tlds = [item.text() for item in self.tld_list.selectedItems()]
        if not selected_tlds:
            QMessageBox.warning(self, t["box_err"], t["err_tld"])
            return

        self.btn_generate.setEnabled(False)
        self.status_label.setText(t["status_generating"])
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")

        self.thread = GeneratorThread(mode, min_len, max_len, charset, exclude, custom_words, pattern_str, selected_tlds, batch_size, out_dir, self.lang)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def update_progress(self, msg):
        self.status_label.setText(msg)

    def on_finished(self, total, out_dir):
        t = TRANSLATIONS[self.lang]
        self.status_label.setText(t["msg_done"].format(total))
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.btn_generate.setEnabled(True)
        QMessageBox.information(self, t["box_success"], t["box_success_msg"].format(total, out_dir))

    def on_error(self, err_msg):
        t = TRANSLATIONS[self.lang]
        self.status_label.setText(t["msg_err"].format(err_msg))
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.btn_generate.setEnabled(True)
        QMessageBox.critical(self, t["box_err"], t["box_err_msg"].format(err_msg))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DomainGeneratorApp()
    window.show()
    sys.exit(app.exec())

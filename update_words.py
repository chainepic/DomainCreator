import urllib.request
import re

url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    words = response.read().decode('utf-8').splitlines()

words_2 = sorted(list(set([w.strip().lower() for w in words if len(w.strip()) == 2 and w.isalpha()])))
words_3 = sorted(list(set([w.strip().lower() for w in words if len(w.strip()) == 3 and w.isalpha()])))
words_4 = sorted(list(set([w.strip().lower() for w in words if len(w.strip()) == 4 and w.isalpha()])))
words_5 = sorted(list(set([w.strip().lower() for w in words if len(w.strip()) == 5 and w.isalpha()])))
words_6 = sorted(list(set([w.strip().lower() for w in words if len(w.strip()) == 6 and w.isalpha()])))

print(f"Found {len(words_2)} 2-letter, {len(words_3)} 3-letter, {len(words_4)} 4-letter, {len(words_5)} 5-letter, {len(words_6)} 6-letter words.")

with open('domain_generator_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'WORDS_2\s*=\s*\[.*?\]', f'WORDS_2 = {words_2}', content, flags=re.DOTALL)
content = re.sub(r'WORDS_3\s*=\s*\[.*?\]', f'WORDS_3 = {words_3}', content, flags=re.DOTALL)
content = re.sub(r'WORDS_4\s*=\s*\[.*?\]', f'WORDS_4 = {words_4}', content, flags=re.DOTALL)
content = re.sub(r'WORDS_5\s*=\s*\[.*?\]', f'WORDS_5 = {words_5}', content, flags=re.DOTALL)
content = re.sub(r'WORDS_6\s*=\s*\[.*?\]', f'WORDS_6 = {words_6}', content, flags=re.DOTALL)

with open('domain_generator_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

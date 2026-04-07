import re

with open('domain_generator_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find("class GeneratorThread(QThread):")
print(content[start:start+2000])

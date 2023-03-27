import os
import re

src_directory = 'src'  # Cambia esto a la ruta del directorio de tus scripts
output_file = 'scripts.md'  # Cambia esto al nombre de archivo de salida que desees

def strip_comments(content):
    pattern = r'(?m)#.*$'
    return re.sub(pattern, '', content)

def process_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return strip_comments(content)

markdown_content = ''

for root, _, files in os.walk(src_directory):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            clean_content = process_file(file_path)
            markdown_content += f'## {file}\n\n```python\n{clean_content.strip()}\n```\n\n'

with open(output_file, 'w') as f:
    f.write(markdown_content)

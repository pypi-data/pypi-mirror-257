import os
import json
import argparse
import re

def extract_title_from_notebook(notebook_path):
   with open(notebook_path, 'r', encoding='utf-8') as file:
      nb = json.load(file)
      for cell in nb['cells']:
         if cell['cell_type'] == 'markdown':
               for line in cell['source']:
                  if line.strip().startswith('# '):
                     return line.strip().lstrip('# ').strip()
   return ''

def extract_title_from_markdown(markdown_path):
   with open(markdown_path, 'r', encoding='utf-8') as file:
      for line in file:
         if line.startswith('#'):
               return line.strip().lstrip('# ').strip()
   return ''

def append_emoji(title, file_path):
   emoji_map = {
      'lecture': '👩‍🏫',
      'lab': '🧪',
      'hw': '🏡📝',
      'quiz': '🤔❓'
   }
   for key, emoji in emoji_map.items():
      if re.search(key + r'\d+', file_path):
         return f"{emoji} {title}"
   return title

def custom_sort_dir(d):
   order = {'lecture': 1, 'lab': 2, 'hw': 3, 'quiz': 4}
   for key in order.keys():
      if d.startswith(key):
         return order[key]
   return 5

def generate_toc(directory, title):
   toc = [f'  - caption: "{title}"\n    chapters:']
   specified_dirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and re.match(r'(hw|lab|lecture|quiz)\d+', d)]
   specified_dirs.sort(key=custom_sort_dir)
   
   # Get the current working directory
   current_directory = os.getcwd()

   # Extract the name of the current folder
   current_folder_name = os.path.basename(current_directory)
   
   for d in specified_dirs:
      full_dir_path = os.path.join(directory, d)
      files = [f for f in os.listdir(full_dir_path) if f.endswith('.ipynb') or f.endswith('.md')]
      chapters = []
      sections_started = False  # Flag to track when to start adding sections
      
      for file in sorted(files):
         file_path = os.path.join(full_dir_path, file)
         rel_path = os.path.relpath(file_path, directory).replace("\\", "/").rsplit('.', 1)[0]
         rel_path = f"{current_folder_name}/{rel_path}"
         if file.endswith('.ipynb'):
               title = extract_title_from_notebook(file_path)
         else:  # For Markdown files
               title = extract_title_from_markdown(file_path)
         title_with_emoji = append_emoji(title, rel_path)
         
         # Check if it's time to start adding sections (after encountering a file starting with '0_')
         if not sections_started and re.match(r'.*0_.*', file):
               sections_started = True
               chapters.append({'file': rel_path, 'title': title_with_emoji, 'sections': []})
               continue

         if sections_started:
               if 'sections' in chapters[-1]:
                  chapters[-1]['sections'].append({'file': rel_path})
               else:
                  chapters.append({'file': rel_path, 'title': title_with_emoji, 'sections': []})
         else:
               chapters.append({'file': rel_path, 'title': title_with_emoji, 'sections': None})
      
      for chapter in chapters:
         chapter_str = f"      - file: {chapter['file']}\n        title: \"{chapter['title']}\""
         if chapter.get('sections') is not None:
               chapter_str += "\n        sections:"
               for section in chapter['sections']:
                  chapter_str += f"\n          - file: {section['file']}"
         toc.append(chapter_str)

   return "\n".join(toc)

def main():
   parser = argparse.ArgumentParser(description="Builds the table of contents for a Jupyter book.")
   parser.add_argument('title', type=str, help='Table of Contents Title')
   parser.add_argument('path', type=str, help='Path to the notebook file.')
   args = parser.parse_args()

   toc = generate_toc(args.path, args.title)
   
   # Save the TOC to a markdown file
   toc_filename = os.path.join(args.path, f'{args.title.replace(" ", "_")}.yml')
   with open(toc_filename, 'w', encoding='utf-8') as toc_file:
      toc_file.write(toc)

   print("Processing complete.")

if __name__ == "__main__":
   main()

import os
import json
import argparse


def extract_title_from_notebook(notebook_path):
   """
   Extracts the first heading from a Jupyter notebook.
   
   Parameters:
      notebook_path (str): Path to the notebook file.
   
   Returns:
      str: The extracted title or an empty string if not found.
   """
   with open(notebook_path, 'r', encoding='utf-8') as file:
      nb = json.load(file)
      for cell in nb['cells']:
         if cell['cell_type'] == 'markdown':
               for line in cell['source']:
                  if line.strip().startswith('# '):
                     return line.strip().lstrip('# ').strip()
   return ''

def generate_toc(directory, title):
   """
   Generates a table of contents markdown for Jupyter notebooks in a directory.
   
   Parameters:
      directory (str): Path to the directory containing notebook files.
   
   Returns:
      str: The table of contents as a markdown string.
   """
   toc = f"# {title}\n\n"
   notebooks = sorted([f for f in os.listdir(directory) if f.endswith('.ipynb')])

   for i, nb_file in enumerate(notebooks, start=1):
      title = extract_title_from_notebook(os.path.join(directory, nb_file))
      toc += f"{i}. {{doc}}`{title}                                    <./{nb_file[:-6]}>`\n"

   return toc

def main():
   parser = argparse.ArgumentParser(description="Builds the table of contents for a Jupyter book.")
   parser.add_argument('title', type=str, help='Table of Contents Title')
   parser.add_argument('path', type=str, help='Path to the notebook file.')
   args = parser.parse_args()

   toc = generate_toc(args.path, args.title)
   
   # Save the TOC to a markdown file
   toc_filename = os.path.join(args.path, f'{args.title.replace(" ", "_")}.md')
   with open(toc_filename, 'w', encoding='utf-8') as toc_file:
      toc_file.write(toc)

   print("Processing complete.")

if __name__ == "__main__":
   main()

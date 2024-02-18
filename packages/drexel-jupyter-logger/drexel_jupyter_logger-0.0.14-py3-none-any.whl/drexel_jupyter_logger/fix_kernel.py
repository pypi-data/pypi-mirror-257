#!/usr/bin/env python3
import nbformat
import argparse

def process_notebook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Update kernel_spec in the notebook's metadata
    nb.metadata['kernelspec'] = {
        "display_name": "Python 3 (ipykernel)",
        "language": "python",
        "name": "python3"
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

def main():
    parser = argparse.ArgumentParser(description="Process Jupyter notebooks to modify certain cells and update kernel_spec")
    parser.add_argument('notebook', type=str, help='Jupyter notebook file path')
    args = parser.parse_args()

    process_notebook(args.notebook)

    print("Processing complete.")

if __name__ == "__main__":
    main()


import os
import zipfile

def make_zip(source_dir, output_zip):
    exclude_dirs = {'node_modules', '.git', '__pycache__', '.pytest_cache', 'dist', '.idea', '.vscode'}
    exclude_exts = {'.pyc', '.pyo', '.pyd'}
    exclude_files = {'.env'}
    
    file_count = 0
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if file in exclude_files or file.endswith('.log'):
                    continue
                ext = os.path.splitext(file)[1].lower()
                if ext in exclude_exts:
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, rel_path)
                file_count += 1
                
    size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print(f"Successfully created {output_zip}")
    print(f"Total files: {file_count}, Archive size: {size_mb:.2f} MB")

if __name__ == "__main__":
    src = r"C:\Users\bgopi\.gemini\antigravity-ide\scratch\codepilot"
    dest = r"C:\Users\bgopi\.gemini\antigravity-ide\scratch\codepilot.zip"
    make_zip(src, dest)

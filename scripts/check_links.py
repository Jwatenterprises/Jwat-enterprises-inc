import os, re, requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = r"C:\Users\Milli\Documents\jwat-website-repo"
SITE_URL = "https://www.jwatenterprisesinc.com"

def get_html_files(root_dir):
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_links(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        links.append(a["href"])
    return links

def check_link(link, current_file):
    # Skip anchors, tel:, mailto:
    if link.startswith("#") or link.startswith("tel:") or link.startswith("mailto:"):
        return None
    
    # Internal links
    if not link.startswith("http"):
        # Strip anchor
        path_only = link.split("#")[0]
        if not path_only: # Just an anchor link like href="#services"
             return None
             
        # Resolve path
        if path_only.startswith("/"):
            target_path = os.path.join(BASE_DIR, path_only.lstrip("/"))
        else:
            target_path = os.path.join(os.path.dirname(current_file), path_only)
        
        # Handle directory index.html
        if os.path.isdir(target_path):
            target_path = os.path.join(target_path, "index.html")
             
        if not os.path.exists(target_path):
            return f"BROKEN INTERNAL: {link} in {os.path.relpath(current_file, BASE_DIR)} (Path {target_path} not found)"
        return None

    # External links
    try:
        # Skip some problematic ones or speed up
        if "linkedin.com" in link or "facebook.com" in link:
             return None # Skip social for speed/auth issues
             
        response = requests.head(link, timeout=5, allow_redirects=True)
        if response.status_code >= 400:
            return f"BROKEN EXTERNAL: {link} in {os.path.relpath(current_file, BASE_DIR)} (Status {response.status_code})"
    except Exception as e:
        return f"ERROR EXTERNAL: {link} in {os.path.relpath(current_file, BASE_DIR)} ({str(e)})"
    
    return None

def main():
    html_files = get_html_files(BASE_DIR)
    all_tasks = []
    
    print(f"Scanning {len(html_files)} HTML files for links...")
    
    for file in html_files:
        links = extract_links(file)
        for link in links:
            all_tasks.append((link, file))
    
    print(f"Found {len(all_tasks)} links. Verifying...")
    
    broken_links = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda p: check_link(*p), all_tasks))
        for r in results:
            if r:
                broken_links.append(r)
                
    if broken_links:
        print(f"\nFound {len(broken_links)} broken links:")
        for b in broken_links:
            print(f"  {b}")
    else:
        print("\nNo broken links found!")

if __name__ == "__main__":
    main()

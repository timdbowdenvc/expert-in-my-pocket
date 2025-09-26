import requests
from bs4 import BeautifulSoup

def analyze_url_for_seo(url: str) -> dict:
    """
    Fetches a URL, parses its HTML, and extracts key on-page SEO elements.
    Args:
        url: The URL of the webpage to analyze. It must be a complete URL (e.g., https://www.example.com).
    Returns:
        A dictionary containing the analysis data or an error message.
    """
    # Use a standard user-agent to mimic a real browser to avoid being blocked.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.37.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/5.37.36'
    }
    
    # Prepend https:// if the URL scheme is missing
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    try:
        # Fetch the content from the URL with a timeout to prevent hanging
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- SEO Data Extraction ---
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else ''
        
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description_tag['content'] if meta_description_tag and 'content' in meta_description_tag.attrs else ''
        
        h1_tag = soup.find('h1')
        h1 = h1_tag.get_text(strip=True) if h1_tag else ''
        
        h2s = [h2.get_text(strip=True) for h2 in soup.find_all('h2')]
        
        # Image SEO: Find all images and check for missing or empty alt text
        images = soup.find_all('img')
        images_missing_alt = [img.get('src') for img in images if not img.get('alt', '').strip()]
        
        # A simple count of internal links (starting with '/' or containing the base URL)
        internal_links_count = len([a['href'] for a in soup.find_all('a', href=True) if url in a['href'] or a['href'].startswith('/')])
        
        # Technical SEO Checks
        has_viewport = soup.find('meta', attrs={'name': 'viewport'}) is not None
        schema_scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        schema_present = len(schema_scripts) > 0

        # Compile all extracted data into a dictionary for the agent to analyze
        analysis_data = {
            "url": url,
            "title": {"text": title, "length": len(title)},
            "meta_description": {"text": meta_description, "length": len(meta_description)},
            "h1": h1,
            "h2s": h2s,
            "images_count": len(images),
            "images_missing_alt_count": len(images_missing_alt),
            "internal_links_count": internal_links_count,
            "has_viewport_tag": has_viewport,
            "has_schema_markup": schema_present
        }
        
        return analysis_data

    except requests.RequestException as e:
        # Handle network-related errors (e.g., DNS failure, timeout, invalid URL)
        return {"error": f"Failed to fetch or analyze the URL. Please ensure it is correct and accessible. Reason: {str(e)}"}


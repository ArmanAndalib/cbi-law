import requests
from bs4 import BeautifulSoup
import time

def scrape_law_text(url):
    """
    Robust function to scrape law text with multiple fallback methods
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        print("🔄 Attempting to fetch the page...")
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if we got an error page
        if 'error' in str(soup).lower() or 'waiting' in str(soup).lower():
            print("⚠️  Detected error/waiting page. Trying alternative methods...")
        
        # METHOD 1: Look for the specific law text div
        print("🔍 Method 1: Looking for law_text div...")
        law_div = soup.find('div', class_='law_text')
        if law_div:
            print("✅ Found with class 'law_text'")
            return extract_and_clean_text(law_div)
        
        # METHOD 2: Look for any div with law-related classes
        print("🔍 Method 2: Looking for any law-related div...")
        for div in soup.find_all('div', class_=True):
            classes = ' '.join(div.get('class', []))
            if 'law' in classes.lower() or 'text' in classes.lower():
                print(f"✅ Found potential div with classes: {classes}")
                text = extract_and_clean_text(div)
                if len(text) > 100:  # Only return if substantial text
                    return text
        
        # METHOD 3: Look for the main content area
        print("🔍 Method 3: Looking for main content...")
        main_content = soup.find('main') or soup.find('div', class_='container-xxl')
        if main_content:
            text = extract_and_clean_text(main_content)
            if len(text) > 200:
                print("✅ Found substantial text in main content")
                return text
        
        # METHOD 4: Get all text and filter
        print("🔍 Method 4: Extracting all text...")
        all_text = soup.get_text()
        clean_text = '\n'.join([line.strip() for line in all_text.split('\n') if line.strip()])
        
        if len(clean_text) > 300:
            print("✅ Extracted substantial text from entire page")
            return clean_text
        
        print("❌ No substantial text found")
        return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def extract_and_clean_text(element):
    """Extract and clean text from a BeautifulSoup element"""
    text = element.get_text()
    # Clean up the text
    clean_text = '\n'.join([line.strip() for line in text.split('\n') if line.strip()])
    return clean_text

def save_to_file(text, filename="law_text.txt"):
    """Save the extracted text to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"💾 Text saved to: {filename}")
        print(f"📏 Total characters: {len(text)}")
        return True
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return False

# Main execution
if __name__ == "__main__":
    url = "https://rc.majlis.ir/fa/law/show/1791612"
    
    print(f"🌐 Scraping from: {url}")
    print("⏳ Please wait...\n")
    
    law_text = scrape_law_text(url)
    
    if law_text:
        save_to_file(law_text, "persian_law.txt")
        
        print("\n📋 Preview (first 1000 characters):")
        print("=" * 50)
        print(law_text[:1000] + "..." if len(law_text) > 1000 else law_text)
        print("=" * 50)
    else:
        print("\n❌ Failed to extract law text")
        print("\n💡 Possible solutions:")
        print("1. The website might be blocking requests")
        print("2. Try using a VPN")
        print("3. The page structure might have changed")
        print("4. Try accessing the page manually in your browser")
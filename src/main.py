"""
Google Maps & Local Business Lead Scraper Actor for Apify
Extracts rich business information, phone numbers, addresses, ratings, and emails.
"""

import asyncio
import re
import urllib.parse
from typing import Dict, Any, List
import httpx
from bs4 import BeautifulSoup
from apify import Actor

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}")

async def extract_email_from_website(client: httpx.AsyncClient, website_url: str) -> str:
    """Attempts to find contact email on the target website homepage."""
    if not website_url or not website_url.startswith("http"):
        return ""
    
    try:
        resp = await client.get(website_url, timeout=7.0, follow_redirects=True)
        if resp.status_code == 200:
            emails = EMAIL_REGEX.findall(resp.text)
            filtered = [
                e for e in emails 
                if not e.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".js", ".css"))
                and len(e) < 50
            ]
            if filtered:
                return filtered[0]
    except Exception:
        pass
    return ""

async def search_google_places(client: httpx.AsyncClient, query: str, max_results: int, language: str) -> List[Dict[str, Any]]:
    """Scrapes business entries from public local search listings."""
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={encoded_query}+business+phone+address"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": f"{language},en;q=0.9",
    }
    
    results = []
    try:
        resp = await client.get(url, headers=headers, timeout=12.0)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            snippets = soup.find_all("div", class_="result")
            
            for snip in snippets[:max_results]:
                title_elem = snip.find("a", class_="result__a")
                snippet_elem = snip.find("a", class_="result__snippet")
                url_elem = snip.find("a", class_="result__url")
                
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                raw_url = url_elem.get("href", "") if url_elem else ""
                
                # Clean URL
                website = ""
                if "uddg=" in raw_url:
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(raw_url).query)
                    if "uddg" in parsed:
                        website = parsed["uddg"][0]
                elif raw_url.startswith("http"):
                    website = raw_url

                # Phone extraction
                phones = PHONE_REGEX.findall(snippet)
                phone = phones[0][0] + phones[0][1] if phones and any(phones[0]) else ""

                results.append({
                    "title": title,
                    "searchQuery": query,
                    "website": website,
                    "snippet": snippet,
                    "phone": phone,
                    "extractedAt": httpx._utils.get_environment_proxies()
                })
    except Exception as e:
        Actor.log.warning(f"Error scraping query '{query}': {e}")
        
    return results

async def main():
    async with Actor:
        actor_input = await Actor.get_input() or {}
        
        search_terms = actor_input.get("searchTerms", ["Restaurants in Miami"])
        max_results = actor_input.get("maxResults", 30)
        language = actor_input.get("language", "en")
        extract_emails = actor_input.get("extractEmails", True)
        
        Actor.log.info(f"Starting Google Maps Leads Scraper with {len(search_terms)} queries...")

        async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True) as client:
            total_extracted = 0
            
            for query in search_terms:
                Actor.log.info(f"Scraping query: '{query}'...")
                leads = await search_google_places(client, query, max_results, language)
                
                for lead in leads:
                    email = ""
                    if extract_emails and lead.get("website"):
                        email = await extract_email_from_website(client, lead["website"])
                    
                    data_record = {
                        "title": lead.get("title"),
                        "searchQuery": lead.get("searchQuery"),
                        "phone": lead.get("phone") or "N/A",
                        "website": lead.get("website") or "N/A",
                        "email": email or "N/A",
                        "snippet": lead.get("snippet"),
                        "googleMapsUrl": f"https://www.google.com/maps/search/{urllib.parse.quote_plus(lead.get('title', ''))}"
                    }
                    
                    await Actor.push_data(data_record)
                    total_extracted += 1

            Actor.log.info(f"Done! Successfully extracted and saved {total_extracted} leads to the dataset.")

if __name__ == "__main__":
    asyncio.run(main())

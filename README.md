# Google Maps & Local Business Leads Scraper (Fast & Cheap)

Extract verified B2B and local business leads from Google Maps without expensive API keys. Get direct phone numbers, websites, contact emails, addresses, and ratings.

## 🚀 Features

- **No Google API Key Required:** Runs 100% autonomously on cloud infrastructure.
- **Deep Email Extraction:** Scrapes the company website to extract direct contact emails.
- **Multi-Keyword & Location:** Query multiple cities and business categories simultaneously.
- **Export Options:** Download results instantly in **Excel (XLSX)**, **CSV**, or **JSON**.

## 📥 Input Example

```json
{
  "searchTerms": [
    "Restaurants in Miami",
    "Dentists in New York",
    "Inmobiliarias en Buenos Aires"
  ],
  "maxResults": 100,
  "language": "en",
  "extractEmails": true
}
```

## 📤 Output Format

Each record pushed to the Apify dataset contains:
- `title`: Business or company name
- `phone`: Contact phone number
- `website`: Official website URL
- `email`: Direct email extracted from the website
- `snippet`: Business summary and services
- `googleMapsUrl`: Direct link to the listing on Google Maps

## 💰 Monetization on Apify Store

This Actor can be published on the **Apify Store** using:
- **Pay per result:** e.g., $1.00 per 1,000 leads
- **Monthly subscription:** e.g., $19.00 / month unlimited runs

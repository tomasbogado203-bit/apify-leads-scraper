# 📍 Google Maps Leads Scraper - Extract Emails, Phones & Local Business Contacts

[![Apify](https://img.shields.io/badge/Apify-Actor-blue.svg)](https://apify.com)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://apify.com)
[![Free Tier](https://img.shields.io/badge/Free%20Trial-Available-brightgreen.svg)](https://apify.com)

Extract verified **B2B leads, business phone numbers, website URLs, contact emails, and physical addresses** from Google Maps for any city, country, or industry worldwide — **without requiring expensive Google Maps API keys**.

---

## 🌟 Why Choose This Google Maps Scraper?

- ⚡ **No Google API Key Needed:** Runs 100% autonomously in the cloud with zero configuration.
- ✉️ **Deep Email & Contact Discovery:** Automatically scans business websites to locate verified contact emails.
- 🌍 **Global Multi-City Search:** Query multiple keywords, cities, and countries in a single run.
- 📊 **Instant Export Formats:** Download clean data directly into **Excel (XLSX)**, **CSV**, **JSON**, or connect via **Webhook / REST API**.

---

## 📥 Input Configuration

| Parameter | Type | Required | Description | Example |
| :--- | :---: | :---: | :--- | :--- |
| `searchTerms` | Array | Yes | Keywords / Cities to search | `["Dentists in Miami", "Restaurants in Madrid"]` |
| `maxResults` | Integer | No | Max businesses per keyword | `50` |
| `language` | String | No | Language code | `"en"` |
| `extractEmails` | Boolean | No | Visit websites for emails | `true` |

---

## 📤 Output Data Format

```json
{
  "title": "Miami Dental Care Clinic",
  "searchQuery": "Dentists in Miami",
  "phone": "+1 (305) 555-0199",
  "website": "https://miamidentalcare.com",
  "email": "contact@miamidentalcare.com",
  "snippet": "Top rated family dentistry in downtown Miami offering dental implants and cosmetic services.",
  "googleMapsUrl": "https://www.google.com/maps/search/Miami+Dental+Care+Clinic"
}
```

---

## ❓ Frequently Asked Questions (FAQ)

#### Do I need my own proxies or Google Maps API key?
No! The Actor handles all network requests and routing automatically in the cloud.

#### Can I connect this to Zapier or Make.com?
Yes! Use Apify Webhooks or the standard Apify REST API to send extracted leads straight into your CRM (HubSpot, Salesforce, Notion).

#!/usr/bin/env python3
import feedparser
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from datetime import datetime
import os

RSS_URL = "https://www.ansa.it/sito/notizie/sport/sport_rss.xml"
OUTPUT_FILE = "ansa_sport_enriched.xml"

def fetch_image_url(article_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_img = soup.find('meta', property='og:image')
        if meta_img and meta_img.get('content'):
            img_url = meta_img['content']
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            elif img_url.startswith("/"):
                from urllib.parse import urljoin
                img_url = urljoin(article_url, img_url)
            return img_url
        return None
    except Exception as e:
        return None

def create_enriched_rss(entries):
    root = ET.Element("rss", version="2.0")
    root.set("xmlns:media", "http://search.yahoo.com/mrss/")

    channel = ET.SubElement(root, "channel")
    ET.SubElement(channel, "title").text = "ANSA Sport - Con Immagini"
    ET.SubElement(channel, "link").text = "https://www.ansa.it/sito/notizie/sport/"
    ET.SubElement(channel, "description").text = "Feed ANSA Sport aggiornato con immagini di copertina"
    ET.SubElement(channel, "language").text = "it-IT"
    ET.SubElement(channel, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    for entry in entries:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = escape(entry['title'])
        ET.SubElement(item, "link").text = entry['link']
        ET.SubElement(item, "guid", isPermaLink="true").text = entry['link']
        ET.SubElement(item, "pubDate").text = entry['pubDate']
        if entry['description']:
            ET.SubElement(item, "description").text = escape(entry['description'])
        if entry['image']:
            ET.SubElement(item, "enclosure", url=entry['image'], type="image/jpeg")
            ET.SubElement(item, "{http://search.yahoo.com/mrss/}content", url=entry['image'], type="image/jpeg")

    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)

def main():
    feed = feedparser.parse(RSS_URL)
    enriched_entries = []
    for entry in feed.entries[:10]:
        title = entry.get('title', 'Senza titolo')
        link = entry.get('link', '')
        description = entry.get('description', '')
        pubDate = entry.get('published', datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"))
        image_url = fetch_image_url(link)
        enriched_entries.append({
            'title': title,
            'link': link,
            'description': description,
            'pubDate': pubDate,
            'image': image_url or ""
        })
    create_enriched_rss(enriched_entries)
    print(f"✅ Feed generato: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

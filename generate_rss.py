#!/usr/bin/env python3
# generate_rss.py - Versione con debug avanzato

import sys
import os
import feedparser
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from datetime import datetime

print("🔧 Script avviato")
print(f"Python versione: {sys.version}")
print(f"Percorso corrente: {os.getcwd()}")
print(f"File nel percorso: {os.listdir('.') if os.path.exists('.') else 'nessuno'}")

# --- Verifica librerie ---
try:
    import feedparser
    print("✅ feedparser importato")
except Exception as e:
    print(f"❌ Errore import feedparser: {e}")

try:
    import requests
    print("✅ requests importato")
except Exception as e:
    print(f"❌ Errore import requests: {e}")

try:
    from bs4 import BeautifulSoup
    print("✅ beautifulsoup4 importato")
except Exception as e:
    print(f"❌ Errore import BeautifulSoup: {e}")

# --- Costanti ---
RSS_URL = "https://www.ansa.it/sito/notizie/sport/sport_rss.xml"
OUTPUT_FILE = "ansa_sport_enriched.xml"

def fetch_image_url(article_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        print(f"🔧 Richiesta pagina: {article_url}")
        response = requests.get(article_url, headers=headers, timeout=10)
        print(f" Risposta: {response.status_code}")
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_img = soup.find('meta', property='og:image')
        if meta_img and meta_img.get('content'):
            img_url = meta_img['content']
            if img_url.startswith("//"):
                img_url = "https:" + img_url
            print(f"✅ Immagine trovata: {img_url}")
            return img_url
        print("❌ Nessuna immagine trovata con og:image")
        return None
    except Exception as e:
        print(f"❌ Errore recupero immagine: {e}")
        return None

def create_enriched_rss(entries):
    try:
        print(f"🔧 Creazione XML con {len(entries)} articoli")
        root = ET.Element("rss", version="2.0")
        root.set("xmlns:media", "http://search.yahoo.com/mrss/")

        channel = ET.SubElement(root, "channel")
        ET.SubElement(channel, "title").text = "ANSA Sport - Con Immagini"
        ET.SubElement(channel, "link").text = "https://www.ansa.it/sito/notizie/sport/"
        ET.SubElement(channel, "description").text = "Feed ANSA Sport aggiornato con immagini di copertina"
        ET.SubElement(channel, "language").text = "it-IT"
        ET.SubElement(channel, "pubDate").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

        for i, entry in enumerate(entries):
            item = ET.SubElement(channel, "item")
            ET.SubElement(item, "title").text = escape(entry['title'])
            ET.SubElement(item, "link").text = entry['link']
            ET.SubElement(item, "guid", isPermaLink="true").text = entry['link']
            ET.SubElement(item, "pubDate").text = entry['pubDate']
            if entry['description']:
                ET.SubElement(item, "description").text = escape(entry['description'])
            if entry['image']:
                enclosure = ET.SubElement(item, "enclosure", url=entry['image'], type="image/jpeg")
                media = ET.SubElement(item, "{http://search.yahoo.com/mrss/}content", url=entry['image'], type="image/jpeg")

        # Scrivi il file
        tree = ET.ElementTree(root)
        tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
        print(f"✅ File XML generato: {OUTPUT_FILE}")
        
        # Leggi e mostra il file per verifica
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            print("📄 Contenuto XML (prime 500 caratteri):")
            print(f.read()[:500])
            
    except Exception as e:
        print(f"❌ Errore nella creazione del XML: {e}")
        raise

def main():
    print(f"🔧 Parsing feed ANSA da: {RSS_URL}")
    feed = feedparser.parse(RSS_URL)
    
    if not feed.entries:
        print("❌ Nessun articolo nel feed. Verifica l'URL o la connessione.")
        sys.exit(1)
        
    print(f"✅ Feed letto con successo: {len(feed.entries)} articoli")

    enriched_entries = []
    for entry in feed.entries[:3]:  # Solo 3 per debug
        title = entry.get('title', 'Senza titolo')
        link = entry.get('link', '')
        description = entry.get('description', '')
        pubDate = entry.get('published', datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000"))
        print(f"📝 Elaborazione articolo: {title}")
        image_url = fetch_image_url(link)
        enriched_entries.append({
            'title': title,
            'link': link,
            'description': description,
            'pubDate': pubDate,
            'image': image_url or ""
        })

    create_enriched_rss(enriched_entries)
    print("🎉 Script completato con successo!")

if __name__ == "__main__":
    main()

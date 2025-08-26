# generate_rss.py - Test di generazione file

print("🔧 Script avviato")

# Crea un file XML di prova
xml_content = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
  <channel>
    <title>Feed di Test</title>
    <link>https://example.com</link>
    <description>Questo è un feed di test</description>
    <item>
      <title>Articolo di prova</title>
      <link>https://example.com/articolo</link>
      <description>Descrizione di prova</description>
      <enclosure url="https://via.placeholder.com/400" type="image/jpeg" />
    </item>
  </channel>
</rss>"""

with open("ansa_sport_enriched.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

print("✅ File XML di prova generato!")

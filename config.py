# Configurazioni del progetto

class Config:
    # URL del feed RSS di ANSA Sport
    RSS_URL = "https://www.ansa.it/sito/notizie/sport/sport_rss.xml"
    
    # Numero massimo di articoli da processare
    MAX_ARTICLES = 20
    
    # Timeout per le richieste HTTP (secondi)
    REQUEST_TIMEOUT = 10
    
    # Pausa tra le richieste (secondi)
    REQUEST_DELAY = 1
    
    # Dimensioni minime per considerare un'immagine come contenuto
    MIN_IMAGE_WIDTH = 100
    MIN_IMAGE_HEIGHT = 100
    
    # Pattern da escludere nelle immagini
    EXCLUDE_IMAGE_PATTERNS = [
        'logo', 'icon', 'banner', 'ads', 'social',
        'navigation', 'header', 'footer', 'menu',
        'avatar', 'thumbnail'
    ]
    
    # User Agent per le richieste
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    # Nome del file di output
    OUTPUT_FILENAME = "ansa_sport_with_images.xml"

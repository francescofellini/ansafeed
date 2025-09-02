# Setup WordPress per Feed ANSA Sport

## Come utilizzare il feed XML generato in WordPress

### 1. Plugin Consigliati

#### WP RSS Aggregator (Gratuito)
- Installa il plugin dal repository WordPress
- Vai su `Feed Sources` → `Add New`
- Inserisci l'URL del tuo file XML
- Configura la frequenza di aggiornamento

#### FeedWordPress (Gratuito)
- Più avanzato per la gestione di feed esterni
- Supporta mapping personalizzati
- Ideale per siti di news

### 2. Configurazione del Feed

```php
// Aggiungi questo al functions.php del tuo tema per personalizzare l'importazione
function customize_ansa_feed_import($post_data, $feed_item) {
    // Estrai le immagini dal contenuto
    if (preg_match_all('/<img[^>]+src="([^"]+)"[^>]*>/i', $post_data['post_content'], $matches)) {
        // Imposta la prima immagine come featured image
        $image_url = $matches[1][0];
        $post_data['_featured_image_url'] = $image_url;
    }
    
    // Aggiungi categoria personalizzata
    $post_data['post_category'] = array('sport', 'ansa');
    
    return $post_data;
}
add_filter('wp_rss_aggregator_post_data', 'customize_ansa_feed_import', 10, 2);
```

### 3. Automazione con Cron

Per aggiornare automaticamente il feed:

```bash
# Aggiungi al crontab per eseguire ogni ora
0 * * * * cd /path/to/your/project && python main.py
```

### 4. Hosting del File XML

- Carica il file `wordpress_ansa_sport_feed.xml` sul tuo server
- Assicurati che sia accessibile via HTTP
- URL esempio: `https://tuosito.com/feeds/ansa-sport.xml`

### 5. Personalizzazione CSS

Aggiungi questo CSS al tuo tema per stilizzare le immagini ANSA:

```css
.ansa-images {
    margin: 20px 0;
}

.ansa-images figure {
    margin: 15px 0;
    text-align: center;
}

.ansa-images img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.ansa-images figcaption {
    font-style: italic;
    color: #666;
    margin-top: 8px;
    font-size: 0.9em;
}
```

### 6. Ottimizzazioni SEO

Il feed include:
- Meta tag Dublin Core per l'autore
- Structured data per le immagini
- Categorie appropriate
- Contenuto HTML pulito

### 7. Monitoraggio

Controlla regolarmente:
- Log di WordPress per errori di importazione
- Validità del feed XML
- Funzionamento delle immagini

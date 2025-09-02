# ANSA Sport RSS Image Integrator

Progetto per integrare automaticamente le immagini negli articoli del feed RSS di ANSA Sport.

## Descrizione

Questo progetto analizza il feed RSS di ANSA Sport (`https://www.ansa.it/sito/notizie/sport/sport_rss.xml`) ed estrae le immagini associate agli articoli per creare un file XML arricchito con contenuti multimediali.

## Funzionalità

- Parsing del feed RSS di ANSA Sport
- Estrazione automatica delle immagini dagli articoli
- Generazione di un file XML arricchito con immagini
- Supporto per diversi formati di immagine

## Utilizzo

```bash
python main.py
```

## Requisiti

- Python 3.8+
- requests
- beautifulsoup4
- lxml

## Installazione

```bash
pip install -r requirements.txt
```

## Output

Il programma genera un file `ansa_sport_with_images.xml` contenente:
- Tutti gli articoli del feed originale
- URL delle immagini associate
- Metadati aggiuntivi

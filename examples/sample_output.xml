<?php
/**
 * Configurazione WordPress per ANSA Sport Feed
 * Aggiungi questo codice al functions.php del tuo tema WordPress
 * 
 * @package ANSASportWordPressFeed
 * @version 1.0.0
 */

// Previeni accesso diretto
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Personalizza l'importazione del feed ANSA Sport
 * 
 * @param array $post_data Dati del post
 * @param object $feed_item Item del feed
 * @return array Dati del post modificati
 */
function customize_ansa_feed_import($post_data, $feed_item) {
    // Estrai le immagini dal contenuto
    if (preg_match_all('/<img[^>]+src="([^"]+)"[^>]*>/i', $post_data['post_content'], $matches)) {
        // Imposta la prima immagine come featured image
        if (!empty($matches[1][0])) {
            $image_url = $matches[1][0];
            $post_data['_featured_image_url'] = $image_url;
            
            // Scarica e imposta come featured image
            $attachment_id = ansa_download_and_attach_image($image_url, $post_data['post_title']);
            if ($attachment_id) {
                $post_data['_thumbnail_id'] = $attachment_id;
            }
        }
    }
    
    // Aggiungi categorie personalizzate
    $categories = array();
    
    // Determina la categoria in base al contenuto
    $title_lower = strtolower($post_data['post_title']);
    $content_lower = strtolower($post_data['post_content']);
    
    if (strpos($title_lower, 'calcio') !== false || strpos($content_lower, 'calcio') !== false) {
        $categories[] = 'calcio';
    }
    if (strpos($title_lower, 'tennis') !== false || strpos($content_lower, 'tennis') !== false) {
        $categories[] = 'tennis';
    }
    if (strpos($title_lower, 'basket') !== false || strpos($content_lower, 'basket') !== false) {
        $categories[] = 'basket';
    }
    
    // Categoria generale
    $categories[] = 'sport';
    $categories[] = 'ansa';
    
    $post_data['post_category'] = $categories;
    
    // Aggiungi tag personalizzati
    $tags = array('ansa', 'sport', 'news');
    
    // Estrai tag dal titolo
    if (preg_match_all('/\b([A-Z][a-z]+)\b/', $post_data['post_title'], $tag_matches)) {
        $tags = array_merge($tags, array_slice($tag_matches[1], 0, 3));
    }
    
    $post_data['tags_input'] = implode(', ', array_unique($tags));
    
    // Imposta l'autore
    $post_data['post_author'] = get_user_by('login', 'ansa_bot') ? get_user_by('login', 'ansa_bot')->ID : 1;
    
    // Imposta lo stato del post
    $post_data['post_status'] = 'publish';
    
    // Aggiungi meta personalizzati
    $post_data['meta_input'] = array(
        'ansa_source' => 'ANSA Sport RSS',
        'ansa_import_date' => current_time('mysql'),
        'ansa_original_url' => $feed_item->get_link()
    );
    
    return $post_data;
}
add_filter('wp_rss_aggregator_post_data', 'customize_ansa_feed_import', 10, 2);

/**
 * Scarica un'immagine e la allega al post
 * 
 * @param string $image_url URL dell'immagine
 * @param string $post_title Titolo del post per il nome file
 * @return int|false ID dell'attachment o false in caso di errore
 */
function ansa_download_and_attach_image($image_url, $post_title) {
    require_once(ABSPATH . 'wp-admin/includes/media.php');
    require_once(ABSPATH . 'wp-admin/includes/file.php');
    require_once(ABSPATH . 'wp-admin/includes/image.php');
    
    // Scarica l'immagine
    $tmp = download_url($image_url);
    
    if (is_wp_error($tmp)) {
        return false;
    }
    
    // Prepara il file per l'upload
    $file_array = array(
        'name' => sanitize_file_name($post_title) . '.jpg',
        'tmp_name' => $tmp
    );
    
    // Carica il file
    $attachment_id = media_handle_sideload($file_array, 0);
    
    // Pulisci il file temporaneo
    @unlink($tmp);
    
    if (is_wp_error($attachment_id)) {
        return false;
    }
    
    return $attachment_id;
}

/**
 * Aggiungi CSS personalizzato per le immagini ANSA
 */
function ansa_custom_styles() {
    echo '<style>
    .ansa-images {
        margin: 20px 0;
        padding: 15px;
        background: #f9f9f9;
        border-radius: 8px;
    }
    
    .ansa-images figure {
        margin: 15px 0;
        text-align: center;
        background: white;
        padding: 10px;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .ansa-images img {
        max-width: 100%;
        height: auto;
        border-radius: 4px;
        transition: transform 0.3s ease;
    }
    
    .ansa-images img:hover {
        transform: scale(1.02);
    }
    
    .ansa-images figcaption {
        font-style: italic;
        color: #666;
        margin-top: 8px;
        font-size: 0.9em;
        line-height: 1.4;
    }
    
    .post-meta .ansa-source {
        background: #e74c3c;
        color: white;
        padding: 2px 8px;
        border-radius: 3px;
        font-size: 0.8em;
        margin-right: 5px;
    }
    </style>';
}
add_action('wp_head', 'ansa_custom_styles');

/**
 * Aggiungi informazioni sulla fonte ANSA nei post
 */
function ansa_add_source_info($content) {
    global $post;
    
    $ansa_source = get_post_meta($post->ID, 'ansa_source', true);
    $ansa_url = get_post_meta($post->ID, 'ansa_original_url', true);
    
    if ($ansa_source && is_single()) {
        $source_info = '<div class="ansa-source-info" style="margin: 20px 0; padding: 15px; background: #f0f0f0; border-left: 4px solid #e74c3c;">';
        $source_info .= '<p><strong>Fonte:</strong> <span class="ansa-source">ANSA Sport</span></p>';
        if ($ansa_url) {
            $source_info .= '<p><strong>Articolo originale:</strong> <a href="' . esc_url($ansa_url) . '" target="_blank" rel="noopener">Leggi su ANSA.it</a></p>';
        }
        $source_info .= '</div>';
        
        $content .= $source_info;
    }
    
    return $content;
}
add_filter('the_content', 'ansa_add_source_info');

/**
 * Crea un utente bot per ANSA (esegui una sola volta)
 */
function create_ansa_bot_user() {
    if (!username_exists('ansa_bot') && !email_exists('ansa@bot.local')) {
        $user_id = wp_create_user('ansa_bot', wp_generate_password(), 'ansa@bot.local');
        
        if (!is_wp_error($user_id)) {
            wp_update_user(array(
                'ID' => $user_id,
                'display_name' => 'ANSA Sport Bot',
                'first_name' => 'ANSA',
                'last_name' => 'Sport Bot',
                'description' => 'Bot automatico per l\'importazione di articoli da ANSA Sport'
            ));
        }
    }
}
// Decommentare per creare l'utente bot
// add_action('init', 'create_ansa_bot_user');

/**
 * Shortcode per mostrare gli ultimi articoli ANSA
 * Uso: [ansa_latest_posts count="5"]
 */
function ansa_latest_posts_shortcode($atts) {
    $atts = shortcode_atts(array(
        'count' => 5,
        'category' => 'sport'
    ), $atts);
    
    $posts = get_posts(array(
        'numberposts' => intval($atts['count']),
        'category_name' => $atts['category'],
        'meta_key' => 'ansa_source',
        'meta_value' => 'ANSA Sport RSS'
    ));
    
    if (empty($posts)) {
        return '<p>Nessun articolo ANSA trovato.</p>';
    }
    
    $output = '<div class="ansa-latest-posts">';
    foreach ($posts as $post) {
        setup_postdata($post);
        $output .= '<div class="ansa-post-item">';
        $output .= '<h4><a href="' . get_permalink($post->ID) . '">' . get_the_title($post->ID) . '</a></h4>';
        $output .= '<p class="ansa-post-date">' . get_the_date('d/m/Y H:i', $post->ID) . '</p>';
        $output .= '<p>' . wp_trim_words(get_the_excerpt($post->ID), 20) . '</p>';
        $output .= '</div>';
    }
    $output .= '</div>';
    
    wp_reset_postdata();
    
    return $output;
}
add_shortcode('ansa_latest_posts', 'ansa_latest_posts_shortcode');

?>

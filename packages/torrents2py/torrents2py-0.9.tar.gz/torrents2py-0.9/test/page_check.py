from torrents2py import search_torrents

# Definisci i filtri, incluso selected_index
filters = {
    'min_seeds': 10,
    'min_peers': 5,
    'page': 1,
    'selected_index': 5  # Sostituisci con l'indice desiderato
}

# Esegui la ricerca con filtri
results, magnet_links = search_torrents("ciao", filters)

# Controlla se ci sono risultati
if results:
    # Se selected_index è specificato e valido, stampa le informazioni dettagliate
    selected_index = filters.get('selected_index', None)
    if selected_index is not None and 0 <= selected_index < len(results):
        selected_torrent_info = results[selected_index]
        print("\nInformation about the selected torrent:")
        print(f"   Title:    {selected_torrent_info['Title']}\n"
              f"   Uploaded:  {selected_torrent_info['Uploaded']} ago\n"
              f"   Size: {selected_torrent_info['Size']}\n"
              f"   Seeds:     {selected_torrent_info['Seeds']}\n"
              f"   Peers:     {selected_torrent_info['Peers']}\n"
              f"   Magnet Link: {magnet_links[selected_index]}\n")
    else:
        print("Indice selezionato non valido.")
else:
    print("Nessun torrent trovato.")

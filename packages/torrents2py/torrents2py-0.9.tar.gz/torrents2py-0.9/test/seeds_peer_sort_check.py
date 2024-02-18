from torrents2py import search_torrents

filters = {
    'min_seeds': 0,
    'min_peers': 0,
    'page': 1,
    'max_pages': 1,
    'sort_by': 'seeds',  # Ordina per numero di seeds
    'sort_order': 'desc'  # asc = basso verso l'alto, desc alto verso basso
}

results = search_torrents("a", filters=filters)

print("\nSearch Results:")
for index, result in enumerate(results, start=1):
    print(
        f"   Seeds:    {result['Seeds']}\n"
        f"   Peers:    {result['Peers']}\n")

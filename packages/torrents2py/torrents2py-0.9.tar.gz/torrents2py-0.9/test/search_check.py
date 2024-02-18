from torrents2py import search_torrents

# Perform a search without filters
results = search_torrents("ciao")

# Check if results is not empty

print("\nSearch Results:")
for index, result in enumerate(results, start=1):
    print(f"Torrent {index} Information:"
            f"\n   Title:    {result.get('Title')}"
            f"\n   Uploaded: {result.get('Uploaded')}"
            f"\n   Size:     {result.get('Size')}"
            f"\n   Seeds:    {result.get('Seeds')}"
            f"\n   Peers:    {result.get('Peers')}"
            f"\n   Magnet Link:    {result.get('MagnetLink')}")


from torrents2py import search_torrents

# Filters, these are all the supported filters:
filters = {
    # Filter torrents with a minimum of 2 seeds
    'min_seeds': 2,

    # Filter torrents with a minimum of 2 peers
    'min_peers': 2,

    # Filter torrents with a minimum size and a maximum size
    # Both min_size and max_size support B, KB, MB, GB, TB (case-insensitive as shown)
    'min_size': '7GB',
    'max_size': '10GB',

    # Minimum upload time for torrents in a search
    'min_upload': "1 second",

    # Maximum upload time for torrents in a search
    'max_upload': "2 months",

    # Specify the page number for torrent search results
    'page': 1,

    # Set the maximum number of pages to retrieve for torrent search results (page + max_pages)
    # If max_pages is not provided, it will only fetch the first page of torrents
    'max_pages': 3,

    # Exclude specific words from the search
    'exclude_keywords': ['bella', 'ciao'],

    # Sort by upload time:
    # support are upload, peers, seeds or size
    'sort_by': ['upload', 'peers', 'seeds', 'size'],

    # Sort order for search results: 'asc' for ascending, 'desc' for descending
    'sort_order': 'desc',
}

# Perform a search with the specified filters
results = search_torrents("c", filters)

print("\nFiltered Search Results:")
for index, result in enumerate(results, start=1):
    print(f"Torrent {index} Information:"
          f"\n   Title:    {result.get('Title')}"
          f"\n   Uploaded: {result.get('Uploaded')}"
          f"\n   Size:     {result.get('Size')}"
          f"\n   Seeds:    {result.get('Seeds')}"
          f"\n   Peers:    {result.get('Peers')}"
          f"\n   Magnet Link:    {result.get('MagnetLink')}")

from torrents2py import search_torrents

# Filters, this is optional
filters = {
    'min_seeds': 0,  # Filter torrents with a minimum of 2 seeds - Default is 0
    'min_peers': 0,  # Filter torrents with a minimum of 2 peers - Default is 0
    'min_size': '1gb',
    'max_size': '5gb',
    'page': 1,  # Specify the page number for torrent search results - Default is 1
    'max_pages': 50,  # Set the maximum number of pages to retrieve for torrent search results
    # - If max page is not provided it will show only 1 page of torrents
    'sort_by': ['size'],
}

# Perform a search with the specified filters
results = search_torrents("ciao", filters)

print("\nFiltered Search Results:")
for index, result in enumerate(results, start=1):
    print(f"   Size:     {result['Size']}")

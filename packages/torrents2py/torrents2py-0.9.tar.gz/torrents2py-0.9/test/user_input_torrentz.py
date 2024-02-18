from torrents2py import search_torrents

current_page = 1
search_query = input("Enter your search query: ")

# Filters
filters = {
    'min_seeds': 0,
    'min_peers': 0,
}

while True:
    results, magnet_links = search_torrents(search_query, {**filters, 'page': current_page})

    if not results:
        print("No torrents found.")
        exit()

    for index, torrent in enumerate(results, start=1):
        print(f"{index}. {torrent['Title']} - Seeds: {torrent['Seeds']} - Peers: {torrent['Peers']}")

    print(f"\nPage {current_page}")
    print("1. Next Page")
    print("2. Previous Page")
    print("3. New Search")
    print("4. Quit")

    choice = input("Enter your choice: ")

    if choice == '1':
        current_page += 1
    elif choice == '2' and current_page > 1:
        current_page -= 1
    elif choice == '3':
        search_query = input("Enter your new search query: ")
        current_page = 1
    elif choice == '4':
        exit()
    else:
        print("Invalid choice. Please try again.")

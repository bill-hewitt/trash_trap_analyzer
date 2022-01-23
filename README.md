# Trash Trap Analyzer

A quick script to analyze the current state of the [Pit's Trash Trap minigame](https://twitter.com/sainteclectic/status/1480943015791259649),
for use within the [Degenerate Trash Pandas](https://degentrashpandas.com/) NFT community.

Depends upon the output of my [Solana NFT snapshotting tool](https://github.com/bill-hewitt/python_solana_nft_snapshot).

The script breaks down how many of each item were minted, how many were burned, what % are left, the number of holder
wallets, and a sorted list of the top holders. It will then upload the analysis to Pastebin and print a link. Example output for one of the 6 items:

    Tomato Soup
    ---------------
    Total: 1000
    Burned: 14
    % Left: 98.6
    
    Total Holder Wallets: 508
    Top Holders:
    -----
    GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp: 68, 6.80% (MagicEden)
    7NejjRHwW91LCHeW3soGfDJW4gR54s9WPS54khmdxMb9: 26, 2.60%
    BACJ68NuawFRuMbg5d4ooeSwoXZrHUeif88ocw7tBM5P: 22, 2.20%
    DApMC6Wn1HGWViVmjG2EVUQCGyXnon9manzFWrTjrvGu: 19, 1.90%
    GtVyQ49T3v6ELg2qPqY1KtdP9nkGkZuDbnXkaUrQQU8T: 15, 1.50%
    trshC9cTgL3BPXoAbp5w9UfnUMWEJx5G61vUijXPMLH: 14, 1.40%
    8hYxFkcGgeBN32atnLymRkEGP3uMYMz7tsZRWU1yezJg: 14, 1.40%
    8DUNm14fTqbxbXqJzLvxXtM2hC5cAr6Cf4Pcx5t8nDLM: 12, 1.20%
    BwTsrCysuz4UrNjzFyBtgkVJeB11KvaTBWNWKbkCazkE: 10, 1.00%
    8TtZrVnYA4WSqjcaBH56J42vxzx1bfB17FQE3YndrCHm: 10, 1.00%

## Setup

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
You also need to create a `.env` file in the directory containing your Pastebin dev API key:

    PASTEBIN_API_KEY = <your_api_key_value>

## Usage
    usage: tt_analyzer.py [-h] [-i ITEM_NAME] SNAPSHOT_FILE
    
    positional arguments:
      SNAPSHOT_FILE  file to read the CSV snapshot from
    
    optional arguments:
      -h, --help     show this help message and exit
      -i ITEM_NAME   Print all item details and holder wallets for just a single item

## Examples

### Fetching snapshot data to feed into the script, using [Solana NFT snapshotting tool](https://github.com/bill-hewitt/python_solana_nft_snapshot)
The first time running the snapshot requires fetching the token list, which takes a bit of time. Run this from your `python_solana_nft_snapshot` checkout:

    % python nft_snapshot.py -ts --cmid=CApZmLZAwjTm59pc6rKJ85sux4wCJsLS7RMV1pUkMeVK -f trash_snap.csv tokenlist_trash.txt

You can simply refresh the snapshot every time you want updated data after that, which should be much faster:

    % python nft_snapshot.py -s -f trash_snap.csv --bust-cache tokenlist_trash.txt

### Running the analyzer script
Run the analyzer by pointing it to the snapshot you produced in the previous steps. Run this from your `trash_trap_analyzer` directory
(example assumes you cloned `python_solana_nft_snapshot` and `trash_trap_analyzer` repos from the same directory):

    % python tt_analyzer.py ../python_solana_nft_snapshot/tokenlist_trash.txt

If you want the full list of holder wallets for a particular game item, you can pass -i with the item name:

    % python tt_analyzer.py -i "Juice Box" ../python_solana_nft_snapshot/trash_snap.csv

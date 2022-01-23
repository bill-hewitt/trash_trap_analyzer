"""Analyzes a CSV snapshot of holder data (from https://github.com/bill-hewitt/python_solana_nft_snapshot)
to determine the state of the various items in the Degen Trash Pandas Pit's Trash Trap mini-game.

Prints the results to the console and uploads a guest Pastebin, then prints the link.
"""

import requests
from argparse import ArgumentParser
from datetime import datetime, timezone
from dotenv import dotenv_values


# List of marketplaces, from https://github.com/theskeletoncrew/air-support/blob/main/1_record_holders/src/main.ts
MARKETPLACE_WALLETS = {
    "GUfCR9mK6azb9vcpsxgXyj7XRPAKJd4KMHTTVvtncGgp": "MagicEden",
    "3D49QorJyNaL4rcpiynbuS3pRH4Y7EXEM6v6ZGaqfFGK": "Solanart",
    "4pUQS4Jo2dsfWzt3VgHXy3H6RYnEDd11oWPiaM2rdAPw": "AlphaArt",
    "F4ghBzHFNgJxV4wEQDchU5i7n4XWWMBSaq7CuswGiVsr": "DigitalEyes",
}
ITEM_NAMES_BY_RARITY = [
    "Tomato Soup",
    "Pandos",
    "McDegens Paper Bag",
    "Cardboard Box",
    "Beer Can",
    "Juice Box",
]


def main(filename: str, pastebin_api_key: str, item_name: str = None):
    with open(filename) as infile:
        # Burn the header line
        lines = infile.readlines()
    lines.pop(0)

    item_data = {}
    for line in lines:
        data = line.split(",")
        name = data[2]
        holder = data[4]

        if not item_data.get(name):
            item_data[name] = {"total": 0, "burned": 0, "holders": {}}

        cur_item = item_data[name]
        cur_item["total"] += 1
        if holder == "trshC9cTgL3BPXoAbp5w9UfnUMWEJx5G61vUijXPMLH":
            cur_item["burned"] += 1

        if not cur_item["holders"].get(holder):
            cur_item["holders"][holder] = 0
        cur_item["holders"][holder] += 1

    output = ""
    if item_name:
        item = item_data[item_name]
        item["holders"] = sort_dict_by_values(item["holders"], reverse=True)
        output += construct_item_details_string(item_name, item)
    else:
        for name in ITEM_NAMES_BY_RARITY:
            item = item_data[name]
            item["holders"] = sort_dict_by_values(item["holders"], reverse=True)
            output += construct_item_details_string(name, item, 10)
    print(output)

    url = "https://pastebin.com/api/api_post.php"
    post_data = {
        "api_option": "paste",
        "api_dev_key": pastebin_api_key,
        "api_paste_name": "Trash Trap Snapshot, {}".format(
            datetime.now(timezone.utc).isoformat(sep=" ", timespec="seconds")
        ),
        "api_paste_code": output,
    }

    resp = requests.post(url, data=post_data)
    print(f"Pastebin URL: {resp.text}")


def sort_dict_by_values(dictionary: dict, reverse: bool = False):
    """Sort a dictionary by its values (default ascending)"""
    holder_list = sorted(((v, k) for (k, v) in dictionary.items()), reverse=reverse)
    return dict([(k, v) for (v, k) in holder_list])


def construct_item_details_string(name: str, item: dict, holder_count: int = None) -> str:
    output = f"{name}\n---------------\n"
    output += "Total: {}\n".format(item["total"])
    output += "Burned: {}\n".format(item["burned"])
    output += "% Left: {}\n".format((1 - item["burned"] / item["total"]) * 100)
    output += "\nTotal Holder Wallets: {}\n".format(len(item["holders"]))
    output += "Top Holders:\n-----\n"
    for holder, count in item["holders"].items():
        percent = count / item["total"] * 100
        marketplace_suffix = (
            " (" + MARKETPLACE_WALLETS[holder] + ")" if holder in MARKETPLACE_WALLETS else ""
        )
        output += "{}: {}, {:.2f}%{}\n".format(holder, count, percent, marketplace_suffix)
        if holder_count is not None:
            holder_count -= 1
            if holder_count == 0:
                break
    output += "\n"
    return output


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "filename", metavar="SNAPSHOT_FILE", type=str, help="file to read the CSV snapshot from"
    )
    parser.add_argument(
        "-i",
        dest="item_detail",
        help="Print all item details and holder wallets for just a single item",
        metavar="ITEM_NAME",
    )

    args = parser.parse_args()
    if args.item_detail is not None and args.item_detail not in ITEM_NAMES_BY_RARITY:
        print(f"Please enter a valid item name: {ITEM_NAMES_BY_RARITY}")
        exit(1)
    main(args.filename, dotenv_values(".env")["PASTEBIN_API_KEY"], args.item_detail)

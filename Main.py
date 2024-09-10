import requests
import os
import json
import asyncio


def get_card_info():
    save_path = "C:\\YGOImages"
    os.chdir("C:\\")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    try:
        response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
        return response.json()['data'],save_path
    except: pass

async def download_image(url, save_in_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error on a bad status
        with open(save_in_path, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {save_in_path}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")


async def download_card(card, save_path):
    folder = ''
    if type(card['card_images'][0]['image_url']) != "none":
        url = card['card_images'][0]['image_url']
        # Characters to remove
        chars_to_remove = '/[/\\?%*:|"<>]/g'
        # Create translation table
        translation_table = str.maketrans('', '', chars_to_remove)
        filename = card['name'].translate(translation_table)
        if "onster" in card['type']:
            folder = "Monsters"
        else:
            folder = "Spells_Traps"

        n = url.rfind('.')
        extension = url[n:]
        save_path = os.path.join(save_path, folder, filename + extension)
        await download_image(url, save_path)

async def yugioh_downloader():
    cards_to_download = 15
    data, save_path = get_card_info()
    while True:
        last_idx = 0
        card_batch = [download_card(card, save_path) for card in data[last_idx: last_idx + cards_to_download]]
        await asyncio.gather(*card_batch)
        last_idx += cards_to_download
        print("Sleeping one second.")
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(yugioh_downloader())
import random
import traceback

from better_proxy import Proxy
from loguru import logger
import asyncio

from get_extension_id import get_ext_id
from settings import concurrent_tasks, PROFILES_PATH, PROXIES_PATH
from utils import get_accounts_from_excel, print_stats, get_list_from_txt


async def task(profile, profiles_stats, new_, no_green_id, semaphore, lock, subscribe):
    while True:
        try:
            result = await profile.process(profiles_stats, new_, no_green_id, semaphore, lock, subscribe)
            if result == 'Proxy failure!':
                proxy: Proxy = Proxy.from_str(random.choice(get_list_from_txt(PROXIES_PATH)))
                logger.debug(f'Changing {profile.name} proxy to {proxy.as_url.strip()}')
                result = await profile.process(profiles_stats, new_, no_green_id, semaphore, lock, subscribe, proxy.as_playwright_proxy)
            break  # Запилил такую конструкцию для того чтобы если с профилем какие-то траблы он пытался еще раз

        except Exception as ex:
            traceback.print_exc()
            await asyncio.sleep(.3)
            logger.error(f'Name: {profile.name} {ex}')
            continue


async def main():
    profiles_stats = []
    semaphore = asyncio.Semaphore(concurrent_tasks)
    lock = asyncio.Lock()
    subscribe = False
    new_acc = False
    no_green_id = False
    try:
        match int(input('Menu: \n'
                        '1) Create new accounts on Mint Forest \n'
                        '2) Maintain accounts until Green ID is minted (skip social tasks)\n'
                        '3) !!! Regular launch with all activities \n'
                        '4) Get your EXTENTION_IDENTIFIER \n'
                        '5) Subscribe for usernames on X\n'
                        '> ')):
            case 1:
                new_acc = True
                no_green_id = True
            case 2:
                new_acc = False
                no_green_id = True
            case 3:
                new_acc = False
                no_green_id = False
            case 4:
                print('extension ID: ', await get_ext_id())
                return
            case 5:
                subscribe = True

        profiles = get_accounts_from_excel(PROFILES_PATH)
        random.shuffle(profiles)
        tasks = [asyncio.create_task(task(profile, profiles_stats, new_acc, no_green_id, semaphore, lock, subscribe)) for profile
                 in profiles]
        if len(tasks) == 0:
            logger.error(f"Can't get profiles from the 'not_done' sheet. Please check /user_files/profiles.xlsx")

        logger.info(f"Starting {len(tasks)} tasks")
        await asyncio.wait(tasks)

        print_stats(profiles_stats)

    except (UnicodeDecodeError, KeyboardInterrupt):
        print('\nThank you for using this software!')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt):
        pass

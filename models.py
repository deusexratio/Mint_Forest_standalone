import os
from asyncio import Semaphore, Lock
import random

from better_proxy import Proxy
from patchright.async_api import async_playwright
from pydantic import BaseModel
from loguru import logger

import settings


# class Profile(BaseModel):
#     id: int
#     name: str
#     seed: str
#     password: str
#     ref_code: str | None
#     proxy: str | None
#     user_dir: str
#
#     def __repr__(self):
#         return (f"Name: {self.name} | bubble_amount: {self.bubble_amount}, "
#                 f"tasks_done: {self.tasks_done}, total_win_amount: {self.total_win_amount}")


class Profile:
    def __init__(self, name: str, proxy: str | None, seed: str, ref_code: str | None, cookie: dict | None, x_username: str | None):
        from utils import touch

        self.name = str(name)

        if proxy:
            self.proxy = Proxy.from_str(proxy)

        self.seed = seed

        self.ref_code = ref_code

        self.cookie = cookie

        self.user_dir = os.path.join(settings.USER_FILES_FOLDER, 'profile_browsers', self.name)
        touch(self.user_dir)

        self.x_username = x_username

        self.bubble_amount = 0
        self.tasks_done = 0
        self.total_win_amount = 0
        self.reg = False

    def __repr__(self):
        return f"Name: {self.name} | proxy: {self.proxy}, tasks_done: {self.cookie}"

    async def process(self, profiles_stats: list, new: bool, no_green_id: bool, semaphore: Semaphore, lock: Lock, subscribe):
        from utils import write_results_for_profile, move_profile_to_done
        from mint_forest import Mint

        async with semaphore:
            async with async_playwright() as p:
                if settings.PROXY:
                    proxy = self.proxy.as_playwright_proxy

                args: list = [
                    f"--disable-extensions-except={settings.EXTENTION_PATH}",
                    f"--load-extension={settings.EXTENTION_PATH}",
                    f"--lang=en-US",
                    f"--mute-audio"
                ]

                if settings.HEADLESS:
                    args.append(f"--headless=new")

                if settings.USE_FIXED_VIEWPORTS:
                    viewport = random.choice(settings.VIEWPORTS)
                    context = await p.chromium.launch_persistent_context(
                        user_data_dir=self.user_dir,
                        channel='chrome',
                        headless=settings.HEADLESS,
                        args=args,
                        proxy=proxy,
                        slow_mo=settings.SLOW_MO,
                        viewport=viewport,
                        user_agent=settings.USER_AGENT,
                    )

                else:
                    context = await p.chromium.launch_persistent_context(
                        user_data_dir=self.user_dir,
                        channel='chrome',
                        headless=settings.HEADLESS,
                        args=args,
                        proxy=proxy,
                        slow_mo=settings.SLOW_MO,
                        no_viewport=True,
                        user_agent=settings.USER_AGENT,
                    )

                await context.add_cookies([self.cookie])

                mint = Mint(context, self)

                if subscribe:
                    await mint.subscribe()
                    return

                await mint.restore_rabby_wallet()
                await mint.unlock_rabby()

                if new and no_green_id:
                    await mint.register_account(self.ref_code)
                    self.bubble_amount = await mint.daily_bubble()
                    # if bubble_amount == 0:
                    #     amount_to_bridge = await mint.relay()
                    #     bubble_amount = await mint.daily_bubble()
                    self.reg = True

                elif no_green_id:
                    await mint.all_preparations()

                    # Пока не делаю твиттер таски на новорегах потому что там селектора другие если нет грин айди
                    self.bubble_amount = await mint.daily_bubble()
                    # tasks_done = await mint.mint_socials(no_green_id)
                    self.total_win_amount = await mint.lucky_roulette(no_green_id)
                    await mint.spend_mint_energy()

                else:
                    await mint.all_preparations()

                    self.bubble_amount = await mint.daily_bubble()
                    # if bubble_amount == 0:
                    #     return False
                    self.tasks_done = await mint.mint_socials()
                    self.total_win_amount = await mint.lucky_roulette()
                    await mint.spend_mint_energy()

            result = Result(name=str(self.name), bubble_amount=int(self.bubble_amount),
                            tasks_done=int(self.tasks_done), total_win_amount=int(self.total_win_amount), reg=self.reg)

            profiles_stats.append(result)
            async with lock:
                write_results_for_profile(settings.RESULTS_PATH, self, result)
                move_profile_to_done(settings.PROFILES_PATH, self)

            logger.success(f'Name: {self.name} done')
            await context.close()


class Result(BaseModel):
    name: str
    bubble_amount: int
    tasks_done: int
    total_win_amount: int
    reg: bool

    def __repr__(self):
        return (f"Name: {self.name} | bubble_amount: {self.bubble_amount}, "
                f"tasks_done: {self.tasks_done}, total_win_amount: {self.total_win_amount}, reg: {self.reg}")

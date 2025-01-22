import os
import asyncio

from patchright.async_api import async_playwright, Playwright, BrowserContext
from loguru import logger

import settings


async def get_extension_id(context: BrowserContext, extension_name: str) -> str | None:
    """
    Gets the extension id from the installed applications page chrome://extensions/
    :param context: BrowserContext
    :param extension_name: str
    :return: Extension ID: str
    """
    logger.debug(f'GETTING "{extension_name}" EXTENSION ID')
    page = await context.new_page()
    try:
        await page.goto('chrome://extensions/')
        session = await context.new_cdp_session(page)

        response = await session.send('Runtime.evaluate', {
            'expression': """
        new Promise((resolve) => {
            chrome.management.getAll((items) => {
                resolve(items);
            });
        });
    """,
            'awaitPromise': True
        })


        object_id = response['result']['objectId']

        # Get the properties of the extension array
        properties_response = await session.send('Runtime.getProperties', {
            'objectId': object_id,
            'ownProperties': True  # Получаем только собственные свойства
        })
        logger.debug(properties_response)
        # Extracting extension data
        extensions = []
        for prop in properties_response['result']:
            if 'value' in prop and prop['value']['type'] == 'object':
                extension = prop['value']
                # Extracting the properties of the extension
                extension_properties = await session.send('Runtime.getProperties', {
                    'objectId': extension['objectId'],
                    'ownProperties': True
                })

                logger.debug(extension_properties)

                # Save the extension data
                extension_data = {}
                for ext_prop in extension_properties['result']:
                    if 'value' in ext_prop:
                        extension_data[ext_prop['name']] = ext_prop['value'].get('value', None)
                extensions.append(extension_data)

        # Search for the required extension and return its ID
        for extension in extensions:
            if extension_name.lower() in extension.get("name").lower():
                app_id = extension.get("id")
                logger.success(f'{extension_name} EXTENSION ID: {app_id}')
                return app_id
    except Exception as ex:
        logger.error(f'{extension_name} EXTENSION ID NOT FOUND')
        return None
    # finally:
    #     await page.close()


path_to_extension = settings.EXTENTION_PATH
user_data_dir = ''


async def run(playwright: Playwright):
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        args=[
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
    )

    ext_id = await get_extension_id(context=context, extension_name='Rabby')

    await context.close()
    return ext_id


async def get_ext_id():
    async with async_playwright() as playwright:
        ext_id = await run(playwright)
        return ext_id


# asyncio.run(main())

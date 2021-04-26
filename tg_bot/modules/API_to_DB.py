import json
import requests

from tg_bot.db.models import Region, Category, Form


async def update_regions():
    regions = json.loads(requests.get('https://cptgrants.org/api/regions/').content.decode('utf-8'))
    for region in regions:
        await Region.get_or_create(code=region["code"],
                                   name=region["name"])


async def update_categories():
    categories = json.loads(requests.get('https://cptgrants.org/api/categories/').content.decode('utf-8'))
    for category in categories:
        await Category.get_or_create(name=category["name"])


async def update_forms():
    forms = json.loads(requests.get('https://cptgrants.org/api/forms/').content.decode('utf-8'))
    for form in forms:
        await Form.get_or_create(name=form["name"])



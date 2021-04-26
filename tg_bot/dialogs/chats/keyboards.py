from ...db.models import Category, Form
from ...modules.keyboard import KeyboardInline, KeyboardReply
from itertools import islice

def chunks(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}

region = lambda: KeyboardInline([{"Выбрать регион": "in_q"}]).get()


async def form():
    forms = await Form.all()
    return KeyboardInline([{f.name: str(f.id) for f in forms}]).get()


async def type_category():
    categories = await Category.all()
    return KeyboardInline([{c.name: str(c.id) for c in categories}]).get()

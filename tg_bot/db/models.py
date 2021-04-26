from tortoise.models import Model
from tortoise import fields


class BotUser(Model):
    tg_id = fields.BigIntField(default=0)
    username_or_full_name = fields.CharField(max_length=200, default="")
    region = fields.ForeignKeyField("models.Region", "bot_users")
    category = fields.ForeignKeyField("models.Category", "bot_users")
    form = fields.ForeignKeyField("models.Form", "bot_users")

    def __str__(self):
        return str(self.username_or_full_name)


class Region(Model):
    code = fields.CharField(max_length=10)
    name = fields.CharField(max_length=250)


class Category(Model):
    name = fields.CharField(max_length=250)


class Form(Model):
    name = fields.CharField(max_length=250)

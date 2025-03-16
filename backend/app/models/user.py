from tortoise import models, fields


class User(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255, null=True)
    username = fields.CharField(max_length=255, null=True)
    photo_url = fields.CharField(max_length=512, null=True)
    birthday = fields.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''} (@{self.username})"

from tortoise import fields, models


class UserProfile(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50, null=True)
    username = fields.CharField(max_length=50, null=True)
    birth_date = fields.DateField(null=True)

    class Meta:
        table = "user_profiles"

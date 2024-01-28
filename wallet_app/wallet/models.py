from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class RecordModel(models.Model):
    type = models.CharField(max_length=40)
    category = models.CharField(max_length=40, default=None)
    sub_category = models.CharField(max_length=40, default=None)
    payment = models.CharField(max_length=40)
    amount = models.FloatField()
    date = models.DateField(
        auto_now_add=True
    )
    time = models.TimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return "{}. {} - {} - {} - {}".format(self.id, self.type, self.category, self.payment, self.amount, self.user)

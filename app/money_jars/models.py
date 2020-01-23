from django.db import models


class TimestampedModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class Currency(TimestampedModel):
    code = models.TextField()

    name = models.TextField(
        null=True,
        blank=True
    )
    symbol = models.TextField(
        null=True,
        blank=True
    )

    value = models.FloatField(
        help_text="abstract number related with currency to represent currency value and achieve exchange"
        # decimal_places=2
    )

    def __str__(self):
        return f'{self.code} {self.name}'


class Jar(TimestampedModel):
    name = models.CharField(
        unique=True,
        db_index=True,
        max_length=255
    )
    amount = models.FloatField(
        # decimal_places=2
        default=0
    )
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.PROTECT,
    )

    # TODO: add owner (user)
    # owner =
    # value = # currency value * amount

    def __str__(self):
        return f'{self.name} {self.currency.code}'


class Operation(TimestampedModel):
    jar = models.ForeignKey(
        to=Jar,
        on_delete=models.PROTECT,
    )

    amount_before = models.FloatField(
        # decimal_places=2
    )
    amount_after = models.FloatField(
        # decimal_places=2
    )
    amount_operation = models.FloatField(
        # decimal_places=2
    )

    # TODO: income outcome
    # operation_type =
    # planned_time =
    # value = # currency value * operation amount

    def __str__(self):
        return f'{self.updated} {self.jar} {self.amount_operation}'


class Transaction(TimestampedModel):
    title = models.TextField(
        null=True,
        blank=True
    )
    deposit = models.ForeignKey(
        to=Operation,
        related_name='deposit',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    withdraw = models.ForeignKey(
        to=Operation,
        related_name='withdraw',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.PROTECT,
    )

    # planned_time =

    def __str__(self):
        return f'{self.created} {self.title}'

# TODO: add exchange to transfer different currencies between jars
# class Exchange(TimestampedModel):
#     transaction = models.ForeignKey(
#         to=Operation,
#         on_delete=models.PROTECT,
#         # null=True,
#         # blank=True
#     )
#     target_currency = models.ForeignKey(
#         to=Currency,
#         on_delete=models.PROTECT,
#         # null=True,
#         # blank=True
#     )

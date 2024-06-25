from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, related_name='branch_organizations', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tallon(models.Model):
    TALLON_NUMBER_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('1, 2', '1, 2'),
        ('1, 3', '1, 3'),
        ('2, 3', '2, 3'),
        ('1, 2, 3', '1, 2, 3'),
    ]
    fullname = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT)
    position = models.CharField(max_length=250)
    date_received = models.DateField()
    tallon_number = models.CharField(max_length=30, choices=TALLON_NUMBER_CHOICES)
    reason_received = models.CharField(max_length=255)
    discipline_order = models.CharField(max_length=50)
    discipline_order_date = models.DateField()
    discipline_type = models.CharField(max_length=255)
    consequence_amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullname

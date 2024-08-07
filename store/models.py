from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
   category = models.CharField(max_length=100, null=True, blank=True)
   name=models.CharField(max_length=100)
   quantity=models.PositiveIntegerField()
   created_by=models.ForeignKey(User, on_delete=models.DO_NOTHING)
   created_date=models.DateTimeField(auto_now_add=True)
   initial_quantity=models.PositiveIntegerField(null=True, blank=True)
   comment = models.CharField(max_length=100, null=True, blank=True)



   def __str__(self):
       return self.name


class IssueItem(models.Model):
    dept_choices=(
        ('Field','Field'),
        ('Security','Security'),
        ('Unused', 'Unused'),
        ('Routine destination', 'Routine destination'),
        ('Will be return back', 'Will be return back')
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    issued_quantity = models.PositiveIntegerField()
    issued_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    issued_to = models.CharField(max_length=100)
    department=models.CharField(max_length=30, choices=dept_choices)
    issued_date = models.DateTimeField(auto_now_add=True)
    return_date=models.DateTimeField()
    is_returned=models.BooleanField(default=False)
    comment_more = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return f'{self.item}-{self.issued_to}'


class ReturnItem(models.Model):
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
    returned_date=models.DateTimeField(auto_now_add=True)
    returned_quantity=models.PositiveIntegerField()
    all_items_returned=models.BooleanField(default=False)
    returned_by=models.CharField(max_length=100)
    comment_more = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.item}-{self.returned_by}'

class RestockItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp=models.DateTimeField(auto_now_add=True)
    initial_value=models.PositiveIntegerField(null=True, blank=True)
    comment_more = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
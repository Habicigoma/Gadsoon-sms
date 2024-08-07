from django import forms
from .models import Item, IssueItem,RestockItem, ReturnItem

class AddItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['category','name','quantity','comment']

    def clean_category(self):
        category=self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError('this field is required')
        return category


    def clean_name(self):
        name=self.cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('this field is required')

        for instance in Item.objects.all():
           if instance.name == name:
            raise forms.ValidationError(name + ' is already created')

        return name



class UpdateItemForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['name','quantity','category','comment']

class IssueItemForm(forms.ModelForm):
    class Meta:
        model=IssueItem
        fields=['item','issued_quantity','issued_to','department','return_date','comment','comment_more']

class ReturnItemForm(forms.ModelForm):
    class Meta:
        model=ReturnItem
        fields=['item', 'returned_quantity','returned_by','comment','comment_more']

class RestockItemForm(forms.ModelForm):
    class Meta:
        model=RestockItem
        fields=['item', 'quantity','comment','comment_more']


class ItemSearchForm(forms.ModelForm):
    export_to_csv=forms.BooleanField(required=False)
    class Meta:
        model=Item
        fields=['category']


from django.shortcuts import render, redirect
from django.contrib import messages
from .form import AddItemForm, UpdateItemForm, IssueItemForm, ReturnItemForm, RestockItemForm
from .models import Item, IssueItem, ReturnItem, RestockItem
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import AddItemForm, UpdateItemForm, IssueItemForm, ReturnItemForm, RestockItemForm, ItemSearchForm
from .models import Item, IssueItem, ReturnItem, RestockItem
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
import csv
from django.http import HttpResponse
# Create your views here.


def add_item(request):
    if request.method=='POST':
        form=AddItemForm(request.POST or None)
        if form.is_valid():
            var=form.save(commit=False)
            var.created_by=request.user
            var.initial_quantity=var.quantity
            var.save()
            messages.info(request, 'New Item has been added to the store')
            return redirect('all_items')
        else:
            messages.warning(request,'Something went wrong')
            return redirect('add_item')
    else:
        form=AddItemForm()
        context={'form':form}
        return render(request, 'store/add_item.html', context)





def update_item(request, pk):
    item=Item.objects.get(pk=pk)
    if request.method=='POST':
        form=UpdateItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.info(request, 'Item info has been updated')
            return redirect('all_items')
        else:
            messages.warning(request,'Something went wrong')
            #return redirect('add-items')
    else:
        form=UpdateItemForm(instance=item)
        context={'form':form}
        return render(request, 'store/update_item.html', context)


def all_items(request):
    items=Item.objects.all()
    title='LIST OF ITEMS'
    form=ItemSearchForm(request.POST or None)

        # set up pagination
    stock = Item.objects.all()
    paginator = Paginator(items,5)
    page=request.GET.get('page')
    try :
        items=paginator.page(page)
    except PageNotAnInteger:
        items=paginator.page(1)
    except EmptyPage:
        items=paginator.page(paginator.num_pages)

    context={
        'items':items,
        'page': page,
        'title':title,
        'form':form,
        'stock':stock
    }

    if request.method=='POST':
        items=Item.objects.filter(category__icontains=form['category'].value(),
                                     # name__icontains=form['name'].value()
                                      )
        if form['export_to_csv'].value()==True:
            response=HttpResponse(content_type='text/csv')
            response['Content-Disposition']='attachment; filename="list of items.csv"'
            writer=csv.writer(response)
            writer.writerow(['CATEGORY','ITEM NAME','QUANTITY', 'COMMENT'])
            instance=items
            for stock in instance:
                 writer.writerow([stock.category,stock.name,stock.quantity,stock.comment])
            return response
        context={
            'form':form,
            'title':title,
            'items':items
        }


    return render(request, 'store/all_items.html', context)

"""
def delete_item(request, pk):
    item=Item.obejects.get(pk=pk)
    if request.method=='POST':
        item.delete()
        messages.info(request, 'Item has been deleted')
        return redirect('/all_items')
    context={'item':item}
    return render(request, 'store/delete_item.html',context)
"""

def delete_item(request, pk):
    item=Item.objects.get(pk=pk)
    if request.method=='POST':
        item.delete()
        messages.info(request, 'Item has been deleted')
        return redirect('/store/all_items')
    return render(request, 'store/delete_item.html')






def issue_item(request):
    if request.method =='POST':
        form=IssueItemForm(request.POST)
        if form.is_valid():
            var=form.save(commit=False)
            var.issued_by=request.user
            get_item=Item.objects.get(pk=var.item.pk)
            if get_item.quantity !=0:
                if get_item.quantity >= var.issued_quantity:
                    get_item.quantity=get_item.quantity - var.issued_quantity
                    get_item.save()
                    var.save()
                    messages.info(request, f'Item has been issued to {var.issued_to}')
                    return redirect('all_items')
                else:
                    messages.warning(request, f'No much items remaining in the store! We only have {get_item.quantity} left!')
                    return redirect('all_items')
            else:
                messages.warning(request,'No item in the store')
                return redirect('all_items')

        else:
            messages.warning(request, 'Something went wrong')
            return redirect('issue_item')
    else:
        form=IssueItemForm()
        context= {'form':form}
        return render(request,'store/issue_item.html', context)

def issue_history(request):
    items=IssueItem.objects.all().order_by('-issued_date')
    paginator = Paginator(items, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context={'items':items, 'page':page}

    return render(request, 'store/issue_history.html', context)


def return_item(request): #not used in this app
    if request.method=='POST':
        form=ReturnItemForm(request.POST)
        if form.is_valid():
            var=form.save(commit=False)
            get_item=Item.objects.get(pk=var.item.pk)
            get_item.quantity=get_item.quantity + var.returned_quantity
            get_item.save()
            var.save()
            messages.info(request, 'The item has been received in the store')
            return redirect('all_items')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('return_item')
    else:
        form=ReturnItemForm()
        context={'form':form}
        return render(request, 'store/return_item.html', context)

def return_history(request):
    items=ReturnItem.objects.all()

    paginator = Paginator(items, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context={'items':items, 'page':page}
    return render(request, 'store/return_history.html', context)


def restock_item(request):
    if request.method=='POST':
        form=RestockItemForm(request.POST)
        if form.is_valid():
            var=form.save(commit=False)
            get_item=Item.objects.get(pk=var.item.pk)
            var.initial_value=get_item.initial_quantity
        #   get_item.initial_quantity = get_item.initial_quantity + var.quantity
            get_item.quantity = get_item.quantity + var.quantity
            get_item.save()
            var.save()
            messages.info(request,'Item has been received in the store.')
            return redirect('all_items')
        else:
            messages.warning(request, 'Something went wrong')
            return redirect('restock_item')
    else:
        form=RestockItemForm()
        context={'form':form}
        return render(request, 'store/restock_item.html', context)

def restock_history(request):
    items=RestockItem.objects.all()

    paginator = Paginator(items, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context={'items':items, 'page':page }
    return render(request, 'store/restock_history.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from todos.models import TodoList, TodoItem
from todos.forms import CreateForm, ItemCreateForm

# Create your views here.
def todo_list_list(request):
    todo_lists = TodoList.objects.all()
    for todo_list in todo_lists:
        todo_list.item_count = todo_list.items.count()
    context = {
        "todo_list_object": todo_lists,
    }
    return render(request, "todos/todos.html", context)

def todo_list_detail(request, id):
    todo_list = get_object_or_404(TodoList, id=id)
    todo_items = todo_list.items.all()
    context = {
        "todo_list": todo_list,
        "todo_items": todo_items,
    }
    return render(request, "todos/detail.html", context)

def todo_list_create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            todo_list = form.save()
            return redirect("todo_list_detail", id=todo_list.id)
    else:
        form = CreateForm()
    context = {
        "form": form
    }
    return render(request, "todos/create.html", context)

def todo_list_update(request, id):
    todo_list = get_object_or_404(TodoList, id=id)
    if request.method == "POST":
        form = CreateForm(request.POST, instance=todo_list)
        if form.is_valid():
            todo_list = form.save()
            return redirect("todo_list_detail", id=todo_list.id)
    else:
        form = CreateForm(instance=todo_list)
    context = {
        "todo_list": todo_list,
        "form": form,
    }
    return render(request, "todos/update.html", context)

def todo_list_delete(request, id):
    todo_list = TodoList.objects.get(id=id)
    if request.method == "POST":
        todo_list.delete()
        return redirect("todo_list_list")
    return render(request, "todos/delete.html")

def todo_item_create(request):
    if request.method == "POST":
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            item = form.save()
            return redirect("todo_list_detail", id=item.list.id)
    else:
        form = ItemCreateForm()
    context = {
        "form": form
    }
    return render(request, "todos/itemcreate.html", context)

def todo_item_update(request, id):
    todo_item = get_object_or_404(TodoItem, id=id)
    if request.method == "POST":
        form = ItemCreateForm(request.POST, instance=todo_item)
        if form.is_valid():
            todo_item = form.save()
            return redirect("todo_list_detail", id=todo_item.list.id)
    else:
        form = ItemCreateForm(instance=todo_item)
    context = {
        "form": form,
    }
    return render(request, "todos/itemupdate.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView, TemplateView, UpdateView, DetailView, DeleteView
from Warehouse.forms import IncomingProductForm
from Warehouse.models import Category, Product, IncomingProduct


# Create your views here.
class CreateCategory(CreateView):
    model = Category
    template_name = "Warehouse/create_category.html"
    fields = ('parent','name',)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.parent is None:
            return reverse_lazy('listcategory', kwargs={'pk': self.object.pk})
        else:
            cat = self.object.get_ancestors().filter(parent=None).first()
            return reverse_lazy('listcategory', kwargs={'pk': cat.pk})


class CreateProduct(CreateView):
    model = Product
    template_name = "Warehouse/create-product.html"
    fields = ('name', 'category', 'price', 'quantity',)

    def get_success_url(self):
        return reverse_lazy('list', kwargs={'pk': self.object.category.pk})

    def form_valid(self, form):
        form.instance.availability = True
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ListCategory(DetailView):
    model = Category
    template_name = "Warehouse/list_category.html"

    def get_queryset(self):
        category = Category.objects.filter(pk=self.kwargs['pk'])
        return category


class ListProduct(DetailView):
    model = Category
    template_name = "Warehouse/detail_category.html"
    context_object_name = "products"


class IncomingProductCreate(CreateView):
    template_name = 'Warehouse/incoming_product.html'
    form_class = IncomingProductForm

    def form_valid(self, form):
        products = get_object_or_404(Product, pk=form.instance.product.pk)
        products.quantity += form.instance.quantity
        products.save()
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list', kwargs={'pk': self.object.product.category.pk})

# Create your views here.

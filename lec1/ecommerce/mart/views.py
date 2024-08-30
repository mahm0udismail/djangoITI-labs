from django.utils.http import urlencode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods
from prodects.models import Product

# In-memory dictionary to store data
data_store = {"mahmoud":"1",
              "ismail":"2",
              }


def get_data(request):
  if request.method == "POST":
    selected_products = request.POST.getlist('products')
    query_string = urlencode({'options': selected_products})
    return redirect(f'/mart/add-data/?{query_string}')

  return render(request, 'data_display.html', {'data': data_store})


def add_data(request):
  selected_products = request.GET.getlist('options')
  return HttpResponse(f'Selected products: {selected_products}')


def product_list(request):
    # Fetch all products from the products app
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
    
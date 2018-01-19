from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render, redirect
from .forms import CheckoutContactForm
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from orders import context_processors


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        pass
    else:
        total_price = "{0}".format(int(data['price']) * int(data['nmb']))
        request.session['cart'].append({"product_id": data['product_id'],
                                        "name_product": data['name_product'],
                                        "price": data['price'],
                                        "nmb": data["nmb"],
                                        "total_price": total_price})
    request.session.modified = True
    # common code for 2 cases
    products_in_basket = request.session.get('cart')
    products_total_nmb = len(products_in_basket)
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["product_id"] = item['product_id']
        product_dict["name_product"] = item['name_product']
        product_dict["price_per_item"] = item["price"]
        product_dict["nmb"] = item['nmb']
        product_dict['total_price'] = item['total_price']
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = request.session['cart']

    form = CheckoutContactForm(request.POST or None)
    if request.method == "POST":
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name})

            order = Order.objects.create(user=user, name_customer=name, phone_customer=phone, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)
                    print(type(value))

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    Product_Order.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                 price_per_item=product_in_basket.price_per_item,
                                                 total_price=product_in_basket.total_price,
                                                 order=order)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'orders/checkout.html', locals())


def basket_update(request):
    return_dict = dict()
    session_key = request.session.session_key
    data = request.POST
    if data.get("is_delete"):
        i = 0
        while i < len(request.session['cart']):
            if str(request.session['cart'][i].get('product_id')) in data.getlist("product_id_list[]"):
                request.session['cart'].pop(i)
            else:
                i += 1
    elif data.get('delete_all'):
        request.session['cart'].clear()
    else:
        product_id = data.get("product_id")
        total_price_all_products = 0.00
        for item in request.session['cart']:
            if int(product_id) == item['product_id']:
                item['numb'] = data.get('number')
                item["total_price"] = "{0:.2f}".format(
                    int(item['numb']) * float(item['price'].replace(",", ".")))
            total_price_all_products += float(item['total_price'].replace(",", "."))
        total_price_all_products = "{0:.2f}".format(total_price_all_products).replace(".", ",")
        return_dict['total_price_all_products'] = total_price_all_products
    request.session.modified = True
    return_dict["products"] = list()
    for item in request.session['cart']:
        product_dict = dict()
        product_dict["id"] = item["product_id"]
        product_dict["price_per_item"] = item["price"]
        product_dict["name"] = item["name_product"]
        product_dict["numb"] = item["nmb"]
        product_dict["total_price"] = "{0:.2f}".format(
            float(product_dict["price_per_item"].replace(",", ".")) * int(product_dict["numb"])).replace(".", ",")
        return_dict['products'].append(product_dict)
    return JsonResponse(return_dict)


class PrepareOrder(TemplateView):
    form = None
    template_name = "orders/prepare_order.html"

    def get(self, request, *args, **kwargs):
        self.form = CheckoutContactForm()
        return super(PrepareOrder, self).get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PrepareOrder, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['name_product'] = Product.objects.order_by("name_product")
        # context['brands'] = Brand.objects.order_by("name")
        # context['categorys'] = Category.objects.order_by("name")
        return context

    def post(self, request, *args, **kwargs):
        self.form = CheckoutContactForm(request.POST)
        total_price_all_products = 0
        for product_in_cart in request.session['cart']:
            total_price_all_products += int("{0}".format(
                int(product_in_cart["price"]) *
                int(product_in_cart["nmb"])
            ))
        self.form.total_price = total_price_all_products
        if self.form.is_valid():
            order = self.form.save()
            for product_in_cart in request.session['cart']:
                product = Product.objects.get(pk=product_in_cart['product_id'])
                total_price = int("{0}".format(
                    int(product_in_cart["price"]) *
                    int(product_in_cart["nmb"])
                ))
                # Нужно проверить Product_Order на совпадение полей, они должны быть одинаковыми, для того
                # Для того, чтобы сохранять заказ
                # Он почему-то жалуется, что используются фильтры (наши товары) (Артем)
                product_in_order = Product_Order.objects.create(order=order, product=product,
                                                                nmb=product_in_cart['nmb'],
                                                                price_per_item=product_in_cart["price"])
            request.session['cart'].clear()
            request.session.modified = True
            return render(request, "orders/thanks.html", locals())
        else:
            return super(PrepareOrder, self).get(request, *args, **kwargs)


def basket_del(request):
    #print(request.GET)
    i = 0
    while i < len(request.session['cart']):
        if request.session['cart'][i].get('product_id') in request.GET.getlist('is_del'):
            request.session['cart'].pop(i)
        else:
            i += 1
    request.session.modified = True
    return redirect("checkout")


def basket_del_all(request):
    request.session['cart'].clear()
    request.session.modified = True
    return redirect("checkout")

from django.shortcuts import render, redirect
from basic_app.forms import ProductForm
from django.contrib import messages
from firebase import firebase

import requests
from bs4 import BeautifulSoup


# Create your views here.
def saved(request):
    return render(request, "basic_app/saved.html", {})

def index(request):
    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid() and prod_valid(request.POST["product_url"]):
            # form.save()
            save_to_fb(request.POST)
            return redirect("/saved/")
        else:
            messages.info(request, "Invalid Product Link !")
            return redirect("/")
    else:
        form = ProductForm()
        return render(request, "basic_app/index.html", {"form":form})


def save_to_fb(data_dict):
    fb = firebase.FirebaseApplication("https://barcode-scanner-92b37.firebaseio.com/", None)
    data = {
        "product_name" : data_dict["product_name"],
        "product_url" : data_dict["product_url"],
        "target_price" : data_dict["target_price"],
        "your_email" : data_dict["your_email"]
    }

    fb.post("/Products/", data)
    print("saved data !!")

def prod_valid(url):
    USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/57.0.2987.110 '
                     'Safari/537.36'),  # chrome
                    ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/61.0.3163.79 '
                     'Safari/537.36'),  # chrome
                    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
                     'Gecko/20100101 '
                     'Firefox/55.0'),  # firefox
                    ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/61.0.3163.91 '
                     'Safari/537.36'),  # chrome
                    ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/62.0.3202.89 '
                     'Safari/537.36'),  # chrome
                    ('Mozilla/5.0 (X11; Linux x86_64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/63.0.3239.108 '
                     'Safari/537.36'),
                    ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'), ]

    for u in USER_AGENTS:
        HEADERS = {"User-Agent" : u}
        data = requests.get(url, headers=HEADERS).text
        soup = BeautifulSoup(data, "html.parser")

        title_item = soup.find(id="productTitle")
        title = ""

        if title_item:
            title = title_item.get_text().strip()
            return len(title) > 0

    return 0


###############################################

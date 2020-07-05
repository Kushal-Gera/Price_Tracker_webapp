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
    HEADERS = {"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}

    data = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(data, "html.parser")

    title_item = soup.find(id="productTitle")
    title = ""

    if title_item:
     title = title_item.get_text().strip()

    print(title)
    return len(title) > 0



###############################################

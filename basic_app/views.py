from django.shortcuts import render, redirect
from basic_app.forms import ProductForm
from django.contrib import messages

import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):

    if request.POST:
        form = ProductForm(request.POST)
        if form.is_valid() and prod_valid(request.POST["product_url"]):
            form.save()
            return redirect("/saved/")
        else:
            messages.info(request, "Invalid Product Link !")
            return redirect("/")
    else:
        form = ProductForm()
        return render(request, "basic_app/index.html", {"form":form})


def saved(request):
    return render(request, "basic_app/saved.html", {})


def prod_valid(url):
    HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}

    data = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(data, "html.parser")

    title = soup.find(id="productTitle").get_text().strip()

    return title != None



###############################################

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import csv
import sys
import os
from django.conf import settings
from recommender.models import Item, Review
import spacy
csv.field_size_limit(sys.maxsize)

def index(request):
    context = {}
    return render(request, 'recommender/index.html', context)

def load_data(request):
    with open(os.path.join(settings.BASE_DIR, 'DatafinitiElectronicsProductData.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count >= 1 and line_count%7 == 0:
                if len(Item.objects.filter(item_name = row[13])) == 0:
                    Item.objects.create(item_name = row[13], item_image = row[9].split(",")[0])
                item = Item.objects.get(item_name = row[13])
                Review.objects.create(review_item = item, review_text = row[22]+" "+row[21])
            line_count += 1
    with open('info.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for item in Item.objects.all():
            iteminfo = ""
            for review in Review.objects.all():
                if review.review_item == item:
                    iteminfo += " " + review.review_text
            writer.writerow([item.id, iteminfo])
    return redirect(index)

def get_info(request):
    if request.POST:
        info = request.POST.get("info", "")
        with open('info.csv') as csv_file:
            nlp = spacy.load("en_core_web_md")
            csv_reader = csv.reader(csv_file, delimiter=',')
            max_val = 1
            max_sim = -1
            for row in csv_reader:
                sim = nlp(info).similarity(nlp(row[1]))
                if sim > max_sim:
                    max_val = row[0]
                    max_sim = sim
            print(max_val)
        return redirect('/recommender/itemview/'+str(max_val))
    context = {}
    return render(request, "recommender/ask.html", context)

def item_info(request, idinp):
    context = {}
    item = Item.objects.get(id=idinp)
    context["name"] = item.item_name
    context["image"] = item.item_image
    return render(request, "recommender/iteminfo.html", context)

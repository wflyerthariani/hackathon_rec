from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
import csv
import os
from django.conf import settings
from recommender.models import Item, Review

def index(request):
    context = {}
    return render(request, 'recommender/index.html', context)

def load_data(request):
    with open(os.path.join(settings.BASE_DIR, 'DatafinitiElectronicsProductData.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count >= 1:
                if len(Item.objects.filter(item_name = row[13])) == 0:
                    Item.objects.create(item_name = row[13], item_image = row[9].split(",")[0])
                item = Item.objects.get(item_name = row[13])
                Review.objects.create(review_item = item, review_text = row[22]+" "+row[21])
            line_count += 1
    return redirect(index)

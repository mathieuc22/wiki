from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown

from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):
    return render(request, "encyclopedia/new.html", {
    })

def entry(request, entry):
    return render(request, f"encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(entry))
    })
    #return HttpResponse(markdowner.convert(util.get_entry(entry)))
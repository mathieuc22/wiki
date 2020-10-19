from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from markdown2 import Markdown
from django.http import Http404

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
    e = util.get_entry(entry)
    if  e is None:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    else:
        return render(request, f"encyclopedia/entry.html", {
            "entry": markdowner.convert(e)
        })

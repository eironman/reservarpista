from django.shortcuts import render

from search.forms import SearchSportForm


def index(request):
    """Homepage"""
    form = SearchSportForm()
    return render(request, 'core/homepage.html', {'form': form})

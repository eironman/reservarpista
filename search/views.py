import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from search.mailer import SearchMailer
from search.forms import SearchSportForm
from core.models import SportsCenter


def get_sports_centers_page(sports_centers_list, page_num):
    """Returns the list of sports centers in a page"""

    sports_centers_per_page = 3
    paginator = Paginator(sports_centers_list, sports_centers_per_page)
    try:
        sports_centers = paginator.page(page_num)
    except PageNotAnInteger:
        sports_centers = paginator.page(1)
    except EmptyPage:
        sports_centers = paginator.page(paginator.num_pages)

    return sports_centers


def index(request, sport_slug, location_slug):
    """Search results"""

    # Set values in the search form
    form_values = request.GET.copy()
    form_values['sport'] = sport_slug
    form_values['location'] = location_slug
    form = SearchSportForm(form_values)

    # Get the centers in the first page
    sports_centers = []
    sports_centers_locations = []
    if form.is_valid():
        sports_centers_list = SportsCenter.objects.search(form_values)
        sports_centers = get_sports_centers_page(sports_centers_list, 1)

        # Get the centers locations
        for sports_center in sports_centers_list:
            sports_centers_locations.append(
                {
                'lat': sports_center.latitude,
                'lng': sports_center.longitude,
                'id': sports_center.id,
                'phone': sports_center.phone,
                'name': sports_center.name
                }
            )

    context = {
        'form': form,
        'sports_centers': sports_centers,
        'sports_centers_locations': json.dumps(sports_centers_locations)
    }

    return render(request, 'search/search_results.html', context)


def get_sports_center(request, sport_slug, location_slug, id):
    """Returns a sports center"""
    try:
        sports_center = SportsCenter.objects.get(id=id, active=True)
        html_sport_center = render_to_string(
            'search/blocks/sports_center_card.html',
            {'sports_center': sports_center, 'images': sports_center.sportscentermedia_set.all()})

        data = {
            'result': 'ok',
            'html_sport_center': html_sport_center
        }

    except ObjectDoesNotExist:
        data = {
            'result': 'ko'
        }

    return JsonResponse(data)


def go_to_page(request, sport_slug, location_slug, page):
    """Renders a page of sports centers"""

    # Set values in the search form
    form_values = request.GET.copy()
    form_values['sport'] = sport_slug
    form_values['location'] = location_slug
    form = SearchSportForm(form_values)

    if form.is_valid():
        # Get the centers in the page
        sports_centers_list = SportsCenter.objects.search(form_values)
        sports_centers = get_sports_centers_page(sports_centers_list, page)

        # Render the paginator
        html_paginator = render_to_string('search/blocks/paginator.html', {'list': sports_centers})

        # Render the sports centers
        html_list = ''
        for sports_center in sports_centers:
            html_list += render_to_string(
                'search/blocks/sports_center_card.html',
                {'sports_center': sports_center, 'images': sports_center.sportscentermedia_set.all()}
            )

        data = {
            'result': 'ok',
            'html_list': html_list,
            'html_paginator': html_paginator
        }
    else:
        data = {
            'result': 'ko'
        }

    return JsonResponse(data)


def send_booking_request(request, sport_slug, location_slug):
    """Sends the booking request email to the sports center, the user and reservar pista"""

    mail = SearchMailer(request)
    if mail.send_request():

        data = {
            'result': 'ok'
        }

    else:

        data = {
            'result': 'ko'
        }

    return JsonResponse(data)



































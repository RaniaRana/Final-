from django import template

register = template.Library()

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='calc_pages')
def calc_pages(length, items_per_page):
    return range((length + items_per_page - 1) // items_per_page)

@register.filter(name='add_one')
def add_one(value):
    return value + 1

@register.filter(name='chunk')
def chunk(films, chunk_size):
    for i in range(0, len(films), chunk_size):
        yield films[i:i + chunk_size]

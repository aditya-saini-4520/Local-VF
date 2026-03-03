from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def sub(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    try:
        return round((float(value) / float(total)) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0


@register.filter
def split(value, arg):
    try:
        return str(value).split(str(arg))
    except (ValueError, TypeError):
        return []


@register.filter
def trim(value):
    try:
        return str(value).strip()
    except (ValueError, TypeError):
        return value


@register.filter
def index(value, arg):
    try:
        return value[int(arg)]
    except (ValueError, TypeError, IndexError):
        return None


@register.filter
def concat(value, arg):
    try:
        return str(value) + str(arg)
    except (ValueError, TypeError):
        return value


@register.filter
def get(dictionary, key):
    """Get a value from a dictionary by key: {{ my_dict|get:key }}"""
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return ''


@register.filter
def get_item(dictionary, key):
    """Alias for get filter"""
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return ''


@register.filter
def stars_range(value):
    """Return a range for star rendering: {{ 5|stars_range }}"""
    try:
        return range(1, int(value) + 1)
    except (ValueError, TypeError):
        return range(0)


@register.filter
def empty_stars(value, total=5):
    """Return empty stars count"""
    try:
        return range(int(value), int(total))
    except (ValueError, TypeError):
        return range(0)


@register.filter  
def rating_percent(value, total=5):
    """Convert rating to percentage for CSS width"""
    try:
        return round((float(value) / float(total)) * 100)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
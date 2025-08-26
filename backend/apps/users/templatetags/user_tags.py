# apps/users/templatetags/user_tags.py

from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def user_dashboard_url(context):
    user = context['user']
    if not user.is_authenticated:
        return reverse("login")

    group = user.groups.first().name if user.groups.exists() else ""
    return {
        "Admin": reverse("admin_dash:dashboard"),
        "Tourism Officer": reverse("tourism_dash:dashboard"),
        "Business Owner": reverse("business_dash:dashboard"),
        "Event Organizer": reverse("event_dash:dashboard"),
        "Tourist": reverse("tourist_dash:dashboard"),
    }.get(group, reverse("public-home"))

@register.simple_tag(takes_context=True)
def user_dashboard_name(context):
    user = context['user']
    if not user.is_authenticated:
        return "Login"

    group = user.groups.first().name if user.groups.exists() else ""
    return {
        "Admin": "Admin Dashboard",
        "Tourism Officer": "Tourism Dashboard",
        "Business Owner": "Business Dashboard",
        "Event Organizer": "Event Dashboard",
        "Tourist": "My Dashboard",
    }.get(group, "Public Home")

@register.simple_tag(takes_context=True)
def user_dashboard_icon(context):
    user = context['user']
    if not user.is_authenticated:
        return "bi bi-box-arrow-in-right"

    group = user.groups.first().name if user.groups.exists() else ""
    return {
        "Admin": "bi bi-speedometer2",
        "Tourism Officer": "bi bi-flag-fill",
        "Business Owner": "bi bi-shop",
        "Event Organizer": "bi bi-calendar-event",
        "Tourist": "bi bi-person",
    }.get(group, "bi bi-house")
def get_dashboard_cards(user_role, stats=None):
    stats = stats or {}

    if user_role == "Tourist":
        return {
            "approved_spots_count": stats.get("approved_spots_count", 0),
            "saved_spots_count": stats.get("saved_spots_count", 0),
            "visited_spots_count": stats.get("visited_spots_count", 0),
        }

    elif user_role == "Admin":
        return [
            {
                "icon": "bi bi-map-fill",
                "title": "Tourist Spots",
                "description": "Manage all tourist spots, from volcanoes to beaches.",
                "link": "admin:tourism_touristspot_changelist",
                "button": "Manage Spots"
            },
            {
                "icon": "bi bi-tag-fill",
                "title": "Categories",
                "description": "Organize spots by categories like 'Nature' or 'Historical'.",
                "link": "admin:tourism_category_changelist",
                "button": "Manage Categories"
            },
            {
                "icon": "bi bi-pin-map-fill",
                "title": "Locations",
                "description": "Manage provinces and cities where spots are located.",
                "link": "admin:tourism_location_changelist",
                "button": "Manage Locations"
            },
            {
                "icon": "bi bi-people-fill",
                "title": "Users",
                "description": "Manage all registered users and their roles.",
                "link": "admin:users_customuser_changelist",
                "button": "Manage Users"
            },
            {
                "icon": "bi bi-images",
                "title": "Content",
                "description": "Manage other site content and media.",
                "link": "admin:tourism_gallery_changelist",
                "button": "Manage Content"
            }
        ]

    elif user_role == "Business Owner":
        return [
            {
                "icon": "bi bi-shop",
                "title": "My Business Listings",
                "description": "Manage your business profiles and visibility.",
                "link": "business:business_listings",
                "button": "Manage Listings"
            },
            {
                "title": "Add New Business",
                "icon": "bi bi-plus-circle",
                "link": "business:add_business",
            }
        ]

    elif user_role == "Event Organizer":
        return [
            {
                "icon": "bi bi-calendar-event",
                "title": "My Events",
                "description": "Manage tourism-related events.",
                "link": "events:manage_events",
                "button": "Manage Events"
            },
            {
                "title": "Create Event",
                "icon": "bi bi-plus-circle",
                "link": "events:create_event",
            }
        ]

    elif user_role == "Tourism Officer":
        return [
            {
                "icon": "bi bi-flag-fill",
                "title": "Review Submissions",
                "description": "Review new tourist spot and event submissions.",
                "link": "tourism:review_spots",
                "button": "Review Now"
            },
            {
                "title": "Reported Spots",
                "icon": "bi bi-flag",
                "link": "tourism:reported_spots",
            }
        ]

    return []

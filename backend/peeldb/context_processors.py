from django.conf import settings

def get_pj_icons(request):
    domain = getattr(settings, 'PEEL_URL', '').rstrip('/')
    logos = {
        "jobopenings": f"{domain}/static/img/jobopenings1.png",
        "logo": f"{domain}/static/logo.svg",
        "favicon": f"{domain}/static/img/favicon.png",
        "cdn_path": f"{domain}/static/",
    }
    return logos

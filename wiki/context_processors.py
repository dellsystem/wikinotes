from django.conf import settings


def config(request):
    return {
        'compile_less': settings.COMPILE_LESS,
        'site_url': settings.SITE_URL,
    }

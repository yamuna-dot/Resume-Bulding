import os
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    (images, fonts, css, etc.)
    """
    # Use settings.STATIC_URL and settings.STATIC_ROOT
    if uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.BASE_DIR, 'static', uri.replace(settings.STATIC_URL, ''))
        if not os.path.isfile(path) and hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    else:
        # Check if it's already an absolute path
        path = uri

    if os.path.isfile(path):
        return path
    return uri


def render_to_pdf(template_src, context_dict=None, filename="resume.pdf", download=True):
    """
    Renders an HTML template into a PDF response using xhtml2pdf.
    """
    if context_dict is None:
        context_dict = {}

    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)

    if not pdf.err:
        disposition = 'attachment' if download else 'inline'
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'{disposition}; filename="{filename}"'
        return response

    return HttpResponse(f"Error rendering PDF: {pdf.err}", status=500)

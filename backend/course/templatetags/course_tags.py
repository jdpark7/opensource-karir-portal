import base64
from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def generate_course_svg(course_id, course_name):
    """
    Generates a unique Base64-encoded SVG inline string based on course_id and name.
    Matches a pastel Google Classroom-style aesthetic with soft geometric patterns.
    """
    # Define a set of pleasing pastel gradients/solid colors
    colors = [
        ("#9F96F2", "#B8B1F5"), # Light purple
        ("#3999ED", "#59ACF5"), # Light blue
        ("#8685EF", "#A2A2F3"), # Periwinkle
        ("#F4628E", "#F782A6"), # Pink
        ("#CACDCF", "#D7D9DB"), # Light gray
        ("#EDBA54", "#F4CF7F"), # Yellow/Orange
        ("#D3D9DE", "#E2E6E9"), # Pale gray
        ("#64E3DE", "#81EDE9"), # Cyan/Mint
        ("#524BC8", "#6660DA"), # Darker purple
        ("#1F87E0", "#3CA1F2"), # Darker blue
        ("#0FBD7F", "#29D499"), # Green
        ("#20C1A3", "#3FD3B8"), # Teal
    ]
    
    # Pick gradient deterministically based on course ID
    try:
        cid = int(course_id) if course_id else 0
    except (ValueError, TypeError):
        cid = sum(ord(c) for c in str(course_name))
        
    c1, c2 = colors[cid % len(colors)]
    
    # Select deterministic geometric shapes arrangement
    shape_variant = cid % 5
    if shape_variant == 0:
        # Concentric overlapping circles
        shapes = f'''
        <pattern id="pat{cid}" width="80" height="80" patternUnits="userSpaceOnUse">
            <circle cx="40" cy="40" r="35" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="8"/>
            <circle cx="40" cy="40" r="20" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="5"/>
            <circle cx="0" cy="0" r="35" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="8"/>
            <circle cx="80" cy="80" r="35" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="8"/>
        </pattern>
        <rect width="100%" height="100%" fill="url(#pat{cid})" />
        '''
    elif shape_variant == 1:
        # Squares / Checkerboard
        shapes = f'''
        <pattern id="pat{cid}" width="60" height="60" patternUnits="userSpaceOnUse">
            <rect x="0" y="0" width="30" height="30" fill="rgba(255,255,255,0.08)"/>
            <rect x="30" y="30" width="30" height="30" fill="rgba(255,255,255,0.05)"/>
            <rect x="15" y="15" width="30" height="30" fill="rgba(255,255,255,0.06)"/>
            <rect x="45" y="45" width="15" height="15" fill="rgba(255,255,255,0.1)"/>
        </pattern>
        <rect width="100%" height="100%" fill="url(#pat{cid})" />
        '''
    elif shape_variant == 2:
        # Honeycomb Hexagons
        shapes = f'''
        <pattern id="pat{cid}" width="52" height="90" patternUnits="userSpaceOnUse">
            <path d="M26 0 L52 15 L52 45 L26 60 L0 45 L0 15 Z" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
            <path d="M26 90 L52 75 L52 45 L26 60 L0 45 L0 75 Z" fill="rgba(255,255,255,0.03)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
            <path d="M-26 45 L0 30 L0 60 L-26 75 L-52 60 L-52 30 Z" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
            <path d="M78 45 L104 30 L104 60 L78 75 L52 60 L52 30 Z" fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
        </pattern>
        <rect width="100%" height="100%" fill="url(#pat{cid})" />
        '''
    elif shape_variant == 3:
        # Triangles
        shapes = f'''
        <pattern id="pat{cid}" width="60" height="60" patternUnits="userSpaceOnUse">
            <polygon points="0,0 60,0 30,60" fill="rgba(255,255,255,0.04)" />
            <polygon points="30,60 90,60 60,0" fill="rgba(255,255,255,0.06)" />
            <polygon points="-30,60 30,60 0,0" fill="rgba(255,255,255,0.03)" />
            <polygon points="0,120 60,120 30,60" fill="rgba(255,255,255,0.05)" />
        </pattern>
        <rect width="100%" height="100%" fill="url(#pat{cid})" />
        '''
    else:
        # Overlapping large curves
        shapes = f'''
        <pattern id="pat{cid}" width="100" height="100" patternUnits="userSpaceOnUse">
            <circle cx="0" cy="50" r="40" fill="rgba(255,255,255,0.06)"/>
            <circle cx="100" cy="50" r="40" fill="rgba(255,255,255,0.06)"/>
            <circle cx="50" cy="0" r="40" fill="rgba(255,255,255,0.04)"/>
            <circle cx="50" cy="100" r="40" fill="rgba(255,255,255,0.04)"/>
            <circle cx="50" cy="50" r="20" fill="rgba(255,255,255,0.08)"/>
        </pattern>
        <rect width="100%" height="100%" fill="url(#pat{cid})" />
        '''
        
    xml = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
  <defs>
    <linearGradient id="grad{cid}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{c1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{c2};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#grad{cid})" />
  {shapes}
</svg>'''

    # Encode raw data to Base64 to ensure perfectly valid HTML tag injection
    b64_data = base64.b64encode(xml.encode('utf-8')).decode('utf-8')
    data_uri = f"data:image/svg+xml;base64,{b64_data}"
    
    return format_html(data_uri)

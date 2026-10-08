# CATopalian_PY_PySide6DOM_Earthquake_Map.py

import urllib.request
from pyside6dom import *

my_icon = os.path.join("src", "media", "textures", "icons", "001.png")

init_window('CATopalian PY PySide6DOM Earthquake Map', 1000, 800, my_icon)

set_theme('''
    body {
        background-color: rgb(20, 20, 25);
        color: white;
        font-family: 'Segoe UI', Arial; 
        margin: 0px;
        padding: 0px;
    }
    .map_canvas {
        background-color: rgb(30, 35, 45); 
        border-bottom: 3px solid rgb(100, 100, 120);
    }
    .eq_dot {
        background-color: rgba(255, 50, 50, 0.7);
        border-radius: 5px;
    }
    .list_row {
        padding: 10px;
        border-bottom: 1px solid #444;
    }
    .list_row:hover {
        background-color: #333;
    }
    .mag_badge {
        background-color: #ff3333;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        margin-right: 10px;}
''')

MAP_WIDTH = 1000
MAP_HEIGHT = 500

# ===
# UI LAYOUT
# ===
# Top Half: The Map
map_view = ce('div')
map_view.className = 'map_canvas'
map_view.style.width = MAP_WIDTH
map_view.style.height = MAP_HEIGHT
map_view.style.position = 'relative' 
ba(map_view)

# Add the Map Image Background
map_bg = ce('img')
map_bg.src = os.path.join("src", "media", "textures", "maps", "Earthmap1000x500.jpg")
map_bg.style.position = 'absolute'
map_bg.style.left = 0
map_bg.style.top = 0
map_bg.width = MAP_WIDTH
map_bg.height = MAP_HEIGHT
map_view.append(map_bg)

# Bottom Half: The Data List
list_view = ce('scroll_div')
list_view.style.width = MAP_WIDTH
list_view.style.height = 300
list_view.style.padding = 10
ba(list_view)

# ===
# THE MATH 
# ===
def lat_lon_to_xy(lat, lon):
    x = (lon + 180.0) * (MAP_WIDTH / 360.0)
    y = (90.0 - lat) * (MAP_HEIGHT / 180.0)
    return x, y

# ===
# FETCH AND PLOT DATA
# ===
def load_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"
    
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        features = data.get('features', [])

        for eq in features:
            props = eq['properties']
            coords = eq['geometry']['coordinates'] 
            
            mag = props['mag']
            place = props['place']
            lon = coords[0]
            lat = coords[1]

            # Draw the Dot
            x, y = lat_lon_to_xy(lat, lon)

            dot = ce('div')
            # Add the Rich Text Tooltip
            dot.title = f"<b>{place}</b><br>Magnitude: {mag:.1f}"
            dot.titleFontSize = "16px"
            dot.className = 'eq_dot'
            dot.style.position = 'absolute'
            dot.style.left = int(x) - 5
            dot.style.top = int(y) - 5
            
            size = max(6, int(mag * 2)) 
            dot.style.width = size
            dot.style.height = size
            map_view.append(dot)

            # Draw the Row
            row = ce('div')
            row.className = 'list_row'
            row.style.display = 'flex'
            row.style.flexDirection = 'row'
            row.style.alignItems = 'center'
            row.raw.setCursor(Qt.CursorShape.PointingHandCursor)

            badge = ce('text')
            badge.className = 'mag_badge'
            badge.textContent = f"M {mag:.1f}"
            badge.raw.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # Ghost fix
            row.append(badge)

            info = ce('text')
            info.textContent = place
            info.style.fontSize = '16px'
            info.raw.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents) # Ghost fix!
            row.append(info)

            list_view.append(row)

            # ===
            # THE HOVER & CLICK INTERACTIVITY
            # ===
            # We pass px=x and py=y to remember the exact map coordinates
            def hover_in(d=dot, r=row, s=size, px=x, py=y):
                d.style.backgroundColor = 'rgb(0, 255, 255)'
                d.style.width = s + 6
                d.style.height = s + 6
                # Shift left and up by 3 pixels to stay centered
                d.style.left = int(px) - 5 - 3  
                d.style.top = int(py) - 5 - 3
                d.style.border = '2px solid white'
                d.raw.raise_() 
                r.style.backgroundColor = '#444'

            def hover_out(d=dot, r=row, s=size, px=x, py=y):
                d.style.backgroundColor = 'rgba(255, 50, 50, 0.7)'
                d.style.width = s
                d.style.height = s
                # Return the dot to its original position
                d.style.left = int(px) - 5
                d.style.top = int(py) - 5
                d.style.border = 'none'
                r.style.backgroundColor = 'transparent'

            def open_maps(lt=lat, ln=lon):
                url = f"https://www.google.com/maps/search/?api=1&query={lt},{ln}"
                QDesktopServices.openUrl(QUrl(url))

            row.addEventListener('mouseenter', hover_in)
            row.addEventListener('mouseleave', hover_out)
            row.onclick = open_maps
            
            dot.raw.setCursor(Qt.CursorShape.PointingHandCursor)
            dot.addEventListener('mouseenter', hover_in)
            dot.addEventListener('mouseleave', hover_out)
            dot.onclick = open_maps

    except Exception as e:
        print(f"Failed to load earthquake data: {e}")

load_earthquakes()
run_app()

####

# Dedicated to God the Father
# (c) Copyright 2026 Christopher Andrew Topalian All Rights Reserved
# https://github.com/ChristopherTopalian
# https://github.com/ChristopherAndrewTopalian
# https://sites.google.com/view/CollegeOfScripting


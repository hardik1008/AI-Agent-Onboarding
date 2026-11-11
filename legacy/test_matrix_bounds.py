import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding="utf-8")

with open(r"C:\Users\vajja\Desktop\PolicyNest_AI_Suite\static\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's verify matrix grid
start_grid = html.find('id="matrix-card-pan"')
if start_grid != -1:
    prev_div = html.rfind('<div class="grid', 0, start_grid)
    end_card6 = html.find('id="matrix-card-form1a"')
    end_div = html.find('<!-- DigiLocker 1-Click Pull -->', end_card6)
    print("Matrix block found:")
    print("Start:", prev_div)
    print("End:", end_div)
    print(html[prev_div:prev_div+200])
    print("...")
    print(html[end_div-200:end_div])

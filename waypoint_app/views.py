from django.shortcuts import render
from django.http import Http404
from waypoint_app.data import TRAILS_DB

def home(request):
    trails_list = list(TRAILS_DB.values())
    return render(request, 'home.html', {
        'welcome_msg': 'Welcome to Waypoint Trail Finder!',
        'trails': trails_list
    })

def trail_detail(request, trail_id):
    trail = TRAILS_DB.get(str(trail_id))
    if not trail:
        raise Http404("Trail not found")
    return render(request, 'trail_detail.html', {'trail': trail})

def report(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Hiker')
        trail = request.POST.get('trail', 'Unknown')
        note = request.POST.get('note', '')
        return render(request, 'thank_you.html', {'name': name, 'trail': trail, 'note': note})
    return render(request, 'report.html')

def search(request):
    query = request.GET.get('q', '').strip().lower()
    results = []
    if query:
        results = [
            t for t in TRAILS_DB.values()
            if query in t.name.lower() or query in t._difficulty.lower()
        ]
    return render(request, 'search.html', {'query': query, 'results': results})
from django.shortcuts import render, get_object_or_404
from trails.models import Trail

def home(request):
    # Query open trails ordered by distance
    trails = Trail.objects.filter(is_open=True).order_by('-distance_km')
    
    context = {
        'welcome_msg': 'Welcome to Waypoint!',
        'trails': trails,
    }
    return render(request, 'home.html', context)

def trail_detail(request, trail_id):
    # Fetch trail from DB by primary key or return 404
    trail = get_object_or_404(Trail, pk=trail_id)
    return render(request, 'trail_detail.html', {'trail': trail})

def report(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        return render(request, 'thank_you.html', {'name': name})
    return render(request, 'report.html')

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Search open trails by name matching query
        results = Trail.objects.filter(is_open=True, name__icontains=query)
    return render(request, 'search.html', {'query': query, 'results': results})
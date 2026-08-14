from django.test import TestCase
from django.urls import reverse
from trails.models import Trail, Park
from waypoint_core.domain import Distance  # Adjust path if Distance lives in waypoint_core.models or similar


class DistanceDomainTests(TestCase):
    def test_distance_rejects_negative_magnitude(self):
        """WP-801: Verify Distance raises ValueError for negative inputs."""
        with self.assertRaises(ValueError):
            Distance(-5, "km")

    def test_distance_addition_operator(self):
        """WP-801: Verify Distance addition operator works as expected."""
        d1 = Distance(3, "km")
        d2 = Distance(2, "km")
        total = d1 + d2
        self.assertEqual(total.magnitude, 5.0)


class WaypointViewTests(TestCase):
    def setUp(self):
        """Set up test Park and Trail records matching models.py."""
        self.park = Park.objects.create(name="Algonquin", region="Ontario")

        # Create an open trail
        self.open_trail = Trail.objects.create(
            name="Centennial Ridges",
            distance_km=10.4,
            elevation_gain=440,
            difficulty="EXPERT",
            is_open=True,
            park=self.park
        )

        # Create a closed trail
        self.closed_trail = Trail.objects.create(
            name="Track and Tower",
            distance_km=7.5,
            elevation_gain=200,
            difficulty="MODERATE",
            is_open=False,
            park=self.park
        )

    def test_open_trails_query(self):
        """WP-801: Verify catalog/home page loads successfully."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_trail_detail_404(self):
        """WP-801: Verify non-existent trail ID returns 404 Not Found."""
        response = self.client.get(reverse('trail_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)
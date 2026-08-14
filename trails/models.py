from django.db import models


class Park(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} ({self.region})'


class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ('EASY', 'Easy'),
        ('MODERATE', 'Moderate'),
        ('HARD', 'Hard'),
        ('EXPERT', 'Expert'),
    ]

    park = models.ForeignKey(
        Park, on_delete=models.CASCADE, null=True, blank=True
    )

    name = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty = models.CharField(
        max_length=10, choices=DIFFICULTY_CHOICES, default='MODERATE'
    )
    is_open = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.distance_km} km)'
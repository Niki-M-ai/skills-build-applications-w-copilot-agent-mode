from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data in correct order (delete individually for Djongo)
        for model in [Activity, Workout, Leaderboard, User, Team]:
            try:
                model.objects.all().delete()
            except Exception:
                pass

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Team Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='Team DC Superheroes')

        # Create Users
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel, is_superhero=True),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel, is_superhero=True),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc, is_superhero=True),
            User(name='Batman', email='batman@dc.com', team=dc, is_superhero=True),
        ]
        for user in users:
            user.save()

        # Create Activities
        Activity.objects.create(user=users[0], type='Running', duration=30, date=timezone.now())
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date=timezone.now())
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date=timezone.now())
        Activity.objects.create(user=users[3], type='Yoga', duration=40, date=timezone.now())

        # Create Workouts
        w1 = Workout.objects.create(name='Hero HIIT', description='High intensity workout for heroes')
        w2 = Workout.objects.create(name='Power Yoga', description='Yoga for strength and flexibility')
        w1.suggested_for.set([marvel])
        w2.suggested_for.set([dc])

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))

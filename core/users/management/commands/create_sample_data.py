from django.core.management.base import BaseCommand
from core.users.models import User

class Command(BaseCommand):
    help = 'Create a superuser and sample data for testing'
    
    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
            self.stdout.write('Superuser created: admin/adminpassword')
        
        # Create sample users
        if not User.objects.filter(username='creator1').exists():
            user = User.objects.create_user('creator1', 'creator1@example.com', 'password')
            user.is_creator = True
            user.bio = 'Sample creator account'
            user.save()
            self.stdout.write('Sample creator created: creator1/password')
        
        if not User.objects.filter(username='user1').exists():
            User.objects.create_user('user1', 'user1@example.com', 'password')
            self.stdout.write('Sample user created: user1/password')
        
        self.stdout.write('Sample data created successfully.')

from django.core.management.base import BaseCommand
from nilusweb.accounts.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin","michel.carvalho22@gmaill.com","admin")
import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import Quote, Show, Role

class Command(BaseCommand):
    help = 'Load movie quotes from original JSON file format'

    def handle(self, *args, **options):
        # Pfad zur JSON-Datei
        json_file_path = os.path.join(settings.BASE_DIR, 'movie_quotes.json')
        
        if not os.path.exists(json_file_path):
            self.stdout.write(
                self.style.ERROR(f'File not found: {json_file_path}')
            )
            return
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                quotes_data = json.load(file)
            
            created_count = 0
            shows_created = 0
            roles_created = 0
            
            for quote_data in quotes_data:
                # Erstelle oder hole Show (Movie)
                show, show_created = Show.objects.get_or_create(
                    name=quote_data['movie']
                )
                if show_created:
                    shows_created += 1
                    self.stdout.write(f'🎬 Created show: {show.name}')
                
                # Erstelle oder hole Role (Character) - verwende "Unknown" da nicht in JSON
                role, role_created = Role.objects.get_or_create(
                    name='Unknown Character'
                )
                if role_created:
                    roles_created += 1
                    self.stdout.write(f'🎭 Created role: {role.name}')
                
                # Erstelle Quote mit korrekten Feldnamen
                quote, created = Quote.objects.get_or_create(
                    quote=quote_data['quote'],  # 'quote' field im Model
                    defaults={
                        'show': show,                                    # ForeignKey zu Show
                        'role': role,                                    # ForeignKey zu Role  
                        'contain_adult_lang': False,                     # Boolean field
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f'✅ Created quote: "{quote.quote[:50]}..." from {show.name}'
                    )
                else:
                    self.stdout.write(
                        f'⚡ Quote exists: "{quote.quote[:30]}..."'
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎬 Movie Quotes loaded successfully!\n'
                    f'✅ New quotes: {created_count}\n'
                    f'🎬 New shows: {shows_created}\n'
                    f'🎭 New roles: {roles_created}\n'
                    f'📝 Total processed: {len(quotes_data)}\n'
                    f'🚀 Your API now has {Quote.objects.count()} quotes!'
                )
            )
            
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON format: {e}')
            )
        except KeyError as e:
            self.stdout.write(
                self.style.ERROR(f'Missing required field in JSON: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading quotes: {e}')
            )

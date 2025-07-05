import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import Quote  # Anpassen falls dein Model anders heißt

class Command(BaseCommand):
    help = 'Load movie quotes from original JSON file format'

    def handle(self, *args, **options):
        # Pfad zur JSON-Datei (deine originale movie_quotes.json)
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
            
            for quote_data in quotes_data:
                # Arbeite direkt mit deinem JSON-Format:
                # {"quote": "...", "movie": "...", "type": "movie", "year": 1890}
                
                quote, created = Quote.objects.get_or_create(
                    text=quote_data['quote'],  # 'quote' aus deiner JSON
                    defaults={
                        'movie': quote_data['movie'],           # 'movie' aus deiner JSON
                        'character': 'Unknown',                 # Nicht in deiner JSON
                        'author': 'Unknown',                    # Nicht in deiner JSON
                        'year': quote_data.get('year', 2000),   # 'year' aus deiner JSON
                        'censored': False,                      # Default
                    }
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(
                        f'✅ Created: "{quote.text[:50]}..." from {quote.movie}'
                    )
                else:
                    self.stdout.write(
                        f'⚡ Already exists: "{quote.text[:30]}..."'
                    )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎬 Movie Quotes loaded successfully!\n'
                    f'✅ New quotes created: {created_count}\n'
                    f'📝 Total quotes processed: {len(quotes_data)}\n'
                    f'🎭 Your API now has movie quotes!'
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
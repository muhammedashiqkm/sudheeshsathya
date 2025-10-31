# home/management/commands/seed_db.py

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

# Import all your models
from home.models import (
    PostCategory, 
    Post, 
    ContentBlock, 
    VideoCategory, 
    Video, 
    AboutPage, 
    Subscriber
)

class Command(BaseCommand):
    help = 'Seeds the database with realistic test data.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Clearing all existing data...'))
        self._clear_data()

        self.stdout.write(self.style.SUCCESS('Seeding database...'))
        
        # Initialize Faker
        fake = Faker()

        # === 1. Create Categories ===
        self.stdout.write('Creating Post and Video Categories...')
        post_categories = []
        for _ in range(5):
            cat = PostCategory.objects.create(
                name=fake.word().capitalize(),
                description=fake.sentence()
            )
            post_categories.append(cat)

        video_categories = []
        for _ in range(3):
            cat = VideoCategory.objects.create(
                name=f"{fake.word().capitalize()} Videos",
                description=fake.sentence()
            )
            video_categories.append(cat)
        
        # === 2. Create Posts and Content Blocks ===
        self.stdout.write('Creating Posts and Content Blocks...')
        for _ in range(20): # Create 20 posts
            post = Post.objects.create(
                title=fake.sentence(nb_words=6),
                excerpt=fake.text(max_nb_chars=150),
                category=random.choice(post_categories),
                is_published=random.choice([True, False]),
                is_featured=random.choice([True, False])
            )
            
            # Create content blocks for each post
            ContentBlock.objects.create(
                post=post,
                order=1,
                block_type='heading',
                content=fake.sentence(nb_words=4)
            )
            ContentBlock.objects.create(
                post=post,
                order=2,
                block_type='rich_text',
                content=f"<p>{fake.paragraph(nb_sentences=5)}</p><p>{fake.paragraph(nb_sentences=5)}</p>"
            )
            ContentBlock.objects.create(
                post=post,
                order=3,
                block_type='image',
                caption=fake.sentence(nb_words=8)
                # Note: ImageField is not populated here, 
                # as it requires an actual file.
            )

        # === 3. Create Videos ===
        self.stdout.write('Creating Videos...')
        youtube_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=3JZ_D3ELwOQ',
            'https://www.youtube.com/watch?v=C0DPdy98e4c'
        ]
        for _ in range(15): # Create 15 videos
            Video.objects.create(
                title=fake.sentence(nb_words=5),
                excerpt=fake.text(max_nb_chars=150),
                description=fake.paragraph(nb_sentences=3),
                video_url=random.choice(youtube_urls),
                category=random.choice(video_categories),
                is_published=random.choice([True, False]),
                is_featured=random.choice([True, False])
            )

        # === 4. Create Subscribers ===
        self.stdout.write('Creating Subscribers...')
        for _ in range(50): # Create 50 subscribers
            Subscriber.objects.get_or_create(
                email=fake.email(),
                defaults={'is_active': random.choice([True, True, False])} # 2/3 active
            )

        # === 5. Create About Page ===
        self.stdout.write('Creating About Page...')
        AboutPage.objects.get_or_create(
            title="About Me",
            defaults={
                'subtitle': fake.sentence(),
                'content': f"<h2>{fake.sentence()}</h2><p>{fake.paragraph(nb_sentences=10)}</p>"
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))


    def _clear_data(self):
        """
        Deletes all data from the models in the correct order 
        to avoid foreign key constraints.
        """
        ContentBlock.objects.all().delete()
        Post.objects.all().delete()
        PostCategory.objects.all().delete()
        Video.objects.all().delete()
        VideoCategory.objects.all().delete()
        Subscriber.objects.all().delete()
        AboutPage.objects.all().delete()
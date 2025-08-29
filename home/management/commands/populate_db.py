import random
from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import Category, Tag, Post, ContentBlock, VideoCategory, Video

class Command(BaseCommand):
    help = 'Populates the database with 40 posts and 20 videos.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clean up old data
        self.stdout.write('Deleting old data...')
        Category.objects.all().delete()
        Tag.objects.all().delete()
        Post.objects.all().delete()
        VideoCategory.objects.all().delete()
        Video.objects.all().delete()

        # --- Create Categories ---
        tech_category = Category.objects.create(name='Technology')
        other_categories = [
            Category.objects.create(name='Travel'),
            Category.objects.create(name='Food & Cooking'),
            Category.objects.create(name='Lifestyle'),
            Category.objects.create(name='Data Science'),
        ]
        self.stdout.write(self.style.SUCCESS(f'Created {1 + len(other_categories)} categories.'))

        # --- Create Tags ---
        tags = [
            Tag.objects.create(name='Python'), Tag.objects.create(name='Django'),
            Tag.objects.create(name='Web Development'), Tag.objects.create(name='Machine Learning'),
            Tag.objects.create(name='Europe'), Tag.objects.create(name='Asia'),
            Tag.objects.create(name='Healthy Recipes'), Tag.objects.create(name='Productivity'),
            Tag.objects.create(name='Photography'), Tag.objects.create(name='Tutorial'),
            Tag.objects.create(name='Career'), Tag.objects.create(name='Gadgets'),
        ]
        self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} tags.'))

        # --- Create Video Categories and 20 Videos ---
        vid_cat_tutorials = VideoCategory.objects.create(name='Tutorials', description='Helpful programming tutorials.')
        vid_cat_vlogs = VideoCategory.objects.create(name='Vlogs', description='Updates from my travels and life.')
        self.stdout.write(self.style.SUCCESS('Created 2 video categories.'))
        
        video_titles = [
            "Building a Django Blog from Scratch", "Exploring the Streets of Tokyo", "Advanced Python Tips",
            "My Top 5 Productivity Hacks", "Django for Beginners: Part 1", "A Culinary Tour of Italy",
            "Data Science with NumPy", "What's In My Tech Bag?", "Weekend Trip to the Mountains",
            "How to Cook the Perfect Steak", "React.js Crash Course", "A Day in the Life of a Developer",
            "Travel Guide: Barcelona", "Mastering CSS Grid", "My Desk Setup for 2025",
            "Simple Meal Prep for the Week", "Introduction to Docker", "Cinematic Travel Video: Iceland",
            "How to Start a Successful Blog", "JavaScript ES6 Features You Should Know"
        ]
        
        video_categories = [vid_cat_tutorials, vid_cat_vlogs]
        for title in video_titles:
            Video.objects.create(
                title=title,
                video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ', # Placeholder URL
                description=f"A detailed video about '{title}'. Watch to learn more!",
                category=random.choice(video_categories),
                is_featured=(random.random() < 0.2) 
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(video_titles)} videos.'))

        # --- Create 20 Posts in the "Technology" Category ---
        tech_post_titles = [
            "Getting Started with Django 5.0", "A Guide to REST APIs", "Advanced Git Techniques",
            "Understanding SQL Joins", "Deploying Your Django App", "Top 10 Python Libraries",
            "Introduction to Docker", "JavaScript ES6 Features", "Mastering CSS Grid",
            "Data Science with NumPy", "React.js Crash Course", "What's In My Tech Bag?",
            "Building Microservices with FastAPI", "An Overview of Serverless Architecture",
            "Web Security Best Practices", "Optimizing Database Performance", "Introduction to GraphQL",
            "The Rise of WebAssembly", "CI/CD Pipelines Explained", "A Deep Dive into WebSockets"
        ]

        for title in tech_post_titles:
            post = Post.objects.create(
                title=title,
                excerpt=f"A deep dive into '{title}'. This post covers essential concepts for developers.",
                category=tech_category,
                is_published=True
            )
            post.tags.set(random.sample(tags, k=random.randint(2, 4)))
            ContentBlock.objects.create(post=post, order=1, block_type='heading', content=f"Introduction to {title}")
            ContentBlock.objects.create(post=post, order=2, block_type='rich_text', content="The main body for this technology article goes here, exploring the topic in detail.")

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(tech_post_titles)} posts in the "{tech_category.name}" category.'))

        # --- Create the Remaining 20 Posts in Other Categories ---
        other_post_titles = [
            "My Journey Through Southeast Asia", "The Perfect Sourdough Recipe", "10 Habits for a Productive Life",
            "Backpacking in the Swiss Alps", "Mastering Italian Pasta", "Hidden Gems of Lisbon",
            "A Weekend in Paris", "Digital Detox: A How-To Guide", "Introduction to Pandas for Data Analysis",
            "Visualizing Data with Matplotlib", "Quick and Healthy Weeknight Dinners", "Setting Up a Personal Development Plan",
            "The Science of Baking a Perfect Cake", "A Culinary Tour of Italy", "What's In My Travel Bag?",
            "Weekend Trip to the Mountains", "My Desk Setup for 2025", "Simple Meal Prep for the Week",
            "Cinematic Travel Video: Iceland", "How to Start a Successful Blog"
        ]

        for title in other_post_titles:
            post = Post.objects.create(
                title=title,
                excerpt=f"An engaging summary about '{title}'. Read more to discover tips and stories.",
                category=random.choice(other_categories),
                is_published=True
            )
            post.tags.set(random.sample(tags, k=random.randint(2, 4)))
            ContentBlock.objects.create(post=post, order=1, block_type='heading', content=f"Exploring {title}")
            ContentBlock.objects.create(post=post, order=2, block_type='rich_text', content="Detailed exploration of this topic, with personal insights and tips for a better experience.")

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(other_post_titles)} posts in other categories.'))
        self.stdout.write(self.style.SUCCESS('Database population complete! ✅'))
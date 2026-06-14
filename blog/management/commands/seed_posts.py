
from django.core.management.base import BaseCommand
from blog.models import Post

class Command(BaseCommand):
    help = 'Seed the database with 4 placeholder posts'

    def handle(self, *args, **kwargs):
        placeholders = [
            {
                'title': 'Getting Started with Modern Web Development',
                'content': 'The web development landscape has evolved dramatically over the past decade. From simple HTML pages to complex single-page applications, the tools and frameworks available today empower developers to build incredible experiences. In this post, we explore the essential technologies every modern developer should know: HTML5 semantic elements, CSS Grid and Flexbox, JavaScript ES6+ features, and the rise of progressive web apps. Whether you are just starting out or looking to refresh your skills, understanding these fundamentals will set you up for success in any web project.',
                'author': 'Alex Chen',
                'category': 'Tutorial',
            },
            {
                'title': 'The Art of Clean Code: Best Practices',
                'content': 'Writing clean code is not just about making your programs work—it is about making them work well for everyone who reads them. Clean code is readable, maintainable, and testable. Key principles include meaningful naming conventions, keeping functions small and focused, avoiding unnecessary comments by writing self-documenting code, and following the DRY (Do Not Repeat Yourself) principle. Remember: code is read far more often than it is written. Invest time in clarity, and your future self (and your teammates) will thank you.',
                'author': 'Sarah Miller',
                'category': 'Engineering',
            },
            {
                'title': 'Understanding Async JavaScript',
                'content': 'Asynchronous programming is at the heart of modern JavaScript. From callbacks to promises and now async/await, the language has continuously improved how we handle operations that take time. This post dives deep into the event loop, microtasks, macrotasks, and how JavaScript manages concurrency despite being single-threaded. We will look at practical examples of fetching data from APIs, handling errors gracefully, and avoiding common pitfalls like callback hell or unhandled promise rejections. Mastering async patterns is essential for building responsive web applications.',
                'author': 'Marcus Johnson',
                'category': 'JavaScript',
            },
            {
                'title': 'Design Systems: Building for Scale',
                'content': 'A design system is more than a style guide—it is a comprehensive set of standards, components, and patterns that help teams build consistent user interfaces at scale. Companies like Google (Material Design), IBM (Carbon), and Atlassian have pioneered how design systems drive product consistency and development velocity. This article covers the core elements of a design system: design tokens for colors and typography, reusable UI components, accessibility guidelines, and documentation. We also discuss how to introduce a design system to your organization and measure its impact on product quality and team collaboration.',
                'author': 'Emily Rodriguez',
                'category': 'Design',
            },
        ]

        for data in placeholders:
            Post.objects.get_or_create(
                title=data['title'],
                defaults={
                    'content': data['content'],
                    'author': data['author'],
                    'category': data['category'],
                    'is_placeholder': True,
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded 4 placeholder posts!'))

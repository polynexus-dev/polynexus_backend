from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField

class Service(models.Model):
    id = models.CharField(max_length=50, primary_key=True, help_text="URL-safe slug or primary key (e.g. design, governance)")
    icon = models.CharField(max_length=50, help_text="Lucide react icon name (e.g. Zap, Database)")
    title = models.CharField(max_length=100)
    shortDesc = models.TextField(max_length=250, help_text="Short description displayed directly in the grid card")
    fullDesc = models.TextField(help_text="In-depth description shown inside the engineering modal specsheet")
    features = ArrayField(models.CharField(max_length=255), help_text="List of key integration pillars / bullet points")
    specs = models.JSONField(help_text="Key-value pairs representing engineering specs (e.g. {'Speed': '100% Core Performance'})")

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.title


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('enterprise', 'Enterprise Management'),
        ('logistics', 'Custom Operations & Logistics'),
        ('saas', 'Productivity & B2B SaaS'),
    ]
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, help_text="Project category (enterprise, logistics, or saas)")
    desc = models.TextField(help_text="Detailed description of the business/technical solution")
    metric = models.CharField(max_length=50, help_text="High-impact metric value (e.g. 0.15ms, 100%)")
    metricLabel = models.CharField(max_length=100, help_text="Label explaining the metric value (e.g. Vector Resolution)")
    icon = models.CharField(max_length=50, help_text="Lucide icon reference name (e.g. Cpu, Database)")
    tech = ArrayField(models.CharField(max_length=100), help_text="Array of technologies used")
    image = models.URLField(max_length=500, blank=True, null=True, help_text="URL path to the dashboard mockup screenshot image")
    image_data = models.BinaryField(blank=True, null=True, help_text="Binary screenshot image data")
    image_mime_type = models.CharField(max_length=50, blank=True, null=True, help_text="Mime type of the binary image")
    file = models.CharField(max_length=100, blank=True, null=True, help_text="Shell file label shown in the Hero mockup header (e.g. cognitive-query-api.sh)")
    longDesc = models.TextField(blank=True, null=True, help_text="Detailed narrative case study description")
    benefits = ArrayField(models.CharField(max_length=255), blank=True, null=True, help_text="List of key benefits and value delivered")
    results = ArrayField(models.CharField(max_length=255), blank=True, null=True, help_text="List of measurable results/outcomes achieved")
    price = models.CharField(max_length=100, blank=True, null=True, help_text="Starting price of the project (e.g. ₹599 / month)")
    price_detail_html = models.TextField(blank=True, null=True, help_text="Raw HTML table/content for detailed pricing modal")

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="Job title (e.g. VP of Platform Engineering)")
    company = models.CharField(max_length=100, help_text="Company name (e.g. NovusAI)")
    content = models.TextField(max_length=500, help_text="Testimonial narrative content text")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Numerical rating score (typically 5)")
    avatar = models.URLField(max_length=500, help_text="Reviewer's profile photo URL")

    class Meta:
        db_table = 'testimonials'

    def __str__(self):
        return f"{self.name} - {self.company}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(help_text="Detailed markdown/text answer block")

    class Meta:
        db_table = 'faqs'

    def __str__(self):
        return self.question


class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=100)
    date = models.DateField(help_text="Publication date")
    readTime = models.CharField(max_length=50, help_text="Estimated reading duration (e.g. 6 min read)")
    summary = models.TextField(max_length=300, help_text="Brief text abstract shown on the grid card")
    imageUrl = models.URLField(max_length=500, help_text="Post teaser header image URL")

    class Meta:
        db_table = 'blog_posts'

    def __str__(self):
        return self.title


class ContactSetting(models.Model):
    email = models.EmailField(default='info@polynexus.com')
    phone = models.CharField(max_length=50, default='+91 9226318818')
    address = models.CharField(max_length=255, default='Nagpur, Maharashtra')
    est_response = models.CharField(max_length=255, default='EST RESPONSE TIME: < 15 MINUTES')

    class Meta:
        db_table = 'settings'
        verbose_name = 'Contact Settings'
        verbose_name_plural = 'Contact Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Global Contact Settings"


class HeroSetting(models.Model):
    badge = models.CharField(max_length=255, default='CO-CREATING DIGITAL EXCELLENCE')
    title_prefix = models.CharField(max_length=255, default='Building ')
    title_highlight = models.CharField(max_length=255, default='custom software')
    title_suffix = models.CharField(max_length=255, default=' to maximize your business impact')
    subtitle = models.TextField(default='We deeply understand your unique operational bottlenecks and design tailored engineering pathways to solve them. Skip rigid, off-the-shelf limitations and scale with bespoke solutions built strictly around your users, your workflows, and your long-term goals.')
    cta1_text = models.CharField(max_length=100, default='Get Your Custom Solution')
    cta1_link = models.CharField(max_length=100, default='#contact')
    cta2_text = models.CharField(max_length=100, default='View Our Services')
    cta2_link = models.CharField(max_length=100, default='#services')
    trust_indicators = models.JSONField(default=list, help_text="List of dicts containing label, value, icon, color")

    class Meta:
        db_table = 'hero_settings'
        verbose_name = 'Hero Settings'
        verbose_name_plural = 'Hero Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if created or not obj.trust_indicators:
            obj.trust_indicators = [
                {"label": "Core Team", "value": "100% Expert Led", "icon": "Sparkles", "color": "text-secondary"},
                {"label": "Performance", "value": "1.2ms Latency", "icon": "Zap", "color": "text-[#E27000]"},
                {"label": "Availability", "value": "99.99% SLA", "icon": "Activity", "color": "text-purple-500"}
            ]
            obj.save()
        return obj

    def __str__(self):
        return "Global Hero Settings"


class AdminToken(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    token = models.CharField(max_length=64, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_tokens'

    def __str__(self):
        return f"{self.user.username} - {self.token[:8]}..."

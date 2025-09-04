from django.conf import settings
from django.db import models
from django.utils.text import slugify

# 1. Category Model (matches tourism_touristspot_category)
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)  # id column: bigint, PK, IDENTITY
    name = models.CharField(max_length=100)     # name: varchar(100), EXTENDED, collation default

    class Meta:
        app_label = 'tourism'
        db_table = 'tourism_touristspot_category'

    def __str__(self):
        return self.name

# 2. Location Model (matches tourism_location)
class Location(models.Model):
    id = models.BigAutoField(primary_key=True)  # id column: bigint, PK, IDENTITY
    name = models.CharField(max_length=100)     # name: varchar(100), EXTENDED, collation default
    province = models.CharField(max_length=100, blank=True)   # province: varchar(100)
    region = models.CharField(max_length=100, blank=True)     # region: varchar(100)

    class Meta:
        app_label = 'tourism'
        db_table = 'tourism_location'

    def __str__(self):
        return self.name

# 3. TouristSpot Model (matches tourism_touristspot)
class TouristSpot(models.Model):
    id = models.BigAutoField(primary_key=True)  # id column: bigint, PK, IDENTITY
    name = models.CharField(max_length=200)         # name: varchar(200)
    description = models.TextField()                # description: text
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')  # category_id is FK to Category.id
    location = models.ForeignKey(Location, on_delete=models.CASCADE, db_column='location_id')  # location_id is FK to Location.id
    image = models.CharField(max_length=255, blank=True, null=True)  # image: filename string
    rating = models.FloatField(blank=True, null=True)                # rating: double precision
    address = models.CharField(max_length=255, blank=True, null=True)
    map_embed = models.TextField(blank=True, help_text="Google Maps embed link")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    website = models.URLField(blank=True, null=True)
    name_url = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        app_label = 'tourism'
        db_table = 'tourism_touristspot'

    def save(self, *args, **kwargs):
        if not self.name_url:
            self.name_url = slugify(self.name.replace(" ", ""))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def province(self):
        # province is on the related location
        return self.location.province if self.location else None

    @property
    def region(self):
        # region is on the related location
        return self.location.region if self.location else None

    @property
    def category_name(self):
        return self.category.name if self.category else None

    @property
    def location_name(self):
        return self.location.name if self.location else None

# 4. Review, Gallery, OperatingHour, SavedSpot, VisitedSpot remain unchanged except FK to new TouristSpot/Location/Category

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} review for {self.tourist_spot.name}'

class Gallery(models.Model):
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Image of {self.tourist_spot.name}'

class OperatingHour(models.Model):
    DAYS_OF_WEEK = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK, default='Mon')
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f'{self.tourist_spot.name} - {self.get_day_of_week_display()}'

class SavedSpot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_spots')
    spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'spot')

class VisitedSpot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visited_spots')
    spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'spot')

# --- Deprecated/legacy/CSV compatibility models below (not for normal relational use) ---
class TourismReportedSpotAlbay(models.Model):
    """
    Direct ORM mapping to tourism_reported_spots table,
    which was imported from tourism_reported_spots_albay.csv.
    """
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)  # double precision

    class Meta:
        app_label = "tourism"
        db_table = "tourism_touristspot"
        managed = False  # Django won’t try to create/migrate this table
        verbose_name = "Tourism Reported Spot"
        verbose_name_plural = "Tourism Reported Spots"

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        if self.image:
            return f"/static/images/reported_spots/albay/{self.image}"
        return "/static/images/reported_spots/albay/default.jpg"

class ReportedSpot(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="reported_spots/", blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.province})"
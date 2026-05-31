from django.db import models


class SiteStatistics(models.Model):
    """Store site-wide statistics displayed on home page"""
    beaches_count = models.IntegerField(default=12, help_text="Number of beaches")
    matrimony_profiles = models.IntegerField(default=500, help_text="Number of matrimony profiles")
    events_per_year = models.IntegerField(default=50, help_text="Events per year")
    local_vendors = models.IntegerField(default=200, help_text="Number of local vendors")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Statistics"
        verbose_name_plural = "Site Statistics"

    def __str__(self):
        return f"Statistics (Updated: {self.updated_at.strftime('%Y-%m-%d')})"


class BusTiming(models.Model):
    """Bus timings information"""
    route_name = models.CharField(max_length=200)
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    bus_type = models.CharField(max_length=50, choices=[
        ('ordinary', 'Ordinary'),
        ('express', 'Express'),
        ('deluxe', 'Deluxe'),
        ('ac', 'AC'),
    ])
    frequency = models.CharField(max_length=100, help_text="e.g., Daily, Mon-Fri, etc.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.from_location} to {self.to_location} - {self.departure_time}"


class ContactMessage(models.Model):
    """Store contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class CricketMatch(models.Model):
    """Cricket match for local live scoring"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    series_name = models.CharField(max_length=200, default='Karwar District League')
    team1_name = models.CharField(max_length=100)
    team1_score = models.CharField(max_length=50, blank=True, default='')
    team1_overs = models.CharField(max_length=20, blank=True, default='')
    team2_name = models.CharField(max_length=100)
    team2_score = models.CharField(max_length=50, blank=True, default='')
    team2_overs = models.CharField(max_length=20, blank=True, default='')
    toss_winner = models.CharField(max_length=100, blank=True, default='')
    toss_decision = models.CharField(max_length=20, blank=True, choices=[
        ('bat', 'Bat'),
        ('bowl', 'Bowl'),
    ])
    venue = models.CharField(max_length=200, blank=True, default='')
    match_date = models.DateTimeField()
    overs_limit = models.IntegerField(default=20, help_text='Total overs per side')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    result_text = models.CharField(max_length=300, blank=True, default='')
    current_batsman = models.CharField(max_length=100, blank=True, default='')
    current_bowler = models.CharField(max_length=100, blank=True, default='')
    last_commentary = models.TextField(blank=True, default='', help_text='Ball-by-ball updates')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-match_date']
        verbose_name = 'Cricket Match'
        verbose_name_plural = 'Cricket Matches'
    
    def __str__(self):
        return f"{self.team1_name} vs {self.team2_name} - {self.match_date.strftime('%d %b %Y')}"

    @staticmethod
    def team_abbr(name):
        """Generate 3-letter abbreviation from team name"""
        parts = name.strip().split()
        if len(parts) >= 3:
            return (parts[0][0] + parts[1][0] + parts[2][0]).upper()
        elif len(parts) == 2:
            return (parts[0][0] + parts[1][0:2]).upper()
        else:
            return name[0:3].upper()

    @property
    def team1_abbr(self):
        return self.team_abbr(self.team1_name)

    @property
    def team2_abbr(self):
        return self.team_abbr(self.team2_name)

    def ensure_innings(self):
        """Create both innings if they don't exist yet"""
        for num in [1, 2]:
            Innings.objects.get_or_create(
                match=self,
                innings_number=num,
                defaults={
                    'batting_team': self.team1_name if num == 1 else self.team2_name,
                    'batting_data': [{'name': f'Batter {i}', 'runs': 0, 'balls': 0, 'fours': 0, 'sixes': 0, 'how_out': 'batting', 'at_crease': False} for i in range(1, 12)],
                    'bowling_data': [{'name': f'Bowler {i}', 'overs': 0, 'maidens': 0, 'runs': 0, 'wickets': 0, 'is_active': False} for i in range(1, 9)],
                }
            )


class Innings(models.Model):
    """Per-innings scorecard data for a cricket match"""
    match = models.ForeignKey(CricketMatch, on_delete=models.CASCADE, related_name='innings_set2')
    innings_number = models.IntegerField(choices=[(1, '1st Innings'), (2, '2nd Innings')])
    batting_team = models.CharField(max_length=100, blank=True, default='')
    total_runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    overs = models.CharField(max_length=10, default='0', blank=True)
    extras = models.IntegerField(default=0)
    extras_detail = models.CharField(max_length=200, blank=True, default='', help_text='e.g. b 0, lb 2, w 5, nb 1')
    current_run_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    required_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    status_text = models.CharField(max_length=300, blank=True, default='', help_text='e.g. CSK need 45 runs in 30 balls')
    result = models.CharField(max_length=300, blank=True, default='', help_text='e.g. CSK won by 5 wickets')
    fall_of_wickets = models.TextField(blank=True, default='', help_text='e.g. 1-25 (Rohit, 3.2), 2-48 (SKY, 6.1)')
    batting_data = models.JSONField(default=list, blank=True, help_text='JSON array of batter objects')
    bowling_data = models.JSONField(default=list, blank=True, help_text='JSON array of bowler objects')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('match', 'innings_number')
        ordering = ['innings_number']
        verbose_name = 'Innings'
        verbose_name_plural = 'Innings'

    def __str__(self):
        return f"{self.match} - {self.get_innings_number_display()}"

    @property
    def score_display(self):
        """Returns formatted score like '185/4'"""
        return f"{self.total_runs}/{self.wickets}"


class MatrimonyProfile(models.Model):
    """Matrimony profile submissions"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    CASTE_CHOICES = [
        ('Gowda', 'Gowda'),
        ('Bhandari', 'Bhandari'),
        ('Gunagi', 'Gunagi'),
        ('Ambig', 'Ambig'),
        ('Konkan Maratha', 'Konkan Maratha'),
        ('Kombarpath', 'Kombarpath'),
        ('Harikantra', 'Harikantra'),
        ('Sonar', 'Sonar'),
        ('Brahman', 'Brahman'),
        ('Dalvi', 'Dalvi'),
        ('Gabith', 'Gabith'),
        ('Nadar', 'Nadar'),
        ('Other', 'Other'),
    ]
    
    # Basic Information
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.CharField(max_length=20, blank=True, help_text="e.g., 5'8\"")
    caste = models.CharField(max_length=50, choices=CASTE_CHOICES)
    photo = models.ImageField(upload_to='matrimony/profiles/', blank=True, null=True)
    
    # Education & Occupation
    qualification = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200, blank=True)
    
    # Contact Information
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    # Additional Details
    additional_info = models.TextField(blank=True, help_text="Any additional information")
    
    # Admin fields
    is_approved = models.BooleanField(default=False, help_text="Admin approval required")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Matrimony Profile'
        verbose_name_plural = 'Matrimony Profiles'
    
    def __str__(self):
        return f"{self.full_name} - {self.caste} ({self.age})"


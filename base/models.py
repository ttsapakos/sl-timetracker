# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class College(models.Model):
    name = models.CharField(primary_key=True, max_length=200)

    class Meta:
        db_table = 'College'


class CommunityPartner(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'Community_Partner'


class Course(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=200)
    department = models.ForeignKey('Department', models.DO_NOTHING)

    class Meta:
        db_table = 'Course'


class Department(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    college = models.ForeignKey(College, models.DO_NOTHING)

    class Meta:
        db_table = 'Department'


class Enrollment(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    semester = models.ForeignKey('Semester', models.DO_NOTHING)
    meeting_days = models.CharField(max_length=5)
    meeting_start_time = models.TimeField()
    meeting_end_time = models.TimeField()
    project = models.ForeignKey('Project', models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    crn = models.CharField(max_length=5)

    class Meta:
        db_table = 'Enrollment'


class Project(models.Model):
    name = models.CharField(max_length=45)
    course = models.ForeignKey(Course, models.DO_NOTHING)
    community_partner = models.ForeignKey(CommunityPartner, models.DO_NOTHING)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        db_table = 'Project'


class Record(models.Model):
    enrollment = models.ForeignKey(Enrollment, models.DO_NOTHING)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    total_hours = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0.1),
                                                                                  MaxValueValidator(24)])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    category = models.ForeignKey('RecordCategory', models.DO_NOTHING)
    is_active = models.BooleanField(default=True)
    comments = models.TextField(blank=True, null=True, validators=[MinLengthValidator(1)])
    extra_field = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Record'

    def clean(self):
        if (self.longitude and not self.latitude) or (not self.longitude and self.latitude):
            raise ValidationError(_(u"Need to provide both longitude and latitude or neither!"))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Record, self).save(*args, **kwargs)


class RecordCategory(models.Model):
    TRAININGS_AND_ORIENTATIONS = 'TO'
    DIRECT_SERVICE = 'DS'
    INDIVIDUAL_RESEARCH = 'IR'
    TEAM_RESEARCH = 'TR'
    CATEGORIES = (
        (TRAININGS_AND_ORIENTATIONS, 'Trainings & Orientations'),
        (DIRECT_SERVICE, 'Direct Service'),
        (INDIVIDUAL_RESEARCH, 'Individual Research & Planning'),
        (TEAM_RESEARCH, 'Team Research & Planning'),
    )
    name = models.CharField(primary_key=True, max_length=2, choices=CATEGORIES)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Record_Category'


class Semester(models.Model):
    name = models.CharField(primary_key=True, max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField()

    class Meta:
        db_table = 'Semester'



class UserProfile(models.Model):
    STUDENT = 'S'
    INSTRUCTOR = 'I'
    ADMIN = 'A'
    ROLE_CHOICES = (
        (STUDENT, 'Student'),
        (INSTRUCTOR, 'Instructor'),
        (ADMIN, 'Admin'),
    )
    user = models.OneToOneField(User)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=STUDENT)

    class Meta:
        db_table = 'UserProfile'

def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a user profile with a role of `instructor` if the email address is
    neu.edu or northeastern.edu. Otherwise set the role to `student`.
    """
    if created:
        role = UserProfile.STUDENT
        domain = instance.username.split('@')[-1]
        if domain in ("northeastern.edu", "neu.edu"):
            role = UserProfile.INSTRUCTOR
        UserProfile.objects.create(user=instance, role=role)

# Every time a user is created, the above method runs.
post_save.connect(create_user_profile, sender=User)

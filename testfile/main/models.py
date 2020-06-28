# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
import logging

class Academy(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'academy'


class Ast(models.Model):
    id = models.OneToOneField('Department', models.DO_NOTHING, db_column='id', primary_key=True)
    quota = models.SmallIntegerField(blank=True, null=True)
    chinese = models.FloatField()
    english = models.FloatField()
    math1 = models.FloatField()
    math2 = models.FloatField()
    physical = models.FloatField()
    chemistry = models.FloatField()
    biological = models.FloatField()
    history = models.FloatField()
    geography = models.FloatField()
    citizen = models.FloatField()

    class Meta:
        managed = False
        db_table = 'ast'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Career(models.Model):
    id = models.OneToOneField('Department', models.DO_NOTHING, db_column='id', primary_key=True)
    career1 = models.CharField(max_length=100, blank=True, null=True)
    career2 = models.CharField(max_length=100, blank=True, null=True)
    career3 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'career'


class University(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'university'

class Department(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    university = models.ForeignKey('University', models.DO_NOTHING)
    academy = models.ForeignKey(Academy, models.DO_NOTHING, db_column='academy')

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Future(models.Model):
    id = models.OneToOneField(Department, models.DO_NOTHING, db_column='id', primary_key=True)
    work_ratio = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'future'


class Gsat(models.Model):
    id = models.OneToOneField(Department, models.DO_NOTHING, db_column='id', primary_key=True)
    quota = models.SmallIntegerField(blank=True, null=True)
    chinese = models.SmallIntegerField()
    english = models.SmallIntegerField()
    math = models.SmallIntegerField()
    society = models.SmallIntegerField()
    science = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'gsat'


class Maindepartment(models.Model):
    academy = models.OneToOneField(Academy, models.DO_NOTHING, db_column='academy', primary_key=True)
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'maindepartment'
        unique_together = (('academy', 'department'),)



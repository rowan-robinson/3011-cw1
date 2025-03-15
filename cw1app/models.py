from django.db import models

# - DB MODEL : Professor
# professors of modules with a code and a name
class Professor(models.Model):
    # unique identifier 'code', one for each professor
    code = models.CharField(primary_key=True, max_length=3, unique=True, blank=True, default='AAA')
    name = models.CharField(max_length=20, blank=True, default='')
    avgRating = models.IntegerField(choices=[(-1, -1), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=-1)
    
    class Meta:
        ordering = ['code']

# - DB MODEL : Module
# a module with just a code and a name; year/semester/professor is given by specific instances
# see ModuleInstance for such information
class Module(models.Model):
    # unique identifier 'code', one for each module
    code = models.CharField(primary_key=True, max_length=3, unique=True, blank=True, default='AAA')
    name = models.CharField(max_length=20, blank=True, default='')
    
    class Meta:
        ordering = ['code']

# - DB MODEL : ModuleInstance
# a specific instance of a module, so a code and a name;
# but also the year and semester it was taught it, and the professor(s) who taught it
class ModuleInstance(models.Model):
    # unique identifier 'code' from Module model
    # CASCADE deletes this instance if the module gets deleted
    code = models.ForeignKey(Module, on_delete=models.CASCADE, to_field='code')
    year = models.IntegerField(default='2024')
    semester = models.IntegerField(choices=[(1, 1), (2, 2)])
    # denotes who teaches (leads) the module, uses a many-to-many relationship
    leaders = models.ManyToManyField(Professor)
    
    class Meta:
        ordering = ['code']

# - DB MODEL : Rating
# a rating of an instance of a module, given by a user, on a score of 1 - 5
class Rating(models.Model):
    # unique identifier 'code' from Module model
    # CASCADE deletes this instance if the module gets deleted
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, to_field='code')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, to_field='code')
    year = models.IntegerField(default='2024')
    semester = models.IntegerField(choices=[(1, 1), (2, 2)])
    # user gives a score from 1 - 5
    score = models.IntegerField(choices=[
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)
    ])
    
    class Meta:
        unique_together = ('user', 'professor', 'module', 'year', 'semester', 'score')
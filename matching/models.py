from django.db import models

class MatchingQueue(models.Model):
    user_id = models.CharField(max_length=100, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='waiting')
    match_id = models.CharField(max_length=100, blank=True, null=True)
    
class MatchUser(models.Model):
    user_id = models.CharField(max_length=100)

    def __str__(self):
        return self.user_id
    
class MatchGroup(models.Model):
    match_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    additional_info = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(MatchUser)  # User 모델과의 ManyToMany 관계 설정
    user_id1 = models.CharField(max_length=100, null=True)
    user_id2 = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"MatchGroup #{self.id}"


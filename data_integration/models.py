from django.core.serializers import deserialize
from django.db import models

# Create your models here.

class ProjectModel(models.Model):
    name = models.CharField(max_length=500)
    businessUnit = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    createdTime = models.DateTimeField(auto_now_add=True, null=True)
    lastAccessed = models.DateTimeField(auto_now=True, null=True)

class ClusterModel(models.Model):
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    nodes = models.IntegerField(default=0)
    # 0 1 2 3分别为
    autoSuspend = models.IntegerField(default=0)
    date = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    # 集群的状态：0停止，1运行，2挂起?
    statusOfCluster = models.IntegerField(default=0)
    createdTime = models.DateTimeField(auto_now_add=True, null=True)
    lastAccessed = models.DateTimeField(auto_now=True, null=True)
    projectOfCluster = models.ForeignKey(ProjectModel,on_delete=models.CASCADE)

class FlowModel(models.Model):
    name = models.CharField(max_length=500)
    status = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    dataOfFlow = models.TextField()
    createdTime = models.DateTimeField(auto_now_add=True)
    lastAccessed = models.DateTimeField(auto_now=True)
    clusterOfFlow= models.ForeignKey(ClusterModel,on_delete=models.CASCADE)

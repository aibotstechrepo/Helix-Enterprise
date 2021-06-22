from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
import jsonfield
# Create your models here.
class task_creation(models.Model):
	task_id = models.CharField(max_length = 100 , primary_key = True)
	task_name = models.CharField(max_length = 100)
	task_desc = models.CharField(max_length = 100)
	template_id = models.CharField(max_length = 100)
	input_file_name = models.CharField(max_length = 1000)
	output_file_name = models.CharField(max_length = 1000)
	file_name_pattern = models.CharField(max_length = 100)
	status = models.CharField(max_length = 100 , default="Pending")


class viewdatafilepath(models.Model):
	dataid = models.AutoField(primary_key=True)
	timestamp = models.CharField(max_length = 1000)
	inputfilelocation = models.CharField(max_length = 10000)
	filename = models.CharField(max_length = 10000)
	#arr(arr(arr(arr(arr(arr(arr(main threre elements)))))))
	#EngineData = ArrayField(ArrayField(ArrayField(ArrayField(ArrayField(ArrayField(ArrayField(ArrayField(models.CharField(max_length=10000, blank=True)))))))))
	EngineData = models.TextField()
	dataextracted = models.IntegerField()
	dataaccuracy = models.IntegerField()
	noisepercentage = models.IntegerField()
	totalpages = models.IntegerField()
	status = models.CharField(max_length = 1000,default = "pending")
	EngineData1 = jsonfield.JSONField(default='')

	
class tabletask(models.Model):
	taskid = models.AutoField(primary_key=True)
	timestamp = models.CharField(max_length = 1000)
	inputfilelocation = models.CharField(max_length = 100000)
	outputfilelocatin = models.CharField(max_length = 100000)
	processedfilelocation = models.CharField(max_length = 100000)
	excelfilename = models.CharField(max_length = 100000)
	totalnumberoffiles = models.IntegerField()

class labeldata(models.Model):
	label = models.CharField(max_length=10000)

class testtable(models.Model):
	tid = models.IntegerField()
	myfile = models.FileField(validators=[
        FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'ppt', 'xlsx'])
    ])

	#testarray = ArrayField(ArrayField(models.CharField(max_length = 1000),blank = True))
	



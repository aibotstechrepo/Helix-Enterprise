from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect 
from .models import *
import json
import threading
import time
import os
import subprocess
import shutil
from shutil import copyfile
from datetime import date, datetime
import asyncio
import media.Hocr_Functionality as hocrf
import pandas as pd
from bs4 import BeautifulSoup
import cv2
import csv




#================ Login Check =====================
def login(request):
	return render(request,"login.html")

def  login_check(request):
	name = request.POST['name']
	pswd = request.POST['pswd']
	if name == "user@abt.com" and pswd == "user":
		print("Succes User")
		return HttpResponse(json.dumps("Suceess_user"), content_type="application/json")
	elif name == "admin@mediast.com" and pswd == "admin":
		return HttpResponse(json.dumps("Suceess_process"), content_type="application/json")
	else:
		return HttpResponse(json.dumps("unSuceess"), content_type="application/json")


## Move images from input loction to project directory and displaying the images.
PInputaddress = r"D:\OCR\Helix Enterprise Engine v1.0\static\tempdata"

## Dictonarty Excel address
DictFile = r"D:\OCR\Helix Enterprise Engine v1.0\Dictonary.xlsx"

## Excel output file
ExcelOutputFile = r"output.xlsx"

##Excel Label Data
ExcelLabelData = r"D:\OCR\Helix Enterprise Engine v1.0\media\1library.csv"

##Image magicexe Address

ImageMagickAddress = r"C:\Program Files\ImageMagick-7.0.9-Q16\convert.exe"


#================= queue =========================
def copytree(src,i, dst = PInputaddress, symlinks=False, ignore=None):

	if os.path.isdir(dst+"\\"+i.rstrip(".pdf")) == False:
		os.mkdir(dst+"\\"+i.rstrip(".pdf"))

		for item in os.listdir(src):
		    s = os.path.join(src, item)
		    d = os.path.join(dst + "\\" + i.rstrip(".pdf"), item)
		    if os.path.isdir(s):
		        shutil.copytree(s, d, symlinks, ignore)
		    else:
		        shutil.copy2(s, d)

def queue(request):
	queuedata = viewdatafilepath.objects.all()
	return render(request,"queue.html",{'queuedata':queuedata})

#================ Training Model ================
# def Training(request,id):
# 	return render(request,"TrainingEngine.html",{'id':id})


def Training(request,id): 
	return render(request,"TrainingEngine-V12.html",{'id':id})

def LalbelData(request):
	queuedata = labeldata.objects.all()
	SendLabel = []
	for q in queuedata:
		SendLabel.append(q.label)

	print("asdsdsd",SendLabel)
	sdata = { 'Labels' : SendLabel}
	return HttpResponse(json.dumps(sdata), content_type="application/json")


def FindListOfHeaders(request):
	f = open(r"D:\OCR\Helix Enterprise Engine v1.0\media\1library-1-Mapping.csv", "r")
	reader = csv.reader(f)
	headers = next(reader,None)
	f.close()
	sdata = { 'Labels' : headers}
	return HttpResponse(json.dumps(sdata), content_type="application/json")

def FindSubList(request):
	sublabel = request.POST['sublabel']
	f = open(r"D:\OCR\Helix Enterprise Engine v1.0\media\1library-1-Mapping.csv", "r")
	reader = csv.reader(f)
	headers = next(reader,None)
	f.close()

	df = pd.read_csv(r"D:\OCR\Helix Enterprise Engine v1.0\media\1library-1-Mapping.csv", usecols=headers)
	incoms = df[sublabel].values.tolist()
	incoms = [incom for incom in incoms if str(incom) != 'nan']
	sdata = { 'sublabels' : incoms}
	return HttpResponse(json.dumps(sdata), content_type="application/json")

def PushValuesToCSV(request):
	ALabelsArray = request.POST['ALabelsArray']
	ASubLabelArray = request.POST['ASubLabelArray']
	ANewLabelArray = request.POST['ANewLabelArray']

	ALabelsArray = json.loads(ALabelsArray)
	ASubLabelArray = json.loads(ASubLabelArray)
	ANewLabelArray = json.loads(ANewLabelArray)

	print(ALabelsArray,ASubLabelArray,ANewLabelArray)

	f = open(r"D:\OCR\Helix Enterprise Engine v1.0\media\1library-1-Mapping.csv", "r")
	reader = csv.reader(f)
	headers = next(reader,None)
	f.close()

	df = pd.read_csv(r"D:\OCR\Helix Enterprise Engine v1.0\media\1library-1-Mapping.csv", usecols=headers)

	i = 0
	for La in ALabelsArray:
	    if La == "NewLabel":
	        df[ANewLabelArray[i]] = ''
	        df.set_value(len(df), ANewLabelArray[i], ASubLabelArray[i])
	    if ASubLabelArray[i] == "NewSub":
	        df.set_value(len(df), La, ANewLabelArray[i])
	    i += 1

	df.to_csv(r'D:\OCR\Helix Enterprise Engine v1.0\media\1library-1-Mapping.csv',index=False)

	# df.to_excel(r'D:\OCR_WEB_DEVELOPEMENT\Helix_OCR\media\Temp.csv',index=False)

	return HttpResponse(json.dumps("sdata"), content_type="application/json")	

def PushLables(request):

	# ALabelArray = request.POST['ALabelArray']
	# ASepArray = request.POST['ASepArray']

	# ALabelArray = json.loads(ALabelArray)
	# ASepArray = json.loads(ASepArray)

	# print(ALabelArray)

	# writer = pd.ExcelWriter(ExcelLabelData, engine='xlsxwriter')


	# df2 = pd.DataFrame(ALabelArray)
	# # df2 = df2.transpose()
	# df2.to_excel(writer,header=False,index=False) 
	
	# writer.save()

	# with open(ExcelLabelData, 'a') as file:
	# 	writer = csv.writer(file)
	# 	try:
	# 		for La in ALabelArray:
	# 			writer.writerow(['']+['']+['']+[La])
	# 	except Exception as e:
	# 		print(e)


	filename = request.POST['filename']

	# print(PInputaddress + "\\"+ filename + ".pdf")

	try:
		if os.path.isfile(PInputaddress + "\\"+ filename +"\\"+filename + ".hocr"):
			

			print("====== engine funcion called =======")
			extarctedoututdata = hocrf.mainfunction(PInputaddress + "\\"+ filename +"\\"+filename + ".hocr") 
			print("====== engine funcion ended =======")
			#print(extarctedoututdata) 
			testd = viewdatafilepath.objects.filter(filename=filename).update(EngineData=extarctedoututdata)
			print("======== Data Saved ================") 

	except Exception as e:
		print(e)




	return HttpResponse(json.dumps("rjdata"), content_type="application/json")


#================ data view ======================

def dataview(request,id):
	#pippin = view_data_filepath.objects.create(filepath='Peregrin Took',EngineData=['apples', 'lembas bread', 'potatoes',['t','j']])
	#pippin.save()
	# print(id)
	return render(request,"data_view.html",{'id':id})


def retivedatafromdb(request):
	rid = request.POST['rid']
	rdata = viewdatafilepath.objects.filter(dataid = rid)

	for r in rdata:
		finalarraytojson = TextToArray(r.EngineData)
		filaname = r.filename

	filepath = PInputaddress
	listoffilename = []
	for r, d, f in os.walk(filepath + "\\" + filaname.rstrip(".pdf") ):
		for file in f:
			if '.png' in file:
				listoffilename.append(file)
	fileNames = []
	if len(listoffilename) == 0:
		fileNames.append(listoffilename[0])
	elif len(listoffilename) == 1:
		fileNames.append(listoffilename[0])
	else:
		if len(listoffilename) > -1:
			fileName = filaname.rstrip(".pdf")
			for i in range(len(listoffilename)):
				fileNames.append(fileName+"-"+str(i)+".png")

	

	
	#tempdataarr = [[[[[' Date Qty “Unit Rate', 894, 1632, 977, 1679, 70], [':', 1509, 1620, 1521, 1680, 14], [' Gross Dise. Amt Net Amt', 1582, 1644, 1681, 1671, 93]]], [[[' SI', ' Particulars', ' | Date', ' Qty', ' “Unit Rate', ' :', ' Gross', ' Dise. Amt', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', ' i', '', '', ' _', ' Amount |', '', '', ''], [100, 100, 100, 100, 100]], [[' :', ' Administrative', ' Charges', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 1', ' [Administrative', ' surcharge {29-10-2019', ' 1)', ' 3,708.00;', '', ' ~———3,708.00.', ' 185.40,', '', ''], [100, 100, 100, 100, 100]], [['', ' Sub Total :', '', '', '', '', ' 3,708.00', ' 185.40', '', ''], [100, 100, 100, 100, 100]], [[' .', ' Bed Charges', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 2 |', ' DELUXEROOMCHARGES', ' 25-10-2019', '', ' 4,500.00.', '', ' 4,500.00', ' «225.00,', '', ' «4,275.00.'], [100, 100, 100, 100, 100]], [[' 3', ' DELUXE', ' ROOM CHARGES 26-10-2019', ' 1', ' 4,500.00', '', ' 4,500.00', ' 225.00', '', ' 4 275.'], [100, 100, 100, 100, 100]], [[' 4', ' ‘DELUXE', ' ROOM CHARGES = : 27-10-2019', ' 1', ' 4,500.00', '', ' 4,500.00', ' 225.00', '', ' 4, 275,'], [100, 100, 100, 100, 100]], [[' 5', ' |DELUXEROOMCHARGES', ' 28-10-2019', ' 1', ' 4,500.00', '', ' 4,500.00', ' 225,00', '', ''], [100, 100, 100, 100, 100]], [[' 6', ' Room Charges', ' (Half Day} 29-10-2019', ' 1', ' 2,250,00', '', ' 2,200,00', ' 112,505', '', ' 2,1'], [100, 100, 100, 100, 100]], [['', ' Sub Total :', '', '','', '', ' 20,250.00', ' 1012.50', '', ''], [100, 100, 100, 100, 100]], [[' secant', '', ' ses', '', '', '', ' one', ' a', '', ' .'], [100, 100, 100, 100, 100]], [['', '‘Consultation', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 7', ' IP visit (Dr', ' Pushkar Vinayak 25-10-2019', ' 1', ' 650.00', '', ' 650,00!', ' 32.50', '', ''], [100, 100, 100, 100, 100]], [[' ,', ' Bhide}', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 8 IP', ' visit (Dr', ' Pushkar Vinayak 26-10-2019', ' 2:', ' 650.00', '', ' 1,300. 00.', ' 65.00:', '', ''], [100, 100, 100, 100, 100]]]], [[], [[[' Sl', ' Particulars', ' Date', ' Qty', ' Unit Rate', '', ' Gross', ' Disc. Amt |', ' Net', ' a'], [100, 100, 100, 100, 100]], [['', '', '', '', '', '', ' Amount', '', '', ''], [100, 100, 100, 100, 100]], [['', ' Consultation', '','', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 9', ' IP visit (Dr', ' Pushkar Vinayak - 27-10-2019', ' 1', ' ~~ 650.00,', '', ' «650.00', ' 32.50', '', ''], [100, 100, 100, 100, 100]], [['', ' Bhide)', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 10', ' IP visit (Dr', ' Priya Rajesh 28-F0-2019', ' 2', '', ' 650.00:', ' 1,300.00', ' 65.00', '', ''], [100, 100, 100, 100, 100]], [['', ' Mankare)', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 14', ' IP visit (Dr', ' Pushkat Vinayak 28-10-2019', ' 1', ' 650,00', '', ' 650.00;', ' 32.50', '', ''], [100, 100, 100, 100, 100]], [[' :', ' Bhide)', '', '', ' . -', '', '', '', '', ''], [100, 100, 100, 100, 100]], [['', ' Sub Total :', '', '', '', '', ' 4,550.00', ' 227.50', '', ''], [100, 100, 100, 100, 100]], [['', ' DRUGS', '', '', '', '','', '', '', ''], [100, 100, 100, 100, 100]], [[' 42', ' (|PANSEC40MGINJ', ' | 25-10-2019', ' 2', '', ' “48.79', ' «97.58.', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' i', ' AFM9059/', ' 31-05-2021', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 13', ' NS S500ML IV', ' | 93NI304072/ 25-10-2019', ' 1', ' 30.70', '',' 30.70', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-08-2022', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 14', ' |EMESET INJ', ' 2MG/ML X 2ML 25-10-2019', ' 2', ' 12.81', '', ' 25.62', ' 0.00:', '', ''], [100, 100, 100, 100, 100]], [[' |', ' L690218/', ' 30-06-2022', '', '', '', ' :', '', '', ''], [100, 100, 100, 100, 100]], [[' 15', ' RLECTRAL', ' 25 SACHETS x 25-10-2019', ' 1', '', ' 19,39:', ' 19.39,', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' i', ' 21.80GM |', ' 039G017/', '', ' i', '', ' i', '', '', ''], [100, 100, 100, 100, 100]], [['', ' 3006-2021', ' |', '', ' 2', '', '', '', '', ''], [100, 100, 100, 100, 100]]]], [[[[' MRN', 192, 842, 280, 886, 92], [':', 519, 853, 523, 869, 0], [' ABI104583', 571, 848, 748, 877, 52]]], [[[' Sl -', ' "Particulars', ' Date', ' Oty', ' Unit Rate', '', ' ~ Gross', ' Disc. Amt', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', ' :', '', '', '', ' Amount', '', '', ''], [100, 100, 100, 100, 100]], [['', ' DRUGS', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 18 |', ' DNS 500MLIV|', ' 93ni111003/ 25-10-2019', ' 3', '', ' 33.64!', ' 100.92,', '', ' 0.00;', ''],[100, 100, 100, 100, 100]], [[' i', ' 31-08-2022', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 17', ' CALPOL', ' TAB 15 S| EW578/ =| 25-10-2019', '15', ' 0.97', '', ' 14.55', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 30-06-2022', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 18', ' DNS 500ML', ' IV | 93ni111003/ =: 26-10-2019', ' 3', ' 33.64', '', ' 100,92', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-08-2022', '', '', '', '', ' . .', 'So', '', ''], [100, 100, 100, 100, 100]], [[' 19', ' {ELECTRAL', ' 25SACHETSx — 26-10-2019', ' 3', '', ' 19.39:', ' 58.17.', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 21,80 GM |', ' 069H002/', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-07-2021', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' :20', ' EMESET INJ', ' 2MG/ML X 2ML i 26-10-2019', ' 3:', ' 12,81', '', ' 38,43', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' : {', ' L690218/', ' 30-06-2022 i', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 21', ' MCOSVIR 75', ' MG CAP (X) | 26-10«2019', ' 10', ' 49.50', '', ' 495.00', ' 0.00,', '', ''],[100, 100, 100, 100, 100]], [['', ' MCO-035/', ' 31-07-2022', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 22', ' PANSEC', ' 40MG INI | 26-10-2019', ' 1', ' 48.79', '', ' 48,79', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' AFM9059/', ' 31-05-2021', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 23', ' SPORLAC', ' PLUS SACHET | 26-10-2019', ' 3:', ' 12,32', '', ' 36.96', ' 0.00:', '', ''], [100, 100, 100, 100, 100]], [['', ' 2AQ219002/', ' 31-07-2020', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 24', ' Z&D DS', ' 20MG (DRY SYP) 26-10-2019', ' 1', ' 80.50', '', ' 80.50', ' 0.00:', '', ''], [100, 100, 100, 100, 100]], [['', ' ISML | AH90052/', ' 31-05-2021:', ' :', ' :', '', '', ' :', '', ''], [100, 100, 100, 100, 100]]]], [[[[' MRN > ABI104583 Patient Name', 201, 855, 288, 897, 73], [':', 1701, 862, 1705, 880, 74], [' ADITYA BHARDWAJ', 1758, 857, 1898, 884, 72]], [[' Date', 1500, 913, 1573, 938, 94], [':', 1701, 916, 1705, 932, 72], [' 29/10/2019 11:06 AM', 1758, 911, 1924, 938, 74]], [[' Address', 201, 953, 330, 1003, 96], [':', 523, 970, 528, 986, 90], [' FLAT NO.402, MANDHAR, PRASUN DHAM, CHINCHWAD, , 411033, PUNE, Maharashtra, INDIA', 577, 965, 667, 992, 85]]], [[[' ‘Sl', ' Particulars', ' = ate', ' gty,', ' Wnt Rate,', '', ' Gross.', ' Disc. Amt |', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', ' :', '', '', '', ' Amount', '', '', ''], [100, 100, 100, 100, 100]], [['', ' DRUGS', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 26 |', ' DNS 500MLIV|93ni111003/', ' | 27-10-2019', '', ' 333A.', '', ' 100,92;', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-08-2022', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 26', ' ?ELECTRAL', ' 25 SACHETS x 27-10-2019', ' 2)', '', ' 19.39', ' 38.78', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' :21.80 GM |', ' 069HO002/ i', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' :', ' 31-07-2021', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 27', ' EMESET INJ', ' 2MG/ML X 2ML : 27-10-2019 :', ' 4', '', ' 12.81', ' . $1.24', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' i |',' 1.690218/', ' 30-06-2022 :', '', '', ' :', '', '', '', ''], [100, 100, 100, 100, 100]], [[' :28', ' NS 500ML', ' TV | 93NI304072/ 27-10-2019', ' 1', '', ' 30.70', ' 30.70', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-08-2022', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' :29', ' PANSEC', ' 40MGINJ | 27-10-2019', ' 1', '', ' 48.79', ' 48.79', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' :', ' AFM9059/', ' 31-05-2021', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 30 i:', ' SPORLAC', ' PLUS SACHET | 27-10-2019', ' 3', '', ' 12.32', ' 36.96', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' :G2AQ219007/', ' 30-11-2020', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 31 |', ' ELECTRAL25SACHETSx', ' | 28-10-2019', ' 2', '', ' 19,39', ' 38.78:', ' 0.00:', '', ''], [100, 100, 100, 100, 100]], [[' :', ' 21.80 GM |', ' 069H002/ :', '', '', ' :', '', ' :', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-07-2021', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 32 |', ' PANSEC', ' 40MG INI | 28-10-2019', ' ir', '', ' 49.79:', ' 49,79', ' 0.00:', '', ''], [100, 100, 100, 100, 100]], [['i', ' AFM9050/', ' 31-05-2021 :', '', '', '', '', ' :', '', ''], [100, 100, 100, 100, 100]], [[' THES IS', ' A SYSTEM', ' GENERATED REPORT', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' Prepared', ' By', ' Pravin Dabhade', '', '', '', '', ' Prepared On =', ' 29/10/2019', ''], [100, 100, 100, 100, 100]], [[' Generated', ' By', ' Pravin Dabhade', '', '', '', '', ' Generated On =.', ' 29/10/2019', ''], [100, 100, 100, 100, 100]]]], [[[[' Date Oty', 898, 1641, 985, 1684, 87], [':', 1258, 1626, 1269, 1686, 6], [' Unit Rate os Gross Disc. Amt Net Amt', 1321, 1648, 1386, 1674, 80]]], [[[' Sl', ' Particulars', ' Date', ' Oty :', ' Unit Rate', ' os', ' Gross',' Disc. Amt', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', '', ' i', '', '', ' Amount', '', '', ''], [100, 100, 100, 100, 100]], [['', ' DRUGS', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 33°', ' EMESHT INJ', ' 2MG/ML X 2ML / 28-10-2019', '', ' 1 BL', '', ' 25.62', '', ' 0.00', ''], [100, 100, 100, 100, 100]], [[' |', ' L690218/', ' 30-06-2022', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 34', ' SPORLAC', ' PLUS SACHET | 28-10-2019', ' 1', ' 12,32', '',' 12.32:', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' G2A0219007/', ' 30-11-2020', '', '', '', ' :', '', '', ''], [100, 100, 100, 100, 100]], [[' :35', ' DNSS500ML', ' IV | 93ni111003/ =: 28-10-2019', ' 2', ' 33.64', '', ' 67,28', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-08-2022', '', '', '', '', '', '', '',''], [100, 100, 100, 100, 100]], [['', ' Sub Total :', '', '', '', '', ' 1,648.71', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' :', ' Diet Items', '', '', '', '','', '', '', ''], [100, 100, 100, 100, 100]], [[' %', ' Mineral Water', ' Siege :', ' me', '', ' een', '', ' en', '', ''], [100, 100, 100, 100, 100]], [[' 37', ' MineralWater', ' 26-10-2019', ' 1', ' 20.00', '', ' 20,00', ' 1.00', '', ''], [100, 100, 100, 100, 100]], [[' 38 |', ' Veg Sandwich', ' 27-10-2019', ' I', ' 35.00.', '', ' = 35.00', ' 1.75', '', ''], [100, 100, 100, 100, 100]], [[' 39 «|', ' Tea', ' 27-10-2019', ' 2', ' ~', ' 18.00,', ' 36.00', ' 1.80', '', ''], [100, 100, 100, 100, 100]], [[' 40', ' Tea', ' 27-10-2019', ' 1', ' 18.00', '', ' 18.00', ' 0,90', '', ''], [100, 100, 100, 100, 100]], [[' 41', ' (Upma', ' 27-10-2019', ' 1', ' 40.00', '', ' 40.00',' 2.00:', '', ''], [100, 100, 100, 100, 100]], [['', ' Sub Total ;', '', '', '', '', ' 169.00', ' 8.45', '', ' -'], [100, 100, 100, 100, 100]]]], [[], [[[' Sl', ' Particulars', ' Date', ' Oty,', ' UnitRate 7', ' P', ' Gross |', ' Disc. Amt', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', '', '', '', ' :', ' Amount', '', '', ''], [100, 100, 100, 100, 100]], [[' .', ' Laboratory', ' Services', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 42', ' (ELECTROLYTES', ' -BLOOD 25-10-2019', ' “Th', '', ' 850,00:', ' "$50.00.', ' 42,50', '', ' .'], [100, 100, 100, 100, 100]], [['', ' (Nak & Cl)', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 43 |', ' HAEMOGRAM', ' | 25-10-2019', ' “Le', '', ' 400,00', ' 400,00', ' 20.00', '', ''], [100, 100, 100, 100, 100]], [[' 44', ' ALANINE', ' TRANSAMINASE 25-10-2019', ' ert', ' 375,00', '', ' 375,00', ' 18.75', '', ''], [100, 100, 100, 100, 100]], [['', ' {ALT/SGPT)', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 45 |', ' RAPID', ' MALARIAL ANTIGEN 25-10-2019', ' 1', '', ' 923.00.', ' 923,00.', ' 46.15', '', ''], [100, 100, 100, 100, 100]], [[' ‘46', ' CRP(C-REACTIVE', ' 25-10-2019', '', ' 1 541.00', '', ' 541,00', ' 27.05', '', ''], [100, 100, 100, 100, 100]], [['', ' PROTEIN)-', ' Full Range :', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 47', ' FERRITIN', ' . 25-10-2019', ' i', ' 1,076.00', '', ' 1,076.00', ' 53.80:', '', ''], [100, 100, 100, 100, 100]], [[' 48', ' AEROBIC', ' BLOOD CULTURE. | 25-10-2019', '', ' 1 1,771.00', '', ' 1,771.00.', ' 88,55,', '', ''], [100, 100, 100, 100, 100]], [['', ' BY BACTALERT', ' RAPID', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [['', ' METHOD', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 49°', ' HAEMOGRAM', ' 26-10-2019', '', ' 429.00', '', ' 449.00,', ' 22.45,', '', ''], [100, 100, 100, 100, 100]], [[' 136°"', ' ngs', ' Anboay Gants 7° i019', '', ' eee', '', ' vases', '', ' areas', ''], [100, 100, 100, 100, 100]],[[' "51', ' Dengue', ' Antigen (NS1) "26-10-2019', ' 1', '', '', ' 600.00:', '', '', ''], [100, 100, 100, 100, 100]], [[' 52', ' Dengue Antibody', ' (IgG) 2610-2019', 'Le', '', '', ' 600.00', ' 30', '', ' .'], [100, 100, 100, 100, 100]], [[' 53', ' HAEMOGRAM', ' 27-10-2019', ' L:', '', '', ' "449.00:', '', '', ''], [100, 100, 100, 100, 100]], [[' THIS IS', ' A SYSTEM', ' GENERATED REPORT', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' Prepared', ' By', ' Pravin Dabhade', '', '', '', '', ' Prepared On', ' 29/10/2019', ''], [100, 100, 100, 100, 100]]]], [[], [[[' “Sl', ' Particulars', ' Date', ' Oty', ' Unit Rate', '', ' Gross', ' Disc. Amt |', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', '', '', '', '', ' Amount', '', '', ''], [100, 100, 100, 100, 100]], [['', ' Laboratory', ' Services', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 55', ' HAEMOGRAM', ' 29-10-2019', ' 1', ' 449.00', '', ' 449.00', '', '', ''], [100, 100, 100, 100, 100]], [['', ' Sub Total :','', '', '', '', ' 9,532.00', ' 476.60', ' 9055.399999999', ''], [100, 100, 100, 100, 100]], [['', ' MATERIALS', '', ' |', '', ' -', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 56', ' SYRINGE', ' SML (ROMO JET)| 25-10-2019', ' 4', ' 7.50', '', ' 30.00:', ' 0.00;', '', ''], [100, 100, 100, 100, 100]], [['', ' G39294/', ' 30-08-2023', '', '', '', ' i', ' :', '', ''], [100, 100, 100, 100, 100]], [[' 87', ' =SYRINGE', ' 2ML (ROMO JET) | | 25-10-2019', ' I', '', ' 6.00.', ' 6.00;', ' 0.00:', '', ''], [100, 100, 100, 100, 100]], [['', ' G38299/', ' 31-05-2023', '', '', ' i', ' :', '', '', ''], [100, 100, 100, 100, 100]], [[' 58', ' SYRINGE', ' 1OML (ROMO JET) | 25-10-2019', ' 4', '', ' 12.00,', ' 48.00;', ' 0,00', '', ''], [100, 100, 100, 100, 100]], [[' |', ' G393 16/', ' 31-08-2023', '', '', '', '', '', '', ''], [100, 100, 100, 100,100]], [[' 59', '  Q-SYTE', ' ACACIA BI- 25-10-2019', ' 1', ' 391.00', '', ' 391.00', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' :', ' EXTENSION', ' STET REF', '', '', '', ' i', '', '', ''], [100, 100, 100, 100, 100]], [['', ' 385163 |', ' 9014666/ 31-12-2021:', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 60', 'IV SET', ' (ROMSON) | G37840/ | 25-10-2019', ' 1', ' 293.06', '', ' 293.00', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [['', ' 31-03-2023', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' :61', ' =INTROCAN', ' WG-24 | . 25-10-2019', ' 1', ' 250.00', '', ' 250.00', ' 0.00,', '', ''], [100, 100, 100, 100, 100]], [[' i', ' 18E24G8391/', ' 31-05-2023', '', '', ' i', '', ' i', '', ''], [100, 100, 100, 100, 100]]]], [[], [[[' sl', ' Particulars', ' Date', ' Oty,', ' ‘Unit Rate', '', ' Gross', ' ‘Disc. Amt |', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', ' i', '', '', ' :', ' Amount', ' i', '', ''], [100, 100, 100, 100, 100]], [['', ' MATERIALS', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 62', ' HANDRUBCHG100ML|', ' (25-10-2019', '', '', ' 99000,', ' 220.00', ' 000°', '', ''], [100, 100,100, 100, 100]], [['', ' RO7190625/', ' 30-06-2021', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 63', ' GLOVES', ' MICRO OPTIC 25-10-2019', ' Ll:', ' 95.00', '', ' 95,00', ' 6.00', '', ''], [100, 100, 100, 100, 100]], [['', ' STERILE', ' NO.-6.5 |', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [['', ' 1909055605/', ' 30-09-2022', '', '', ' :', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 64.', ' COTTON.BALLS', ' .5GM X 200 | 25-10-2019', ' ]', ' 35.00', '', ' 35,00', '0.00', '', ''], [100, 100, 100, 100, 100]], [[' |', ' 0319366L/', ' 29-02-2024', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 65', ' COTTON', ' BALLS .5GM XK 200 : 25-10-2019 :', ' 1', ' 35.00', '', ' 35,00', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' |', ' 0319366L/', ' 29-02-2024', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 66', ' SYRINGE', ' 5ML (ROMO JET) | 26-10-2019', ' 3:', ' 7.50', '', ' 37.50', ' 0.00:', '', ''], [100, 100, 100, 100, 100]], [['', ' G39294/', ' 30-08-2023', ' :', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 67', ' SYRINGE', ' 2ML (ROMO JET)| : 26-10-2019', ' 4.', ' 6,00.', '', ' 24,00:', ' 9.00', '', ''], [100, 100, 100, 100, 100]], [['', ' G38299/', ' 31-05-2023', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 68', ' URINE POT', ' MALE 26-10-2019', ' ]', ' 70.00', '', ' 70.00', ' 0,00 :', '', ''], [100, 100, 100, 100, 100]], [['', ' (PLASTIC) |', ' URINE POT', '', '', '', '', ' :', '', ''], [100, 100, 100, 100, 100]], [['', ' MALE/', ' 28-02-2022', '', '', '', ' :', '', '', ''], [100, 100, 100, 100, 100]], [[' :69', ' SYRINGE', ' 2ML (ROMO JET} | : 27-10-2019', ' 5:', '', ' 6.00:', ' 30.00:', ' 0.00', '', ''], [100, 100, 100, 100, 100]], [[' :', ' :G38299/', ' 31-05-2023', '', '', '', ' i', '', '', ''], [100, 100, 100, 100, 100]], [[' THIS IS', ' A SYSTEM', ' GENERATED REPORT', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' Prepared', ' By', ' Pravin Dabhade', '', '', '', '', ' PreparedOn =', ' 29/10/2019', ''], [100, 100, 100, 100, 100]]]], [[], [[[' sl', ' Particulars', ' Date', ' Oty |', ' Unit Rate', '', ' Gross', ' ise. Amt', ' Net', ' Amt'], [100, 100, 100, 100, 100]], [['', '', '', ' :', '', '', ' Amount', '', '', ''], [100, 100, 100, 100, 100]], [[' :', ' MATERIALS', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 70 |', ' SYRINGE', ' 5ML (ROMO JET)| (27-10-2019', ' 1', ' 7.50', '', ' 7.50,', ' 0.00:', '', ' ~'], [100, 100, 100, 100, 100]], [['', ' G39294/', ' 30-08-2023 :', '', '', '', '', ' i', '', ''], [100, 100, 100, 100, 100]], [['', ' Sub Total :', '', '', '', '', ' 1,572.00', ' 6.00', '', ''], [100, 100, 100, 100, 100]], [[' i .', ' ‘Nursing Care', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [[' 71', ' Nursing', ' Charges — 25-10-2019 :', ' Li', ' 550.00', '', ' 530.00','', ' :', ''], [100, 100, 100, 100, 100]], [[' 72 =|', ' Nursing', ' Charges 26-10-2019', ' 1', ' 550.00', '', ' 550.00', '', '', ''], [100, 100, 100, 100, 100]], [[' 73', ' Nursing', ' Charges (27-10-2019', ' 1', ' 550.00', '', ' 550.00', '', '', ''], [100, 100, 100, 100, 100]], [[' 74 |', ' Nursing', ' Charges 28-10-2019', ' 1', '', ' 550.00.', ' 550.00', '', '', ''], [100, 100, 100, 100, 100]], [[' 75', ' Nursing', ' Charges 29-10-2019', ' L', ' 550.00', '', ' $50.00:', '', '', ''], [100, 100, 100,100, 100]], [['', ' Sub Total :', '', '', '', '', ' 2,750.00', ' 137.50', '', ''], [100, 100, 100, 100, 100]], [['', ' Others', '', '', '', '', '', '', '', ''], [100, 100, 100, 100, 100]], [['', ' “Biomedical', ' Waste Charges 29-10-2019', ' L', '', ' 50.00.', ' 50.00:', ' 2.50.', '', ''], [100, 100, 100, 100, 100]], [['', ' Sub Total:', '', '', '', '', ' 50.00', ' 2.50', '', ''], [100, 100, 100, 100, 100]]]], [[[[' MRN * AB1104583 Patient Name', 202, 853, 290, 897, 78], [':', 1702, 868, 1707, 884, 29], [' ADITYA BHARDWAJ', 1759, 863, 1901, 892, 54]], [[' Address', 201, 959, 330, 1002, 94], [':', 525, 970, 529, 986, 56], [' FLAT NO,402, MANDHAR, PRASUN DHAM, CHINCHWAD, , 411033, PUNE, Maharashtra, INDIA', 579, 971, 670, 998, 88]], [[' Discharge Summary', 1367, 1184, 1522, 1255, 76], [':', 1673, 1184, 1702, 1240, 60], [' 24 |', 1746,1199, 1815, 1283, 75]]], [[['', '', '', '', '', '', '', ' Discount :', '', ''], [100, 100, 100, 100, 100]], [['', '', '', '', '', '', '', ' Total :', '', ''], [100, 100, 100, 100, 100]], [['', '', '', '', '', '', '', ' Sponsor Amount :', '', ''], [100, 100, 100, 100, 100]], [['', '', ' —_', '', ' -', '', ' Co-Payment/Deductible', ' ;','', ''], [100, 100, 100, 100, 100]], [[' SINe.', ' | Date', ' Receipt No', '', '', '', ' Original Amt.', '', ' Adjusted', ''], [100, 100, 100, 100, 100]], [[' Pon', '',' eres', '', ' ene', '', '', '', '', ''], [100, 100, 100, 100, 100]]]]]	
	#for r in rdata:
	#	rjdata = {'edata' : r.EngineData,'totalpages':r.totalpages,'dataextracted': r.dataextracted,'dataaccuracy':r.dataaccuracy,'noisepercentage':r.noisepercentage,'filename':r.filename,'totalpages':r.totalpages}

	rjdata = {'edata' : finalarraytojson,'imagefilename' : fileNames, 'filename' : filaname,'totalnumberofpages':len(listoffilename)}
	return HttpResponse(json.dumps(rjdata), content_type="application/json")

def comparevalue(request):
	particulaval = request.POST['particulaval']
	amountval = request.POST['amountval'] 

	particulaval = json.loads(particulaval)
	amountval = json.loads(amountval)

	# print("particulaval",particulaval)
	# print("amountval",amountval)

	data = pd.read_excel(DictFile)
	df = pd.DataFrame(data, columns= ['Particulars','Amount'])
	listpro = df.values.tolist() 

	#print(listpro)
	val = 1
	comparedal = [None] * len(particulaval)
	# print(len(particulaval))
	for k in range(len(particulaval)):
		for j in listpro:
			if str(particulaval[k]) == j[0]:
				try:
					#print(float(amountval[k].strip()),j[1])
					#print(float(amountval[k].strip()) - j[1])
					comparedal[k] = float(amountval[k].strip()) - float(j[1])
					break
				except:
					print("")
	# print(comparedal)			
	rjdata_Dat = {'comparedval' : comparedal }
	return HttpResponse(json.dumps(rjdata_Dat), content_type="application/json")

def updatexlxs(request):
	updateparticularval = request.POST['updateparticularval']
	updateamountval = request.POST['updateamountval']

	print(updateparticularval)
	print(updateamountval)

	df = pd.DataFrame({"Particulars":[updateparticularval], "Amount":[updateamountval]})
	append_df_to_excel(df, DictFile)

	return HttpResponse(json.dumps("saved"), content_type="application/json")

def insertvaluetoexcel(request):
	sendHeaders = request.POST['sendHeaders']
	sendHeaders = json.loads(sendHeaders)

	sendData = request.POST['sendData']
	sendData = json.loads(sendData)

	sendtabledata = request.POST['sendtabledata']
	sendtabledata = json.loads(sendtabledata)

	# print(sendtabledata[0])

	writer = pd.ExcelWriter(ExcelOutputFile, engine='xlsxwriter')


	

	i = 1
	for t in sendtabledata:
		df2 = pd.DataFrame(t)
		# df2 = df2.transpose()
		df2.to_excel(writer, sheet_name='Table Data - '+str(i),header=False,index=False)

		workbook1  = writer.book
		worksheet1 = writer.sheets['Table Data - '+str(i)]

		font_fmt = workbook1.add_format({'font_name': 'Arial', 'font_size': 10})
		header_fmt = workbook1.add_format({'font_name': 'Arial', 'font_size': 10, 'bold': True})

		worksheet1.set_column('A:A', None, font_fmt)
		worksheet1.set_row(0, None, header_fmt)
		i += 1


	i = 1
	for a in sendHeaders:

		df2 = pd.DataFrame(a)
		df2 = df2.transpose()
		df2.to_excel(writer, sheet_name='Extracted Data - '+str(i),header=False,index=False)

		workbook1  = writer.book
		worksheet1 = writer.sheets['Extracted Data - '+str(i)]

		font_fmt = workbook1.add_format({'font_name': 'Arial', 'font_size': 10})
		header_fmt = workbook1.add_format({'font_name': 'Arial', 'font_size': 10, 'bold': True})

		worksheet1.set_column('A:A', None, font_fmt)
		worksheet1.set_row(0, None, header_fmt)
		i += 1

	i = 1
	for a in sendData:

		df2 = pd.DataFrame(a)
		df2 = df2.transpose()
		df2.to_excel(writer, sheet_name='Extracted Data - '+str(i),header=False,startrow=1,index=False)

		workbook1  = writer.book
		worksheet1 = writer.sheets['Extracted Data - '+str(i)]

		font_fmt = workbook1.add_format({'font_name': 'Arial', 'font_size': 10})
		header_fmt = workbook1.add_format({'font_name': 'Arial', 'font_size': 10, 'bold': True})

		worksheet1.set_column('A:A', None, font_fmt)
		worksheet1.set_row(0, None, header_fmt)
		i += 1

	writer.save()


	return HttpResponse(json.dumps("saved"), content_type="application/json")

def append_df_to_excel(df, excel_path):
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_path, index=False)	

def TextToArray(AllPageText):
    EachPageArray = AllPageText.split("%%%%%%")
    FinalLableAndTableForAllPageArray = []
    for EachPage in EachPageArray:
        PageLableData = []
        PageTableData = []
        PageLableTableArray = EachPage.split("$$$$$$")
        if(len(PageLableTableArray)>0):
            LableArray = PageLableTableArray[0].split("######")
            for eachLableGroup in LableArray:
                eachLableRow = eachLableGroup.split("@@@@@@")
                lableRow = []
                seperatorRow = []
                valueRow = []
                if(len(eachLableRow)>0):
                    lableRow = eachLableRow[0].split("!!!!!!")
                if(len(eachLableRow)>1):
                    seperatorRow = eachLableRow[1].split("!!!!!!")
                if(len(eachLableRow)>2):
                    valueRow = eachLableRow[2].split("!!!!!!")
                PageLableData.append([lableRow,seperatorRow,valueRow])
        if(len(PageLableTableArray)>1):
            TableArray = PageLableTableArray[1].split("^^^^^^")
            CurrentPageTableData = []
            for eachTable in TableArray:
                AlltablesInEachPageArray =eachTable.split("######")
                for eachTableGroup in AlltablesInEachPageArray:
                    eachTableRow = eachTableGroup.split("@@@@@@")
                    TableDataValue = []
                    TableDataCoordinates = []
                    if(len(eachTableRow)>0):
                        TableDataValue = eachTableRow[0].split("!!!!!!")
                    if(len(eachTableRow)>1):
                        TableDataCoordinates = eachTableRow[1].split("!!!!!!")
                    CurrentPageTableData.append([TableDataValue,TableDataCoordinates])
                PageTableData.append(CurrentPageTableData)
                CurrentPageTableData=[]
            FinalLableAndTableForAllPageArray.append([PageLableData,PageTableData])
    return FinalLableAndTableForAllPageArray

#================= Tasks ===========================
def user_process_new_task(request):
	datat = tabletask.objects.all()
	return render(request,"user_process_new.html",{'datat': datat})
def vaidate_file(request):
	fname = request.POST[r'fname']
	if os.path.isdir(fname) == True:
		return HttpResponse(json.dumps("Suceess"), content_type="application/json")
	else:
		return HttpResponse(json.dumps("unSuceess"), content_type="application/json")


def  processinput(request):
	ifname = request.POST[r'ifname']
	ofname = request.POST[r'ofname']
	oename = request.POST[r'oename']
	pname = request.POST[r'pname']
	print(ifname,ofname,oename)
	listofpdf = []
	exe = ImageMagickAddress
	for r, d, f in os.walk(ifname):
		for file in f:
			if '.pdf' in file:
				listofpdf.append(file)

	for i in listofpdf:
		os.rename(ifname+"\\" + i,ifname+"\\" + i.replace(" ","__"))

	listofpdf = []
	for r, d, f in os.walk(ifname):
		for file in f:
			if '.pdf' in file:
				listofpdf.append(file)

	print(listofpdf)
	entertaskdetailstodb(ifname,ofname,pname,oename,listofpdf) 
	

	jdata = {
		'listoffile' : listofpdf 
	}
	return HttpResponse(json.dumps(jdata), content_type="application/json")

def entertaskdetailstodb(ifname,ofname,pname,oename,listofpdf): 
	today = date.today()
	now = datetime.now()
	current_time = str(today) + " " + str(now.strftime("%H:%M:%S"))
	#print("Today's date:", today,current_time)

	datatoenter = tabletask(timestamp = current_time,inputfilelocation = ifname,outputfilelocatin= ofname,processedfilelocation = pname,excelfilename = oename,totalnumberoffiles =len(listofpdf))
	datatoenter.save()
	ocrconverionengine(current_time,ifname,ofname,pname,oename,listofpdf)
	
def ocrconverionengine(current_time,ifname,ofname,pname,oename,listofpdf):
	"""
	listofpdf = []
	
	for r, d, f in os.walk(ifname):
			for file in f:
				if '.pdf' in file:
					listofpdf.append(file)
	"""
	exe = "C:\Program Files\ImageMagick-7.0.9-Q16\convert.exe"
	for i in listofpdf: 
		if os.path.isdir(ofname+"\\"+i.rstrip(".pdf")) == False:
			os.mkdir(ofname+"\\"+i.rstrip(".pdf"))
		cmd1 = exe +' -strip -alpha off -density 300 "' + ifname + "\\"+i + '" -depth 2 -quality 300 "' +  ofname + "\\" + i.rstrip(".pdf") + "\\" + i.rstrip(".pdf")+'.tiff"'
		subprocess.call(cmd1)
		print("======= pdf to tiff conversion ========")
		cmd = exe +' -density 250 "' + ifname + "\\"+i + '" -quality 300 "' +  ofname + "\\" + i.rstrip(".pdf") + "\\" + i.rstrip(".pdf")+'.png"'
		#print(cmd)
		subprocess.call(cmd)
		print("======== pdf to png conversion =========")

		shutil.move(ifname + "\\"+i,pname + "\\" + i) 
		#print(ofname+"\\"+i.rstrip(".pdf")+"\\"+i.replace(".pdf",".tiff"))
		if os.path.exists(ofname+"\\"+i.rstrip(".pdf")+"\\"+i.replace(".pdf",".tiff")) == True:
			print("enter")
			test_cmd = "tesseract " + ofname+"\\"+i.rstrip(".pdf")+"\\"+i.replace(".pdf",".tiff") +" "+ ofname +"\\"+i.rstrip(".pdf")+"\\"+i.rstrip(".pdf") + " --dpi 300 --psm 3 hocr"
			print("=== tesseract command=====::",test_cmd)
			subprocess.call(test_cmd)

		print("====== engine funcion called =======")
		extarctedoututdata = hocrf.mainfunction(ofname +"\\"+i.rstrip(".pdf")+"\\"+i.replace(".pdf",".hocr")) 
		print("====== engine funcion ended =======")
		#print(extarctedoututdata)
		testd = viewdatafilepath(timestamp = current_time,inputfilelocation = ofname +"\\"+i.rstrip(".pdf"),filename = i.rstrip(".pdf"),EngineData = extarctedoututdata, dataextracted= 86,dataaccuracy = 96,noisepercentage = 12,totalpages = len(listofpdf))
		testd.save()
		print("======== Data Saved ================")
		#print(i)

		 

		copytree(ofname+"\\" + i.rstrip(".pdf"),i)

def div_ocr_page_extract_hihg(div_p_word):
    div_ocr_page_id = []
    div_ocr_page_cordinate = []
    div_ocr_page_data = []
    return_array_page = []

    div_p_word = div_p_word.find_all('div',class_='ocr_page')

    for word in div_p_word:
        div_ocr_page_id.append(word.get('id'))
        div_temp = word.get('title').split(";")[1].split(" ")
        div_ocr_page_cordinate.append([int(div_temp[2]),int(div_temp[3]),int(div_temp[4]),int(div_temp[5])])
        div_ocr_page_data.append(word)

        #    print("------------------")
        #    print(div_ocr_page_id)
    return_array_page.append([div_ocr_page_id,div_ocr_page_cordinate,div_ocr_page_data])
    # print("length",len(return_array_page[0][2]))
    return div_ocr_page_data


def ocrfunctionalitytest(request): 
	temp = "fas"
	tst = json.dumps(temp)
	current_time = "1/7/2020"
	ofname = "D:/mediaeast/Testing/output/50272"
	fiename = "50272"
	fname = r"D:\mediaeast\Testing\5045.pdf"
	#tt = [[1,2,3,4],[1,2,3,'']]
	#testd = testtable(tid = 1, myfile = fname)
	
	#testd = viewdatafilepath(timestamp = current_time,inputfilelocation = ofname ,filename = fiename,EngineData = temp, dataextracted= 86,dataaccuracy = 96,noisepercentage = 12,totalpages = len(temp[0]))
	#testd.save()
	a = ""
	rdata = testtable.objects.all()
	for r in rdata: 
		a = r.myfile
	return HttpResponse(json.dumps(a), content_type="application/json")


def testingocrfunction(request):
	"""	
	fil = r"D:\mediaeast\Testing\output\test\test.hocr"
	extarctedoututdata = hocrf.mainfunction(fil)
	print(extarctedoututdata)
	testd = view_data_filepath(EngineData = extarctedoututdata)
	testd.save()
	
	extarctedoututdata = [['a',1,2,3,4],['b',4,5,6,7]]
	testd = view_data_filepath(EngineData = extarctedoututdata)
	testd.save()
	datat = view_data_filepath.objects.all()
	for d in datat:
		for i in d.EngineData:
			for j in i:
				print(j)
				"""
	ofname = "D:\mediaeast\Testing\output"
	i = "ADITYA__B__FINAL__BILL"
	copytree(ofname+"\\" + i.rstrip(".pdf"))
	return HttpResponse(json.dumps("test"), content_type="application/json")



def loadtaskdata(request):
	returndata = []
	datat = tabletask.objects.all()
	async def test():
		loop = asyncio.get_event_loop()
		await asyncio.sleep(3)
		print("test called")

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(test())
	loop.close()

	"""
	for d in datat:
		returndata.append([d.taskid,d.timestamp,d.inputfilelocation,d.outputfilelocatin,d.processedfilelocation,d.excelfilename,d.totalnumberoffiles])

	"""
	jdata1 = {
		'tabledata' : returndata
	}
	
	return HttpResponse(json.dumps(jdata1), content_type="application/json")	

#================= User Process ====================



def user_details(request):
	t_id = request.POST['t_id']
	t_name = request.POST['t_name']
	t_desc = request.POST['t_desc']
	template_details = request.POST['templates_details']
	input_filename = request.POST['input_file_name']
	output_filename = request.POST['output_file_name']
	file_name_pattern = request.POST['file_name_pattern'] 
	task_details = task_creation(task_id = t_id, task_name = t_name, task_desc = t_desc, template_id =template_details,input_file_name = input_filename,output_file_name = output_filename,file_name_pattern = file_name_pattern)
	task_creation.save(task_details)
	#task_operation.check_task_status()
	#insert_data_todb.insert_data_val()
	#task_operation.arr_clear()
	return HttpResponse(json.dumps("Created"), content_type="application/json")

def list_of_task(request):
	list_task = task_creation.objects.all()
	print(list_task)
	return render(request,"user_process_view.html",{'list_task':list_task})






#================== Model Function ===================

input_filename = []
output_filename = []
t1 = ""
def Find_number_of_files(request):
	global t1 
	t1 = threading.Thread(target=test_function)
	t1.start()
	
	return HttpResponse(json.dumps("Created"), content_type="application/json")



def test_function():
	task_s = task_creation.objects.filter(status="Pending")
	for t in task_s:
		input_filename.append(t.input_file_name)
		output_filename.append(t.output_file_name)
	print(input_filename,output_filename)
	time.sleep(5)
	global t1
	t1.join()
	input_filename.clear()
	output_filename.clear()


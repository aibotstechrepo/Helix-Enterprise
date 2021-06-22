from bs4 import BeautifulSoup
import media.Table_Extraction as table
import pandas as pd

# image = "D:/mediaeast/Test sample 2/50517-1-0.jpg"
# img = cv2.imread(image)


def hocr_function(hocr):
    #file_open = open("output.csv", "w")
    # hocr_retur_arrr = []
    page_t = div_ocr_page_extract(hocr)
    page_t1 = page_t[0][2]
    # Page for Looop
    page_num = 0
    #EachPageLableArray = []
    FinalLableAndTableForAllPageArray = []
    #EachPageTableArray = []
    tempValuesForTableCoulmnCounter = 0
    returnextracttabklevalue = []
    tempTableHeader = []
    for p in page_t1:
        #print("--------------------------------------------------------------------------------")
        # file_open.write("++++++++++++++ PAGE STARTED "+str(page_num)+"++++++++++++++++++" +"\n")
        EachPageLableArray = []
        EachPageTableArray = []
        EachTableArray = []
        carea_t = div_ocr_carea_extract(p)
        carea_t = carea_t[0][2]
        # c_are Looop
        for c in carea_t:
            # print("################## Div STARTED ############")
            par_t = div_ocr_par_extract(c)
            par_t = par_t[0][2]
            labelCounter = 0
            labelSeperator = 0
            CounterTableStart = 0
            CounterTableEnd = 0
            CounterTableRow = 0
            TableInstances = 0
            TableNextLineSkipCurrentRowCounter = 0
            # Paragraph Loop
            for pr in par_t:
                # print("$$$$$$$$$$$$$$ PAR STARTED $$$$$$$$$$$$")
                line_t = div_ocr_line_extract(pr)
                line_t1 = line_t[0][2]
                # Line Loop
                labelvaluecounter = []
                for l in line_t1:
                    EachlineCounterToValidateTableStartToSkipEndInCurrentRow = 0
                    lableFoundLocationWordIndex = -1
                    lableSeparatorFoundLocationWordIndex = -1
                    lableValueEndFoundLocationWordIndex = -1
                    #templableFoundInsideEndCounter = 0
                    lableFoundCounter = 0
                    lableSeperatorCounter = 0
                    lableValueFoundCounter = 0
                    # print("%%%%%%%%%%%% LINE STARTED %%%%%%%%%%")
                    w = div_ocr_word_extract(l)
                    # each Word loop
                    totalWordsinEachLine = len(w[0][2])
                    eachWordIndexInLine = 0
                    # print("totalWordsinEachLine",totalWordsinEachLine)
                    temp_val_array = []
                    temp_cor_array = []
                    temp_label_data = []
                    for str_data_send_to_find_occurance in w:
                        for tmpe_a in str_data_send_to_find_occurance[2]:
                            temp_val_array.append(tmpe_a)
                        for tmpe_cor in str_data_send_to_find_occurance[1]:
                            temp_cor_array.append(tmpe_cor)
                        for str_send in str_data_send_to_find_occurance[2]:
                            temp_str_send = str_send.strip()
                            #print("data" ,temp_str_send,"legth",len(temp_str_send))
                            if len(temp_str_send) > 0:
                                dat = table.Table_Extraction(str_send,"orginal")
                                #print(dat)
                                if len(dat) > 0:
                                    #print("column ",dat[0][1])
                                    #for ReturnLibColumnIndex in range(len(dat)):
                                    #if(temp_str_send == "Number"):
                                        #print("")
                                    if dat[0][1] == "label":
                                        if len(dat[0][1]) > 1:
                                            dat = table.Table_Extraction(str_send,"Labels")
                                            # print(dat)
                                            # try:
                                            #     temp_val_array[0] = dat[0][1]
                                            #     # a = a
                                            # except Exception as e:
                                            #     print(e)
                                            # print("temp",temp_val_array)
                                        #print("each line count", eachWordIndexInLine)
                                        if lableFoundCounter > 0 and lableSeperatorCounter > 0:
                                            if eachWordIndexInLine-1 > -1:
                                                lableValueEndFoundLocationWordIndex = eachWordIndexInLine-1
                                                #print("Eneded ", lableValueEndFoundLocationWordIndex)
                                                lableValueFoundCounter = lableValueFoundCounter + 1
                                                lableFoundLocationWordIndex = eachWordIndexInLine
                                                # print("start inside - ",lableFoundLocationWordIndex)
                                                lableFoundCounter = lableFoundCounter+1
                                                #templableFoundInsideEndCounter = templableFoundInsideEndCounter + 1
                                                labelCounter += 1
                                        elif lableFoundLocationWordIndex == -1 and lableFoundCounter == 0:
                                            # print(str_data_send_to_find_occurance)
                                            if eachWordIndexInLine > 0:
                                                currentValPosBL =str_data_send_to_find_occurance[1][eachWordIndexInLine][0]
                                                previousValPosBR =str_data_send_to_find_occurance[1][eachWordIndexInLine-1][2]
                                                tempDistance = currentValPosBL - previousValPosBR
                                                if tempDistance < 14:
                                                    lableFoundLocationWordIndex = eachWordIndexInLine - 1
                                                else:
                                                    lableFoundLocationWordIndex = eachWordIndexInLine
                                            else:
                                                lableFoundLocationWordIndex = eachWordIndexInLine
                                            #print("start - ",lableFoundLocationWordIndex)
                                            lableFoundCounter = lableFoundCounter+1
                                            labelCounter += 1

                                    elif dat[0][1] == "labelseperator" and lableFoundCounter > 0:
                                        # elif temp_str_send == ":":
                                        labelSeperator += 1
                                        lableSeparatorFoundLocationWordIndex = eachWordIndexInLine
                                        #print("seperator - " ,lableSeparatorFoundLocationWordIndex)
                                        lableSeperatorCounter = lableSeperatorCounter + 1
                                        #templableFoundInsideEndCounter = 0;
                                    elif dat[0][1] == "tablestartpriority1":
                                        CounterTableStart += 1
                                        TableInstances = TableInstances + 1
                                        #if(CounterTableStart > 2):
                                            #tempValuesForTableCoulmnCounter = 0
                                        EachlineCounterToValidateTableStartToSkipEndInCurrentRow =+1
                                    elif dat[0][1] == "tablendpriority1":
                                        CounterTableEnd += 1
                                    for ReturnLibColumnIndex in range(len(dat)):
                                        if dat[ReturnLibColumnIndex][1] == "tablestartNextLine":
                                            if len(returnextracttabklevalue) > 0:
                                                EachlineCounterToValidateTableStartToSkipEndInCurrentRow =+1
                                                CounterTableStart += 1
                                                TableNextLineSkipCurrentRowCounter +=1
                            # Store last word index as lable value in case of missing next lable
                            if lableValueEndFoundLocationWordIndex == -1 :
                                if eachWordIndexInLine == totalWordsinEachLine - 1:  
                                    if lableSeperatorCounter > 0 :
                                        lableValueEndFoundLocationWordIndex = eachWordIndexInLine
                            # store Lable position and Lable Seprattor location and Lable value loaction\
                            # print(lableValueEndFoundLocationWordIndex)
                            if lableValueEndFoundLocationWordIndex > -1:
                                # temp_label_data.append(str_data_send_to_find_occurance[lableValueEndFoundLocationWordIndex][1])
                                temp_label_data.append(lableValueEndFoundLocationWordIndex)
                                lableValueEndFoundLocationWordIndex = -1
                            elif lableFoundLocationWordIndex > -1:
                                # temp_label_data.append(str_data_send_to_find_occurance[lableFoundLocationWordIndex][1])
                                temp_label_data.append(lableFoundLocationWordIndex)
                                # print(temp_label_data)
                                lableFoundLocationWordIndex = -1
                            elif lableSeparatorFoundLocationWordIndex > -1:
                                # temp_label_data.append(str_data_send_to_find_occurance[lableSeparatorFoundLocationWordIndex][1])
                                temp_label_data.append(lableSeparatorFoundLocationWordIndex)
                                lableSeparatorFoundLocationWordIndex = -1
                            if lableFoundCounter > 0 and  lableSeperatorCounter > 0  and lableValueFoundCounter > 0 :
                                if lableFoundCounter > 1 :
                                    lableFoundCounter = 1
                                else :
                                    lableFoundCounter = 0
                                lableSeperatorCounter = 0
                                lableValueFoundCounter = 0
                            eachWordIndexInLine = eachWordIndexInLine + 1
                        #print("Test Valus",temp_val_array[lableValueEndFoundLocationWordIndex],temp_val_array[lableFoundLocationWordIndex],temp_val_array[lableSeparatorFoundLocationWordIndex])                         
                        # for t_l in temp_label_data:
                        #     print(temp_val_array[t_l])
                        if len(temp_label_data)>0:
                            #print(temp_val_array)
                            return_array = appending_array(temp_label_data)
                            #print(return_array)
                            for i in return_array:
                                # print(i)
                                Lable = ""
                                Sep = ""
                                Value = ""

                                lableBBoxLeft = 0
                                lableBBoxWidth = 0
                                lableBBoxTop = 0
                                lableBBoxHeight = 0

                                lableConfidence = 0
                                lableSeperatorBBoxLeft = 0
                                lableSeperatorBBoxWidth = 0
                                lableSeperatorBBoxTop = 0
                                lableSeperatorBBoxHeight = 0

                                lableSeperatorConfidence = 0
                                ValueBBoxLeft = 0
                                ValueBBoxWidth = 0
                                ValueBBoxTop = 0
                                ValueBBoxHeight = 0

                                ValueConfidence = 0 

                                if len(i) > 2:
                                    eachLableWordIndex = 0
                                    for eachWord in range(i[0], (i[1])):
                                        if(eachLableWordIndex == 0):
                                            lableBBoxLeft = temp_cor_array[eachWord][0]
                                            lableBBoxWidth = temp_cor_array[eachWord][2]
                                        if(eachLableWordIndex == (len(i[0:1]) - 1)):
                                            lableBBoxTop = temp_cor_array[eachWord][1]
                                            lableBBoxHeight = temp_cor_array[eachWord][3]
                                        Lable = Lable + " " + temp_val_array[eachWord]
                                        lableConfidence = int(lableConfidence) + int( temp_cor_array[eachWord][4])
                                        eachLableWordIndex = eachLableWordIndex + 1
                                    try:
                                        lableConfidence = int(lableConfidence/eachLableWordIndex)
                                    except:
                                        lableConfidence = 70
                                    eachLableSeparatorWordIndex = 0
                                    tempSperatorEndLen = -1
                                    for eachWord in range(i[1], (i[1]+1)):
                                        tempSperatorEndLen = tempSperatorEndLen+1


                                    for eachWord in range(i[1], (i[1]+1)):
                                        if(eachLableSeparatorWordIndex == 0):
                                            lableSeperatorBBoxLeft = temp_cor_array[eachWord][0]
                                            lableSeperatorBBoxWidth = temp_cor_array[eachWord][2]
                                        if(eachLableSeparatorWordIndex == tempSperatorEndLen):
                                            lableSeperatorBBoxTop = temp_cor_array[eachWord][1]
                                            lableSeperatorBBoxHeight = temp_cor_array[eachWord][3]
                                        Sep = Sep + temp_val_array[eachWord]
                                        lableSeperatorConfidence = int(lableSeperatorConfidence) + int( temp_cor_array[eachWord][4])
                                        eachLableSeparatorWordIndex = eachLableSeparatorWordIndex + 1
                                    lableSeperatorConfidence = int(lableSeperatorConfidence/eachLableSeparatorWordIndex)
                                    eachValueWordIndex = 0
                                    tempValueEndLen = -1
                                    for eachWord in range(i[1]+1, (i[2]+1)):
                                        tempValueEndLen = tempValueEndLen + 1

                                    for eachWord in range(i[1]+1, (i[2]+1)):
                                        if(eachValueWordIndex == 0):
                                            ValueBBoxLeft = temp_cor_array[eachWord][0]
                                            ValueBBoxWidth = temp_cor_array[eachWord][2]
                                        if(eachValueWordIndex == tempValueEndLen):
                                            ValueBBoxTop = temp_cor_array[eachWord][1]
                                            ValueBBoxHeight = temp_cor_array[eachWord][3]
                                        Value = Value + " " + temp_val_array[eachWord]
                                        ValueConfidence = int(ValueConfidence) + int( temp_cor_array[eachWord][4])
                                        eachValueWordIndex = eachValueWordIndex + 1
                                    try:
                                        ValueConfidence = int(ValueConfidence/eachValueWordIndex)
                                    except:
                                        ValueConfidence = 70
                                    EachPageLableArray.append([[Lable,lableBBoxLeft,lableBBoxTop,lableBBoxWidth,lableBBoxHeight,lableConfidence],[Sep,lableSeperatorBBoxLeft,lableSeperatorBBoxTop,lableSeperatorBBoxWidth,lableSeperatorBBoxHeight,lableSeperatorConfidence],[Value,ValueBBoxLeft,ValueBBoxTop,ValueBBoxWidth,ValueBBoxHeight,ValueConfidence]])
                                #print(EachPageLableArray)
                        #if(len(temp_label_data) >0):
                            #EachPageLableArray.append(temp_label_data)
                        temp_label_data.clear()
                        #print(temp_val_array)

                        #print(labelvaluecounter)
                    if EachlineCounterToValidateTableStartToSkipEndInCurrentRow < 1 :
                        # print("EachlineCounterToValidate", EachlineCounterToValidate)
                        # print("CounterTableEnd", CounterTableEnd)
                        if CounterTableEnd > 2:
                            CounterTableStart = 0
                            CounterTableRow = 0
                            CounterTableEnd = 0
                    # Condition
                    # print("start:",CounterTableStart)
                    # print("end:",CounterTableEnd)
                    if CounterTableStart > 2:
                        temp = []
                        EachTableLineTemp = []
                        if(TableNextLineSkipCurrentRowCounter == 0):
                            if(len(tempTableHeader)>0):
                                EachTableArray.append(tempTableHeader[0])
                                tempTableHeader = []
                            for str_data_send_to_find_occurance in w:
                                for cordata in str_data_send_to_find_occurance[1]:
                                    temp.append([cordata[0],cordata[2],cordata[1],cordata[3],cordata[4]])
                                a = ""
                                i = 0
                                for str_send in str_data_send_to_find_occurance[2]:
                                    a = a + "," + str_send
                                    EachTableLineTemp.append([str_send,temp[i][0],temp[i][1],temp[i][2],temp[i][3],temp[i][4]])
                                    i += 1
                                if(TableInstances > 2):
                                    TableInstances = 0
                                    tempValuesForTableCoulmnCounter = 0
                                if tempValuesForTableCoulmnCounter < 1 :
                                    returnextracttabklevalue = []
                                    tempTableHeader = []
                                    if(len(EachTableArray)>0):
                                        EachPageTableArray.append(EachTableArray)
                                        EachTableArray = []
                                    returnextracttabklevalue = extractHeaderColumnSpaceing(EachTableLineTemp)
                                    tempValuesForTableCoulmnCounter = 1
                                if len(returnextracttabklevalue) > 0 :
                                    temp1 = ExtractTableRow(returnextracttabklevalue,EachTableLineTemp)
                                    con = CheckConfidence(EachTableLineTemp,5)
                                    #print(temp1)
                                    EachTableArray.append([temp1,[returnextracttabklevalue[0][1],EachTableLineTemp[0][3],returnextracttabklevalue[len(returnextracttabklevalue)-1][2],EachTableLineTemp[len(EachTableLineTemp)-1][4],con]])
                                #print(EachPageTableArray)
                                #print(a)
                                #file_open.write(a +"\n")
                                #file_open.write("------------------------------------------------" +"\n")
                                CounterTableEnd = 0
                                #tempValuesForTableCoulmnCounter = 0
                                # print("------")
                        else:
                            TableNextLineSkipCurrentRowCounter = 0
                            tempTableHeader.append([ExtractTableRow(returnextracttabklevalue,returnextracttabklevalue),[100,100,100,100,100]])


                            # print(w[0][2])
        #file_open.write("===========PAGE End "+str(page_num)+" ===============" +"\n")
        #zprint("===========PAGE End "+str(page_num)+" ===============")
        if(len(EachTableArray)>0):
            EachPageTableArray.append(EachTableArray)
            #print("------------------------")
            #print(EachPageTableArray)
            EachTableArray = []
        #print(EachPageTableArray)
        for CurrentEachPageTable in EachPageTableArray:
            CurrentEachPageTable = TableRowVerifyAndAppend(CurrentEachPageTable)
        FinalLableAndTableForAllPageArray.append([EachPageLableArray, EachPageTableArray])
        page_num +=1

    #df = pd.DataFrame(FinalLableAndTableForAllPageArray[2][1])
    #df.to_excel(excel_writer = "ADITYA-0.xlsx")
    return FinalLableAndTableForAllPageArray

def appending_array(temp_label_data):
    r_array = []
    counter = 0
    for i in range(len(temp_label_data)):
        valueToCheck = (i+1) % 3
        if (valueToCheck == 0):
            r_array.append(temp_label_data[counter:i+1])
            counter = i+1
        elif i == len(temp_label_data)-1:
            r_array.append(temp_label_data[counter: len(temp_label_data)])
    return r_array

def div_ocr_page_extract(div_p_word):
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
    return return_array_page

def div_ocr_carea_extract(div_c_word):
    div_ocr_carea_id = []
    div_ocr_carea_cordinate = []
    div_ocr_carea_data = []
    return_array_care = []
    div_c_word = div_c_word.find_all('div',class_='ocr_carea')
    for word in div_c_word:
        div_ocr_carea_id.append(word.get('id'))
        div_temp = word.get('title').split(" ")
        div_ocr_carea_cordinate.append([int(div_temp[1]),int(div_temp[2]),int(div_temp[3]),int(div_temp[4])])
        div_ocr_carea_data.append(word)
    #    print("------------------")
    #    print(div_ocr_carea_id)
    return_array_care.append([div_ocr_carea_id,div_ocr_carea_cordinate,div_ocr_carea_data])
    return return_array_care

def div_ocr_par_extract(div_pa_word):
    div_ocr_par_id = []
    div_ocr_par_cordinate = []
    div_ocr_par_data = []
    return_array_par = []

    div_pa_word = div_pa_word.find_all('p',class_='ocr_par')

    for word in div_pa_word:
        div_ocr_par_id.append(word.get('id'))
        div_temp = word.get('title').split(" ")
        div_ocr_par_cordinate.append([int(div_temp[1]),int(div_temp[2]),int(div_temp[3]),int(div_temp[4])])
        div_ocr_par_data.append(word)
    #    print("------------------")
    #    print(div_ocr_par_id)
    return_array_par.append([div_ocr_par_id,div_ocr_par_cordinate,div_ocr_par_data])
    return return_array_par

def div_ocr_line_extract(div_li_word):
    div_ocr_line_id = []
    div_ocr_line_cordinate = []
    div_ocr_line_data = []
    return_array_line = []
    div_li_word = div_li_word.find_all('span',class_='ocr_line')

    for word in div_li_word:
        div_ocr_line_id.append(word.get('id'))
        div_temp = word.get('title').split(" ")
        div_ocr_line_cordinate.append([int(div_temp[1]),int(div_temp[2]),int(div_temp[3]),int(div_temp[4].rstrip(';'))])
        div_ocr_line_data.append(word)
    #    print("------------------")
    #    print(div_ocr_line_data)
    return_array_line.append([div_ocr_line_id,div_ocr_line_cordinate,div_ocr_line_data])
    return return_array_line

def div_ocr_word_extract(div_w_word):
    div_ocr_w_id = []
    div_ocr_w_cordinate = []
    div_ocr_w_data = []
    return_array_w = []

    div_w_word = div_w_word.find_all('span',class_='ocrx_word')

    for word in div_w_word:
        div_ocr_w_id.append(word.get('id'))
        div_temp = word.get('title').split(" ")
        div_ocr_w_cordinate.append([int(div_temp[1]),int(div_temp[2]),int(div_temp[3]),int(div_temp[4].rstrip(';')),int(div_temp[6])])
        div_ocr_w_data.append(word.get_text()) 
    return_array_w.append([div_ocr_w_id,div_ocr_w_cordinate,div_ocr_w_data])
    return return_array_w

def extractHeaderColumnSpaceing(temp):
    rangeVaues  = []
    rangeFrom = -1
    data = ""
    #print(len(temp))

    for i in range(len(temp)):
        #print(temp[i + 1][1] - temp[i][2], temp[i][0], temp[i + 1][0])
        #rangeVaues.append(temp[i + 1][1] - temp[i][2])
        if i < len(temp) -1 :
            difference  = temp[i + 1][1] - temp[i][2]
            if data is None:
                data = data + temp[i][0]
            else:
                data = data + " " + temp[i][0]
            if rangeFrom < 0 :
                rangeFrom = temp[i][1]
            if difference > 10  and ((temp[i][2] - temp[i][1]) > 5):
                #rangeFrom = temp[i][2]
                rangeTo = temp[i + 1][1]
                rangeVaues.append([data.strip(),rangeFrom , rangeTo])
                rangeFrom = -1
                data = ""
        elif i == len(temp) -1 :
            if data is None:
                data = data + temp[i][0]
            else:
                data = data + " " + temp[i][0]
            if rangeFrom < 0 :
                rangeFrom =temp[i][1]
            if(temp[i][2] <= 1800):
                rangeTo = 1800
            else :
                rangeTo = temp[i][2] + 50
            rangeVaues.append([data,rangeFrom , rangeTo])
            rangeFrom = -1
            data = ""
    return rangeVaues

def scrapBasedOnTableSpacing(dataTemp,temp):
    finalValue = []
    #rangeVaues.sort()
    #print(rangeVaues)
    #rangeVaues = [['SI', 48, 87], ['Description', 87, 261], ['Batch /', 261, 378], ['Ord Doc.', 378, 456], ['� SCH', 456, 527], ['MFR', 527, 568], ['UOM', 568, 662], ['Qty', 662, 745], ['Amount', 745, 954], ['Taxable Value', 954, 1138], ['cast*', 1138, 1272], ['sGsT*', 1272, 1397], ['IGST*', 1397, 1449], ['�_', 1449, 1482], [' Payable Total', 1482, 1574]]
    #print(len(rangeVaues))
    #dataTemp = [['SI', 48, 87], ['Description', 87, 261], ['Batch /', 261, 378], ['Ord Doc.', 378, 456], ['� SCH', 456, 527], ['MFR', 527, 568], ['UOM', 568, 662], ['Qty', 662, 745], ['Amount', 745, 954], ['Taxable Value', 954, 1138], ['cast*', 1138, 1272], ['sGsT*', 1272, 1397], ['IGST*', 1397, 1449], ['�_', 1449, 1482], [' Payable Total', 1482, 1574]]
    for eachWord in temp :
        for i in range(len(dataTemp)):
            if ( eachWord[1] >= dataTemp[i][1] ) and ( eachWord[2] <= dataTemp[i][2] ):
                finalValue.insert(i,eachWord[0])
                break#.encode('ascii', 'ignore')).decode("utf-8")#.encode('ascii', 'ignore'))
                #temp = str(i) + "  :  " + str(dataTemp[i][0].encode('ascii', 'ignore')).decode("utf-8") 
            #print(temp)
    return finalValue

def ExtractWordTopLeftFromParagraph(ParagraphString):
    paragrphValue = []
    
    for wr in ParagraphString: 
        EachLine =[]
        tt = wr.find_all('span',class_='ocrx_word')
        for t in tt:
            top = int(t.get('title').split(" ")[1])
            left = int(t.get('title').split(" ")[3])
            EachLine.append([t.get_text(),top,left])
        paragrphValue.append(EachLine)
    return paragrphValue

def ExtractTableRow(ColumnHeader,ParaValues):
    #dataTemp = [['SI', 48, 87], ['Description', 87, 261], ['Batch /', 261, 378], ['Ord Doc.', 378, 456], ['� SCH', 456, 527], ['MFR', 527, 568], ['UOM', 568, 662], ['Qty', 662, 745], ['Amount', 745, 954], ['Taxable Value', 954, 1138], ['cast*', 1138, 1272], ['sGsT*', 1272, 1397], ['IGST*', 1397, 1449], ['�_', 1449, 1482], [' Payable Total', 1482, 1574]]
    #dataTemp = [['SI', 124, 142], ['Particulars', 202, 329], ['Date', 604, 652], ['Qty', 779, 825], ['Unit', 877, 918], ['Rate', 924, 967], ['Gross', 1051, 1122], ['Disc.', 1192, 1241], ['Amt', 1248, 1294], ['Net', 1346, 1382], ['Amt', 1389, 1434]]
    #dataTemp = extractHeaderColumnSpaceing(dataTemp)
    dataTemp = ColumnHeader
    LineItem = [""] * len(dataTemp)
    #print ("datatemp",len(dataTemp))
    # print ("LineItem",len(LineItem))
    for eachWord in ParaValues :
        for i in range(len(dataTemp)): 
            if(i == 0):
                if(eachWord[1] < dataTemp[i][1]):
                    if(eachWord[2] > dataTemp[i][1] - 10):
                        LineItem[i] = LineItem[i] + " "+eachWord[0]
                        break
            if(i <= len(dataTemp)-2):
                if(eachWord[2]>dataTemp[i][2]):# and  eachWord[2]>dataTemp[i+1][1]):
                    leftWord1 = eachWord[1] - dataTemp[i][1] 
                    rightWord1 = eachWord[2] - dataTemp[i][2]
                    leftWord2 =  dataTemp[i+1][1] -  eachWord[1]
                    rightWord2 =  dataTemp[i+1][2] -  eachWord[2]
                    if(((leftWord1 >= 0) and  (leftWord2 >= 0) )and ( leftWord1 > leftWord2)):
                    #if((leftWord1 >= 0)and ( leftWord1 > leftWord2)):
                        LineItem[i+1] = LineItem[i+1] + " "+ eachWord[0]
                        break
                    elif ( eachWord[1] >= dataTemp[i][1] ) and ( eachWord[2] >= dataTemp[i][2] )  and ( eachWord[1] <= dataTemp[i+1][1] )and ( eachWord[2] <= dataTemp[i+1][2] ):
                        LineItem[i] = LineItem[i] + " "+eachWord[0]
                        break
                    #elif(((leftWord1 >= 0) and  (leftWord2 <= 0) )and ( leftWord1 > leftWord2)):
                    #    LineItem[i+1] = LineItem[i+1] + " "+ eachWord[0]
                    #    break
            if ( eachWord[1] >= dataTemp[i][1] ) and ( eachWord[2] <= dataTemp[i][2] ):
                LineItem[i] = LineItem[i] + " "+eachWord[0]
                break#.encode('ascii', 'ignore')).decode("utf-8")#.encode('ascii', 'ignore'))
                #temp = str(i) + "  :  " + str(dataTemp[i][0].encode('ascii', 'ignore')).decode("utf-8") 
                #print(temp)
            elif ( eachWord[1] >= (dataTemp[i][1] - 10) ) and ( eachWord[2] <= (dataTemp[i][2]) + 10 ):
                LineItem[i] = LineItem[i] + " "+ eachWord[0]
                break#
            
    return LineItem

def JaggedArrayToStringWithDelimeter(jaggedArray, delimiter):
    StringData = ""
    i=0
    for eachArrayValue in jaggedArray:
        if(i == 0):
            StringData = str(eachArrayValue)
        else:
            StringData = str(StringData) + delimiter + str(eachArrayValue)
        i += 1
    return StringData

def ArrayToText(FinalLableAndTableForAllPageArray):
    j=0
    AllPageText = ""
    for EachPage in FinalLableAndTableForAllPageArray:
        PageLable = ""
        PageTable = ""
        i=0
        for EachPageLable in EachPage[0]:
            lable = JaggedArrayToStringWithDelimeter(EachPageLable[0],"!!!!!!")
            separator = JaggedArrayToStringWithDelimeter(EachPageLable[1],"!!!!!!")
            value = JaggedArrayToStringWithDelimeter(EachPageLable[2],"!!!!!!")
            if(i == 0):
                PageLable =  lable + "@@@@@@" + separator+  "@@@@@@" + value
            else:
                PageLable = PageLable + "######" + lable + "@@@@@@" + separator+  "@@@@@@" + value
            i += 1
        i=0
        for EachPageTable in EachPage[1]:
            CurretTable = ""
            k=0
            for eachtable in EachPageTable:
                tableData = JaggedArrayToStringWithDelimeter(eachtable[0],"!!!!!!")
                Coordinates = JaggedArrayToStringWithDelimeter(eachtable[1],"!!!!!!")
                if(k==0):
                    CurretTable =  tableData + "@@@@@@" + Coordinates
                else:
                    CurretTable = CurretTable + "######" + tableData + "@@@@@@" + Coordinates
                k+=1
            if(i == 0):
                PageTable =  CurretTable
            else:
                PageTable = PageTable + "^^^^^^" + CurretTable
            i += 1
        if(j == 0):
            AllPageText =  PageLable + "$$$$$$" + PageTable
        else:
            AllPageText = AllPageText + "%%%%%%" + PageLable + "$$$$$$" + PageTable
        j += 1
    return AllPageText

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

def CheckConfidence(RowArray,index):
    confidence= 0 
    for eachRow in RowArray:
        confidence = confidence + eachRow[index] 
    confidence = confidence / len(RowArray)
    return int(confidence)

def TableRowVerifyAndAppend(tableData):
    if(len(tableData)>0):
        if(len(tableData[0])>0):
            columns = len(tableData[0][0]) 
    if(columns>0):
        tableLen = len(tableData)
        for EachRow in range(tableLen):
            counter = 0
            if(EachRow < tableLen):
                for eachCells in range(len(tableData[EachRow][0])):
                #for eachCells in tableData[EachRow][0]:
                    if(len((tableData[EachRow][0][eachCells].strip())))>0:
                        counter = counter + 1
                if(counter <= ((columns)/2)):
                    if(EachRow>0):
                        for eachCellPosition in range(len(tableData[EachRow][0])):
                            tableData[EachRow-1][0][eachCellPosition] = (tableData[EachRow-1][0][eachCellPosition] + tableData[EachRow][0][eachCellPosition]).strip()
                        tableData[EachRow-1][1][0] = tableData[EachRow][1][0]
                        tableData[EachRow-1][1][2] = tableData[EachRow][1][2]
                        tableData[EachRow-1][1][4] = int(tableData[EachRow-1][1][4] + tableData[EachRow][1][4])/2
                        del(tableData[EachRow]) 
                        tableLen =len(tableData)
                else:
                    for eachCellPosition in range(len(tableData[EachRow][0])):
                            tableData[EachRow][0][eachCellPosition] = tableData[EachRow][0][eachCellPosition].strip()
    if(len(tableData)>0):
        if(len(tableData[0])>0):
            columns = len(tableData[0][0]) 
    if(columns>0):
        tableLen = len(tableData)
        for EachRow in range(tableLen):
            counter = 0
            if(EachRow < tableLen):
                for eachCells in range(len(tableData[EachRow][0])):
                #for eachCells in tableData[EachRow][0]:
                    if(len((tableData[EachRow][0][eachCells].strip())))>0:
                        counter = counter + 1
                if(counter <= ((columns)/2)):
                    if(EachRow>0):
                        for eachCellPosition in range(len(tableData[EachRow][0])):
                            tableData[EachRow-1][0][eachCellPosition] = (tableData[EachRow-1][0][eachCellPosition] + tableData[EachRow][0][eachCellPosition]).strip()
                        tableData[EachRow-1][1][0] = tableData[EachRow][1][0]
                        tableData[EachRow-1][1][2] = tableData[EachRow][1][2]
                        tableData[EachRow-1][1][4] = int(tableData[EachRow-1][1][4] + tableData[EachRow][1][4])/2
                        del(tableData[EachRow]) 
                        tableLen =len(tableData)
                else:
                    for eachCellPosition in range(len(tableData[EachRow][0])):
                            tableData[EachRow][0][eachCellPosition] = tableData[EachRow][0][eachCellPosition].strip()
    if(len(tableData)>0):
        if(len(tableData[0])>0):
            columns = len(tableData[0][0]) 
    if(columns>0):
        tableLen = len(tableData)
        for EachRow in range(tableLen):
            counter = 0
            if(EachRow < tableLen):
                for eachCells in range(len(tableData[EachRow][0])):
                #for eachCells in tableData[EachRow][0]:
                    if(len((tableData[EachRow][0][eachCells].strip())))>0:
                        counter = counter + 1
                if(counter <= ((columns)/2)):
                    if(EachRow>0):
                        for eachCellPosition in range(len(tableData[EachRow][0])):
                            tableData[EachRow-1][0][eachCellPosition] = (tableData[EachRow-1][0][eachCellPosition] + tableData[EachRow][0][eachCellPosition]).strip()
                        tableData[EachRow-1][1][0] = tableData[EachRow][1][0]
                        tableData[EachRow-1][1][2] = tableData[EachRow][1][2]
                        tableData[EachRow-1][1][4] = int(tableData[EachRow-1][1][4] + tableData[EachRow][1][4])/2
                        del(tableData[EachRow]) 
                        tableLen =len(tableData)
                else:
                    for eachCellPosition in range(len(tableData[EachRow][0])):
                            tableData[EachRow][0][eachCellPosition] = tableData[EachRow][0][eachCellPosition].strip()

                        
                        
    return tableData

def mainfunction(filename):
    #if __name__ == "__main__":
    #strn = "a8ac.hocr"
    #strn = r"D:\OCR\Helix Enterprise Engine v0.7\testingfunctionality\AdityaSample.hocr"
    #"D:\OCR\Helix Enterprise Engine v0.9\SamplePageDevided\PRANAB\PRANAB-1.hocr"
    #strn = r"SamplePageDevided\PRAMODINI\PRA-1.hocr";
    #strn = r"SamplePageDevided\PRAMODINI\test.hocr";
    strn = filename
    hocr = open(strn,'r',encoding="utf-8").read()
    soup = BeautifulSoup(hocr,'html.parser')
    FinalLableAndTableForAllPageArray = hocr_function(soup)
    # print(FinalLableAndTableForAllPageArray)
    textvalue = ArrayToText(FinalLableAndTableForAllPageArray)
    #ArrayValue = TextToArray(textvalue)
    #print(ArrayValue)
    return textvalue
    #print(FinalLableAndTableForAllPageArray)
    #finalarraysting = ArrayToText(FinalLableAndTableForAllPageArray)
    #print(tempstr)
    #TextToArray(tempstr)
    #print("Line Counter Value:-",FinalLableAndTableForAllPageArray)
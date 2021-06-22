import sys
file_open = open("D:/mediaeast/11-12-19/test2/otput.txt", "r")
file_open_write = open("D:/mediaeast/11-12-19/test2/output_csv.txt", "w")
f = file_open.readlines()
for data in f:
    file_open_write.writelines(data.replace("||",",").lstrip(",") + "\n")

file_open_write.close()
file_open.close()
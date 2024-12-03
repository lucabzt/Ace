"""
Based on the file by bjornstenger
Github link to the original file - https://github.com/bjornstenger/xml2yolo
"""
import os
import glob
from xml.dom import minidom

#Getting the Name of the classes to make the respective Folders
num = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'] #Value of the Card
type = ['S','C','D','H'] #Type of the Card
combinations = [[i,j] for i in num for j in type] #Getting all the string combinations
classes = []

#Joining the two string to get one class
#For e.g '1' and 'S' to get the class '1S'
for combination in combinations:
	for i in range(1):
		res = combination[i] + combination[i+1]
		classes.append(res)
classes.append('JOKER')


START_BOUNDING_BOX_ID = 1
lut={}

length = len(classes)

for i in range(1,length+1):
	lut[classes[i-1]]=i-1

"""
{'AS': 0, 'AC': 1, 'AD': 2, 'AH': 3, '2S': 4, '2C': 5, '2D': 6, '2H': 7, '3S': 8, '3C': 9, '3D': 10, '3H': 11, '4S': 12, '4C': 13, '4D': 14, '4H': 15, '5S': 16, '5C': 17, '5D': 18, '5H': 19, '6S': 20, '6C': 21, '6D': 22, '6H': 23, '7S': 24, '7C': 25, '7D': 26, '7H': 27, '8S': 28, '8C': 29, '8D': 30, '8H': 31, '9S': 32, '9C': 33, '9D': 34, '9H': 35, '10S': 36, '10C': 37, '10D': 38, '10H': 39, 'JS': 40, 'JC': 41, 'JD': 42, 'JH': 43, 'QS': 44, 'QC': 45, 'QD': 46, 'QH': 47, 'KS': 48, 'KC': 49, 'KD': 50, 'KH': 51, 'JOKER': 52}
"""


def convert_coordinates(size, box):
    dw = 1.0/size[0]
    dh = 1.0/size[1]
    x = (box[0]+box[1])/2.0
    y = (box[2]+box[3])/2.0
    w = box[1]-box[0]
    h = box[3]-box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


def convert_xml2yolo( lut ):

    for fname in glob.glob("*.xml"):
        
        xmldoc = minidom.parse(fname)
        
        fname_out = (fname[:-4]+'.txt')

        with open(fname_out, "w") as f:

            itemlist = xmldoc.getElementsByTagName('object')
            size = xmldoc.getElementsByTagName('size')[0]
            width = int((size.getElementsByTagName('width')[0]).firstChild.data)
            height = int((size.getElementsByTagName('height')[0]).firstChild.data)

            for item in itemlist:
                # get class label
                classid =  (item.getElementsByTagName('name')[0]).firstChild.data
                if classid in lut:
                    label_str = str(lut[classid])
                else:
                    label_str = "1"
                    print ("warning: label '%s' not in look-up table" % classid)

                # get bbox coordinates
                xmin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmin')[0]).firstChild.data
                ymin = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymin')[0]).firstChild.data
                xmax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('xmax')[0]).firstChild.data
                ymax = ((item.getElementsByTagName('bndbox')[0]).getElementsByTagName('ymax')[0]).firstChild.data
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert_coordinates((width,height), b)
                #print(bb)

                f.write(label_str + " " + " ".join([("%.6f" % a) for a in bb]) + '\n')

        print ("wrote %s" % fname_out)



def main():
    convert_xml2yolo( lut )


if __name__ == '__main__':
    main()
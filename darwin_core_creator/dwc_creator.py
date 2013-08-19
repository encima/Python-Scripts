import exiftool, csv
import sys, os, glob
from ConfigParser import SafeConfigParser
from datetime import *

def get_output_dir(output):
	num_archives = len([name for name in os.listdir(output) if os.path.isdir(output + name)])
	output_dir = output + 'dwc_arch' + str(num_archives+1) + '/'
	os.makedirs(output_dir)
	return output_dir

def get_images(directory):
	return ([directory + name for name in os.listdir(directory) if os.path.splitext(name)[1] == '.JPG' and not name.startswith('.')])

def datetime_from_string(datestring):
	time = datetime.strptime(datestring, "%Y:%m:%d %H:%M:%S")
	return time

def create_archive(directory, output_dir, img):
	with exiftool.ExifTool() as et:
	    metadata = et.get_metadata(img)
	    date =  metadata['MakerNotes:DateTimeOriginal'].split(" ")[0]
	    time =  metadata['MakerNotes:DateTimeOriginal'].split(" ")[1]
	    path =  metadata['SourceFile']
	    recBy =  metadata['MakerNotes:SerialNumber']
	setfile = open(output_dir + 'set.csv', 'ab')
	setwriter = csv.writer(setfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	setwriter.writerow([2, 'MovingImage', recBy, date, time, '', '', '', ''])
	return 2

def write_image_csv(id, paths, output_dir):
	image_csv = open(output_dir + 'images.csv', 'ab')
	imgwriter = csv.writer(image_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	imgwriter.writerow(['eventID', 'identifier'])
	for path in paths:
		imgwriter.writerow([2, path])
	image_csv.close()

def setup_csv(output_dir, filename, headers):
	csvfile = open(output_dir + filename, 'wb')
	csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csvwriter.writerow(headers)
	csvfile.close

def write_xml(output_dir, key, parser):
	xml_file = open(output_dir + key + '.xml', 'wb')
	xml_file.write(parser.get('DEFAULT', key))
	xml_file.close


parser = SafeConfigParser()
parser.read('config.ini')
directory  = parser.get('DEFAULT', 'IMG_DIR')
output = parser.get('DEFAULT', 'OUTPUT_DIR')
step = int(parser.get('DEFAULT', 'STEP'))

images = get_images(directory)

for i in range(0, len(images), step):
	output_dir = get_output_dir(output)
	write_xml(output_dir, 'meta', parser)
	write_xml(output_dir, 'eml', parser)
	setup_csv(output_dir, 'images.csv', ['eventID', 'identifier'])
	setup_csv(output_dir, 'set.csv', ['eventID', 'basisOfRecord', 'recordedBy', 'eventDate', 'eventTime', 'locationID', 'scientificName', 'identifiedBy', 'dateIdentified'])
	eventID = create_archive(directory, output_dir, images[i])
	img_to_write = []
	for j in range(i, i+step):
		img_to_write.append(images[j])
	write_image_csv(eventID, img_to_write, output_dir)


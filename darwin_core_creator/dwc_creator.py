import exiftool, csv
import sys, os, glob
from ConfigParser import SafeConfigParser
from datetime import *

def get_output_dir(output):
	num_archives = len([name for name in os.listdir(output) if os.path.isdir(output + name)])
	output_dir = output + 'dwc_arch_' + str(num_archives+1) + '/'
	os.makedirs(output_dir)
	return output_dir

def get_images(directory):
	return ([directory + name for name in os.listdir(directory) if os.path.splitext(name)[1] == '.JPG' and not name.startswith('.')])

def datetime_from_string(datestring):
	time = datetime.strptime(datestring, "%Y:%m:%d %H:%M:%S")
	return time

def create_archiveEXIF(directory, output_dir, img):
	with exiftool.ExifTool() as et:
	    metadata = et.get_metadata(img)
	    date =  metadata['MakerNotes:DateTimeOriginal'].split(" ")[0]
	    time =  metadata['MakerNotes:DateTimeOriginal'].split(" ")[1]
	    path =  metadata['SourceFile']
	    recBy =  metadata['MakerNotes:SerialNumber']
	setfile = open(output_dir + 'set.csv', 'ab')
	setwriter = csv.writer(setfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	setwriter.writerow([eventID, 'MovingImage', recBy, date, time, '', '', '', ''])
	return eventID

def create_archive(output_dir, eventID, basis, recBy, evDate, evTime, loc, species, idBy, idDate):
	setfile = open(output_dir + 'set.csv', 'ab')
	setwriter = csv.writer(setfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	print date
	setwriter.writerow([eventID, basis, recBy, evDate, evTime, loc, species, idBy, idDate])
	return eventID

def write_image_csv(eventID, paths, output_dir):
	image_csv = open(output_dir + 'images.csv', 'ab')
	imgwriter = csv.writer(image_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for path in paths:
		imgwriter.writerow([eventID, path])
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

def __main__():
	parser = SafeConfigParser()
	parser.read('config.ini')
	directory  = parser.get('DEFAULT', 'IMG_DIR')
	output = parser.get('DEFAULT', 'OUTPUT_DIR')
	step = int(parser.get('DEFAULT', 'STEP'))

	images = get_images(directory)
	images = sorted(images, key = lambda x: x[:-4])

	for i in range(0, len(images), step):
		eventID = len([name for name in os.listdir(output) if os.path.isdir(output + name)]) + 1
		output_dir = get_output_dir(output)
		print eventID
		write_xml(output_dir, 'meta', parser)
		write_xml(output_dir, 'eml', parser)
		setup_csv(output_dir, 'images.csv', ['eventID', 'identifier'])
		setup_csv(output_dir, 'set.csv', ['eventID', 'basisOfRecord', 'recordedBy', 'eventDate', 'eventTime', 'locationID', 'scientificName', 'identifiedBy', 'dateIdentified'])
		create_archiveEXIF(directory, output_dir, images[i])
		img_to_write = []
		for j in range(i, i+step):
			print images[j]
			img_to_write.append(images[j])
		print '------'
		write_image_csv(eventID, img_to_write, output_dir)


import pysql as ps
import dwc_creator as dwc
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

cur = ps.connect('MYSQL')
res = ps.query(cur, 'SELECT COUNT(*) AS num_obs FROM Observations;')

num_obs = res[0]['num_obs']

output_root = parser.get('DEFAULT', 'OUTPUT_DIR')

for i in range(1, num_obs):
	res = ps.query(cur, "SELECT o.Obs_ID, group_concat(i.path ORDER BY i.path ASC SEPARATOR ',') AS path, s.Name, \
   c.Contents_ID, \
    o.Taken_ID, \
    o.Obs_Date, \
    o.Obs_Time \
FROM\
    Observations o \
    left join Contents_Classifications_Corr c \
    on o.Obs_ID = c.Obs_ID \
    left join Species s \
    on c.Species_ID = s.Species_ID \
    left join ImageSets i \
    on i.set_id = o.Obs_ID \
WHERE o.Obs_ID = %d \
GROUP BY s.Name;" % i)
	if len(res) > 0:
		output_dir = dwc.get_output_dir(output_root)
		archive = res[0]
		print output_dir
		print archive
		obs_id = archive['Obs_ID']
		time = archive['Obs_Time']
		date = archive['Obs_Date']
		print date
		images = archive['path'].split(',')
		loc_id = archive['Taken_ID']
		sciName = archive['Name']
		dwc.write_xml(output_dir, 'meta', parser)
		dwc.write_xml(output_dir, 'eml', parser)
		dwc.setup_csv(output_dir, 'images.csv', ['eventID', 'identifier'])
		dwc.setup_csv(output_dir, 'set.csv', ['eventID', 'basisOfRecord', 'recordedBy', 'eventDate', 'eventTime', 'locationID', 'scientificName', 'identifiedBy', 'dateIdentified'])
		dwc.create_archive(output_dir, obs_id, 'MovingImage', loc_id, str(date), str(time), loc_id, sciName, '', '')
		dwc.write_image_csv(obs_id, images, output_dir)

import pysql as ps
import dwc_creator as dwc
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('config.ini')

cur = ps.connect('RDS')
res = ps.query(cur, 'SELECT COUNT(*) AS num_obs FROM Observations;')

num_obs = res[0]['num_obs']

# output_dir = dwc.get_output_dir(parser.get('DEFAULT', 'OUTPUT'))

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
	 archive = res[0]
	 print archive['Obs_Time']
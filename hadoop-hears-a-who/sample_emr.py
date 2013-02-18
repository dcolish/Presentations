import datetime

import boto
from boto.emr.instance_group import InstanceGroup
from boto.emr.step import InstallPigStep, PigStep


conn = boto.connect_emr()

instance_groups = [
    InstanceGroup(1, 'MASTER', 'm1.small', 'SPOT', 'master@0.10', '0.10'),
    InstanceGroup(2, 'CORE', 'm1.medium', 'SPOT', 'master@0.10', '0.10'),
]

pig_file = 's3://elasticmapreduce/samples/pig-apache/do-reports2.pig'
INPUT = 's3://elasticmapreduce/samples/pig-apache/input/'
OUTPUT = 's3://org.unencrypted.emr.output/apache_sample/%s' % datetime.datetime.utcnow().isoformat()

pig_args = ['-p', 'INPUT=%s' % INPUT,
            '-p', 'OUTPUT=%s' % OUTPUT]

pig_step = PigStep('Process Reports', pig_file, pig_args=pig_args)
steps = [InstallPigStep(), pig_step]

job_id = conn.run_jobflow(name='sample apache report',

                          steps=steps,
                          log_uri="s3://org.unencrypted.emr.log/sampleflow_logs",
                          enable_debugging=True,
                          ami_version="latest",
                          hadoop_version="1.0.3",
                          instance_groups=instance_groups,
                          keep_alive=False)

print job_id

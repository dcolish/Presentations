from urllib import urlencode
from urllib2 import urlopen

username = ''
password = ''
record = 0
ip = urlopen('http://www.dnsmadeeasy.com/myip.jsp').read().strip()
res = urlopen('http://www.dnsmadeeasy.com/servlet/updateip',
              urlencode(dict(username=username,
                   password=password,
                   id=record,
                   ip=ip)))

if res.code == 200:
    print "Updated record %d with ip %s" % (record, ip)
else:
    print "Failed to update record %d" % record

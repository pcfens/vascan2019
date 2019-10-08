#!/usr/bin/env python

import argparse
import os
import re
from easyzone import easyzone

parser = argparse.ArgumentParser(
    description='Validate that bind zone files meet some local styles.')
parser.add_argument('files', nargs='+', help='Zone files to check')
args = parser.parse_args()

errors = 0

for file in args.files:        
    zone = os.path.splitext(os.path.basename(file))[0]
    if zone.endswith('.internal') or zone.endswith('.external') or zone.endswith('.dc'):
        zone = os.path.splitext(zone)[0]

    try:
        zone = easyzone.zone_from_file(zone, file)

    except:
        print 'Error parsing ' + zone
        errors += 1
        continue

    zone_regex = str(zone.domain).replace('.', '\.')

    fqdn_error = re.compile(
        r"^(.+)\." + zone_regex + zone_regex + "$")

    try:
        for name in zone.names:
            forgot_period = fqdn_error.match(name)
            if forgot_period is not None:
                print "You probably forgot a period in " + name
                errors += 1
    except:
        print "There was some error validating the zone " + zone.domain
        errors += 1
        continue

if errors > 0:
    exit(1)
else:
    exit(0)

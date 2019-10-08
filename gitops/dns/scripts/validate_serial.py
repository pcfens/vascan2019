#!/usr/bin/env python

import argparse
import os
import re
from easyzone import easyzone

parser = argparse.ArgumentParser(
    description='Validate that bind zone files meet some local styles.')
parser.add_argument('files', nargs='+', help='Zone files to check')
args = parser.parse_args()

serial_regex = re.compile(
    r"^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})(?P<increment>\d{2})$")
errors = 0

for file in args.files:
    zone = os.path.splitext(os.path.basename(file))[0]
    if zone.endswith('.internal') or zone.endswith('.external') or zone.endswith('.dc'):
        zone = os.path.splitext(zone)[0]
    try:
        zone = easyzone.zone_from_file(zone, file)
        result = serial_regex.match(str(zone.root.soa.serial))
    except:
        print 'Error parsing ' + zone
        print 'Check serial number (Should match YYYYMMDDNN)'
        errors += 1
        continue

    if result is None:
        print zone.domain + \
            ' has an invalid serial (' + str(zone.root.soa.serial) + ')'
        errors += 1
        continue

if errors > 0:
    exit(1)
else:
    exit(0)

#!/usr/bin/env python

import argparse
import os
import subprocess
import re
import tempfile
from easyzone import easyzone

# A function to filter out changed files that aren't zone files


def filter_zones(file):
    file_regex = re.compile(r"^(?P<zone>.*)\.db$")
    return file_regex.match(file)


# Pass a single argument of the commit ID since the last deploy
parser = argparse.ArgumentParser(
    description='Validate that serial numbers have been updated since a given commit.')
parser.add_argument('commit', help='Commit ID of the previous test')
args = parser.parse_args()

# Initialize an error counter
errors = 0

# Get a list of changed files
file_list = subprocess.check_output(
    ['git', 'diff', '--name-only', args.commit]).splitlines()
file_list = filter(filter_zones, file_list)

# Iterate over the changed zone files
for file in file_list:
    # Determine the zone name (only required because of local views)
    zone_name = os.path.splitext(os.path.basename(file))[0]
    if zone_name.endswith('.internal') or zone_name.endswith('.external') or zone_name.endswith('.dc'):
        zone_name = os.path.splitext(zone_name)[0]

    # The current zone contents
    new_zone = easyzone.zone_from_file(zone_name, file)

    # Load the old zone in after writing it to a temp file (and cleaning up)
    fd, path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w') as tmp:
            old_file = subprocess.check_output(
                ['git', 'show', args.commit + ':' + file])
            tmp.write(old_file)
            try:
                old_zone = easyzone.zone_from_file(zone_name, path)
            except:
                print 'Unable to validate that the serial for ' + zone_name + ' changed.'
    finally:
        os.remove(path)

    # If the new serial is the the same or less than the old serial we have a problem
    if new_zone.root.soa.serial <= old_zone.root.soa.serial:
        print 'Serial number not updated in ' + zone_name
        errors += 1

if errors > 0:
    exit(1)
else:
    exit(0)

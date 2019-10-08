#!/bin/bash
# crudely whip through the zone files and check them
#
PATH=/usr/sbin:/usr/bin:/usr/local/bin:/bin

# parameters to named-checkzone
PARAMS="-i full -m warn -n fail"

if [ ! -x `which named-checkzone` ]; then
  echo "ERROR $0: named-checkzone not found, is it installed?"
  exit 1
fi

exit_code=0;

for file in $(ls *.db); do
  if [ -f "$file" ] && [[ $file == *.db ]]; then
    zone=$(basename "$file" .db)
    if [[ $zone == *.internal ]]; then
      zone=$(basename "$zone" .internal)
    elif [[ $zone == *.external ]]; then
      zone=$(basename "$zone" .external)
    fi
    named-checkzone -q $PARAMS $zone $file
    if [ $? -ne 0 ]; then
      echo "Failure in $file ($zone):"
      named-checkzone $PARAMS $zone $file
      exit_code=1;
    fi
  fi
done

exit $exit_code

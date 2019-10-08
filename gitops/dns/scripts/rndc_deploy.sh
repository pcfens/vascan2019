#!/bin/bash

export PATH="/opt/local/bind/sbin:/usr/local/bin:/usr/sfw/bin:/usr/ccs/bin:/usr/sbin:/usr/local/sbin:/usr/bin:/usr/local/bin"

OLD_COMMIT=$(git rev-parse HEAD)
git pull
UPDATED_FILES=$(git diff --name-only "$OLD_COMMIT")


for updated_file in $UPDATED_FILES; do
  if [ -f "$updated_file" ] && [[ $updated_file == *.db ]]; then
    zone=$(basename "$updated_file" .db)
    if [[ $zone == *.internal ]]; then
      zone=$(basename "$zone" .internal)
      echo "rndc reload $zone in internal"
      rndc reload $zone in internal
    elif [[ $zone == *.external ]]; then
      zone=$(basename "$zone" .external)
      echo "rndc reload $zone in external"
      rndc reload $zone in external
    else
      echo "rndc reload $zone in internal"
      rndc reload $zone in internal
      echo "rndc reload $zone in external"
      rndc reload $zone in external
    fi
  fi
done

#!/bin/bash
if [ $# -ne 1 ]
then
  echo "Usage: $0 <user@host>"
else
  ssh -N -R 0.0.0.0:1234:localhost:3000 $1
fi

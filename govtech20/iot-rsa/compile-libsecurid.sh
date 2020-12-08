#!/bin/bash
gcc -shared -fPIC -o libsecurid.so libsecurid.c 
chmod +x libsecurid.so

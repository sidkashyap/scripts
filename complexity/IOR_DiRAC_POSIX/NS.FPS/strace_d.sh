#!/bin/bash

/usr/bin/strace  -T -ttt -o /scratch/dr002/shared/IOR_DiRAC/NS.FPS/strace_out/strace.out.$$ /scratch/dr002/shared/DiRAC3-testsuite/bin/ior $@

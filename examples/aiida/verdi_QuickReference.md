# Verdi - Quick Reference

## Verdi - Computer Setup

  verdi computer setup -L {tutor} -H {localhost} -T core.local -S core.direct -w `echo $PWD/work` -n
  verdi computer configure core.local {tutor} --safe-interval 1 -n



    label (-L): tutor
    hostname (-H): localhost
    transport (-T): local
    scheduler (-S): direct
    work-dir (-w): The work subdirectory of the current directory

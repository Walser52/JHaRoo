PROGRAM WriteData
  IMPLICIT NONE

  INTEGER :: iuni
  CHARACTER(LEN=100) :: filename
  INTEGER :: ik, ispin, nspin

  ! Assign values to variables
  iuni = 10
  filename = 'test.wfc'
  ik = 13
  ispin = 12
  nspin = 14

  CALL WriteToFile(iuni, filename, ik, ispin, nspin)

CONTAINS

  SUBROUTINE WriteToFile(iuni, filename, ik, ispin, nspin)
    INTEGER, INTENT(IN) :: iuni
    CHARACTER(LEN=*), INTENT(IN) :: filename
    INTEGER, INTENT(IN) :: ik, ispin, nspin

    OPEN (UNIT = iuni, FILE = TRIM(filename)//'.dat', FORM='unformatted', STATUS = 'unknown')

    print *, iuni, ik, ispin, nspin
    WRITE(iuni) ik , ispin
    WRITE(iuni) ik , ispin, nspin

    CLOSE(iuni)
  END SUBROUTINE WriteToFile

END PROGRAM WriteData
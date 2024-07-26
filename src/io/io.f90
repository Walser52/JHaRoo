PROGRAM WriteData
  IMPLICIT NONE
  ! ik, xk, ispin, gamma_only, scalef
  ! ngw, igwx, npol, nbnd



  INTEGER,            INTENT(IN) :: iuni
  CHARACTER(LEN=*),   INTENT(IN) :: filename
  INTEGER,            INTENT(IN) :: ik, ispin, nspin
  ! REAL(DP),           INTENT(IN) :: xk(:)
  ! COMPLEX(DP),        INTENT(IN) :: wfc(:,:)
  ! INTEGER,            INTENT(IN) :: ngw
  ! LOGICAL,            INTENT(IN) :: gamma_only
  ! INTEGER,            INTENT(IN) :: nbnd
  ! INTEGER,            INTENT(IN) :: ngwl
  ! INTEGER,            INTENT(IN) :: igl(:)
  ! INTEGER,            INTENT(IN) :: mill_k(:,:)
  ! REAL(DP),           INTENT(IN) :: b1(3), b2(3), b3(3)    
  ! REAL(DP),           INTENT(IN) :: scalef    

  ! Dummy values for variables
  iuni = 10
  filename = 'test.wfc'
  ik = 12
  ispin = 13
  nspin = 14
  
  OPEN (UNIT = iuni, FILE = TRIM(filename)//'.dat', FORM='unformatted', STATUS = 'unknown')
  WRITE(iuni) ik, ispin, nspin
  WRITE(iuni) ik, ispin, nspin
  WRITE(iuni) ik, ispin, nspin



  ! ngw = 5
  ! nbnd = 3
  ! ngwl = 4
  ! gamma_only = .TRUE.
  ! scalef = 1.0_DP

  ! ALLOCATE(xk(3))
  ! ALLOCATE(wfc(ngw, nbnd))
  ! ALLOCATE(igl(ngwl))
  ! ALLOCATE(mill_k(3, ngw))

  ! xk = (/ 0.1_DP, 0.2_DP, 0.3_DP /)
  ! wfc = CMPLX(RESHAPE([ (DBLE(i) + DBLE(j)*0.1_DP, i = 1, ngw), (j = 1, nbnd) ], (/ngw, nbnd/)), KIND=DP)
  ! igl = (/ 1, 2, 3, 4 /)
  ! mill_k = RESHAPE([ (i + j, i = 1, 3), (j = 1, ngw) ], (/3, ngw/))
  ! b1 = (/ 1.0_DP, 0.0_DP, 0.0_DP /)
  ! b2 = (/ 0.0_DP, 1.0_DP, 0.0_DP /)
  ! b3 = (/ 0.0_DP, 0.0_DP, 1.0_DP /)

  ! Open the file
  ! OPEN (UNIT = iuni, FILE = TRIM(filename)//'.dat', FORM='unformatted', STATUS = 'unknown')

  ! Write data to the file
  ! WRITE(iuni) ik, xk, ispin, gamma_only, scalef
  ! WRITE(iuni) ngw, ngwl, nbnd
  ! WRITE(iuni) b1, b2, b3
  ! WRITE(iuni) igl(1:ngwl)
  
  ! Close the file
  CLOSE(iuni)

  ! Deallocate arrays
  ! DEALLOCATE(xk, wfc, igl, mill_k)

END PROGRAM WriteData

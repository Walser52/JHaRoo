program trim_example
  implicit none
  character(len=20) :: str
  character(len=:), allocatable :: trimmed_str

  str = "Hello, Fortran     "

  ! Using TRIM and creating a new character string with the correct length
  trimmed_str = TRIM(str)

  print *, "Original string: '", str, "' Length:", LEN(str)
  print *, "Trimmed string: '", trimmed_str, "' Length:", LEN(trimmed_str)
end program trim_example

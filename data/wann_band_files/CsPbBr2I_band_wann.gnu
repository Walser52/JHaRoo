set style data dots
set nokey
set xrange [0: 3.98277]
set yrange [ -1.41544 :  9.96486]
set arrow from  0.53525,  -1.41544 to  0.53525,   9.96486 nohead
set arrow from  1.07049,  -1.41544 to  1.07049,   9.96486 nohead
set arrow from  1.82745,  -1.41544 to  1.82745,   9.96486 nohead
set arrow from  2.73851,  -1.41544 to  2.73851,   9.96486 nohead
set arrow from  3.47576,  -1.41544 to  3.47576,   9.96486 nohead
set xtics ("G"  0.00000,"X"  0.53525,"M"  1.07049,"G"  1.82745,"R"  2.73851,"X|M"  3.47576,"R"  3.98277)
 plot "CsPbBr2I_band.dat"

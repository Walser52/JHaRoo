set style data dots
set nokey
set xrange [0: 3.70624]
set yrange [ -2.33771 :  9.91464]
set arrow from  0.49021,  -2.33771 to  0.49021,   9.91464 nohead
set arrow from  0.98043,  -2.33771 to  0.98043,   9.91464 nohead
set arrow from  1.67369,  -2.33771 to  1.67369,   9.91464 nohead
set arrow from  2.52277,  -2.33771 to  2.52277,   9.91464 nohead
set arrow from  3.21603,  -2.33771 to  3.21603,   9.91464 nohead
set xtics ("G"  0.00000,"X"  0.49021,"M"  0.98043,"G"  1.67369,"R"  2.52277,"X|M"  3.21603,"R"  3.70624)
 plot "relCsPBBr3_band.dat"

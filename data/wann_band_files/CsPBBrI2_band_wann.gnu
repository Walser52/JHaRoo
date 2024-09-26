set style data dots
set nokey
set xrange [0: 4.53166]
set yrange [ -0.38262 : 11.36813]
set arrow from  0.48688,  -0.38262 to  0.48688,  11.36813 nohead
set arrow from  1.23056,  -0.38262 to  1.23056,  11.36813 nohead
set arrow from  2.11944,  -0.38262 to  2.11944,  11.36813 nohead
set arrow from  3.13839,  -0.38262 to  3.13839,  11.36813 nohead
set arrow from  4.03350,  -0.38262 to  4.03350,  11.36813 nohead
set xtics ("G"  0.00000,"X"  0.48688,"M"  1.23056,"G"  2.11944,"R"  3.13839,"X|M"  4.03350,"R"  4.53166)
 plot "CsPBBrI2_band.dat"

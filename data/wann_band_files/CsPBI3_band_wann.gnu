set style data dots
set nokey
set xrange [0: 3.81914]
set yrange [ -1.27089 :  9.97441]
set arrow from  0.50515,  -1.27089 to  0.50515,   9.97441 nohead
set arrow from  1.01029,  -1.27089 to  1.01029,   9.97441 nohead
set arrow from  1.72468,  -1.27089 to  1.72468,   9.97441 nohead
set arrow from  2.59961,  -1.27089 to  2.59961,   9.97441 nohead
set arrow from  3.31400,  -1.27089 to  3.31400,   9.97441 nohead
set xtics ("G"  0.00000,"X"  0.50515,"M"  1.01029,"G"  1.72468,"R"  2.59961,"X|M"  3.31400,"R"  3.81914)
 plot "CsPBI3_band.dat"

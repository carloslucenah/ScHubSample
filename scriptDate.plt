set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set xrange ["2019-07-01 18:00:00":"2019-07-02 10:30:00"]
set terminal pngcairo size 1280,720 enhanced font 'Verdana,10'
set output "C:/MEV/Tokyo2020/Trazas_Transacciones/LOG ANALYZER SCRIPT/date.png"
set key left box 
set format x "%Y-%m-%d %H:%M"
plot "C:/MEV/Tokyo2020/Trazas_Transacciones/LOG ANALYZER SCRIPT/results.dat" using 2:7 t "Publish time (ms)" noenhanced ls z pt 7
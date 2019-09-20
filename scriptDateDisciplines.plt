set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
getcolumnvalues(x) = sprintf('python -c "data=set([x.split(\"##\")[%d] for x in open(\"C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/results.csv\",\"r\")][1:]);print(*sorted(data))"',x-1)
disciplines = system(getcolumnvalues(3))
msgTypes = system(getcolumnvalues(4))
print disciplines
#print msgTypes
set xrange ["2019-07-05 01:10:00":"2019-07-05 14:05:00"]
set terminal pngcairo size 1280,720 enhanced font 'Verdana,10'
set key left box 
set format x "%Y-%m-%d %H:%M"
#print strcol(4)
do for [y=1:words(disciplines)]{
#set title "Publish time (ms) - ", word(disciplines,y)
do for [i=1:20] {
    set style line i linecolor rgb hsv2rgb(0.05*(i-1), 1, 1)
}
disciplineTitle = sprintf ("Publish time (ms) - %s", word(disciplines,y))
outputFile = sprintf("C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/%s.png", word(disciplines,y))
set title disciplineTitle
set output outputFile
#print "C:/MEV/Tokyo2020/Trazas_Transacciones/LOG ANALYZER SCRIPT/", word(disciplines,y), ".png"
#set output "C:/MEV/Tokyo2020/Trazas_Transacciones/LOG ANALYZER SCRIPT/", word(disciplines,y), ".png"
##plot for[z=1:words(msgTypes)] "C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/Resultados_Central/results.dat" using 2:(strcol(5) eq word(msgTypes,z)? $7:1/0) t word(msgTypes,z) noenhanced ls z pt 7
plot for[z=1:words(msgTypes)] "C:/MEV/Tokyo2020/Trazas_Transacciones/09072019/new/resultados/results.dat" using 2:((strcol(5) eq word(msgTypes,z)) && (strcol(4) eq word(disciplines,y))? $8:1/0) t word(msgTypes,z) noenhanced ls z pt 7
}
#plot "C:/MEV/Tokyo2020/Trazas_Transacciones/LOG ANALYZER SCRIPT/results.dat" using 2:7 t "Publish time (ms)" pt 420 ps 600
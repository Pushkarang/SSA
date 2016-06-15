gcc genir.c maingenir.c 
./a.out > s.ll
python cfgnu.py>a.txt
python ssa.py>outpuut
dot -Tps outpuut -o ssa.ps
evince ssa.ps


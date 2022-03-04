0dbfs=1

instr 1
    ares noise p4, 0.2 
    kenv linseg 0, 0.05, 1, 0.02, 1, 0.05, 0
    out ares * kenv
endin

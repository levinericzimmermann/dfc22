0dbfs=1

instr 1
    asig poscil3 0.5, p4
    kenv linseg 0, 0.05, 1, p3 - 0.1, 1, 0.05, 0
    out asig * kenv
endin

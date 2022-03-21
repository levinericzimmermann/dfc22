0dbfs=1

instr 1
    ; anoise noise p4 * 0.00000001, 0.2
    anoise noise p4 * 1, 0.2
    iAttackDuration = (rnd(6) + 3) / 1000
    iReleaseDuration = (rnd(10) + 3) / 1000
    kenv linseg 0, iAttackDuration, 1, 0.0075, 1, iReleaseDuration, 0
    iFilterFreq = rnd(80) + 60
    ; by 3/2
    iBandSize = (iFilterFreq * 1.5) - iFilterFreq
    iLowPassFrequency = (rnd(3) + 1) * 2000
    ; anoiseFiltered resonx anoise, iFilterFreq, iBandSize, 2
    anoiseLowpass butterlp anoise, iLowPassFrequency
    anoiseFiltered butterbp anoiseLowpass, iFilterFreq, iBandSize
    out anoiseFiltered * kenv
endin

open angl0.mol2 
sel @/serialNumber=1 
addh spec sel
write format mol2 #0 tmp2.mol2
stop

import sys
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_FACE
for fn in sys.argv[1:]:
    r=STEPControl_Reader(); st=r.ReadFile(fn)
    if st!=IFSelect_RetDone: print(fn,'READ FAIL'); continue
    r.TransferRoots(); sh=r.OneShape()
    ns=0; e=TopExp_Explorer(sh,TopAbs_SOLID)
    while e.More(): ns+=1; e.Next()
    nf=0; e=TopExp_Explorer(sh,TopAbs_FACE)
    while e.More(): nf+=1; e.Next()
    p=GProp_GProps(); BRepGProp.VolumeProperties_s(sh,p)
    print(fn.split('/')[-1],'solids',ns,'faces',nf,'valid',BRepCheck_Analyzer(sh).IsValid(),'vol',round(p.Mass(),1))

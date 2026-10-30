import sys
from OCP.STEPControl import STEPControl_Reader
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID, TopAbs_WIRE
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
for fn in sys.argv[1:]:
    r=STEPControl_Reader(); r.ReadFile(fn); r.TransferRoots(); sh=r.OneShape()
    e=TopExp_Explorer(sh,TopAbs_SOLID); vols=[]
    while e.More():
        p=GProp_GProps(); BRepGProp.VolumeProperties_s(e.Current(),p); vols.append(round(p.Mass(),1)); e.Next()
    bad=[]; e=TopExp_Explorer(sh,TopAbs_FACE)
    while e.More():
        f=e.Current()
        if not BRepCheck_Analyzer(f).IsValid():
            p=GProp_GProps(); BRepGProp.SurfaceProperties_s(f,p); c=p.CentreOfMass()
            nw=0; w=TopExp_Explorer(f,TopAbs_WIRE)
            while w.More(): nw+=1; w.Next()
            bad.append((round(p.Mass(),2),round(c.X(),1),round(c.Y(),1),round(c.Z(),1),nw))
        e.Next()
    print(fn.split('/')[-1],vols,'bad',len(bad),bad[:5])

import sys, os, time
from OCP.STEPControl import STEPControl_Reader, STEPControl_Writer, STEPControl_AsIs
from OCP.ShapeFix import ShapeFix_Shape
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.Interface import Interface_Static
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
Interface_Static.SetCVal_s("write.step.schema","AP214IS"); Interface_Static.SetCVal_s("write.step.unit","MM")
src,dst=sys.argv[1],sys.argv[2]
r=STEPControl_Reader(); r.ReadFile(src); r.TransferRoots(); sh=r.OneShape()
fx=ShapeFix_Shape(sh); fx.Perform(); sh=fx.Shape()
comp=TopoDS_Compound(); bb=BRep_Builder(); bb.MakeCompound(comp)
e=TopExp_Explorer(sh,TopAbs_SOLID); n=0
while e.More():
    so=e.Current(); p=GProp_GProps(); BRepGProp.VolumeProperties_s(so,p)
    if abs(p.Mass())<1e-3: e.Next(); continue
    if p.Mass()<0: so=so.Reversed()
    bb.Add(comp,so); n+=1; e.Next()
p=GProp_GProps(); BRepGProp.VolumeProperties_s(comp,p)
w=STEPControl_Writer(); w.Transfer(comp,STEPControl_AsIs); w.Write(dst)
print(os.path.basename(src),'solidos',n,'valido',BRepCheck_Analyzer(comp).IsValid(),'vol',round(p.Mass(),1),round(os.path.getsize(dst)/1e3),'KB')

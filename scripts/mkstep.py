# STEP de cada peca da pagina (solido costurado, faces coplanares unidas), para exportar no visualizador
import pickle, sys, os, time, numpy as np
from OCP.gp import gp_Pnt
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCP.TopoDS import TopoDS
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.Interface import Interface_Static
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopAbs import TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.TCollection import TCollection_HAsciiString
import trimesh
OUT=sys.argv[1]; only=set(sys.argv[2:])
os.makedirs(OUT,exist_ok=True)
Interface_Static.SetCVal_s("write.step.schema","AP214IS"); Interface_Static.SetCVal_s("write.step.unit","MM")
parts=pickle.load(open('parts.pkl','rb'))
for pid,label,grp,m in parts:
    if grp=='ref' or (only and pid not in only): continue
    t=time.time()
    bodies=m.split(only_watertight=False) if len(m.faces)<400000 else [m]
    comp=TopoDS_Compound(); bb=BRep_Builder(); bb.MakeCompound(comp); ok=True; nsol=0
    for b in bodies:
        b=b.copy(); b.merge_vertices(); b.update_faces(b.nondegenerate_faces())
        if b.is_volume and b.volume<0: b.invert()
        sew=BRepBuilderAPI_Sewing(1e-3)
        V=b.vertices
        for f in b.faces:
            pl=BRepBuilderAPI_MakePolygon(gp_Pnt(*V[f[0]]),gp_Pnt(*V[f[1]]),gp_Pnt(*V[f[2]]),True)
            if not pl.IsDone(): continue
            fc=BRepBuilderAPI_MakeFace(pl.Wire(),True)
            if fc.IsDone(): sew.Add(fc.Face())
        sew.Perform(); sh=sew.SewedShape()
        e=TopExp_Explorer(sh,TopAbs_SHELL)
        while e.More():
            try:
                ms=BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(e.Current())); so=ms.Solid()
                u=ShapeUpgrade_UnifySameDomain(so,True,True,False); u.Build(); so=u.Shape()
                bb.Add(comp,so); nsol+=1
            except Exception as ex: ok=False
            e.Next()
    w=STEPControl_Writer(); w.Transfer(comp,STEPControl_AsIs); w.Write(os.path.join(OUT,pid+'.step'))
    sz=os.path.getsize(os.path.join(OUT,pid+'.step'))
    print(pid, 'solidos',nsol, 'valido',BRepCheck_Analyzer(comp).IsValid(), round(sz/1e3),'KB', round(time.time()-t,1),'s', flush=True)

exec(open('tras_base_versoes.py').read().split('def B1(ax):')[0])
def as03b(ax,xc,yc,zoom=False):
    pp(ax,box(xc-17,yc-9,xc+5,yc+9),'#2a2a2a','#666',0.6,12)
    for dx in (-11,-6,-1): ax.add_patch(plt.Rectangle((xc+dx-1,yc-3),2,6,fc='#777',ec='none',zorder=13))
    pp(ax,box(xc+8,yc-8,xc+20,yc+8),'#c42020','#300',0.6,12); ax.text(xc+14,yc,'I/O',fontsize=4.5,color='w',ha='center',va='center',zorder=14,rotation=90)
    for dx in (-32.0,32.0): ax.add_patch(plt.Circle((xc+dx,yc),2.3,fc='#c43b3b',ec='#000',lw=.4,zorder=13))
def V(ax,var):
    base(ax); c=hexa(-100,100,4,72); ls,il=lados(c)
    pp(ax,c,'#3aa857'); bolts(ax,[(-72,12),(72,12),(-72,62),(72,62)])
    for g in ls:
        if g.centroid.y<42 and g.centroid.x>0 and var>0:
            xc,yc=g.centroid.x+4,20.0
            if var==1:   # janela propria na asa, moldura preta saliente com chanfro (tomada na face)
                mol=op(box(xc-41,yc-17,xc+41,yc+17),4.0); g=g.difference(bf(mol,0.5)); pp(ax,g,'#45b862')
                pp(ax,mol,'#141516','#000',0.9,10); pp(ax,op(box(xc-25,yc-14.5,xc+25,yc+14.5),1.5),'#0a0a0a','#000',0.6,11); as03b(ax,xc,yc)
            else:        # asa recortada: a tomada fica num degrau preto que atravessa a asa ate a borda de baixo
                deg=box(xc-42,-5,xc+120,yc+18); g=maior(op(g.difference(bf(deg,4.0)),R)); pp(ax,g,'#45b862')
                pp(ax,op(box(xc-25,yc-14.5,xc+25,yc+14.5),1.5),'#0a0a0a','#000',0.6,11); as03b(ax,xc,yc)
            continue
        pp(ax,g,'#2f9449' if g.centroid.y>42 else '#45b862')
    for i_ in il:
        if var>0 and i_.centroid.x>0: continue
        pp(ax,i_,'#1a1c1e','#000',0.6,4); pp(ax,grade(i_),'#0a0b0c','#000',0.4,5)
fig,axs=plt.subplots(2,1,figsize=(13,7))
for ax,var,t,n in ((axs[0],1,'B2a — Tomada numa moldura preta saliente na asa','A asa da direita perde o bolsão e ganha uma janela própria: a tomada fica numa moldura preta 1,5 mm acima da verde, com chanfro, rente à face. Fica bem à mostra, presa por 2 parafusos aparentes, e o desenho das asas continua igual.'),
                   (axs[1],2,'B2b — Tomada num recorte da asa','A asa da direita termina antes da tomada: a tomada fica no preto da placa, na face, num painel de conexões entre a asa e a cantoneira. É o destaque maior, porque a tomada vira parte do desenho.')):
    V(ax,var); ax.set_xlim(-300,300); ax.set_ylim(-2,100); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(t+'   (vista de trás)',fontsize=12,loc='left',fontweight='bold'); ax.text(-298,-8,n,fontsize=9,va='top',wrap=True)
plt.tight_layout(h_pad=3.5); plt.savefig('tras_base_b2.png',dpi=105,facecolor='#e9ebe6'); print('ok')

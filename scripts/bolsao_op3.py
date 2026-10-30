exec(open('faixa_versoes.py').read().split('# ---------------- versoes')[0])
src=open('faixa_versoes.py').read()
exec(src[src.index('# ---------------- desenho'):src.index('def painel')])
fit.__defaults__=(6.0,4.0)
sup=fit(sbox(0,47,250,66),[v3,cF],3.0)
def wing(hexb):
    w=fit(sbox(70,2,250,60),[v3,cF,sup],6.0)
    return w.difference(bf(hexb,0))
ilha_min=bf(jan,1.0)    # ilha precisa passar 1 mm alem da janela
# A: aberto embaixo
hA=hexa(101,170,-6,36.5,r=5.0); wA=wing(hA)
# B: fechado, faixa fina embaixo
hB=hexa(101,170,4.0,36.5,r=5.0); wB=wing(hB)
fig,axs=plt.subplots(2,2,figsize=(13,7.2),gridspec_kw=dict(height_ratios=[1,1]))
for col,(t,w,h) in enumerate((('C — asa mais alta, bolsão aberto embaixo (recomendo)',wA,hA),('D — asa mais alta, bolsão fechado (faixa de 2 mm embaixo)',wB,hB))):
  for row in (0,1):
    ax=axs[row][col]
    pp(ax,sbox(40,-10,262,81),'#e9ebe6','none',0,-1)
    pp(ax,sbox(40,2,262,81),'#26292c','#000',0.6,0); pp(ax,cF,'#1b1d1f','#000',0.8,3)
    pp(ax,v3,'#3aa857'); pp(ax,sup,'#2f9449'); pp(ax,w,'#45b862')
    pp(ax,bf(h,-0.5).intersection(sbox(0,2,300,90)),'#1a1c1e','#000',0.6,3); tomada(ax,1)
    if row==0: ax.set_xlim(60,255); ax.set_ylim(-1,70); ax.set_title(t,fontsize=11,loc='left',fontweight='bold')
    else:
        ax.set_xlim(95,177); ax.set_ylim(-9,22); ax.set_title('zoom na borda de baixo',fontsize=9,loc='left')
        ax.text(176,-1.0,'borda de baixo da lateral',ha='right',fontsize=8.5,color='#333')
        if col==0: ax.annotate('sem verde aqui: o bolsão preto vai até a borda',xy=(136,2.6),xytext=(98,-7.5),fontsize=9.5,color='#111',ha='left',arrowprops=dict(arrowstyle='->',color='#111'))
        else: ax.annotate('tira verde de só 2 mm por baixo do bolsão',xy=(136,3.0),xytext=(98,-7.5),fontsize=9.5,color='#111',ha='left',arrowprops=dict(arrowstyle='->',color='#111'))
    ax.set_aspect('equal'); ax.axis('off')
plt.tight_layout(); plt.savefig('bolsao_op3.png',dpi=120,facecolor='#e9ebe6')

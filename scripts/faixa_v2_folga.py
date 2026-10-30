exec(open('faixa_versoes.py').read().split('# ---------------- versoes')[0])
src=open('faixa_versoes.py').read()
exec(src[src.index('def V2'):src.index('def V3')])
exec(src[src.index('# ---------------- desenho'):src.index('for i,(tit,fn)')])
fig,axs=plt.subplots(3,1,figsize=(13,8.2))
for ax,g in zip(axs,(1.0,2.5,4.0)):
    fit.__defaults__=(6.0,g); D=V2(); painel(ax,D,'E'); ax.set_title('Folga entre as peças: %.1f mm'%g+('  (hoje)' if g==1.0 else ''),fontsize=11,loc='left',fontweight='bold')
plt.tight_layout(); plt.savefig('faixa_v2_folgas.png',dpi=120,facecolor='#e9ebe6')

import sys,os,json,collections
from pathlib import Path
K=sys.argv[1]; sys.path.insert(0,K); os.chdir(K)
from tools.building_stats import read_header
M=Path("C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/maps/Muldraugh, KY")
out=[]
for cab in sorted(M.glob("*.lotheader")):
    cx,cy=map(int,cab.stem.split("_"))
    n,lo,hi,rooms,predios=read_header(str(cab))
    for i,ids in enumerate(predios):
        rs=[rooms[k] for k in ids if 0<=k<len(rooms)]
        if not rs: continue
        xs=[x for _n,_l,rc in rs for x,_y,w,_h in rc for x in (x,x+w)]
        ys=[y for _n,_l,rc in rs for _x,y,_w,h in rc for y in (y,y+h)]
        out.append({"cel":cab.stem,"i":i,"w":max(xs)-min(xs),"h":max(ys)-min(ys),
          "niv":sorted({l for _n,l,_r in rs if l>=0}),"c":sorted({r[0] for r in rs})})
json.dump(out,open(sys.argv[2],"w"))
print(len(out))

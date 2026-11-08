import sys,os,subprocess
from pathlib import Path
K,S=sys.argv[1],sys.argv[2]
sys.path.insert(0,K); os.chdir(K)
from tools.building_stats import read_header
from PIL import Image,ImageDraw
M="C:/Program Files (x86)/Steam/steamapps/common/ProjectZomboid/media/maps/Muldraugh, KY"
L=[("hospital","8_23",6),("school","19_30",1),("church","43_26",3),("mechanic","21_23",2),("restaurant","50_6",12),("pub","25_20",35),("cafe","49_7",34),("bank","52_5",2),("bakery","49_4",16),("clothes","9_54",31),("hardware","54_12",28),("books","49_7",3),("alcohol","51_11",12),("butcher","48_12",28),
("CTRL farmacia W","46_26",32),("CTRL armas W","14_33",3),("CTRL mercado S","52_8",191)]
cells=[]
for nome,cel,i in L:
    cx,cy=map(int,cel.split("_"))
    n,lo,hi,rooms,predios=read_header(str(Path(M)/f"{cel}.lotheader"))
    rs=[rooms[k] for k in predios[i]]
    x0=min(x for _n,_l,rc in rs for x,_y,w,_h in rc)+cx*256; y0=min(y for _n,_l,rc in rs for _x,y,_w,_h in rc)+cy*256
    x1=max(x+w for _n,_l,rc in rs for x,_y,w,_h in rc)+cx*256; y1=max(y+h for _n,_l,rc in rs for _x,y,_w,h in rc)+cy*256
    out=f"{S}/f_{nome.split()[0]}_{cel}_{i}.png"
    subprocess.run([sys.executable,"-I","-X","utf8","tools/render_lots.py",M,out,str(x0-4),str(y0-4),str(x1-x0+8),str(y1-y0+8),"--world","--max-level","0","--scale","0.5"],capture_output=True)
    im=Image.open(out).convert("RGB")
    bb=im.point(lambda p:255 if p>30 else 0).convert("L").getbbox()
    im=im.crop(bb); im.thumbnail((470,300))
    c=Image.new("RGB",(480,330),(20,20,20)); c.paste(im,(5,28))
    ImageDraw.Draw(c).text((6,6),f"{nome} {cel}:{i} {x1-x0}x{y1-y0}",fill=(255,255,0))
    cells.append(c)
cols=4; rows=(len(cells)+cols-1)//cols
sheet=Image.new("RGB",(cols*480,rows*330))
for k,c in enumerate(cells): sheet.paste(c,((k%cols)*480,(k//cols)*330))
sheet.save(f"{S}/folha.png"); print(sheet.size)

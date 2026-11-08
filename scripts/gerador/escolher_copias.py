import json,sys
d=json.load(open(sys.argv[1]))
TIPOS={ # nome: (principais, w_max, h_max, area alvo)
 "hospital":({"hospitalroom","medclinic","clinic","medicaloffice"},26,26,250),
 "school":({"classroom","elementaryclassroom","secondaryclassroom"},30,30,300),
 "church":({"church"},24,30,250),
 "mechanic":({"mechanic"},24,24,200),
 "restaurant":({"restaurantdining","restaurantkitchen"},22,22,200),
 "pub":({"bar"},20,20,150),
 "cafe":({"cafe"},18,18,120),
 "bank":({"bank"},20,20,180),
 "bakery":({"bakery"},18,18,130),
 "clothes":({"clothesstore"},20,20,150),
 "hardware":({"toolstore"},22,22,180),
 "electronics":({"electronicsstore"},20,20,150),
 "books":({"bookstore"},20,20,150),
 "alcohol":({"liquorstore"},18,18,120),
 "butcher":({"butcher"},18,18,120),
}
PROIB={"livingroom","kidsbedroom","diningroom","garagestorage","laundry","garage","barn","closet","derelict"}
out={}
for t,(main,wm,hm,alvo) in TIPOS.items():
    c=[]
    for b in d:
        cs=set(b["c"])
        if not cs&main or cs&PROIB: continue
        if "bedroom" in cs and t not in("hospital","school"): continue
        if b["w"]>wm or b["h"]>hm or b["w"]<7 or b["h"]<7 or len(b["niv"])>3: continue
        if len([x for x in cs if x not in("emptyoutside","empty")])<2: continue
        c.append(b)
    c.sort(key=lambda b:abs(b["w"]*b["h"]-alvo))
    out[t]=c[:3]
    print(t,len(c),[ (b["cel"],b["i"],b["w"],b["h"],len(b["niv"])) for b in c[:3]])
json.dump(out,open(sys.argv[2],"w"))

import csv, math, re
from decimal import Decimal as D, ROUND_HALF_UP
q=lambda x: D(x).quantize(D('0.01'),rounding=ROUND_HALF_UP)

# Canadian vaping excise, rate in force since 1 Jul 2025: $1.12 per 2 mL for the first 10 mL,
# then $1.12 per 10 mL. Ontario is in the coordinated regime, so the provincial duty equals the federal.
def fed_excise(ml):
    return D('1.12')*(math.ceil(min(ml,10)/2) + math.ceil(max(ml-10,0)/10))
def excise(ml): return fed_excise(ml)*2

# (brand, line, flavour, mL, pack, carton price on the invoice, price includes excise?, source)
R=[]
def add(brand,line,fl,ml,pack,ctn,incl,src):
    for f in fl: R.append(dict(brand=brand,line=line,flavour=f,ml=ml,pack=pack,ctn=D(ctn),incl=incl,src=src))

# --- Order 1 (STLTH wholesaler, excise billed as separate lines) -----------------------
add('STLTH','ECO 6mL',['Strawberry Banana','Razz Apple Ice','Juicy Peach','Razzy Grape Ice','Cherry Lemon Ice','Peach Ice','Strawberry Kiwi Ice','Polar Mint'],6,6,'40.50',False,'Order 1')
add('ELFBAR','FS70K 20mL',['Strawberry Banana Ice','Kiwi Passion Fruit Guava Ice'],20,4,'39.96',False,'Order 1')
add('STLTH','ECO MINI 2mL',['Strawberry Kiwi Ice','Blue Razz Ice'],2,6,'24.60',False,'Order 1')
add('STLTH','LOOP MAX 70K Pod 30mL',['Green Apple Ice','Peach Berry','Blue Razz'],30,4,'31.36',False,'Order 1')
# --- Pinnacle 19583 (12 Aug) — HST only on the invoice, so the rate already carries excise --------
add('STLTH','x GEEK BAR 80K 30mL',['Banana Burst Ice','Blue Razz','Mango Peach Ice','Purple Grape Ice'],30,4,'131.32',True,'Pinnacle 19583')
add('OVNS','Max 3K 2mL',['Strawberry Peach Mint','White Grape Ice','Peach Mango'],2,6,'85.50',True,'Pinnacle 19583')
add('OVNS','O2 2500 2mL',['(flavour not shown)'],2,10,'102.50',True,'Pinnacle 19583')
add('ELFBAR','GH20K 20mL',['Blue Razz Ice','Sour Blueberry Lemon','Strawberry Kiwi Ice'],20,5,'132.15',True,'Pinnacle 19583')
add('KRAVE','Pulse X 60K 20mL',['Cool Mint','Blue Razz Lemon Head'],20,3,'54.00',True,'Pinnacle 19583')
# --- Pinnacle 19825 (1 Sep) + its order confirmation -----------------------------------
add('OVNS','Max 3K 2mL',['Blue Razz Ice','Mexican Mango'],2,6,'85.50',True,'Pinnacle 19825')
add('OVNS','2500 2mL',['Dragon Fruit Blue Raspberry','Mint Ice'],2,10,'110.00',True,'Pinnacle 19825')
add('ELFBAR','GH20K 20mL',['Peach Mango Watermelon','Grape Ice','Watermelon Ice'],20,5,'132.15',True,'Pinnacle 19825')
add('STLTH','2% Pod Pack (3 pods)',['Double Mint','Frost Mint','Honeydew Menthol','Peach','Tobacco Blend','Berry Blast'],6,1,'14.22',True,'Pinnacle 19825')
# --- Flavour Beast / Level X order, 26 Aug (prices shown with excise included) -----------
add('LEVEL X','M Series Device Kit',['Obsidian Black'],0,4,'32.36',True,'FB order 26 Aug')
add('FLAVOUR BEAST','Beast Mode Max 2 20mL',['Mega Mango','Gushin Watermelon Apple'],20,5,'149.65',True,'FB order 26 Aug')
add('LEVEL X','Boost Pod 20mL',['Mad Mango Peach','Strawberry Raspberry Blueberry Ice','Watermelon Strawberry Kiwi Ice','Super Sour Apple Iced'],20,6,'131.58',True,'FB order 26 Aug')
add('LEVEL X','M Series Starter Kit 30mL',['Bomb Blue Razz',"Flippin' Fruit Flash",'Gusto Green Apple',"Trippin' Triple Berry",'Weekend Watermelon Iced'],30,4,'127.48',True,'FB order 26 Aug')
# --- Order #1373225, 1 Sep (duty billed separately) -------------------------------------
add('ALLO','Ultra 10K 8mL',['Watermelon Ice'],8,6,'62.94',False,'Order 1373225')
add('ALLO','2500 8mL',['Watermelon Ice','Org Mango Guava'],8,5,'57.45',False,'Order 1373225')
add('ELFBAR','FS70K 20mL',['Pineapple Peach Mango Ice','Watermelon Ice','Miami Mint','Mango Ice','Banana Ice'],20,4,'39.96',False,'Order 1373225')
add("DRIP'N",'8mL',['Mango Peach Watermelon','Triple Berry'],8,5,'49.95',False,'Order 1373225')
add('STLTH','ECO MINI 2mL',['Razzy Grape Ice','Juicy Peach','Green Apple'],2,6,'24.60',False,'Order 1373225')
add('STLTH','LOOP 25K Pod 20mL',['Strawberry Lime Ice','Rich Tobacco'],20,5,'40.00',False,'Order 1373225')
add('STLTH','LOOP MAX 70K Pod 30mL',['Strawberry Kiwi','Green Apple Ice'],30,4,'37.65',False,'Order 1373225')
add('FLAVOUR BEAST','Beast Mode Max 2 20mL',['Watermelon G'],20,5,'82.45',False,'Order 1373225')

# --- Big Smoke Distro #9007 (25 Aug) and #9160 (2 Sep): duty itemised per line -----------
add('ELFBAR','GH20K 20mL',['Ice Mint'],20,5,'64.95',False,'Big Smoke 9007')
add('OVNS','2500 2mL',['Blood Orange Ice','Blue Blast','Mango Twist'],2,10,'92.60',False,'Big Smoke 9007')
add('STLTH','LOOP 25K Pod 20mL',['Rich Tobacco'],20,5,'40.00',False,'Big Smoke 9007')
add('STLTH','x GEEK BAR 80K 30mL',['Banana Burst Ice','Blue Razz','Juicy Peach','Wild Watermelon Ice','Canada LE Strawberry Kiwi Ice'],30,4,'68.60',False,'Big Smoke 9007')
add('ALLO','2500 8mL',['Org Mango Guava'],8,5,'57.45',False,'Big Smoke 9160')
add('ALLO','Ultra 10K 8mL',['Watermelon Ice'],8,6,'59.79',False,'Big Smoke 9160')
add('FLAVOUR BEAST','Beast Mode Max 2 20mL',['Watermelon G'],20,5,'82.45',False,'Big Smoke 9160')
add("DRIP'N",'8mL',['Mango Peach Watermelon','Triple Berry'],8,5,'49.95',False,'Big Smoke 9160')
add('ELFBAR','FS70K 20mL',['Banana Ice','Mango Ice','Miami Mint','Pineapple Peach Mango Ice','Watermelon Ice'],20,4,'37.96',False,'Big Smoke 9160')
add('STLTH','ECO MINI 2mL',['Green Apple','Juicy Peach','Razzy Grape Ice'],2,6,'23.37',False,'Big Smoke 9160')
add('STLTH','LOOP 25K Pod 20mL',['Rich Tobacco','Strawberry Lime Ice'],20,5,'38.00',False,'Big Smoke 9160')
add('STLTH','LOOP MAX 70K Pod 30mL',['Green Apple Ice'],30,4,'37.24',False,'Big Smoke 9160')

# prove the model on the two Big Smoke invoices as well
bs1 = 5*fed_excise(20) + 3*10*fed_excise(2) + 5*fed_excise(20) + 5*4*fed_excise(30)
bs2 = 5*fed_excise(8) + 6*fed_excise(8) + 5*fed_excise(20) + 2*5*fed_excise(8) + 5*4*fed_excise(20) + 3*6*fed_excise(2) + 2*5*fed_excise(20) + 4*fed_excise(30)
print(f"Big Smoke 9007 federal duty: model {bs1} vs invoice 257.60  {'OK' if bs1==D('257.60') else 'MISMATCH'}")
print(f"Big Smoke 9160 federal duty: model {bs2} vs invoice 380.80  {'OK' if bs2==D('380.80') else 'MISMATCH'}")

# ---- prove the excise model against the receipts before using it -----------------------
o1 = 8*6*fed_excise(6) + 2*4*fed_excise(20) + 2*6*fed_excise(2) + 3*4*fed_excise(30)
o4 = 6*fed_excise(8) + 2*5*fed_excise(8) + 6*4*fed_excise(20) + 2*5*fed_excise(8) + 3*6*fed_excise(2) + 2*5*fed_excise(20) + 2*4*fed_excise(30) + 5*fed_excise(20)
print(f"Order 1 federal excise: model {o1} vs receipt 322.56  {'OK' if o1==D('322.56') else 'MISMATCH'}")
print(f"Order 1373225 federal duty: model {o4} vs receipt 461.44  {'OK' if o4==D('461.44') else 'MISMATCH'}")
fb = 5*fed_excise(20)
print(f"Beast Mode Max 2 carton: model {fb} vs receipt 'federal tax included' 33.60  {'OK' if fb==D('33.60') else 'MISMATCH'}")

# ---- cost per unit / carton, excise-inclusive, HST-exclusive --------------------------
for r in R:
    ex = excise(r['ml']) if r['ml'] else D(0)
    r['excise_unit']=ex
    if r['incl']:
        r['ctn_incl']=r['ctn']; r['ctn_excl']=r['ctn']-ex*r['pack']
    else:
        r['ctn_excl']=r['ctn']; r['ctn_incl']=r['ctn']+ex*r['pack']
    r['unit_incl']=q(r['ctn_incl']/r['pack'])
    r['unit_excl']=q(r['ctn_excl']/r['pack'])
    r['name']=f"{r['brand']} {r['line']} {r['flavour']}".replace(' (flavour not shown)','')

# dedupe: same product bought twice -> keep the most recent price, note the other
order={'Pinnacle 19583':1,'Big Smoke 9007':2,'FB order 26 Aug':3,'Order 1':4,'Pinnacle 19825':5,'Order 1373225':6,'Big Smoke 9160':7}
seen={}
for r in sorted(R,key=lambda r:order[r['src']]):
    k=r['name'].lower()
    if k in seen and seen[k]['unit_incl']!=r['unit_incl']:
        r['note']=f"also {seen[k]['unit_incl']}/unit on {seen[k]['src']}"
    seen[k]=r
P=list(seen.values())
P.sort(key=lambda r:(r['brand'],r['line'],r['flavour']))
print(f"\ndistinct products: {len(P)}   (from {len(R)} order lines)")

# ---- known barcodes (public search hits) ---------------------------------------------
KNOWN={
 'elfbar gh20k 20ml peach mango watermelon':'641961763513',
 'elfbar gh20k 20ml ice mint':'641961763544',
 'ovns 2500 2ml blood orange ice':'6937057518032',
 'ovns 2500 2ml blue blast':'6937057525825',
 'stlth x geek bar 80k 30ml banana burst ice':'691584124789',
 'stlth x geek bar 80k 30ml blue razz':'691584124796',
 'stlth x geek bar 80k 30ml juicy peach':'691584124864',
 'stlth x geek bar 80k 30ml wild watermelon ice':'691584125496',
 'stlth x geek bar 80k 30ml canada le strawberry kiwi ice':'691584151600',
 'allo 2500 8ml org mango guava':'827152105779',
 'allo ultra 10k 8ml watermelon ice':'641961819685',
 'flavour beast beast mode max 2 20ml watermelon g':'827152198368',
 "drip'n 8ml mango peach watermelon":'827152214761',
 "drip'n 8ml triple berry":'827152214808',
 'elfbar fs70k 20ml banana ice':'6941976245689',
 'elfbar fs70k 20ml mango ice':'6941976245924',
 'elfbar fs70k 20ml miami mint':'6941976246037',
 'elfbar fs70k 20ml pineapple peach mango ice':'6941976246068',
 'elfbar fs70k 20ml watermelon ice':'6941976246488',
 'stlth eco mini 2ml green apple':'691584144336',
 'stlth eco mini 2ml juicy peach':'691584144343',
 'stlth eco mini 2ml razzy grape ice':'691584144398',
}
BC_SOURCE='Big Smoke invoice'

# ---- master list ------------------------------------------------------------------------
with open('vape-products.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['Brand','Product Line','Flavour','mL','Pack Size','Invoice Carton Price','Price Includes Excise',
                'Excise Per Unit (Fed+ON)','Unit Cost ex-excise','Unit Cost incl excise','Carton Cost incl excise',
                'Suggested Retail (x1.45)','Barcode','Source','Note'])
    for r in P:
        sug = (q(r['unit_incl']*D('1.45')).quantize(D('1'))-D('0.01')) if r['ml'] else q(r['unit_incl']*D('1.45'))
        r['sug']=sug
        w.writerow([r['brand'],r['line'],r['flavour'],r['ml'] or '',r['pack'],f"{r['ctn']}",'yes' if r['incl'] else 'no',
                    f"{r['excise_unit']}",f"{r['unit_excl']}",f"{r['unit_incl']}",f"{q(r['ctn_incl'])}",f"{sug}",
                    KNOWN.get(r['name'].lower(),''),r['src'],r.get('note','')])

# ---- Epos import: single + carton line per product ---------------------------------------
ABBR=[('Strawberry','Straw'),('Watermelon','Wtrmln'),('Raspberry','Rasp'),('Blueberry','Blueb'),('Passion Fruit','Passion'),
      ('Pineapple','Pineap'),('FLAVOUR BEAST Beast Mode Max 2','FB Beast Mode Max2'),('LEVEL X M Series Starter Kit','LVLX M-Series Kit'),
      ('LEVEL X M Series Device Kit','LVLX M-Series Device'),('LEVEL X Boost','LVLX Boost'),('STLTH x GEEK BAR 80K','STLTH GeekBar 80K'),
      ('KRAVE Pulse X 60K','Krave PulseX 60K'),('Dragon Fruit Blue Raspberry','Dragonfruit BlueRasp'),('Blue Razz Lemon Head','BlueRazz LemonHead')]
def fit(base, suffix='', n=40):
    s=base
    for a,b in ABBR: s=s.replace(a,b)
    room=n-len(suffix)
    if len(s)>room:            # drop the mL token first, then trim the tail
        s2=re.sub(r' \d+mL','',s)
        s = s2 if len(s2)<=room else s2[:room].rstrip()
    return s+suffix
used=set()
def uniq(name):
    n=name; i=2
    while n in used: n=f"{name[:38]}{i}"; i+=1
    used.add(n); return n
rows=[]
for r in P:
    base=f"{r['brand']} {r['line'].replace(' Pod','').replace(' 2%','')} {r['flavour']}".replace(' (flavour not shown)','')
    cat='VAPE & CIGAR'
    rows.append([KNOWN.get(r['name'].lower(),''),uniq(fit(base)),base[:128],f"{r['unit_incl']}",f"{r['sug']}",'13.00',cat])
    if r['pack']>1:
        rows.append(['',uniq(fit(base,f" CTN{r['pack']}")),f"{base} - carton of {r['pack']}"[:128],f"{q(r['ctn_incl'])}",f"{q(r['sug']*r['pack'])}",'13.00',cat])
with open('vape-epos-import.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['Barcode','Product Name','Product Description','Cost Price','Selling Price','Tax Percentage','Category Name']); w.writerows(rows)
print(f"epos rows: {len(rows)}  (name >40 chars: {sum(1 for x in rows if len(x[1])>40)}, dup names: {len(rows)-len({x[1] for x in rows})})")

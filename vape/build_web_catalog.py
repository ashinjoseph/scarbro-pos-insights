import csv, re, collections
from decimal import Decimal as D, ROUND_HALF_UP
q=lambda x: D(x).quantize(D('0.01'),rounding=ROUND_HALF_UP)

rows=[]
for r in csv.reader(open('newvape_raw.csv')):
    rows.append(dict(barcode=r[0].strip(),raw=r[1].strip(),alias=r[2].strip(),cat=r[3].strip(),
                     price=D(r[4]),cost=D(r[5]),pid=int(r[6]),added=r[7]))

# ---- expand the till's abbreviations -------------------------------------------------
AB=[('STRWBRY','Strawberry'),('STRBRY','Strawberry'),('WTRMLN','Watermelon'),('WRTMLN','Watermelon'),
    ('BLUEBRY','Blueberry'),('RSPBRY','Raspberry'),('RSBRY','Raspberry'),('RASPBERRY','Raspberry'),
    ('DRGNFRT','Dragonfruit'),('DRGNFT','Dragonfruit'),('DRAGONFRUIT','Dragonfruit'),('PINAPL','Pineapple'),
    ('SPRMNT','Spearmint'),('SPRMINT','Spearmint'),('PSN FRT','Passion Fruit'),('GUVA','Guava'),
    ('CCNT','Coconut'),('LYCHEE','Lychee'),('LYCH','Lychee'),('CRNBRY','Cranberry'),('MNGO','Mango'),
    ('MANG','Mango'),('PCH','Peach'),('GRP','Grape'),('APL','Apple'),('LMN','Lemon'),('MNT','Mint'),
    ('BRY','Berry'),('BLST','Blast'),('SPR','Super'),('SOR','Sour'),('BLSSD','Blissed'),('EPIC','Epic'),
    ('GLEMNG','Gleaming'),('DUB','Double'),('MLN','Melon'),('BMB','Bomb'),('GRN','Green'),('FLVR LESS','Flavourless'),
    ('SMOTTH','Smooth'),('PMPDUP','Pumped Up'),('FRT','Fruit'),('RED B','Red Bull'),('PRFLD','Prefilled'),
    ('RSPBERRY','Raspberry'),('RASPBERRY','Raspberry'),('WTRMELN','Watermelon'),('PECH','Peach'),
    ('STRWBRY','Strawberry'),('SPRT','Spirit'),('SLAMMIN','Slammin'),('FLIPPIN','Flippin'),
    ('TRIPPIN','Trippin'),('MIXED','Mixed'),('ORNG','Orange'),('CLASSIC','Classic'),('FIZZ','Fizz')]
TYPO=[('JUICT','Juicy'),('PRACH','Peach'),('PRACHY PEACE','Peachy Peach'),('DOUBLR','Double'),
      ('MANGOI','Mango'),('NECTER','Nectar'),('FLIPPING','Flippin'),('BEAST MODZ','Beast Mode'),
      ('STLTH GEEKBAR','STLTH x Geek Bar'),('LEVELX','Level X'),('BST G2','Boost G2')]

def pretty(s):
    t=' '+s.upper()+' '
    for a,b in TYPO: t=t.replace(' '+a+' ',' '+b.upper()+' ')
    for a,b in sorted(AB,key=lambda x:-len(x[0])): t=re.sub(r'(?<= )'+re.escape(a)+r'(?= )',b.upper(),t)
    t=re.sub(r'\s+',' ',t).strip()
    out=[]
    for w in t.split():
        if w in ('STLTH','OVNS','ELFBAR','ALLO','X','G2','BC','PRO','K','M','LE'): out.append(w)
        elif re.match(r'^\d+K$',w) or re.match(r'^\d+$',w): out.append(w)
        else: out.append(w.capitalize())
    return ' '.join(out).replace('Stlth','STLTH').replace('Ovns','OVNS').replace('Elfbar','Elf Bar').replace('Allo','ALLO')

# ---- brand / line / flavour ----------------------------------------------------------
LINES=[('STLTH GEEKBAR 80K','STLTH','x Geek Bar 80K',30,'Disposable'),
 ('STLTH LOOP MAX POD 70K','STLTH','Loop Max 70K Pod',30,'Replacement Pod'),
 ('STLTH LOOP 25K POD','STLTH','Loop 25K Pod',20,'Replacement Pod'),
 ('STLTH LOOP3 DEVICE','STLTH','Loop 3 Device',0,'Device'),
 ('STLTH ECO MINI','STLTH','ECO Mini',2,'Disposable'),('STLTH ECO','STLTH','ECO',6,'Disposable'),
 ('OVNS MAX 3K','OVNS','Max 3K',2,'Disposable'),('OVNS 2500','OVNS','2500',2,'Disposable'),
 ('OVNS 50K','OVNS','50K',0,'Disposable'),('O2 2500','OVNS','O2 2500',2,'Disposable'),('O2 ','OVNS','O2 2500',2,'Disposable'),
 ('LEVELX BST G2','Level X','Boost G2 Pod 25K',20,'Replacement Pod'),
 ('LEVELX G2 ULTRA 50K','Level X','G2 Ultra 50K',20,'Disposable'),
 ('LEVELX G2 PRO DEVICE','Level X','G2 Pro Device',0,'Device'),('LEVELX G2 DEVICE','Level X','G2 Device',0,'Device'),
 ('LEVEL X M SERIES 120K','Level X','M Series 120K',30,'Disposable'),
 ('BEAST MODZ MAX 2','Flavour Beast','Beast Mode Max 2',20,'Disposable'),
 ('FLAVOUR BEAST 60K','Flavour Beast','60K',20,'Disposable'),
 ('ALLO ULTRA 10K PREFILLED','ALLO','Ultra 10K Prefilled Pod',8,'Replacement Pod'),
 ('ALLO ULTRA 10K POD','ALLO','Ultra 10K Pod',8,'Replacement Pod'),
 ('ALLO ULTRA 1K POD','ALLO','Ultra 10K Pod',8,'Replacement Pod'),
 ('ALLO ULTRA 2500','ALLO','Ultra 2500',8,'Disposable'),
 ("DRIP'N 16K","Drip'n",'16K',8,'Disposable'),
 ('AL FAKHER 75K','Al Fakher','75K',25,'Disposable'),('ALFAKHER 75K','Al Fakher','75K',25,'Disposable'),
 ('ELFBAR BC PRO','Elf Bar','BC Pro 80K',25,'Disposable'),('ELFBAR GH20K','Elf Bar','GH20K',20,'Disposable'),
 ('ELFBAR 70K','Elf Bar','FS70K',20,'Disposable'),
 ('PULSE X','Krave','Pulse X 60K',20,'Disposable'),
 ('BREEZE 6K','Breeze','6K',0,'Disposable'),('BREEZE 4K','Breeze','4K',0,'Disposable'),
 ('INFINITY LEAN','Infinity','Lean',0,'Disposable'),('VICE BOX 2','Vice','Box 2',0,'Disposable')]

for r in rows:
    u=r['raw'].upper()
    r['brand']=r['line']=''; r['ml']=0; r['type']='Disposable'; r['flavour']=''
    for pre,br,ln,ml,ty in LINES:
        if u.startswith(pre):
            r['brand'],r['line'],r['ml'],r['type']=br,ln,ml,ty
            fl=r['raw'][len(pre):].strip()
            fl=re.sub(r'^\d+K\b','',fl).strip()
            r['flavour']=pretty(fl) if fl else ''
            break
    r['name']=(f"{r['brand']} {r['line']} {r['flavour']}".strip() if r['brand'] else pretty(r['raw']))
    r['name']=re.sub(r'\s+',' ',r['name'])

# ---- supplier cost, matched on brand+line+flavour ------------------------------------
FAMILY=[('eco mini','ECOMINI'),('ecomini','ECOMINI'),('eco','ECO'),
 ('geek bar','GEEK80K'),('geekbar','GEEK80K'),
 ('loop max','LOOPMAX70K'),('loop 25k','LOOP25K'),
 ('gh20k','GH20K'),('fs70k','FS70K'),('70k','FS70K'),('bc pro','BCPRO'),
 ('max 3k','MAX3K'),('max3k','MAX3K'),('o2 2500','O2_2500'),('50k','OVNS50K'),('2500','2500'),
 ('boost','BOOST'),('m series starter','MSERIESKIT'),('m series device','MSERIESDEV'),('m series','MSERIES120K'),
 ('g2 ultra','G2ULTRA'),('g2 pro device','G2PRODEV'),('g2 device','G2DEV'),
 ('beast mode max 2','BEASTMAX2'),('60k','FB60K'),
 ('ultra 10k','ULTRA10K'),('ultra 2500','ULTRA2500'),
 ('16k','DRIPN8'),('8ml','DRIPN8'),('75k','ALF75K'),('pulse x','PULSEX'),('lean','LEAN'),('box 2','BOX2'),
 ('6k','BREEZE6K'),('4k','BREEZE4K'),('loop 3','LOOP3DEV'),('loop3','LOOP3DEV')]
STOP={'ice','iced','the','and'}
def fam(brand,line):
    b=re.sub(r'[^a-z0-9]','',brand.lower()).replace('flavourbeast','fb').replace('levelx','lvlx')
    l=' '+line.lower()+' '
    for pat,tag in FAMILY:
        if ' '+pat in l or l.strip().startswith(pat): return b+':'+tag
    return b+':'+re.sub(r'[^a-z0-9]','',line.lower())
def fl_key(f):
    w=[x for x in re.sub(r'[^a-z0-9 ]',' ',f.lower()).split() if x not in STOP]
    return ''.join(sorted(w))
sup={}
for r in csv.DictReader(open('vape-products.csv')):
    sup[(fam(r['Brand'],r['Product Line']),fl_key(r['Flavour']))]=r
matched=0
for r in rows:
    k=(fam(r['brand'],r['line']),fl_key(r['flavour']))
    s=sup.get(k) if r['flavour'] else None
    if s: r['supcost']=D(s['Unit Cost incl excise']); r['supsrc']=s['Source']; matched+=1
    else: r['supcost']=None; r['supsrc']=''

# ---- data-quality flags ---------------------------------------------------------------
namecount=collections.Counter(r['raw'].upper() for r in rows)
for r in rows:
    f=[]
    b=r['barcode']
    if ',' in b: f.append('MULTIPLE barcodes in one field - split into separate products')
    elif not b.isdigit(): f.append('barcode not numeric')
    elif len(b) not in (8,12,13,14): f.append(f'unusual barcode length ({len(b)})')
    if r['price']==0: f.append('no retail price')
    if not r['flavour'] and r['type']!='Device': f.append('flavour missing from the product name')
    if namecount[r['raw'].upper()]>1: f.append('duplicate product name')
    if not r['brand']: f.append('brand not recognised')
    r['flags']='; '.join(f)

# ---- write the catalogue ---------------------------------------------------------------
HST=D('1.13')
out=[r for r in rows if r['price']>0]
out.sort(key=lambda r:(r['brand'],r['line'],r['flavour']))
with open('vape-web-catalog.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['Barcode','SKU','Product Name','Brand','Product Line','Flavour','Type','Nicotine',
                'E-liquid (mL)','Price (ex tax)','Price (incl HST)','Supplier Cost','Margin %','Category','Added','Data Flags'])
    for r in out:
        cost=r['supcost']
        marg = f"{(r['price']-cost)/r['price']*100:.0f}" if cost and r['price'] else ''
        w.writerow([r['barcode'],f"YV-{r['pid']}",r['name'],r['brand'],r['line'],r['flavour'],r['type'],
                    '20 mg/mL' if r['type']!='Device' else '',
                    r['ml'] or '',f"{r['price']}",f"{q(r['price']*HST)}",f"{cost}" if cost else '',marg,
                    r['cat'],r['added'],r['flags']])
print(f"catalogue rows: {len(out)}  (excluded {len(rows)-len(out)} with no price)")
print(f"supplier cost matched on: {matched}")
print(f"rows with a data flag: {sum(1 for r in out if r['flags'])}")
print("\nflags:")
for fl,n in collections.Counter(x for r in out for x in r['flags'].split('; ') if x).most_common(): print(f"  {n:>3}  {fl}")
print("\nby brand:")
for b,n in collections.Counter(r['brand'] or '(unknown)' for r in out).most_common(): print(f"  {n:>3}  {b}")

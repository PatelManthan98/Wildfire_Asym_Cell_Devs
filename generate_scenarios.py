"""
generate_scenarios.py  —  Asymmetric Cell-DEVS Wildfire Scenario Generator
Outputs: scenarios/*.json only
"""
import json, os, math
import numpy as np
from scipy.ndimage import gaussian_filter

os.makedirs("scenarios", exist_ok=True)

WATER=0; GRASS=1; SHRUB=2; FOREST=3; URBAN=4

def cid(r,c): return f"r{r}_c{c}"

def wind_factor(dr, dc, spd, wdir):
    if spd==0: return 1.0
    east=dc; north=-dr
    ang=math.atan2(north,east)*180/math.pi
    diff=abs(ang-wdir)
    if diff>180: diff=360-diff
    return max(0.2, 1.0+(spd/30.0)*math.cos(math.radians(diff)))

def slope_factor(my_e, nbr_e, cell_m=500):
    diff=my_e-nbr_e; ts=abs(diff)/cell_m
    return (1.0+5.275*ts*ts) if diff<=0 else max(0.4,1.0-1.5*ts)

def build_scenario(grid, elev, moisture, wind_speed, wind_dir, temperature,
                   humidity, ffmc, ignition_prob, ignition_cells,
                   cell_size_m=500, name="scenario"):
    R,C=grid.shape
    MOORE=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    cells={}
    for r in range(R):
        for c in range(C):
            ft=int(grid[r,c]); elv=float(elev[r,c]); mst=float(moisture[r,c])
            state={"state":1,"fuel_type":ft,"elevation":round(elv,1),
                   "moisture":round(mst,3),"intensity":0.0,"burn_steps_remaining":0}
            nbhd={}
            if ft!=WATER:
                for dr,dc in MOORE:
                    nr,nc=r+dr,c+dc
                    if not(0<=nr<R and 0<=nc<C): continue
                    if int(grid[nr,nc])==WATER: continue
                    wf=wind_factor(dr,dc,wind_speed,wind_dir)
                    sf=slope_factor(elv,float(elev[nr,nc]),cell_size_m)
                    df=1.0 if(dr==0 or dc==0) else 0.707
                    vic=round(wf*sf*df,4)
                    if vic>0.05: nbhd[cid(nr,nc)]=vic
            cells[cid(r,c)]={"delay":"inertial","state":state,
                "config":{"ignition_prob":ignition_prob,"temperature":temperature,
                          "humidity":humidity,"ffmc":ffmc},"neighborhood":nbhd}
    for r,c in ignition_cells:
        if cid(r,c) in cells and cells[cid(r,c)]["state"]["fuel_type"]!=WATER:
            cells[cid(r,c)]["state"].update({"state":2,"intensity":0.9,"burn_steps_remaining":10})
        else:
            # find nearest non-water cell
            for dr in range(-3,4):
                for dc in range(-3,4):
                    nr,nc=r+dr,c+dc
                    k=cid(nr,nc)
                    if k in cells and cells[k]["state"]["fuel_type"]!=WATER:
                        cells[k]["state"].update({"state":2,"intensity":0.9,"burn_steps_remaining":10})
                        print(f"  Ignition moved to {k} (original was water)")
                        break
                else: continue
                break
    path=f"scenarios/{name}.json"
    with open(path,"w") as f: json.dump({"cells":cells},f,separators=(',',':'))
    print(f"  {path}  ({os.path.getsize(path)//1024}KB, {len(cells)} cells)")

# ── S1: Calm Forest ───────────────────────────────────────────────────────────
def s1(G=50):
    print("\n[1] Calm Forest")
    grid=np.full((G,G),FOREST,dtype=int)
    elev=np.full((G,G),400.0); mst=np.full((G,G),0.20)
    build_scenario(grid,elev,mst,0,0,22,40,85,0.25,[(G//2,G//2)],100,"scenario_calm")

# ── S2: Windy Grassland ───────────────────────────────────────────────────────
def s2(G=50):
    print("\n[2] Windy Grassland")
    grid=np.full((G,G),GRASS,dtype=int); grid[15:26,20:36]=SHRUB
    elev=np.full((G,G),300.0); mst=np.full((G,G),0.10); mst[15:26,20:36]=0.15
    build_scenario(grid,elev,mst,35,0,32,15,95,0.18,[(G//2,5)],100,"scenario_windy")

# ── S3: Firebreaks ────────────────────────────────────────────────────────────
def s3(G=50):
    print("\n[3] Firebreaks")
    grid=np.full((G,G),FOREST,dtype=int)
    grid[:,24:26]=WATER; grid[35:37,:]=WATER; grid[35:37,10:15]=FOREST
    elev=np.full((G,G),400.0); mst=np.full((G,G),0.28); mst[:,24:26]=1.0
    build_scenario(grid,elev,mst,10,0,26,30,90,0.22,[(25,10)],100,"scenario_firebreak")

# ── S4: Urban Interface ───────────────────────────────────────────────────────
def s4(G=50):
    print("\n[4] Urban Interface")
    grid=np.full((G,G),FOREST,dtype=int)
    grid[28:30,:]=WATER; grid[28:30,20:25]=FOREST; grid[30:,:]=URBAN
    elev=np.full((G,G),440.0); elev[30:,:]=415.0
    mst=np.full((G,G),0.20); mst[30:,:]=0.15
    build_scenario(grid,elev,mst,15,270,30,20,93,0.20,[(10,22)],100,"scenario_urban")

# ── S5: Fort McMurray 2016 ────────────────────────────────────────────────────
def s5(G=50):
    print("\n[5] Fort McMurray 2016")
    elev=np.zeros((G,G))
    for r in range(G):
        for c in range(G):
            base=280+(G-c)*5.2
            rc=8+r*0.55; dist=abs(c-rc)
            valley=max(0,45-dist*6)
            city=max(0,20-math.sqrt((r-12)**2+(c-30)**2)*2)
            elev[r,c]=base-valley-city
    elev=gaussian_filter(elev,2.5); elev=np.clip(elev,240,700)

    grid=np.full((G,G),FOREST,dtype=int)
    mst=np.full((G,G),0.18)
    for r in range(G):
        cc=int(8+r*0.55)
        for dc in range(-2,3):
            nc=cc+dc
            if 0<=nc<G:
                if abs(dc)<=1: grid[r,nc]=WATER; mst[r,nc]=1.0
                else: mst[r,nc]=0.60
    grid[24:27,25:]=WATER; mst[24:27,25:]=1.0
    grid[12:25,28:46]=URBAN; mst[12:25,28:46]=0.12
    grid[8:13,25:35]=URBAN;  mst[8:13,25:35]=0.14
    grid[35:,30:]=SHRUB; mst[35:,30:]=0.55
    grid[20:35,5:20]=GRASS; mst[20:35,5:20]=0.10

    # ignition at r20_c15 — confirmed grass cell, not on river
    build_scenario(grid,elev,mst,
        wind_speed=65, wind_dir=45,
        temperature=32, humidity=13, ffmc=97,
        ignition_prob=0.20,
        ignition_cells=[(20,15)],
        cell_size_m=1000,
        name="scenario_fortmcmurray")

print("=== Asymmetric Cell-DEVS Wildfire Scenario Generator ===")
s1(); s2(); s3(); s4(); s5()
print("\nDone. scenarios/ updated.")
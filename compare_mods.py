import os
import re

mod_dir = r'C:\SecondBreakfast\SERVER\mods'
files = [f for f in os.listdir(mod_dir) if f.lower().endswith('.jar')]

def normalize(name):
    name = name.strip()
    name = re.sub(r'\s*\[forge\]|\s*\[FORGE\]|\s*\[Forge\]|\s*\(FORGE\)', '', name, flags=re.I)
    name = re.sub(r'\.jar$', '', name, flags=re.I)
    name = re.sub(r'[-_ ]?\d+(?:\.\d+)*(?:[A-Za-z0-9\+\-_.]*)?$', '', name)
    name = re.sub(r'[^A-Za-z0-9]+', ' ', name).strip().lower()
    return name

current = {normalize(f): f for f in files}
text = '''
[forge]ctov-3.4.14.jar
azurelib-neo-1.20.1-3.1.10.jar
beautify-2.0.2.jar
born_in_chaos_[Forge]1.20.1_1.7.5.jar
borninconfiguration-3.2.1[FORGE].jar
bountiful_npc-forge-1.20.1-1.0.5.jar
bushierflowers-0.0.3-1.20.1.jar
collective-1.20.1-8.25.jar
companions-forge-1.20.1-1.2.3.jar
darkdoppelganger-9.8.2-1.20.1.jar
Darker Depths-1.20.1-2.1.4.jar
decorative_blocks-forge-1.20.1-4.1.3.jar
decorative_core-2.0705-forge-1.20.1.jar
Dungeon Now Loading-forge-1.20.1-2.2.jar
ecologics-forge-1.20.1-2.2.6.jar
floating_islands-1.4.9.jar
ftb-quests-forge-2001.4.22.jar
galosphere_spellbooks-1.1.2.jar
Galosphere-1.20.1-1.5.2-Forge.jar
irons_lib-1.20.1-1.1.0.jar
irons_spellbooks-1.20.1-3.16.0.jar
knightlib-forge-1.20.1-1.5.1.jar
L_Enders_Cataclysm-3.29.jar
legionary-1.0.1-forge-1.20.1.jar
letsdo-lilis_lucky_lures-forge-1.0.2.jar
Longwings-v0.9.5-1.20.1-Forge.jar
mighty_mail-forge-1.20.1-1.1.4.jar
moonlight-1.20-2.16.33-forge.jar
mythsandlegends-0.0.8.8.jar
orcish_depths 1.0.1.jar
Paraglider-forge-20.1.3.jar
riverredux-0.3.1.jar
savage_and_ravage-1.20.1-6.0.1.jar
sky_whale_ship-1.20.1.jar
soulslike-weaponry-1.4.6-1.20.1-forge.jar
spiral_tower_village-0.0.3.jar
subnauticraft-1.0.0-forge-1.20.1.jar
TaxDeepVillager+M.1.20.1+ForM.2.0.0.jar
TaxTreeGiant+M.1.20.1+ForM.2.2.0.jar
TheOuterEnd-1.0.13.jar
totw_additions-1.3.1-1.20.x-forge.jar
totw_modded-forge-1.20.1-1.0.6.jar
variantsandventures-forge-1.0.26+mc1.20.1.jar
wandering_orc-1.2.5-1.20.1.jar
yet_another_config_lib_v3-3.6.6+1.20.1-forge.jar
zombie_variants-forge-1.0.3-1.20.1.jar
'''
listed = [line.strip() for line in text.splitlines() if line.strip()]
listed_norm = {normalize(line): line for line in listed}
missing = [line for key,line in listed_norm.items() if key not in current]
extra = [v for key,v in current.items() if key not in listed_norm]
print('MISSING_FROM_CURRENT:')
print('\n'.join(missing))
print('---')
print('EXTRA_IN_CURRENT_NOT_IN_LIST:')
print('\n'.join(sorted(extra)))

import re
from pathlib import Path

paste_list = [
    '[forge]ctov-3.4.14.jar',
    'azurelib-neo-1.20.1-3.1.10.jar',
    'beautify-2.0.2.jar',
    'born_in_chaos_[Forge]1.20.1_1.7.5.jar',
    'borninconfiguration-3.2.1[FORGE].jar',
    'bountiful_npc-forge-1.20.1-1.0.5.jar',
    'bushierflowers-0.0.3-1.20.1.jar',
    'collective-1.20.1-8.25.jar',
    'companions-forge-1.20.1-1.2.3.jar',
    'darkdoppelganger-9.8.2-1.20.1.jar',
    'Darker Depths-1.20.1-2.1.4.jar',
    'decorative_blocks-forge-1.20.1-4.1.3.jar',
    'decorative_core-2.0705-forge-1.20.1.jar',
    'Dungeon Now Loading-forge-1.20.1-2.2.jar',
    'ecologics-forge-1.20.1-2.2.6.jar',
    'floating_islands-1.4.9.jar',
    'ftb-quests-forge-2001.4.22.jar',
    'galosphere_spellbooks-1.1.2.jar',
    'Galosphere-1.20.1-1.5.2-Forge.jar',
    'irons_lib-1.20.1-1.1.0.jar',
    'irons_spellbooks-1.20.1-3.16.0.jar',
    'knightlib-forge-1.20.1-1.5.1.jar',
    'L_Enders_Cataclysm-3.29.jar',
    'legionary-1.0.1-forge-1.20.1.jar',
    'letsdo-lilis_lucky_lures-forge-1.0.2.jar',
    'Longwings-v0.9.5-1.20.1-Forge.jar',
    'mighty_mail-forge-1.20.1-1.1.4.jar',
    'moonlight-1.20-2.16.33-forge.jar',
    'mythsandlegends-0.0.8.8.jar',
    'orcish_depths 1.0.1.jar',
    'Paraglider-forge-20.1.3.jar',
    'riverredux-0.3.1.jar',
    'savage_and_ravage-1.20.1-6.0.1.jar',
    'sky_whale_ship-1.20.1.jar',
    'soulslike-weaponry-1.4.6-1.20.1-forge.jar',
    'spiral_tower_village-0.0.3.jar',
    'subnauticraft-1.0.0-forge-1.20.1.jar',
    'TaxDeepVillager+M.1.20.1+ForM.2.0.0.jar',
    'TaxTreeGiant+M.1.20.1+ForM.2.2.0.jar',
    'TheOuterEnd-1.0.13.jar',
    'totw_additions-1.3.1-1.20.x-forge.jar',
    'totw_modded-forge-1.20.1-1.0.6.jar',
    'variantsandventures-forge-1.0.26+mc1.20.1.jar',
    'wandering_orc-1.2.5-1.20.1.jar',
    'yet_another_config_lib_v3-3.6.6+1.20.1-forge.jar',
    'zombie_variants-forge-1.0.3-1.20.1.jar',
    'aquamirae-forge-1.20.1-6.2.0.jar',
    'dynamic-fps-3.11.4+minecraft-1.20.0-forge.jar',
    'skillcloaks-1.20.1-1.2.4.1.jar',
    'WeatherRefind-forge-1.20.x-v1.4.jar',
]

lock_paths = [
    Path('SERVER/mods/mods.lock.txt'),
    Path('CLIENT/mods/mods.lock.txt')
]

pattern = re.compile(r'\s*(?:\[forge\]|\[FORGE\]|\[Forge\])?(.+?)(?:\.jar)?\s*$', re.I)


def normalize(name: str) -> str:
    name = name.strip()
    name = re.sub(r'\s*\[forge\]|\s*\[FORGE\]|\s*\[Forge\]|\s*\(FORGE\)', '', name, flags=re.I)
    name = re.sub(r'\.jar$', '', name, flags=re.I)
    name = re.sub(r'[-_ ]?\d+(?:\.\d+)*(?:[A-Za-z0-9\+\-_.]*)?$', '', name)
    return re.sub(r'[^A-Za-z0-9]+', ' ', name).strip().lower()

paste_norm = {normalize(n): n for n in paste_list}

modslock_norm = {}
for p in lock_paths:
    if not p.exists():
        print(f'WARNING: {p} not found')
        continue
    with p.open('r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            line = line.split()[-1] if ' ' in line else line
            n = normalize(line)
            if n:
                modslock_norm[n] = modslock_norm.get(n, []) + [f'{p}:{line}']

missing = [paste_norm[k] for k in sorted(paste_norm) if k not in modslock_norm]
match = [paste_norm[k] for k in sorted(paste_norm) if k in modslock_norm]

print('MATCHING ITEMS IN mods.lock:')
for k in match:
    print(k)
print('\nMISSING ITEMS FROM mods.lock:')
for k in missing:
    print(k)
print(f'\nTotal pasted items: {len(paste_norm)}')
print(f'Total matched in mods.lock: {len(match)}')
print(f'Total missing from mods.lock: {len(missing)}')

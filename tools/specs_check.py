#!/usr/bin/env python3
"""Valida especificacoes/data/specs.json antes de publicar.
- Todo texto traduzido precisa ter os MESMOS valores numéricos em PT, EN e ES.
- Mídias e formatos precisam de id e nome em PT; ids únicos.
- Lista campos sem tradução (aparecem em PT com † no site) e pendências de validação.
Uso: python3 tools/specs_check.py
"""
import json, re, sys, pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'especificacoes' / 'data' / 'specs.json'
data = json.loads(P.read_text(encoding='utf-8'))
def nums(s):
    s = re.sub(r'(\d)[.,](\d{3})(?!\d)', r'\1\2', str(s or ''))
    s = re.sub(r'(\d),(\d)', r'\1.\2', s)
    return sorted(re.findall(r'\d+(?:\.\d+)?', s))
errors, missing, pending = [], [], []
def walk(o, path):
    if isinstance(o, dict) and {'pt', 'en', 'es'} & set(o):
        pt = o.get('pt') or ''
        if 'pendente de validação' in pt: pending.append(path)
        for l in ('en', 'es'):
            v = o.get(l) or ''
            if pt and not v.strip(): missing.append(f'{path} [{l}]')
            elif pt and nums(pt) != nums(v): errors.append(f'{path}: números diferentes entre PT e {l.upper()}\n    PT: {pt}\n    {l.upper()}: {v}')
        return
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f'{path}[{i}]')
ids = [m.get('id') for m in data['media']]
if len(ids) != len(set(ids)): errors.append('ids de mídia repetidos')
for m in data['media']:
    if not re.fullmatch(r'[a-z0-9-]+', m.get('id', '')): errors.append(f"id inválido: {m.get('id')}")
    if not (m.get('names') or {}).get('pt'): errors.append(f"{m['id']}: sem nome em PT")
    if not m.get('version') or not m.get('updated'): errors.append(f"{m['id']}: sem versão/data")
    fids = [f.get('id') for f in m.get('formats', [])]
    if not fids: errors.append(f"{m['id']}: sem formatos")
    if len(fids) != len(set(fids)): errors.append(f"{m['id']}: ids de formato repetidos")
    walk(m, m['id'])
print(f"{len(data['media'])} mídias · {sum(len(m['formats']) for m in data['media'])} formatos · base v{data['library']['version']}")
print(f"Pendências de validação: {len(pending)}")
for p in pending: print('  -', p)
print(f"Campos sem tradução (exibidos em PT com †): {len(missing)}")
for p in missing[:50]: print('  -', p)
if errors:
    print(f"\nERROS ({len(errors)}) — corrija antes de publicar:")
    for e in errors: print('  -', e)
    sys.exit(1)
print('\nOK: pronto para publicar.')

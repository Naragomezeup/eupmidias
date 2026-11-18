"""Gera a versão em espanhol do Media Kit (es.html + data/kit.es.json) a partir da versão em português.

Uso: python3 tools/build_es.py
- Traduções de conteúdo: tools/es_map.json (texto PT -> texto ES).
- Textos fixos da interface: lista UI abaixo.
Textos em português sem tradução são listados no final para serem incluídos no mapa.
"""
import json, re, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
MAP = json.load(open(P('tools', 'es_map.json'), encoding='utf-8'))
SKIP = {'id','frente','status','atualizadoEm','paginasOrigem','src','logo','cor','tipo','arte','whatsappLink','qr','versao','imagem','email','whatsapp','site','social','fontes','produtos'}
missing = []

def tr(o, k=None):
    if isinstance(o, dict):
        return {kk: (v if kk in SKIP and not isinstance(v, (dict, list)) else tr(v, kk)) for kk, v in o.items()}
    if isinstance(o, list):
        return [tr(v, k) for v in o]
    if isinstance(o, str):
        if o.startswith('assets/') or not re.search('[A-Za-zÀ-ú]', o):
            return o
        if o in MAP:
            return MAP[o]
        if re.search('[ãõçáéíóúâêôÁÉÍÓÚÇ]', o):
            missing.append(o)
        return o
    return o

kit = json.load(open(P('data', 'kit.json'), encoding='utf-8'))
funil = kit.get('funil')
es = tr(kit)
if funil:  # ids dos produtos no funil não são traduzidos
    for e_en, e_pt in zip(es['funil']['etapas'], funil['etapas']):
        e_en['produtos'] = [({'id': x['id'], 'rotulo': MAP.get(x['rotulo'], x['rotulo'])} if isinstance(x, dict) else x) for x in e_pt['produtos']]
es['meta']['idioma'] = 'es'
# Produtos que não rodam fora do Brasil: ficam inativos só na versão em inglês (e herdados pelo espanhol) (somem do menu, mandala e funil)
EN_INATIVOS = ['tnt-sports', 'globo', 'pluto-tv', 'webedia', 'telecom', 'canais-impacto', 'tinder', 'uber', 'dooh', 'ctv-cultura-asiatica']
# Ajustes exclusivos da versão em espanhol (18/11/2026)
ES_INATIVOS = EN_INATIVOS + ['netflix', 'prime-video', 'hbo-max', 'sync-experience', 'game-adz', 'chatgpt-ads']
for p in es['produtos']:
    if p['id'] in ES_INATIVOS:
        p['status'] = 'inativo'
# Versão ES: 19 soluções (em vez de 36+) e sem o logo da Pluto TV no ecossistema de CTV
es['quemSomos']['apresentacao'] = es['quemSomos']['apresentacao'].replace('Reunimos más de 36 soluciones', 'Reunimos 19 soluciones')
for n in es['numeros'].get('itens', es['numeros']) if isinstance(es['numeros'], dict) else es['numeros']:
    if isinstance(n, dict) and n.get('valor') == '36+':
        n['valor'] = '19'
def tira_pluto(o):
    if isinstance(o, dict):
        for v in o.values(): tira_pluto(v)
    elif isinstance(o, list):
        if 'assets/p/logo-plutotv.png' in o: o.remove('assets/p/logo-plutotv.png')
        for v in o: tira_pluto(v)
for p in es['produtos']:
    if p['id'] == 'ctv': tira_pluto(p)
json.dump(es, open(P('data', 'kit.es.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

UI = [
 ('<html lang="pt-BR">', '<html lang="es">'),
 ('data/kit.json', 'data/kit.es.json'),
 ('.s-capa .apoio{position:absolute;left:110px;top:788px;width:470px;font:700 33px/1.32 var(--f-body)', '.s-capa .apoio{position:absolute;left:110px;top:780px;width:600px;font:700 30px/1.3 var(--f-body)'),
 ('assets/logo-lockup.png', 'assets/logo-lockup-es.png'),
 ('assets/kv-miolo.webp', 'assets/kv-miolo-es.webp'),
 ('E.UP. Simplesmente diferente. Mais de 36 soluções de mídia em seis frentes de atuação.', 'E.UP. Simplemente diferente. 19 soluciones de medios en seis frentes de actuación.'),
 ('E.UP Mídias, ir para a capa', 'E.UP Mídias, ir a la portada'), ('aria-label="Páginas"', 'aria-label="Páginas"'),
 ('>Quem somos<', '>Quiénes somos<'), ('>Nosso jeito<', '>Nuestra forma<'), ('>Números<', '>Números<'), ('>Frentes<', '>Frentes<'), ('>Soluções<', '>Soluciones<'),
 ('>Baixar PDF<', '>Descargar PDF<'), ('>Fale com a E.UP<', '>Habla con E.UP<'), ('>Notas de revisão<', '>Notas de revisión<'),
 ('Gire o celular para ver as páginas maiores.', 'Gira el celular para ver las páginas más grandes.'), ('<b>Revisão:</b>', '<b>Revisión:</b>'),
 ('Não foi possível carregar os dados do media kit', 'No fue posible cargar los datos del media kit'),
 ('Conheça as seis frentes', 'Conoce los seis frentes'), ('alt="E.UP Mídias. Simplesmente diferente"', 'alt="E.UP Mídias. Simplemente diferente"'),
 ('<p class="neither">Simplesmente</p><p class="diff">diferente<span class="dot">.</span></p>', '<p class="neither">Simplemente</p><p class="diff">diferente<span class="dot">.</span></p>'),
 ('E.UP. Simplesmente <i>diferente.</i>', 'E.UP. Simplemente <i>diferente.</i>'),
 ('Nosso jeito de fazer', 'Nuestra forma de hacer'), ('Nossos números', 'Nuestros números'),
 ('Não pensamos em formatos. <span class="serif">Pensamos em possibilidades.</span>', 'No pensamos en formatos. <span class="serif">Pensamos en posibilidades.</span>'),
 ("'Conquistar é importante. Permanecer é outra história.'", "'Conquistar es importante. Permanecer es otra historia.'"),
 ('Seis frentes de atuação', 'Seis frentes de actuación'), ('Um ecossistema. <span class="serif">Seis caminhos.</span>', 'Un ecosistema. <span class="serif">Seis caminos.</span>'),
 ('Toque em uma frente para ver as soluções que fazem parte dela.', 'Toca un frente para ver las soluciones que forman parte de él.'),
 ('Mandala E.UP com as seis frentes de atuação', 'Mandala E.UP con los seis frentes de actuación'),
 ('Menu de soluções', 'Menú de soluciones'), ('Explore soluções por <span class="serif">desafio, contexto e objetivo.</span>', 'Explora soluciones por <span class="serif">desafío, contexto y objetivo.</span>'),
 ('Vamos conversar?', '¿Hablamos?'), ('Site · redes', 'Sitio web · redes'),
 ('alt="QR code para o WhatsApp comercial da E.UP"', 'alt="Código QR para el WhatsApp comercial de E.UP"'),
 ("'Capa'", "'Portada'"), ("'Quem somos'", "'Quiénes somos'"), ("'Nosso jeito'", "'Nuestra forma'"), ("'Números'", "'Números'"), ("'Frentes'", "'Frentes'"), ("'Menu'", "'Menú'"),
 ("'Funil completo'", "'Embudo completo'"), ("'Contato'", "'Contacto'"), ('← Voltar ao menu', '← Volver al menú'),
 ('>Fonte: ', '>Fuente: '), ("' soluções\"", "' soluciones\""), ('36+ SOLUÇÕES', '19 SOLUCIONES'), ('>Frente de atuação<', '>Frente de actuación<'),
 ("' soluções'", "' soluciones'"), ("' disponível'", "' disponible'"), ('>Ver<', '>Ver<'), ('>Em migração<', '>Próximamente<'),
 ('Preparando o PDF… na janela de impressão, escolha “Salvar como PDF”.', 'Preparando el PDF… en la ventana de impresión, elige “Guardar como PDF”.'),
 ('Não foi possível abrir a impressão neste navegador.', 'No fue posible abrir la impresión en este navegador.'),
 ('O download em PDF funciona no site: ', 'La descarga en PDF funciona en el sitio: '),
 ('Atualizado em ', 'Actualizado el '), ("'Versão '", "'Versión '"),
 ('<a href="en.html" class="lang" hreflang="en">EN</a><a href="es.html" class="lang" hreflang="es">ES</a>', '<a href="index.html" class="lang" hreflang="pt-BR">PT</a><a href="en.html" class="lang" hreflang="en">EN</a>'),
]
html = open(P('index.html'), encoding='utf-8').read()
for a, b in UI:
    html = html.replace(a, b)
open(P('es.html'), 'w', encoding='utf-8').write(html)
left = sorted(set(re.findall(r'>[^<>{}]*[ãõçáéíóúâêôÇ][^<>{}]*<', html)))
left = [x for x in left if 'Mídias' not in x]
print('es.html e data/kit.es.json gerados.')
if missing or left:
    print('Sem tradução:'); [print(' -', m) for m in dict.fromkeys(missing + left)]

"""Gera a versão em inglês do Media Kit (en.html + data/kit.en.json) a partir da versão em português.

Uso: python3 tools/build_en.py
- Traduções de conteúdo: tools/en_map.json (texto PT -> texto EN).
- Textos fixos da interface: lista UI abaixo.
Textos em português sem tradução são listados no final para serem incluídos no mapa.
"""
import json, re, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
MAP = json.load(open(P('tools', 'en_map.json'), encoding='utf-8'))
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
en = tr(kit)
if funil:  # ids dos produtos no funil não são traduzidos
    for e_en, e_pt in zip(en['funil']['etapas'], funil['etapas']):
        e_en['produtos'] = [({'id': x['id'], 'rotulo': MAP.get(x['rotulo'], x['rotulo'])} if isinstance(x, dict) else x) for x in e_pt['produtos']]
en['meta']['idioma'] = 'en'
# Produtos que não rodam fora do Brasil: ficam inativos só na versão em inglês (somem do menu, mandala e funil)
EN_INATIVOS = ['tnt-sports', 'globo', 'pluto-tv', 'webedia', 'telecom', 'canais-impacto', 'tinder', 'uber', 'dooh']
for p in en['produtos']:
    if p['id'] in EN_INATIVOS:
        p['status'] = 'inativo'
json.dump(en, open(P('data', 'kit.en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

UI = [
 ('<html lang="pt-BR">', '<html lang="en">'),
 ('data/kit.json', 'data/kit.en.json'),
 ('assets/logo-lockup.png', 'assets/logo-lockup-en.png'),
 ('assets/kv-miolo.webp', 'assets/kv-miolo-en.webp'),
 ('E.UP. Simplesmente diferente. Mais de 36 soluções de mídia em seis frentes de atuação.', 'E.UP. Simply different. More than 36 media solutions across six areas of expertise.'),
 ('E.UP Mídias, ir para a capa', 'E.UP Mídias, go to cover'), ('aria-label="Páginas"', 'aria-label="Pages"'),
 ('>Quem somos<', '>About us<'), ('>Nosso jeito<', '>Our way<'), ('>Números<', '>Numbers<'), ('>Frentes<', '>Areas<'), ('>Soluções<', '>Solutions<'),
 ('>Baixar PDF<', '>Download PDF<'), ('>Fale com a E.UP<', '>Talk to E.UP<'), ('>Notas de revisão<', '>Review notes<'),
 ('Gire o celular para ver as páginas maiores.', 'Turn your phone sideways to see larger pages.'), ('<b>Revisão:</b>', '<b>Review:</b>'),
 ('Não foi possível carregar os dados do media kit', 'Could not load the media kit data'),
 ('Conheça as seis frentes', 'See the six areas'), ('alt="E.UP Mídias. Simplesmente diferente"', 'alt="E.UP Mídias. Simply different"'),
 ('<p class="neither">Simplesmente</p><p class="diff">diferente<span class="dot">.</span></p>', '<p class="neither">Simply</p><p class="diff">different<span class="dot">.</span></p>'),
 ('E.UP. Simplesmente <i>diferente.</i>', 'E.UP. Simply <i>different.</i>'),
 ('Nosso jeito de fazer', 'Our way of working'), ('Nossos números', 'Our numbers'),
 ('Não pensamos em formatos. <span class="serif">Pensamos em possibilidades.</span>', "We don’t start with formats. <span class=\"serif\">We start with possibilities.</span>"),
 ("'Conquistar é importante. Permanecer é outra história.'", "'Winning clients matters. Keeping them is another story.'"),
 ('Seis frentes de atuação', 'Six areas of expertise'), ('Um ecossistema. <span class="serif">Seis caminhos.</span>', 'One ecosystem. <span class="serif">Six paths.</span>'),
 ('Toque em uma frente para ver as soluções que fazem parte dela.', 'Tap an area to see the solutions it includes.'),
 ('Mandala E.UP com as seis frentes de atuação', 'E.UP mandala with the six areas of expertise'),
 ('Menu de soluções', 'Solutions menu'), ('Explore soluções por <span class="serif">desafio, contexto e objetivo.</span>', 'Explore solutions by <span class="serif">challenge, context and objective.</span>'),
 ('Vamos conversar?', 'Let’s talk?'), ('Site · redes', 'Website · social'),
 ('alt="QR code para o WhatsApp comercial da E.UP"', 'alt="QR code for E.UP sales WhatsApp"'),
 ("'Capa'", "'Cover'"), ("'Quem somos'", "'About us'"), ("'Nosso jeito'", "'Our way'"), ("'Números'", "'Numbers'"), ("'Frentes'", "'Areas'"), ("'Menu'", "'Menu'"),
 ("'Funil completo'", "'Full funnel'"), ("'Contato'", "'Contact'"), ('← Voltar ao menu', '← Back to menu'),
 ('>Fonte: ', '>Source: '), ("' soluções\"", "' solutions\""), ('36+ SOLUÇÕES', '36+ SOLUTIONS'), ('>Frente de atuação<', '>Area of expertise<'),
 ("' soluções'", "' solutions'"), ("' disponível'", "' available'"), ('>Ver<', '>View<'), ('>Em migração<', '>Coming soon<'),
 ('Preparando o PDF… na janela de impressão, escolha “Salvar como PDF”.', 'Preparing the PDF… in the print window, choose “Save as PDF”.'),
 ('Não foi possível abrir a impressão neste navegador.', 'Could not open printing in this browser.'),
 ('O download em PDF funciona no site: ', 'PDF download works on the website: '),
 ('Atualizado em ', 'Updated on '), ("'Versão '", "'Version '"),
 ('<a href="en.html" class="lang" hreflang="en">EN</a><a href="es.html" class="lang" hreflang="es">ES</a>', '<a href="index.html" class="lang" hreflang="pt-BR">PT</a><a href="es.html" class="lang" hreflang="es">ES</a>'),
]
html = open(P('index.html'), encoding='utf-8').read()
for a, b in UI:
    html = html.replace(a, b)
open(P('en.html'), 'w', encoding='utf-8').write(html)
left = sorted(set(re.findall(r'>[^<>{}]*[ãõçáéíóúâêôÇ][^<>{}]*<', html)))
left = [x for x in left if 'Mídias' not in x]
print('en.html e data/kit.en.json gerados.')
if missing or left:
    print('Sem tradução:'); [print(' -', m) for m in dict.fromkeys(missing + left)]

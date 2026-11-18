# Media Kit E.UP — Simplesmente diferente

Site estático do Media Kit Digital da E.UP (páginas 16:9).

- `index.html` — motor de layout (não precisa ser editado para mudar conteúdo)
- `data/kit.json` — todo o conteúdo: institucional, frentes, produtos, funil e contato
- `assets/` — KV, logos e imagens

Publicação: Netlify conectado a este repositório. Cada commit na branch `main` publica automaticamente.
Sem etapa de build: diretório de publicação = raiz do repositório.

## Versão em inglês

- `en.html` + `data/kit.en.json` são **gerados** a partir da versão em português.
- Depois de qualquer alteração em `index.html` ou `data/kit.json`, rode `python3 tools/build_en.py`.
- Traduções de conteúdo ficam em `tools/en_map.json`; o script lista os textos que ainda não têm tradução.
- Endereços: `/` (português) e `/en.html` (inglês). O botão PT | EN no topo alterna mantendo a página atual.

## Versão em espanhol
`python3 tools/build_es.py` gera `es.html` e `data/kit.es.json` a partir da versão em português (traduções em `tools/es_map.json`).
Portfólio exclusivo do espanhol: mesmos produtos ocultos do inglês, mais Netflix, Prime Video, HBO Max, Sync Experience, Game Adz e ChatGPT Ads (lista `ES_INATIVOS`).
Sempre que `index.html` ou `data/kit.json` mudarem, rode os dois scripts (`build_en.py` e `build_es.py`).

## Especificações Técnicas
A Central de Especificações Técnicas fica em `especificacoes/` (endereço `/especificacoes/`). Veja `especificacoes/README.md`. Validação: `python3 tools/specs_check.py`.

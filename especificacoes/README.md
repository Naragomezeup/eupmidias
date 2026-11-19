# Central de Especificações Técnicas E/UP

Endereço público: https://midiakit.e-up.tech/especificacoes/

- `index.html` — interface (biblioteca, busca, filtros, PT | EN | ES, campanha e geração de PDFs no navegador). Não precisa ser editado para mudar especificações.
- `data/specs.json` — base oficial: mídias, formatos, especificações, tutoriais de acesso, versões e histórico de alterações (`log`).

Fontes: apresentação master "ESPECIFICAÇÕES TÉCNICAS 17.pdf" (12/11/2026) e ficha ChatGPT Ads (12/11/2026).

## Como atualizar (via Claude, no projeto ESPECIFICAÇÕES TECNICAS EUP)
1. Peça a alteração no chat. O Claude edita `data/specs.json` em PT, EN e ES, sobe a versão da mídia (ex.: 1.0 → 1.1), atualiza a data e registra a alteração no `log`.
2. Rascunho/revisão: o Claude mostra a mudança (e, se quiser, uma pré-visualização privada) antes de publicar.
3. Validação: `python3 tools/specs_check.py` — bloqueia a publicação se algum número divergir entre PT, EN e ES.
4. Publicação: commit na branch `main`; o Netlify publica em cerca de 1 minuto, no mesmo link.
5. Versões anteriores ficam no histórico do Git (cada commit) e podem ser recuperadas.

Regras: nunca inventar especificações; informação ausente = "Informação técnica pendente de validação"; não traduzir medidas, extensões e siglas.

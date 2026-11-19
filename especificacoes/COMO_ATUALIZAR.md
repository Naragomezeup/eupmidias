# Central de Especificações Técnicas E/UP — como atualizar

Guia para qualquer conversa do Claude no projeto "ESPECIFICAÇÕES TECNICAS EUP" que precise incluir, alterar, desativar ou recuperar produtos.

## Onde fica tudo
- Endereço público (único): https://midiakit.e-up.tech/especificacoes/
- Repositório GitHub: `Naragomezeup/eupmidias` (o mesmo do Media Kit), branch `main`. Cada commit na `main` publica sozinho no Netlify em ~1 minuto.
- Base oficial: `especificacoes/data/specs.json`. É o ÚNICO arquivo editado em atualizações de conteúdo.
- Interface: `especificacoes/index.html`. Não editar para mudar conteúdo.
- Validador: `python3 tools/specs_check.py` (raiz do repositório).

## Passo a passo
1. **Receber o pedido e a fonte.** A Nara envia o produto novo ou a mudança (PDF, print, texto). Se faltar alguma informação técnica, NÃO inventar: usar "Informação técnica pendente de validação" e avisar.
2. **Clonar o repositório**: anexar `Naragomezeup/eupmidias` com acesso de escrita e clonar (`git clone --depth 1`).
3. **Editar `specs.json`** seguindo o modelo abaixo, nos três idiomas (PT oficial, EN, ES).
4. **Versão e histórico** da mídia alterada:
   - Produto novo: `version` "1.0", `updated` = data de hoje (AAAA-MM-DD), `log` com uma entrada.
   - Alteração: subir a versão (1.0 → 1.1; mudança grande → 2.0), atualizar `updated` e acrescentar uma entrada no `log` (`{"date","version","note"}`).
   - Desativar produto: `"active": false` (some do site e dos PDFs, mas continua guardado), com entrada no `log`.
   - Nunca apagar produtos nem sobrescrever sem registrar no `log`. Versões anteriores ficam no histórico do Git e podem ser recuperadas.
5. **Validar**: `python3 tools/specs_check.py` precisa terminar com "OK: pronto para publicar". Ele bloqueia números diferentes entre PT, EN e ES.
6. **Revisão antes de publicar**: mostrar à Nara um resumo do que muda (produto, formatos, valores). Se ela quiser ver antes, gerar pré-visualização (testar localmente ou republicar o artefato privado de pré-visualização). Só publicar com o ok dela, a menos que ela já tenha pedido para publicar direto.
7. **Publicar**: commit na `main` com mensagem em português descrevendo a mudança, `git push`.
8. **Conferir**: abrir https://midiakit.e-up.tech/especificacoes/ e verificar o produto e o PDF.
9. **Atualizar** o documento do projeto `claude/EUP_Central_Especificacoes_Arquitetura.md` se mudar alguma regra ou a contagem de produtos.

## Modelo de produto (um item da lista `media`)
```json
{
  "id": "pinterest-ads",
  "name": "Pinterest Ads",
  "cat": "social",
  "order": 26,
  "names":   {"pt": "Pinterest Ads", "en": "Pinterest Ads", "es": "Pinterest Ads"},
  "tagline": {"pt": "Imagem e vídeo", "en": "Image and video", "es": "Imagen y video"},
  "keywords": "pinterest pins",
  "source":  {"pt": "Fonte enviada pela E/UP (dd/mm/aaaa)", "en": "Source provided by E/UP (mm/dd/yyyy)", "es": "Fuente enviada por E/UP (dd/mm/aaaa)"},
  "version": "1.0", "updated": "AAAA-MM-DD", "active": true,
  "log": [{"date": "AAAA-MM-DD", "version": "1.0", "note": "Produto incluído"}],
  "formats": [
    {
      "id": "pinterest-imagem",
      "name":  {"pt": "Imagem", "en": "Image", "es": "Imagen"},
      "intro": {"pt": "As peças precisam ser confeccionadas em uma das medidas-padrão a seguir.", "en": "Assets must be produced in one of the standard sizes below.", "es": "Las piezas deben producirse en una de las medidas estándar a continuación."},
      "specs": [
        [{"pt": "Proporção", "en": "Aspect ratio", "es": "Proporción"}, "2:3"],
        [{"pt": "Peso máximo", "en": "Maximum file size", "es": "Peso máximo"}, {"pt": "Até 20 MB", "en": "Up to 20 MB", "es": "Hasta 20 MB"}]
      ],
      "table": {"cols": [{"pt": "Dimensões", "en": "Dimensions", "es": "Dimensiones"}], "rows": [["1000x1500"]]},
      "notes": [{"pt": "...", "en": "...", "es": "..."}],
      "links": [{"label": {"pt": "...", "en": "...", "es": "..."}, "url": "https://..."}]
    }
  ],
  "general":   [{"title": {"pt": "...", "en": "...", "es": "..."}, "items": [{"pt": "...", "en": "...", "es": "..."}]}],
  "deadlines": [{"pt": "...", "en": "...", "es": "..."}],
  "notes":     [{"pt": "...", "en": "...", "es": "..."}],
  "pending":   [{"pt": "...", "en": "...", "es": "..."}],
  "links":     [{"label": {"pt": "...", "en": "...", "es": "..."}, "url": "https://..."}],
  "access":    {"title": {...}, "intro": {...}, "groups": [{"title": {...}, "items": [{...}]}], "links": [...]}
}
```
- Os valores acima do Pinterest são só exemplo de formato do arquivo, não especificações reais.
- Obrigatórios: `id`, `name`, `cat`, `order`, `names`, `tagline`, `keywords`, `source`, `version`, `updated`, `active`, `log`, `formats` (com `id`, `name` e `specs` e/ou `table`). O resto é opcional.
- `id` de produto e de formato: só letras minúsculas, números e hífens; únicos.
- Valor técnico igual nos três idiomas (ex.: "1920x1080") pode ser texto simples em vez de `{pt,en,es}`.
- Categorias (`cat`): display, video, audio, native, streaming, google, social, push, ai. Categoria nova: incluir em `categories` com nome nos três idiomas.
- `order` define a posição na biblioteca; reordenar os demais se necessário.
- E-mail que não deve aparecer direto na página: usar `{{email:BASE64}}` (vira botão "Mostrar e-mail"; nos PDFs aparece por extenso).
- `access`: tutorial "Como dar acesso à E/UP" (usado em Meta e TikTok).

## Regras da E/UP (obrigatórias)
1. Nunca inventar especificações. Ausente = "Informação técnica pendente de validação" (nos três idiomas: "Technical information pending validation" / "Información técnica pendiente de validación").
2. Nunca alterar valores numéricos, medidas, extensões, siglas ou nomes comerciais na tradução.
3. Cada produto é individual, sem pacotes (ex.: Display Programático, Drive to Store e Amazon DSP — Display são produtos separados).
4. Não usar "DV360" em nomes de produtos. Amazon pode ser nomeada.
5. Formatos de uma mesma plataforma ficam separados (o cliente escolhe formato a formato).
6. Banner companheiro nunca é formato separado: entra junto com a peça principal. Em áudio é obrigatório; no vídeo programático é altamente recomendado.
7. Não usar o Canva: tutoriais e materiais de apoio ficam dentro da Central.
8. Nada interno no site (notas internas, links de edição, observações de bastidor). O repositório é público.
9. Áudio Programático e Spotify e Plataformas de Áudio são produtos diferentes.

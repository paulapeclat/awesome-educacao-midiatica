# 🔔 Notificações e integração com o blog

As publicações diárias desta lista geram um **feed RSS**:

```
https://raw.githubusercontent.com/paulapeclat/awesome-educacao-midiatica/main/feed.xml
```

Cada item do feed é o recurso publicado no dia (título, link, descrição e seção). Tudo abaixo se conecta a esse feed.

---

## 1. Receber notificação de cada publicação

**Opção A — Leitor de RSS (1 minuto):** adicione a URL do feed no [Feedly](https://feedly.com), Inoreader ou no leitor que preferir. Nova publicação = notificação no app.

**Opção B — Por e-mail (2 minutos):** o [Blogtrottr](https://blogtrottr.com) transforma qualquer feed em e-mail — cole a URL do feed, informe seu e-mail e escolha a frequência "realtime".

**Opção C — n8n (para quem já usa, como eu 😉):** workflow de 2 nós:

1. **RSS Feed Read Trigger** — URL do feed acima, verificação a cada hora
2. **Gmail / Telegram / WhatsApp** — envia `{{ $json.title }}` + `{{ $json.link }}` para onde quiser

O mesmo fluxo pode ramificar para redes sociais (post automático no LinkedIn anunciando o recurso do dia, por exemplo).

## 2. Levar o conteúdo para o blog da APedê (WordPress)

**Opção A — Bloco RSS (zero código, 5 minutos):** no editor do WordPress, adicione o bloco **"RSS"** em qualquer página ou na lateral do blog e cole a URL do feed. O bloco exibe automaticamente os últimos recursos publicados, sempre atualizados.

**Opção B — Rascunho automático por dia (10 minutos, já embutido aqui):** o workflow deste repositório cria um **rascunho de post** no seu WordPress a cada publicação — você só revisa, adapta o texto à sua voz e publica. Para ativar:

1. No WordPress: **Usuários → Perfil → Senhas de aplicação** → crie uma senha chamada `github-publicador`
2. Neste repositório: **Settings → Secrets and variables → Actions → New repository secret**, criando três secrets:
   - `WP_URL` — endereço do site (ex.: `https://paulapeclat.com.br`)
   - `WP_USER` — seu usuário do WordPress
   - `WP_APP_PASSWORD` — a senha de aplicação gerada no passo 1
3. Pronto — no dia seguinte, junto com a publicação das 9h, aparece um rascunho no blog.

Enquanto os secrets não existirem, o passo é simplesmente pulado (o log avisa).

> 💡 Rascunho, não publicação direta: a revisão humana é proposital — o blog tem a sua voz, e conteúdo automático sem curadoria enfraqueceria justamente a credibilidade que a lista constrói.

**Opção C — Plugin agregador:** o [WP RSS Aggregator](https://wordpress.org/plugins/wp-rss-aggregator/) importa o feed como posts automaticamente, se preferir gerenciar pelo painel do WordPress.

## 3. Bônus: divulgar o recurso do dia nas redes

Com o feed + n8n, um nó extra publica o recurso do dia no LinkedIn ou agenda no Buffer. Sugestão de texto: *"📚 Recurso de educação midiática de hoje: {título} — {link}. Da minha lista curada, que cresce um recurso por dia: github.com/paulapeclat/awesome-educacao-midiatica"*.

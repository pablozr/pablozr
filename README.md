# Pablo Farina

**Desenvolvedor backend** · arquitetura, concorrência e verificação de coding agents  
Sistemas de Informação na UNIRIO · Rio de Janeiro

[LinkedIn](https://www.linkedin.com/in/pablo-de-araujo-farina-893a8126b) · [pablo.farina28@outlook.com](mailto:pablo.farina28@outlook.com) · [GitHub](https://github.com/pablozr)

## Sobre mim

Curso Sistemas de Informação na UNIRIO e hoje sou estagiário de desenvolvimento na **Bagaggio**, onde mais de 200 lojas dependem de ferramentas que eu desenvolvi ou ainda mantenho. Antes disso passei por freelance com Next.js e por jogos educativos na própria universidade.

O que me interessa de verdade é o que acontece quando dá errado: duas requisições chegando juntas no último item do estoque, um worker morrendo no meio do processamento, um agente de código mexendo em arquivo que ninguém pediu.

- **200+ lojas** usando sistemas internos que desenvolvi na Bagaggio
- **10+ projetos entregues**, do requisito ao deploy monitorado
- **605 commits** nos últimos 12 meses, em 21 repositórios

## Como eu penso

- **Concorrência.** O problema aparece quando duas pessoas tentam comprar o último item ao mesmo tempo, e a resposta não pode ser decidida depois: ou tem lock e transação explícita, ou o bug aparece em produção num sábado.
- **Domínio.** Cada regra de negócio fica perto de quem entende dela; espalhada pelo controller, ninguém consegue explicar. Mensageria entra pelo mesmo motivo: quem publica um evento não precisa conhecer quem escuta.
- **Verificação.** Agente escreve mais rápido do que eu consigo revisar, e prompt melhor não resolve isso. Foi por isso que o JevGuard começou.

Interesses: backend com FastAPI, async e arquitetura orientada a eventos · concorrência como invariante · verificação de diffs de agentes · pesquisa em embeddings e recuperação.

## Projetos em destaque

| Projeto | O que é | Stack |
| --- | --- | --- |
| [**JevGuard**](https://github.com/pablozr/JevGuard) | Motor de política semântica para coding agents. Verifica o diff que um agente acabou de produzir contra as políticas do repositório e devolve PASS, WARN ou FAIL por regra. | TypeScript · CLI |
| [**PRISMA**](https://github.com/pablozr/PRISMA) | Plataforma acadêmica da UNIRIO. Projetos importados do SIE, login institucional via Google, tokens em Redis e recomendação semântica na busca. | Python · FastAPI · Redis · RAG |
| [**self-checkout-monolith**](https://github.com/pablozr/self-checkout-monolith) | Autoatendimento por mesa. Carrinho anônimo em Redis, checkout Stripe idempotente, reset de senha assíncrono com worker SMTP e cache por produto. | FastAPI · Redis · RabbitMQ · Stripe |
| [**subscription-monolith**](https://github.com/pablozr/subscription-monolith) | Gestão de assinaturas. Regras separadas por domínio, persistência relacional e comunicação assíncrona entre os serviços. | FastAPI · PostgreSQL · RabbitMQ |
| [**FastAPI-Template**](https://github.com/pablozr/FastAPI-Template) | Base de API para produção. Organização modular, configuração por ambiente e docker-compose pronto para subir. | FastAPI · Docker · PostgreSQL |

Também no perfil: [angular-template](https://github.com/pablozr/angular-template), base Angular organizada por features.

## Stack

- **Backend:** Python, FastAPI, Java, Spring Boot, Go
- **Frontend:** Angular, TypeScript, React 19, Next.js 15 (Server Actions), Vite, JavaScript, Phaser
- **Dados e infra:** PostgreSQL, MongoDB, Redis, RabbitMQ, Docker
- **Integração:** APIs RESTful, integração com ERP, WebRTC, SSO
- **Qualidade:** testes unitários com Bun, documentação técnica

<sub>Linguagens por volume de código nos 42 repositórios públicos: TypeScript 49,8% · Python 20,7% · Java 8,4% · HTML 6,6% · SCSS 5,6% · JavaScript 4,3% · CSS 3,7%</sub>

## Formação

- **UNIRIO**, Bacharelado em Sistemas de Informação (2023–2027)
- **Idiomas:** português nativo, inglês C1
- **Liderança:** bolsista de extensão do Clube de Xadrez da UNIRIO; organizei torneios internos

<sub>close the world, open the nExt</sub>

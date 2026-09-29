<div align="center">

<img src="assets/header.svg" alt="Pablo Farina" width="100%" />

<br />

<a href="https://www.linkedin.com/in/pablo-de-araujo-farina-893a8126b"><img src="https://img.shields.io/badge/LinkedIn-0A0A0B?style=for-the-badge&logo=linkedin&logoColor=F5A524" alt="LinkedIn" /></a>
&nbsp;&nbsp;
<a href="mailto:pablo.farina28@outlook.com"><img src="https://img.shields.io/badge/Email-0A0A0B?style=for-the-badge&logo=maildot&logoColor=F5A524" alt="Email" /></a>
&nbsp;&nbsp;
<a href="https://github.com/pablozr"><img src="https://img.shields.io/badge/GitHub-0A0A0B?style=for-the-badge&logo=github&logoColor=F5A524" alt="GitHub" /></a>

</div>

<br />

## Sobre

Desenvolvedor backend em **[FastAPI](https://fastapi.tiangolo.com)**, com **[Angular](https://angular.dev)** no front. Trabalho em sistemas internos que precisam aguentar concorrência real — não é teoria, e sim fila, lock distribuído e transação explícita.

Hoje entrego sistemas na **Bagaggio**, onde mais de **200 lojas** dependem de ferramentas que já desenvolvi ou mantenho. Antes disso: freelance, jogos educativos com Phaser na UNIRIO, e Java/Spring Boot em legado.

Interesso também pelo lado que ninguém vê: **JevGuard**, um motor de política semântica para coding agents — impedir que um agente altere código além do que a tarefa pede. E o **TCC (PRISMA)**, na UNIRIO, que adiciona recomendación semântica sobre busca por palavras-chave.

<br />

<img src="assets/scope.svg" alt="Escopo de trabalho" width="100%" />

<br />

## Como penso

- **Concorrência é invariante, não detalhe.** Toda operação crítica precisa de resposta explícita para o que acontece quando duas requisições chegam juntas.
- **Assíncrono por padrão.** Desacoplamento via mensageria (`RabbitMQ`) e `Redis` pub/sub, com estado explícito.
- **Regras de negócio explícitas.** Arquitetura orientada a domínio para que a regra viva no domínio, não espalhada no controller.
- **Agentes são um problema de engenharia.** Não confio no diff como está; verifico política por regra.

<br />

## Projetos

<div align="center">
<table>
<tr>
<td colspan="2" valign="top">

<h4><a href="https://github.com/pablozr/JevGuard">JevGuard</a> — motor de política semântica para coding agents</h4>
<p>Não é um gerador de código nem um reviewer de prosa. Verifica o diff que um agente acabou de produzir contra as políticas que importam no repositório: cada regra recebe um julgamento semântico via Jev, e um gate determinístico local retorna <code>PASS</code>, <code>WARN</code> ou <code>FAIL</code>.</p>
<p><img src="https://img.shields.io/badge/TypeScript-0A0A0B?style=flat-square&logo=typescript&logoColor=3178c6" alt="TypeScript" /> <img src="https://img.shields.io/badge/semantic_policy-0A0A0B?style=flat-square&logoColor=F5A524" alt="policy" /></p>

</td>
</tr>
<tr>
<td valign="top" width="50%">

<h4><a href="https://github.com/pablozr/PRISMA">PRISMA</a></h4>
<p>Plataforma da UNIRIO que centraliza projetos acadêmicos importados do SIE. Autenticação institucional via Google, sessões com access + refresh token em Redis, e camada de recomendación semântica sobre busca por palavras-chave.</p>
<p><img src="https://img.shields.io/badge/Python-0A0A0B?style=flat-square&logo=python&logoColor=3776ab" alt="Python" /> <img src="https://img.shields.io/badge/RAG-0A0A0B?style=flat-square&logoColor=F5A524" alt="RAG" /></p>

</td>
<td valign="top" width="50%">

<h4><a href="https://github.com/pablozr/self-checkout-monolith">self-checkout-monolith</a></h4>
<p>Fluxo completo de autoatendimento: carrinho anônimo por mesa em Redis, checkout Stripe com idempotência, reset de senha assíncrono via RabbitMQ + worker SMTP, e catálogo com cache por produto.</p>
<p><img src="https://img.shields.io/badge/FastAPI-0A0A0B?style=flat-square&logo=fastapi&logoColor=009688" alt="FastAPI" /> <img src="https://img.shields.io/badge/Redis-0A0A0B?style=flat-square&logo=redis&logoColor=dc382d" alt="Redis" /></p>

</td>
</tr>
<tr>
<td valign="top" width="50%">

<h4><a href="https://github.com/pablozr/subscription-monolith">subscription-monolith</a></h4>
<p>Gestão de assinaturas com regras por domínio, persistência relacional e comunicação assíncrona.</p>
<p><img src="https://img.shields.io/badge/FastAPI-0A0A0B?style=flat-square&logo=fastapi&logoColor=009688" alt="FastAPI" /> <img src="https://img.shields.io/badge/PostgreSQL-0A0A0B?style=flat-square&logo=postgresql&logoColor=4169e1" alt="PostgreSQL" /></p>

</td>
<td valign="top" width="50%">

<h4><a href="https://github.com/pablozr/FastAPI-Template">FastAPI-Template</a></h4>
<p>Template de API em padrão de produção: organização modular, configuração por ambiente, docker-compose e saída de onde eu costumo partir.</p>
<p><img src="https://img.shields.io/badge/Docker-0A0A0B?style=flat-square&logo=docker&logoColor=2496ed" alt="Docker" /> <img src="https://img.shields.io/badge/template-0A0A0B?style=flat-square&logoColor=F5A524" alt="template" /></p>

</td>
</tr>
<tr>
<td colspan="2" valign="top">

<h4><a href="https://github.com/pablozr/angular-template">angular-template</a></h4>
<p>Base Angular por features, componentização reutilizável e estrutura pronta para integração com APIs REST.</p>

</td>
</tr>
</table>
</div>

<br />

## Stack

<img src="assets/languages.svg" alt="Linguagens por volume de código" width="100%" />

<br />

<div align="center">

<h4>Backend</h4>
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="40" alt="Python" title="Python" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="40" alt="FastAPI" title="FastAPI" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="40" alt="Java" title="Java" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="40" alt="Spring Boot" title="Spring Boot" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/go/go-original.svg" width="40" alt="Go" title="Go" />
</p>

<h4>Frontend</h4>
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/angular/angular-original.svg" width="40" alt="Angular" title="Angular" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="40" alt="TypeScript" title="TypeScript" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" width="40" alt="React" title="React" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextdotjs/nextjs-original.svg" width="40" alt="Next.js" title="Next.js" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vitejs/vitejs-original.svg" width="40" alt="Vite" title="Vite" />
</p>

<h4>Dados, mensageria e infra</h4>
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" alt="PostgreSQL" title="PostgreSQL" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" width="40" alt="MongoDB" title="MongoDB" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg" width="40" alt="Redis" title="Redis" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rabbitmq/rabbitmq-original.svg" width="40" alt="RabbitMQ" title="RabbitMQ" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="40" alt="Docker" title="Docker" />
</p>

</div>

<br />

<details>
<summary><b>Também no currículo</b></summary>

- **Frontend:** JavaScript, React 19, Next.js 15, Server Actions, Phaser
- **Infra e integração:** APIs RESTful, integração com ERP, WebRTC, SSO
- **Qualidade:** testes unitários com Bun, documentação técnica
- **Idiomas:** português (nativo), inglês (C1)
- **Formação:** UNIRIO — Bacharelado em Sistemas de Informação (2023–2027)
- **Liderança:** bolsista de extensão do Clube de Xadrez da UNIRIO; organizou torneios internos

</details>

<br />

<img src="assets/footer.svg" alt="" width="100%" />

<br />

<div align="center">
  <sub>Feito sem gerador externo — os SVGs desta página são meus e estão no repositório.</sub>
</div>

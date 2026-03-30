<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=rect&height=140&text=Pablo%20Farina&fontSize=44&fontColor=E6EDF3&color=0:0B0F14,50:111827,100:0F172A" alt="Pablo Farina" />

  <p><strong>Full Stack Developer</strong></p>
  <p><code>FastAPI</code> · <code>Angular</code> · <code>Redis</code> · <code>RabbitMQ</code> · <code>Docker</code> · <code>PostgreSQL</code> · <code>MongoDB</code></p>
  <p>Sistemas orientados a domínio, eventos em tempo real e concorrência previsível.</p>

  <p>
    <a href="https://www.linkedin.com/in/pablo-de-araújo-farina-893a8126b">
      <img src="https://img.icons8.com/color/48/linkedin.png" width="28" alt="LinkedIn" />
    </a>
    &nbsp;&nbsp;
    <a href="mailto:pablo.farina28@outlook.com">
      <img src="https://img.icons8.com/color/48/microsoft-outlook-2019.png" width="28" alt="Email" />
    </a>
  </p>
  <p>
    <a href="https://www.linkedin.com/in/pablo-de-araújo-farina-893a8126b"><strong>LinkedIn</strong></a> ·
    <a href="mailto:pablo.farina28@outlook.com"><strong>Email</strong></a>
  </p>
</div>

---

## Sobre

Sou desenvolvedor full stack com foco em construção de produtos web robustos.  
Atualmente, meu trabalho está concentrado em **FastAPI + Angular**, com uso de **Redis**, **RabbitMQ** e **Docker** para sistemas modulares, escaláveis e observáveis.

Meu repositório mais avançado é o **self-checkout-monolith**, onde aplico fluxo completo de compra com carrinho, checkout, SSE, pub/sub e controle de concorrência em operações críticas.

Também tenho experiência com **Java** e **Spring Boot**. Não é meu foco atual, mas é uma base sólida do meu repertório backend.

## Direção Técnica

- Arquitetura orientada a domínio para manter regras de negócio explícitas.
- Comunicação assíncrona para desacoplamento entre componentes.
- Consistência operacional com lock distribuído e controle de concorrência.
- Frontend com componentização clara e integração orientada a fluxo.

---

## Stack Atual

### Backend
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="44" alt="Python" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" width="44" alt="FastAPI" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg" width="44" alt="Java" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg" width="44" alt="Spring Boot" />
</p>

### Frontend
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/angular/angular-original.svg" width="44" alt="Angular" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="44" alt="TypeScript" />
</p>

### Dados, Mensageria e Infra
<p>
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="44" alt="PostgreSQL" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg" width="44" alt="MongoDB" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg" width="44" alt="Redis" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rabbitmq/rabbitmq-original.svg" width="44" alt="RabbitMQ" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="44" alt="Docker" />
</p>

---

## Projetos Especiais

<div align="center">
  <table>
    <tr>
      <td colspan="2" valign="top">
        <h3>self-checkout-monolith · Projeto principal</h3>
        <p>Fluxo completo de autoatendimento com carrinho e checkout, projetado para manter consistência transacional mesmo sob concorrência.</p>
        <p>
          <img src="https://img.shields.io/badge/Carrinho%20e%20Checkout-0F172A?style=flat-square" alt="Carrinho e Checkout" />
          <img src="https://img.shields.io/badge/SSE%20em%20tempo%20real-1E293B?style=flat-square" alt="SSE em tempo real" />
          <img src="https://img.shields.io/badge/Redis%20pub%2Fsub-334155?style=flat-square" alt="Redis pub/sub" />
          <img src="https://img.shields.io/badge/Locks%20de%20concorr%C3%AAncia-475569?style=flat-square" alt="Locks de concorrência" />
        </p>
        <p><strong>Stack:</strong> <code>FastAPI</code> <code>Angular</code> <code>Redis</code> <code>RabbitMQ</code> <code>Docker</code></p>
        <p><strong>Fluxo crítico:</strong> <code>Carrinho -> Validação de regras -> Lock -> Checkout -> Evento pub/sub -> Atualização SSE</code></p>
        <p>
          <a href="https://github.com/pablozr/self-checkout-monolith">
            <img src="https://img.shields.io/badge/Abrir_reposit%C3%B3rio-181717?style=for-the-badge&logo=github&logoColor=white" alt="Abrir repositório" />
          </a>
        </p>
      </td>
    </tr>
    <tr>
      <td width="50%" valign="top">
        <h3>subscription-monolith</h3>
        <p>Gestão de assinaturas com regras por domínio, persistência relacional e comunicação assíncrona.</p>
        <p><code>FastAPI</code> <code>PostgreSQL</code> <code>Redis</code> <code>RabbitMQ</code> <code>Docker</code></p>
        <a href="https://github.com/pablozr/subscription-monolith">Ver repositório</a>
      </td>
      <td width="50%" valign="top">
        <h3>fast-api-template</h3>
        <p>Template de API em padrão de produção com organização modular e configuração por ambiente.</p>
        <p><code>FastAPI</code> <code>PostgreSQL</code> <code>MongoDB</code> <code>Redis</code> <code>Docker</code></p>
        <a href="https://github.com/pablozr/fast-api-template">Ver repositório</a>
      </td>
    </tr>
    <tr>
      <td colspan="2" valign="top">
        <h3>angular-template</h3>
        <p>Base Angular por features, componentização reutilizável e estrutura pronta para integração com APIs REST.</p>
        <p><code>Angular</code> <code>TypeScript</code> <code>Docker</code></p>
        <a href="https://github.com/pablozr/angular-template">Ver repositório</a>
      </td>
    </tr>
  </table>
</div>

---

## GitHub Stats

<div align="center">
  <img width="96%" src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=pablozr&theme=github_dark" alt="Resumo do GitHub" />
  <img width="48%" src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username=pablozr&theme=github_dark" alt="Repositórios por linguagem" />
  <img width="48%" src="https://github-profile-summary-cards.vercel.app/api/cards/most-commit-language?username=pablozr&theme=github_dark" alt="Linguagem com mais commits" />
</div>

<div align="center">
  <img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color=0:0B0F14,100:111827" alt="Footer" />
</div>

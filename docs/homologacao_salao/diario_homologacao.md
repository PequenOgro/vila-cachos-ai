# 📋 Diário de Homologação — UAT (User Acceptance Testing)
### Projeto: Módulo Web de Diagnóstico Capilar — Vila Cachos AI
### Cliente: Ramon (Proprietário — Salão Vila Cachos, São Luís/MA)
### Link de Staging: [vila-cachos-ai.vercel.app](https://vila-cachos-ai.vercel.app)

---

## Registro de Sessões de Teste

| Data | Funcionalidade Testada | Feedback do Cliente (Ramon) | Status | Observações |
| :--- | :--- | :--- | :---: | :--- |
| 13/09/2026 | Interface responsiva no celular (wizard de anamnese: Curvatura → Porosidade → Química → Queixas) | Interface intuitiva e fluida no smartphone. Fluxo de perguntas coerente com a rotina real de atendimento do salão. | ✅ Aprovado | Testado em iPhone e Android. Cards de recomendação empilham corretamente no mobile. |
| 13/09/2026 | Recomendação do Top 3 de produtos com justificativas XAI | Produtos indicados coerentes com o que seria prescrito manualmente pelo profissional nos cenários testados. | ✅ Aprovado | Cenários: Cacheada Danificada, Ondulada com Frizz, Crespa em Transição. |
| 13/09/2026 | Sistema de feedback por estrelas (1 a 5) | Funcional. Confirmação visual após o envio da avaliação. | ✅ Aprovado | Feedback registrado com sucesso na API (HTTP 200). |
| 13/09/2026 | Dark Mode (alternância Claro/Escuro) | — | 🔄 Pendente | Aguardando teste específico pelo cliente. Funcionalidade já validada internamente. |
| 13/09/2026 | Timeout de inatividade (15 minutos) | — | 🔄 Pendente | Funcionalidade silenciosa, difícil de testar em sessão curta. Validada internamente via cronômetro. |
| 13/09/2026 | Loading Screen com aviso de Cold Start (Render free tier) | — | 🔄 Pendente | Mensagem de "servidor inicializando" exibida corretamente durante o spin-up do Render (~50s). |

---

## Legenda de Status
- ✅ **Aprovado**: Funcionalidade validada e aceita pelo cliente sem ressalvas.
- ⚠️ **Ajustar**: Funcionalidade testada, mas com solicitação de alteração pelo cliente.
- 🔄 **Pendente**: Aguardando teste ou retorno do cliente.
- ❌ **Reprovado**: Funcionalidade com comportamento incorreto ou inaceitável.

---

## Observações Gerais
- O roteiro de testes enviado ao Ramon está documentado em [roteiro_homologacao.md](roteiro_homologacao.md).
- A comunicação de feedback está sendo realizada via WhatsApp.
- Próxima sessão de UAT será agendada após o retorno completo do cliente sobre todos os cenários do roteiro.

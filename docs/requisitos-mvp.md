# Requisitos detalhados do MVP do Quito

## Contexto
O Quito é uma plataforma SaaS voltada aos **anunciantes de imóveis** (corretores, imobiliárias e incorporadoras). O objetivo do MVP é permitir que esses profissionais publiquem anúncios com qualidade, possuam visibilidade sobre a performance e mantenham seus cadastros validados, reforçando a confiança do comprador que consultará essas informações.

## Personas e perfis
- **Corretor**
  - Plano dedicado (R$ 800/mês).
  - Necessidade de validação de CRECI ativo e sem restrições.
  - Foco em publicar e monitorar poucos imóveis com precisão.
- **Imobiliária**
  - Plano dedicado (R$ 2.500/mês).
  - Validação de CNPJ e dados empresariais.
  - Necessidade de gestão multiusuário e múltiplos anúncios simultâneos.
- **Incorporadora**
  - Plano sob demanda (a partir de R$ 7.000/mês).
  - Validação de CNPJ e documentação societária.
  - Interesse em relatórios avançados e integrações com sistemas internos.

## Jornada principal
1. **Onboarding e login**
   - Seleção e contratação do plano via PIX ou cartão com liberação imediata.
   - Possibilidade de logoff e retorno à tela inicial a qualquer momento.
2. **Configuração do perfil**
   - Preenchimento das informações específicas do perfil escolhido.
   - Verificações automáticas de CRECI ou CNPJ com status do registro.
3. **Criação de anúncios**
   - CTA destacado "Anunciar imóvel" ou equivalente.
   - Formulário estruturado em etapas: dados do imóvel, mídia, descrição, precificação.
   - Regras de recomendação para garantir completude (ex.: fotos mínimas, descrição, tour virtual).
4. **Publicação e monitoramento**
   - Analytics essenciais: impressões, cliques, contatos gerados, avaliação do anúncio.
   - Sugestões de melhoria baseadas em desempenho e boas práticas.
5. **Sistema de avaliações**
   - Captura de feedback dos compradores sobre a qualidade do atendimento e do anúncio.
   - Exibição das avaliações no perfil do anunciante, reforçando credibilidade.

## Backoffice e operação
- **Queue de processamento** para moderar anúncios, verificar documentos e aplicar recomendações.
- **Painel administrativo** para a equipe Quito acompanhar validações, status de planos e métricas gerais.
- **Auditoria e logs** para rastrear alterações em perfis e anúncios.

## Métricas mínimas
- Número de anúncios ativos por anunciante.
- Visualizações por anúncio.
- Taxa de cliques no CTA de contato.
- Taxa de anúncios aprovados vs. reprovados na verificação.
- Pontuação média das avaliações dos anunciantes.

## Considerações futuras
- Versão dedicada ao público comprador com busca e filtros avançados.
- Integrações com portais parceiros e CRMs imobiliários.
- Automatização da cobrança recorrente e upsell de planos.


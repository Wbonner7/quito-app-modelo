# Quito – Plataforma para Anunciantes

O **Quito** (pronuncia-se *o Quito*) é uma plataforma SaaS criada para corretores, imobiliárias e incorporadoras anunciarem seus imóveis com foco em performance. Esta versão do produto é direcionada exclusivamente ao público **anunciante**, enquanto uma experiência separada será desenvolvida futuramente para o público comprador.

## Proposta de valor
- **Centralização dos anúncios** em um painel simples e responsivo.
- **Processos de validação profissional** (CRECI para corretores e CNPJ para imobiliárias/incorporadoras) para aumentar a confiança dos compradores.
- **Analytics e recomendações** para melhorar a qualidade dos anúncios e maximizar a geração de leads.
- **Pagamento imediato e self-service**, com planos que se ajustam ao porte do anunciante.

## Planos e modelo de negócios
Todos os planos são pré-pagos (PIX ou cartão) e liberam o uso imediatamente após a confirmação do pagamento.

| Plano          | Valor mensal | Público-alvo                     | Destaques |
|----------------|--------------|----------------------------------|-----------|
| Corretor       | R$ 800       | Profissionais autônomos          | Verificação CRECI, analytics básicos |
| Imobiliária    | R$ 2.500     | Imobiliárias de pequeno e médio porte | Gestão multi-equipe, analytics avançados |
| Incorporadora  | A partir de R$ 7.000 | Incorporadoras e grandes players | Relatórios personalizados, integrações corporativas |

## Fluxos principais do anunciante
1. **Acesso e autenticação** – Login direciona ao painel. O usuário deve conseguir sair da conta e voltar à tela inicial a partir de qualquer seção.
2. **Seleção do plano** – Escolha e pagamento imediato. Liberação automática das funcionalidades após o pagamento.
3. **Formulário do anunciante** – Ao iniciar um anúncio, o sistema carrega o perfil do plano e exige os dados obrigatórios do anunciante:
   - Corretor: CRECI ativo e sem restrições.
   - Imobiliária/Incorporadora: CNPJ válido, documentação e informações relevantes.
4. **Criação de anúncios** – CTA principal "Anunciar imóvel". O fluxo deve ser simples, com etapas orientadas para completude e qualidade do anúncio.
5. **Analytics do anúncio** – Indicadores mínimos (visualizações, leads, compartilhamentos) apresentados no painel do anunciante.
6. **Sistema de avaliações** – Permite feedback sobre corretores, imobiliárias e incorporadoras.

## Arquitetura do MVP
- **Back-end**: micro framework compatível com FastAPI, mas implementado dentro do repositório para funcionar sem dependências externas. Os módulos de rota utilizam o mesmo estilo do FastAPI real.
- **Persistência**: simulador do Supabase (`SupabaseSimulator`) que grava os dados em `.supabase_simulator.json`. Em produção basta substituir o simulador por chamadas ao REST oficial do Supabase.
- **Front-end**: single-page app em `frontend/` construído com HTML, CSS e JavaScript puro que consome a API do Quito.
- **Testes**: `pytest` cobre os fluxos de planos, cadastro de anunciantes e criação de imóveis com métricas.

## Como usar o Quito sem saber programar
### 1. Instale o Python
- Baixe a versão mais recente em [python.org/downloads](https://www.python.org/downloads/).
- Durante a instalação no Windows marque a opção **"Add python.exe to PATH"**.

### 2. Baixe ou clone este projeto
- Clique em **Code → Download ZIP** no GitHub e extraia a pasta em um local fácil (ex.: Área de Trabalho).

### 3. Execute tudo com um único comando
1. Abra o Terminal (macOS/Linux) ou **Prompt de Comando/PowerShell** (Windows).
2. Navegue até a pasta extraída, por exemplo:
   ```bash
   cd caminho/para/quito-app-modelo
   ```
3. Rode o script que liga o back-end e o painel automaticamente:
   ```bash
   python run_quito.py
   ```
   - Se o seu Windows usar o comando `py`, execute `py run_quito.py`.
   - O navegador abrirá sozinho em `http://127.0.0.1:9000` com o painel do anunciante.

Para encerrar, volte à janela do terminal e pressione **CTRL+C**.

> Dica: o script cria servidores apenas enquanto a janela do terminal estiver aberta. Não é necessário instalar nenhum banco de dados manualmente — o simulador do Supabase grava tudo em um arquivo `.supabase_simulator.json` dentro da pasta do projeto.

## Executando apenas o back-end (simulador Supabase)
Se preferir subir a API manualmente, utilize os passos abaixo.

### Requisitos
- Python 3.11+

### Passos
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # arquivo vazio, mantido por compatibilidade
python -m app.server
```

A API ficará disponível em `http://127.0.0.1:8000`.

### Principais endpoints
| Recurso | Método/URL | Descrição |
|---------|------------|-----------|
| Planos | `GET /plans/` | Lista planos disponíveis (corretor, imobiliária, incorporadora). |
| Anunciantes | `POST /advertisers/` | Cria um anunciante com validação de CRECI/CNPJ conforme o perfil. |
| Anunciantes | `GET /advertisers/` | Lista anunciantes filtrando opcionalmente por tipo. |
| Imóveis | `POST /properties/` | Cadastra um imóvel e cria analytics iniciais. |
| Imóveis | `GET /properties/{id}` | Retorna o imóvel com métricas atualizadas. |
| Analytics | `POST /properties/{id}/metrics/{metric}` | Incrementa métricas (`views`, `leads`, `shares`). |
| Avaliações | `POST /reviews/` | Registra avaliações vinculadas ao anúncio. |
| Fila | `GET /queue/` | Lista itens da fila operacional (ex.: revisão de anúncios). |
| Recomendações | `GET /recommendations/properties` | Retorna imóveis com melhor performance de leads. |

## Executando apenas o front-end
Caso precise subir o painel manualmente (sem o script `run_quito.py`), rode:

```bash
cd frontend
python -m http.server 9000
```

Depois acesse `http://127.0.0.1:9000` no navegador.

## Testes automatizados
```bash
pytest
```

Os testes cobrem os fluxos de cadastro de planos, validação de anunciantes e criação de anúncios com métricas.

## Próximos passos sugeridos
1. **Integrações reais com Supabase** utilizando chaves e tabelas hospedadas.
2. **Validação externa de CRECI/CNPJ** com serviços oficiais.
3. **Design system compartilhado** entre o painel do anunciante e o futuro portal do comprador.
4. **Ampliação dos dashboards de analytics** com funil completo de leads.
5. **Implementação da experiência do comprador**, mantendo consistência com os perfis de anunciantes.

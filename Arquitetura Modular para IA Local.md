# **Arquitetura de Sistemas Local-First com Desenvolvimento Assistido por Agentes de IA: Um Guia Exaustivo de Implementação e Evolução Modular**

O desenvolvimento de software contemporâneo está atravessando uma mudança de paradigma fundamental, na qual a colaboração entre o usuário humano e os agentes de inteligência artificial, como o Claude Code, define a nova fronteira da produtividade. Esta evolução exige uma arquitetura que não apenas suporte as funcionalidades desejadas, mas que seja otimizada para a "cognição" da IA e para a agilidade do desenvolvedor humano. A transição para sistemas local-first representa um retorno à soberania dos dados e à resiliência operacional, eliminando a dependência de conectividade constante e reduzindo a latência para níveis sub-milissegundos.1 Para que tal sistema seja viável a longo prazo, a infraestrutura deve ser concebida de forma modular, permitindo que novos componentes sejam acoplados sem comprometer a integridade do núcleo sistêmico.

## **Fundamentos da Arquitetura Hexagonal e Extensibilidade Modular**

A espinha dorsal de um sistema que permite melhorias futuras sem rupturas estruturais é a Arquitetura Hexagonal, também conhecida como Portas e Adaptadores.2 Este padrão de design foca na separação rigorosa entre a lógica de negócio central (o domínio) e as dependências externas, como bancos de dados, interfaces de usuário e APIs de terceiros. Ao isolar o núcleo, o sistema torna-se agnóstico em relação à tecnologia de infraestrutura, o que é vital para a qualidade de vida (QoL) do desenvolvedor e da IA, pois reduz a complexidade do código que precisa ser processado em cada janela de contexto.2

### **O Núcleo do Domínio e o Princípio da Inversão de Dependência**

No centro da aplicação residem as Entidades e os Serviços de Aplicação. As entidades representam os conceitos fundamentais do negócio — por exemplo, transações financeiras, metas de economia ou perfis de comportamento — e são totalmente independentes de frameworks ou mecanismos de persistência.2 A comunicação deste núcleo com o mundo exterior ocorre através de Portas, que são interfaces abstratas definindo o que o sistema precisa fazer, sem especificar como.2

A implementação desta arquitetura facilita a QoL da IA porque permite que o Claude Code trabalhe em módulos isolados. Quando a IA está desenvolvendo um novo adaptador para integração com o Android, ela não precisa processar a lógica interna de cálculo de juros, desde que o contrato da porta seja respeitado.5 Esta modularidade é o que garante que a infraestrutura não "quebre" no futuro; a substituição de um banco de dados SQLite por um sistema de arquivos criptografado ou a adição de um novo módulo de análise comportamental resume-se à implementação de novos adaptadores para portas existentes ou novas.2

### **Comparação de Padrões Arquiteturais para Extensibilidade**

A escolha entre uma arquitetura puramente hexagonal e um sistema de plugins depende da necessidade de dinamismo em tempo de execução. Para um sistema local-first robusto, uma abordagem híbrida oferece o melhor equilíbrio.

| Característica | Arquitetura Hexagonal | Sistema de Plugins | Abordagem Híbrida Proposta |
| :---- | :---- | :---- | :---- |
| **Ponto de Extensibilidade** | Adaptadores em tempo de compilação/deploy. | Módulos carregados dinamicamente em runtime. | Portas fixas para o core; plugins para novos recursos. |
| **Separação de Preocupações** | Rigorosa via inversão de dependência. | Alta; o kernel desconhece os plugins. | Máxima; o core dita as regras, plugins executam. |
| **Facilidade para a IA** | Alta; limites claros e tipos definidos. | Média; requer contratos de interface rígidos. | Otimizada; a IA cria novos plugins sem tocar no core. |
| **Risco de Ruptura** | Baixo, se as portas forem estáveis. | Mínimo para o kernel; alto para plugins. | Controlado via versionamento e injeção de dependência. |
| **Foco em QoL** | Focado na manutenção a longo prazo. | Focado na extensibilidade por terceiros. | Sinergia entre estabilidade e inovação rápida. |

Na arquitetura proposta, o "Kernel" do sistema local-first gerencia a persistência básica e o barramento de eventos, enquanto funcionalidades específicas, como o motor de nudges financeiros, são tratadas como módulos que se registram no sistema através de ganchos (hooks) predefinidos.7

## **Desenvolvimento Orientado por Agentes: O Fluxo de Trabalho com Claude Code**

A implementação de um sistema onde o Claude Code é o principal executor exige que o usuário humano assuma o papel de arquiteto e revisor estratégico. A eficácia da IA está diretamente ligada à qualidade do contexto fornecido e à estrutura do repositório no GitHub.9

### **O Papel Crítico do Arquivo CLAUDE.md**

Para garantir que a IA não cometa erros repetitivos e compreenda as diretrizes do projeto, a criação de um arquivo CLAUDE.md na raiz do repositório é mandatória.4 Este arquivo serve como uma memória persistente que o agente consulta no início de cada sessão. Ele deve conter as convenções de codificação, os comandos de build, as instruções de teste e, crucialmente, as decisões arquiteturais tomadas.5

Sob a perspectiva da QoL do desenvolvedor, o CLAUDE.md atua como um manual de bordo automatizado. Sempre que uma nova regra é estabelecida ou um bug recorrente é identificado, o usuário deve instruir o Claude a atualizar este arquivo: "Atualize o CLAUDE.md para garantir que todos os novos adaptadores de banco de dados utilizem o modo WAL por padrão".9 Isso reduz o atrito e a necessidade de microgerenciamento por parte do usuário.

### **O Ciclo de Desenvolvimento em Quatro Fases**

O processo de desenvolvimento deve ser estruturado em fases iterativas para maximizar a precisão da IA e evitar que o projeto se torne uma "Big Ball of Mud".5

1. **Exploração e Pesquisa**: Nesta fase, o usuário solicita que o Claude analise a base de código existente ou documentações externas. O uso do comando /plan em modo de planejamento permite que a IA realize pesquisas profundas sem alterar arquivos, economizando tokens e evitando commits desnecessários.4  
2. **Planejamento Estratégico**: O Claude propõe uma solução detalhada, incluindo alterações em portas, adaptadores e novos módulos. O usuário deve revisar este plano, desafiando suposições e solicitando alternativas antes de qualquer implementação.5  
3. **Implementação Incremental**: A codificação ocorre em pequenos blocos. Cada funcionalidade é seguida pela criação e execução de testes automatizados. A IA é encorajada a usar subagentes para tarefas de pesquisa paralelas, mantendo a conversa principal focada na implementação.4  
4. **Verificação e Commit**: Após a validação dos testes, o Claude realiza o commit utilizando o formato de Conventional Commits, garantindo um histórico de versão limpo no GitHub.10

### **Gestão de Contexto e QoL da IA**

Um dos maiores desafios no uso de agentes de codificação é a saturação da janela de contexto. À medida que a conversa cresce, a performance da IA degrada.4 Para mitigar isso, o sistema deve ser desenvolvido de forma que os arquivos sejam pequenos e focados (Single Responsibility Principle). A prática de usar o comando /clear periodicamente, após consolidar o progresso em documentos de design ou no próprio código, garante que o Claude sempre trabalhe com uma mente "fresca" e focada no problema atual.5

## **Infraestrutura Local-First e Persistência de Dados**

O paradigma local-first dita que o dispositivo do usuário é a fonte primária da verdade. Isso implica em desafios técnicos únicos relacionados à persistência, sincronização multiusuário e resolução de conflitos.1

### **SQLite como Motor de Dados Robusto**

Para a persistência local, o SQLite continua sendo a escolha predominante devido à sua confiabilidade e ubiquidade.13 No entanto, para suportar uma experiência de usuário fluida e multiusuário, ele deve ser configurado corretamente. O uso do modo Write-Ahead Logging (WAL) permite que operações de leitura e escrita ocorram simultaneamente, essencial para evitar travamentos na UI durante sincronizações de fundo.14

A estrutura de dados deve ser projetada para ser amigável a algoritmos de sincronização. Isso envolve o uso de identificadores globais únicos (UUIDs) em vez de inteiros sequenciais, permitindo que registros criados offline em diferentes dispositivos não colidam quando forem eventualmente mesclados.15

### **Sincronização e Concorrência via CRDTs**

Em cenários onde múltiplos usuários ou dispositivos interagem com os mesmos dados, a resolução de conflitos torna-se o ponto central da infraestrutura. Tipos de Dados Replicados Sem Conflitos (CRDTs) oferecem uma solução matemática para este problema, permitindo que as réplicas de dados convirjam para o mesmo estado sem a necessidade de um coordenador central.13

Para a implementação em Python, o uso de bibliotecas como Yjs (via wrappers) ou a implementação manual de LWW-Element-Sets (Last-Write-Wins) no nível do adaptador de banco de dados permite que o sistema gerencie edições concorrentes de forma transparente.13 O modelo mental deve mudar de "quem escreveu por último no servidor" para "como as intenções dos usuários podem ser mescladas deterministicamente".17

### **Performance e Escalabilidade Local**

Diferente de sistemas baseados em nuvem, a escalabilidade local-first foca na eficiência de recursos no dispositivo. O uso de índices apropriados no SQLite e a minimização de I/O desnecessário são cruciais. Além disso, a arquitetura deve prever o arquivamento de dados históricos para evitar que o banco de dados cresça indefinidamente, afetando a performance de leitura e o tempo de inicialização da aplicação.18

| Métrica de Performance | Alvo Local-First | Estratégia de Implementação |
| :---- | :---- | :---- |
| **Latência de Leitura** | \< 10ms | Índices em colunas de consulta frequente; cache em memória. |
| **Latência de Escrita** | \< 50ms | SQLite em modo WAL; operações assíncronas via asyncio. |
| **Tempo de Sincronização** | Oportunístico | Background workers; replicação diferencial de logs. |
| **Uso de Memória** | \< 200MB (Base) | Carregamento preguiçoso (lazy loading) de módulos e dados. |
| **Integridade de Dados** | 100% | Transações ACID e validação de esquema via Pydantic. |

## **Comunicação Desacoplada: O Barramento de Eventos Interno**

Para que a infraestrutura possibilite melhorias via novos módulos sem quebrar o sistema, a comunicação entre as partes deve ser indireta. O uso de um Barramento de Eventos (Event Bus) interno é a técnica recomendada para desacoplar produtores de dados de seus consumidores.15

### **O Padrão Publish-Subscribe (Pub/Sub)**

Neste modelo, quando uma ação ocorre — por exemplo, o usuário registra uma despesa — o módulo de finanças publica um evento ExpenseRecorded. Outros módulos, como o de análise de orçamento ou o de notificações de nudge, podem estar inscritos para ouvir este evento e agir de acordo, sem que o módulo original saiba de sua existência.15

Este desacoplamento é fundamental para a QoL da IA e do desenvolvedor. Se no futuro o usuário desejar adicionar um módulo que envia relatórios para o Telegram, basta criar um novo assinante para os eventos existentes. Não há necessidade de alterar o código do módulo financeiro, eliminando o risco de efeitos colaterais indesejados.19

### **Implementação Assíncrona com asyncio e bubus**

Em Python, a biblioteca bubus fornece uma implementação de barramento de eventos pronta para produção, baseada em Pydantic e asyncio.16 Ela suporta:

* **Tipagem Forte**: Eventos são classes Pydantic, o que permite que a IA utilize autocompletar e validação estática de tipos, aumentando a segurança do código.16  
* **Concorrência**: Handlers podem ser síncronos ou assíncronos, permitindo que tarefas pesadas de I/O não bloqueiem a interface.15  
* **Persistência de Eventos (WAL)**: Eventos podem ser gravados em disco antes de serem processados, garantindo que não sejam perdidos em caso de falha de energia.16  
* **Prevenção de Ciclos**: O sistema rastreia o caminho do evento para evitar loops infinitos quando módulos disparam novos eventos em resposta a outros.16

Ao estruturar a comunicação desta forma, o sistema torna-se uma coleção de agentes autônomos que colaboram através de mensagens, espelhando a própria estrutura de trabalho entre o usuário e o Claude Code.

## **Interface do Usuário (UI) e Experiência (UX) de Próxima Geração**

O foco na UI e UX é essencial para que a tecnologia local-first seja adotada. O sistema deve ser responsivo, esteticamente agradável e intuitivo, tanto em desktops quanto em dispositivos móveis.

### **Flet como Framework de Escolha**

O framework Flet emerge como a solução ideal para este projeto, permitindo a construção de interfaces modernas utilizando apenas Python, mas com o poder do motor Flutter do Google por trás.22 O Flet resolve o problema da fragmentação de habilidades: o desenvolvedor (ou a IA) utiliza a mesma lógica de backend e frontend em uma única linguagem, o que é extremamente eficiente em termos de consumo de tokens e clareza de contexto.23

A QoL do desenvolvedor é ampliada pela capacidade do Flet de rodar como uma aplicação desktop nativa, um aplicativo web ou até mesmo ser empacotado para mobile, mantendo uma aparência consistente com o Material Design 3 ou Cupertino.22 Para a IA, a sintaxe declarativa do Flet é mais fácil de gerar e validar do que layouts complexos em XML ou HTML/CSS espalhados por múltiplos arquivos.24

### **Sinergia com Pop\!\_OS e COSMIC**

Dado que o desenvolvimento ocorre em ambiente Pop\!\_OS, a integração com o novo desktop COSMIC é um diferencial competitivo. O sistema deve respeitar as diretrizes de interface humana (HIG) do COSMIC, utilizando paletas de cores do sistema e suportando modos claro e escuro automaticamente.25 A aplicação deve ser capaz de disparar notificações nativas do sistema para nudges urgentes, utilizando chamadas de subprocesso para notify-send ou bibliotecas cross-platform como plyer.27

### **Design Responsivo e Adaptabilidade**

Uma aplicação local-first deve brilhar em diferentes fatores de forma. O uso de widgets adaptativos no Flet garante que o layout se ajuste de uma visualização em colunas em um monitor ultrawide para uma lista vertical em um smartphone.23 A UX é reforçada por transições suaves e feedback imediato; como os dados são locais, não há "spinners" de carregamento aguardando o servidor, o que cria uma sensação de performance instantânea que é marca registrada do local-first.1

## **Algoritmos de Nudge e Engenharia Comportamental**

O diferencial deste sistema é a sua capacidade de atuar proativamente na melhoria da qualidade de vida financeira do usuário através de algoritmos baseados em economia comportamental.30

### **Teoria dos Nudges e Arquitetura de Escolha**

A teoria do nudge propõe que pequenas intervenções no ambiente de decisão podem guiar o comportamento humano sem proibir opções ou alterar incentivos financeiros significativos.32 No contexto deste software, o sistema atua como um "arquiteto de escolha".

Algoritmos de nudge eficazes devem combater vieses cognitivos comuns:

* **Viés do Presente**: A tendência de valorizar recompensas imediatas em detrimento de benefícios futuros. O sistema combate isso visualizando o impacto de um gasto impulsivo no longo prazo através de gráficos de projeção.31  
* **Aversão à Perda**: Sentimos a dor da perda com o dobro da intensidade do prazer do ganho. O sistema pode enquadrar uma economia não realizada como uma "perda de oportunidade" para motivar o usuário.31  
* **Contabilidade Mental**: Tratamos o dinheiro de forma diferente dependendo de sua origem ou destino. O sistema utiliza "baldes" virtuais para ajudar o usuário a categorizar fundos de forma racional.31

### **Implementação de Fricção Digital e Controle de Impulsos**

Para combater gastos impulsivos, o sistema pode introduzir "fricção digital" deliberada. Se o motor de análise detecta que o usuário está em um site de compras em um horário de alta vulnerabilidade (identificado pelo "Genoma de Gatilhos"), ele pode disparar uma intervenção.31

Esta intervenção pode ser configurada em níveis de severidade:

1. **Nudge Suave**: Uma notificação lembrando do objetivo de economia do mês.37  
2. **Fricção de Reflexão**: Um pop-up que exige que o usuário descreva em três frases por que aquele item é necessário agora.36  
3. **Bloqueio Temporário**: Utilizando scripts Python para modificar temporariamente o arquivo /etc/hosts ou configurar o firewall do sistema para bloquear o acesso ao domínio do comerciante por um período de "resfriamento" de 24 horas.38

### **O Genoma de Gatilhos e IA Local (Ollama)**

A personalização extrema é alcançada mapeando o "Genoma de Gatilhos" do usuário através de dimensões como emoção, tempo, localização e até qualidade do sono (se integrado a wearables).31 Este mapeamento deve ser processado localmente para garantir a privacidade.

O uso do Ollama permite que modelos de linguagem pequenos (SLMs) como o Phi-3 ou Mistral rodem diretamente no hardware do usuário, analisando padrões de comportamento e gerando nudges altamente personalizados sem que nenhum dado sensível saia do dispositivo.41 A IA pode aprender, por exemplo, que o usuário é mais propenso a compras impulsivas após noites de pouco sono e ajustar a sensibilidade das intervenções nessas manhãs.31

## **Integração Mobile e Automação de Sistema com Android**

Para ser verdadeiramente útil, o sistema local-first deve se estender ao dispositivo móvel, onde ocorre a maioria das interações de consumo.

### **Tasker e Shizuku: O Poder do Controle sem Root**

No ecossistema Android, o Tasker atua como o motor de automação, permitindo disparar ações baseadas em contexto (localização, conexão Wi-Fi, abertura de apps).44 Para intervenções mais profundas, como o bloqueio de aplicativos ou monitoramento de tráfego de rede sem a necessidade de Root, a integração com o Shizuku é a solução moderna.47

O Shizuku permite que o Tasker execute comandos ADB (Android Debug Bridge) com privilégios elevados. Isso possibilita, por exemplo:

* **Suspensão de Apps**: O comando pm suspend com.instagram.android pode desativar temporariamente um aplicativo viciante durante o horário de trabalho.47  
* **Firewall via Shell**: O comando cmd connectivity set-package-networking-enabled false \<package\> pode bloquear o acesso à rede de um app específico, forçando o usuário a focar em outras tarefas ou evitar compras online.48

### **Comunicação entre Desktop e Mobile**

A sincronização entre o Pop\!\_OS e o Android deve ocorrer de forma peer-to-peer sempre que possível. O uso de protocolos de rede local ou a sincronização via pastas compartilhadas (utilizando ferramentas como Syncthing) permite que o banco de dados SQLite e o log de eventos sejam compartilhados entre as instâncias da aplicação sem depender de uma nuvem centralizada.13

O fluxo de dados pode ser resumido na seguinte tabela:

| Direção do Fluxo | Tipo de Dado | Mecanismo de Transporte | Impacto na UX |
| :---- | :---- | :---- | :---- |
| **Mobile \-\> Desktop** | Log de transações e gatilhos. | Syncthing / Local API. | Análise profunda no desktop; visualização macro. |
| **Desktop \-\> Mobile** | Regras de nudge e listas de bloqueio. | P2P Sync. | Proteção em tempo real em qualquer lugar. |
| **Sistema \-\> Usuário** | Nudges e lembretes urgentes. | Notificações Push / Tasker. | Intervenção no momento crítico da decisão. |
| **Usuário \-\> Sistema** | Registro manual de intenções. | Flet UI (Mobile). | Entrada de dados rápida e sem fricção. |

## **Etapas de Implementação: O Roteiro para Usuário e Claude Code**

A construção deste sistema exige uma coordenação precisa. Abaixo estão detalhadas as etapas, dividindo as responsabilidades entre o usuário (arquiteto/estategista) e o Claude Code (desenvolvedor/executor).

### **Fase 1: Configuração do Ambiente e Governança (Usuário)**

Esta fase é fundamental para estabelecer as "regras do jogo".

1. **Inicialização do Repositório**: Criar o repositório no GitHub com uma estrutura de pastas modular.10  
2. **Preparação da Infraestrutura Local**: Instalar Python 3.12+, SQLite3, Ollama (com modelos Llama ou Mistral) e o ambiente Flet.41  
3. **Escrita do CLAUDE.md Inicial**: Definir as diretrizes de arquitetura hexagonal, o uso do barramento de eventos e as preferências de UI.4

### **Fase 2: Construção do Núcleo e Persistência (Claude Code)**

Nesta etapa, o motor da aplicação ganha vida.

1. **Definição do Domínio**: Implementar as entidades centrais e as portas (interfaces) para o repositório de dados e o motor de nudges.2  
2. **Implementação do Adaptador SQLite**: Criar a camada de persistência utilizando transações ACID, modo WAL e suporte a UUIDs.12  
3. **Setup do Barramento de Eventos**: Configurar o bubus para gerenciar a comunicação assíncrona entre módulos.16

### **Fase 3: Desenvolvimento da Interface e UX (Claude Code)**

A aplicação torna-se tangível para o usuário.

1. **Criação do Dashboard Principal**: Desenvolver a UI com Flet, focando em visualização de dados e responsividade.22  
2. **Módulo de Configuração de Nudges**: Implementar uma interface intuitiva para o usuário definir seus próprios gatilhos e níveis de fricção.27  
3. **Integração com Sistema de Notificações**: Conectar o barramento de eventos às notificações nativas do Pop\!\_OS.18

### **Fase 4: Inteligência Comportamental e Mobile (Claude \+ Usuário)**

A fase de maior complexidade e ajuste fino.

1. **Integração com Ollama**: O Claude implementa o adaptador para chamadas locais ao LLM, permitindo que o sistema gere conselhos financeiros em linguagem natural.43  
2. **Automação de Bloqueio de Hosts**: Implementar as funções de modificação de /etc/hosts com as devidas verificações de permissão.38  
3. **Exportação de Regras para Android**: O Claude gera scripts ou arquivos de configuração que o usuário importa no Tasker para automação mobile.47

### **Fase 5: Evolução e Manutenção Modular (Usuário \+ Claude)**

Garantindo a longevidade do sistema.

1. **Refatoração e Compactação de Contexto**: O usuário solicita revisões periódicas do código. O Claude utiliza o comando /compact para resumir o histórico e manter a eficiência dos tokens.5  
2. **Adição de Novos Módulos**: Seguindo o padrão de portas e adaptadores, o usuário solicita novos recursos (ex: integração com APIs bancárias via scraping local), e o Claude os implementa sem alterar o núcleo.2  
3. **Monitoramento de Saúde**: Implementação do comando /doctor para diagnosticar integridade do banco de dados e performance do sistema.11

## **Gestão de Versionamento e Evolução Contínua via GitHub**

O repositório no GitHub não serve apenas para armazenar o código, mas como o registro histórico da evolução da inteligência do sistema.

### **Estratégia de Branching para IA**

Para evitar que a IA sobrescreva trabalhos importantes ou crie conflitos complexos de mesclagem, recomenda-se o uso de branches de funcionalidade (feature branches) efêmeras. O Claude deve criar um branch para cada tarefa específica do plano, realizar os commits e, após a aprovação dos testes, o usuário realiza o merge para a branch main.10

A estrutura de commits deve ser informativa o suficiente para que, em uma nova sessão, o Claude possa reconstruir o contexto histórico rapidamente através do comando git log. O uso de Git Worktrees é incentivado para que o usuário possa supervisionar o Claude trabalhando em diferentes módulos simultaneamente, acelerando o ciclo de desenvolvimento de 3 a 5 vezes.9

### **Automação de CI/CD para Sistemas Local-First**

Embora a aplicação seja local-first, o uso de GitHub Actions é vital para garantir a qualidade. Os workflows de CI devem:

* **Linting e Tipagem**: Rodar mypy e ruff para garantir que o código gerado pela IA adere aos padrões de qualidade.10  
* **Testes de Integração de Banco de Dados**: Executar testes contra instâncias temporárias de SQLite para garantir que as migrações de esquema não quebrem os dados existentes.54  
* **Simulação de Sincronização**: Testar a convergência de dados em cenários de conflito simulados para validar a lógica de CRDT.17

## **Síntese Técnica e Conclusões para o Futuro do Sistema**

A implementação deste sistema representa a convergência de três tendências tecnológicas imparáveis: a soberania dos dados (Local-First), a arquitetura desacoplada (Hexagonal/Event-Driven) e o desenvolvimento assistido por agentes (Claude Code). Ao priorizar a QoL tanto do desenvolvedor humano quanto da IA, cria-se um ambiente onde a inovação é rápida e o risco técnico é minimizado.

A infraestrutura baseada em portas e adaptadores é a única garantia real de que o sistema poderá crescer de forma modular. O foco na UI/UX através do Flet e na inteligência comportamental via nudges automatizados transforma o software de uma ferramenta passiva em um agente ativo de bem-estar para o usuário. A soberania local, garantida pelo SQLite e Ollama, assegura que a privacidade e a performance não sejam sacrificadas no altar da conveniência da nuvem.

Este guia fornece o mapa detalhado para que o usuário e o Claude Code colaborem na construção de um sistema que não é apenas funcional hoje, mas resiliente e adaptável para as décadas de avanços tecnológicos que virão. A chave do sucesso reside na disciplina arquitetural e na manutenção rigorosa do contexto, permitindo que a inteligência artificial execute a complexidade técnica enquanto o humano direciona o propósito evolutivo.

Para implementar o **Controle de Bordo** como um sistema resiliente, modular e focado em qualidade de vida (QoL), a arquitetura deve ser pensada para que o Claude Code (DEV) consiga trabalhar em blocos isolados sem "quebrar" o todo. A transição para uma IA local como a **Luna** exige que a infraestrutura de dados e eventos já esteja preparada para consumo via Model Context Protocol (MCP).

Aqui está o roteiro técnico detalhado para a execução deste projeto.

### **1\. Arquitetura de Infraestrutura: Modularidade e QoL**

A base do projeto utilizará a **Arquitetura Hexagonal (Portas e Adaptadores)**. Isso garante que a lógica central (seus objetivos e finanças) seja separada da infraestrutura (APIs bancárias, notificações do Pop\!\_OS).

* **Núcleo do Domínio:** Onde residem as regras de decisão (ex: "proibir compra se reserva do apartamento \< 10%").  
* **Barramento de Eventos (Event Bus):** Utilização da biblioteca bubus. Ela permite que módulos se comuniquem de forma assíncrona. Quando uma compra é detectada, o módulo de Finanças publica um evento; o módulo de Nudges ouve esse evento e decide se bloqueia o app no celular via Shizuku.  
* **Persistência Local-First:** SQLite com modo **Write-Ahead Logging (WAL)** para permitir que múltiplos processos (seu script de automação e o dashboard UI) acessem o banco simultaneamente sem travamentos.

### **2\. Governança e QoL do Claude Code**

Para que o Claude Code produza código de alta qualidade sem se perder no contexto, você deve implementar o arquivo CLAUDE.md.

* **O Arquivo CLAUDE.md:** Deve conter as "leis" do projeto: padrões de código (PEP8), comandos de teste, regras de branching no GitHub e o mapa da arquitetura hexagonal. Claude lerá este arquivo no início de cada sessão para manter a consistência.  
* **Modo Planejamento (**/plan**):** Antes de cada sprint, o Claude deve gerar um documento de especificação (SPEC.md). Você aprova o plano e só então ele inicia a codificação em pequenos blocos.

### **3\. Proposta de Sprints e Micro-Iterações**

Em vez de sprints de 2 semanas, o projeto deve seguir o modelo de **micro-iterações** de 1 a 3 dias para cada módulo funcional.

| Sprint | Foco | Entregável Principal |
| :---- | :---- | :---- |
| **0** | **Ambiente** | Repositório GitHub, CLAUDE.md e esqueleto da Arquitetura Hexagonal. |
| **1** | **Cérebro de Dados** | SQLite configurado e Barramento de Eventos bubus funcional. |
| **2** | **Guardião Financeiro** | Integração com Belvo/Pluggy e motor de regras contra impulsos. |
| **3** | **Ponte Mobile** | Setup de automação via Shizuku e monitoramento de apps no Android. |
| **4** | **Interface Unificada** | Dashboard Flet com visualização de metas e métricas de estresse. |
| **5** | **Luna Integration** | Local LLM via Ollama configurado como agente decisor MCP. |
| **6** | **Módulos de Sonhos** | Automação Alura/Coursera, Tracker de Escrita e Agenda de Casal. |

### **4\. Levantamento de Tasks (Responsabilidades)**

#### **Tasks do Usuário (Você como Arquiteto)**

1. **Setup Inicial:** Criar o repositório GitHub e configurar o ambiente Python 3.12+ no Pop\!\_OS.  
2. **Chaves e Permissões:** Obter tokens de API (Belvo/Pluggy), configurar o Shizuku no Android e garantir permissões de escrita no /etc/hosts para o bloqueador de sites.  
3. **Definição de Regras:** Fornecer ao Claude a lógica humana (ex: "Se meu HRV estiver baixo, bloqueie reuniões no Teams e sugira natação").  
4. **Revisão Crítica:** Validar cada PR do Claude, garantindo que ele não incluiu mocks excessivos em vez de testes reais.

#### **Tasks do Claude Code (Como Desenvolvedor)**

1. **Criação do Kernel:** Desenvolver a estrutura de pastas hexagonal e o sistema de injeção de dependência.  
2. **Desenvolvimento de Adaptadores:**  
   * **Adaptador Financeiro:** Consumir webhooks de transações e normalizar dados.  
   * **Adaptador Pop\!\_OS:** Monitorar janelas ativas e gerenciar notificações via DBus.  
   * **Adaptador Android:** Gerar scripts de comando ADB/Shizuku para suspender apps compulsivos.  
3. **UI Evolutiva:** Construir a interface responsiva em Flet, focando em baixa carga cognitiva para reduzir o estresse.  
4. **Integração Luna:** Criar o servidor MCP que expõe o banco de dados e as ferramentas de sistema para a Luna (Local LLM) agir sobre eles.

### **5\. Mecanismo de Controle de Impulsos (Deep Dive)**

Para proibir compras impulsivas, o Claude deve implementar um **Filtro de Fricção Digital**:

1. **Detecção:** O Android Accessibility API (via Shizuku) detecta a abertura de apps de compras.  
2. **Intervenção:** O sistema consulta o saldo de reserva para o "Apartamento". Se a meta mensal não estiver batida, o celular exibe um popup exigindo uma justificativa em 3 frases.  
3. **Bloqueio Hard:** Se a tentativa persistir fora do horário permitido, o script Python no Pop\!\_OS altera o /etc/hosts e o Tasker suspende o app no Android.

### **6\. Cronograma Sugerido**

* **Semana 1:** Sprint 0 e 1 (Infraestrutura).  
* **Semana 2:** Sprint 2 (Finanças) \- Foco no ROI financeiro imediato.  
* **Semana 3:** Sprint 3 e 4 (Mobile e Dashboard UI).  
* **Semana 4:** Sprint 5 e 6 (Inteligência Luna e Módulos de Estudo/Escrita).

Este plano garante que o Controle de Bordo nasça como uma ferramenta profissional, versionada e pronta para crescer conforme você e sua parceira evoluem em suas rotinas.

#### **Referências citadas**

1. Why Local-First Software Is the Future and its Limitations | RxDB \- JavaScript Database, acessado em março 22, 2026, [https://rxdb.info/articles/local-first-future.html](https://rxdb.info/articles/local-first-future.html)  
2. Hexagonal Architecture \- System Design \- GeeksforGeeks, acessado em março 22, 2026, [https://www.geeksforgeeks.org/system-design/hexagonal-architecture-system-design/](https://www.geeksforgeeks.org/system-design/hexagonal-architecture-system-design/)  
3. Building Maintainable Python Applications with Hexagonal Architecture and Domain-Driven Design \- DEV Community, acessado em março 22, 2026, [https://dev.to/hieutran25/building-maintainable-python-applications-with-hexagonal-architecture-and-domain-driven-design-chp](https://dev.to/hieutran25/building-maintainable-python-applications-with-hexagonal-architecture-and-domain-driven-design-chp)  
4. Best Practices for Claude Code \- Claude Code Docs, acessado em março 22, 2026, [https://code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices)  
5. Claude Code Best Practices \- GitHub Pages, acessado em março 22, 2026, [https://rosmur.github.io/claudecode-best-practices/](https://rosmur.github.io/claudecode-best-practices/)  
6. Understanding Modern Software Architectural Patterns: Clean, Hexagonal, Onion, and Plugin… \- Medium, acessado em março 22, 2026, [https://medium.com/@vikasgoel53/understanding-modern-software-architectural-patterns-clean-hexagonal-onion-and-plugin-06c559a2b211](https://medium.com/@vikasgoel53/understanding-modern-software-architectural-patterns-clean-hexagonal-onion-and-plugin-06c559a2b211)  
7. How to Build Plugin Systems in Python \- OneUptime, acessado em março 22, 2026, [https://oneuptime.com/blog/post/2026-01-30-python-plugin-systems/view](https://oneuptime.com/blog/post/2026-01-30-python-plugin-systems/view)  
8. Plugin Architecture for Python | Binary Coders \- WordPress.com, acessado em março 22, 2026, [https://binarycoders.wordpress.com/2023/07/22/plugin-architecture-for-python/](https://binarycoders.wordpress.com/2023/07/22/plugin-architecture-for-python/)  
9. 10 Claude Best Practices by Boris | by Amit Vishwakarma | Feb, 2026, acessado em março 22, 2026, [https://medium.com/@amitvishwak/10-claude-best-practices-by-boris-a35fcd5cfec2](https://medium.com/@amitvishwak/10-claude-best-practices-by-boris-a35fcd5cfec2)  
10. How We Integrated Claude Code Into Our GitHub Workflow \- Chamith Madusanka \- Medium, acessado em março 22, 2026, [https://chamith.medium.com/how-we-integrated-claude-code-into-our-github-workflow-97a5db8bcb8e](https://chamith.medium.com/how-we-integrated-claude-code-into-our-github-workflow-97a5db8bcb8e)  
11. claude-code-best-practice/CLAUDE.md at main · shanraisshan ..., acessado em março 22, 2026, [https://github.com/shanraisshan/claude-code-best-practice/blob/main/CLAUDE.md](https://github.com/shanraisshan/claude-code-best-practice/blob/main/CLAUDE.md)  
12. Local first tooling · trailbaseio trailbase · Discussion \#1 \- GitHub, acessado em março 22, 2026, [https://github.com/trailbaseio/trailbase/discussions/1](https://github.com/trailbaseio/trailbase/discussions/1)  
13. Local-first architecture with Expo, acessado em março 22, 2026, [https://docs.expo.dev/guides/local-first/](https://docs.expo.dev/guides/local-first/)  
14. Can SQLite support multiple users? \- Stack Overflow, acessado em março 22, 2026, [https://stackoverflow.com/questions/5102027/can-sqlite-support-multiple-users](https://stackoverflow.com/questions/5102027/can-sqlite-support-multiple-users)  
15. How to Build an Event Bus with asyncio in Python \- OneUptime, acessado em março 22, 2026, [https://oneuptime.com/blog/post/2026-01-25-event-bus-asyncio-python/view](https://oneuptime.com/blog/post/2026-01-25-event-bus-asyncio-python/view)  
16. browser-use/bubus: Production-ready python event bus ... \- GitHub, acessado em março 22, 2026, [https://github.com/browser-use/bubus](https://github.com/browser-use/bubus)  
17. CRDT and SQLite: Local-First Value Synchronization \- Hacker News, acessado em março 22, 2026, [https://news.ycombinator.com/item?id=45527840](https://news.ycombinator.com/item?id=45527840)  
18. Building a Custom Python Notification System for System Events \- Python in Plain English, acessado em março 22, 2026, [https://python.plainenglish.io/building-a-custom-python-notification-system-for-system-events-b2835e83e85b](https://python.plainenglish.io/building-a-custom-python-notification-system-for-system-events-b2835e83e85b)  
19. How to de-couple your business logic by writing a simple EventBus module | Ndifreke Ekott, acessado em março 22, 2026, [https://ndifreke-ekott.com/posts/how-to-decouple-your-business-logic-using-eventbus/](https://ndifreke-ekott.com/posts/how-to-decouple-your-business-logic-using-eventbus/)  
20. Simple Yet Powerful: Building an In-Memory Async Event Bus in Python | by Kuba Szwajka, acessado em março 22, 2026, [https://python.plainenglish.io/simple-yet-powerful-building-an-in-memory-async-event-bus-in-python-f87e3d505bdd](https://python.plainenglish.io/simple-yet-powerful-building-an-in-memory-async-event-bus-in-python-f87e3d505bdd)  
21. Decoupled Modules with Elixir EventBus | by Mustafa Turan | ElixirLabs \- Medium, acessado em março 22, 2026, [https://medium.com/elixirlabs/decoupled-modules-with-elixir-eventbus-a709b1479411](https://medium.com/elixirlabs/decoupled-modules-with-elixir-eventbus-a709b1479411)  
22. FLET VS KIVY: WHICH ONE SHOULD YOU USE FOR YOUR NEXT PYTHON GUI APP, acessado em março 22, 2026, [https://dev.to/arseytech/flet-vs-kivy-which-one-should-you-use-for-your-next-python-gui-app-2ak4](https://dev.to/arseytech/flet-vs-kivy-which-one-should-you-use-for-your-next-python-gui-app-2ak4)  
23. 9 Python GUI Libraries to Build Modern Applications | by James Miller | Medium, acessado em março 22, 2026, [https://medium.com/@james.miller941/9-python-gui-libraries-to-build-modern-applications-2c04396b11d8](https://medium.com/@james.miller941/9-python-gui-libraries-to-build-modern-applications-2c04396b11d8)  
24. GNOME Builder: Using Python, Libadwaita and Blueprint | by codenomad \- Medium, acessado em março 22, 2026, [https://medium.com/@codenomad/gnome-builder-using-python-libadwaita-and-blueprint-c9c3e138801e](https://medium.com/@codenomad/gnome-builder-using-python-libadwaita-and-blueprint-c9c3e138801e)  
25. Will System76 develop a library like libadwaita and Granite? : r/pop\_os \- Reddit, acessado em março 22, 2026, [https://www.reddit.com/r/pop\_os/comments/s6nx5t/will\_system76\_develop\_a\_library\_like\_libadwaita/](https://www.reddit.com/r/pop_os/comments/s6nx5t/will_system76_develop_a_library_like_libadwaita/)  
26. Will the new COSMIC DE utilize QT apps instead of libadwaita GTK apps? \- Reddit, acessado em março 22, 2026, [https://www.reddit.com/r/pop\_os/comments/143im8n/will\_the\_new\_cosmic\_de\_utilize\_qt\_apps\_instead\_of/](https://www.reddit.com/r/pop_os/comments/143im8n/will_the_new_cosmic_de_utilize_qt_apps_instead_of/)  
27. Build a Habit Tracker with Python and AI: A Modular Approach to Wellness and Balance, acessado em março 22, 2026, [https://python.plainenglish.io/build-a-habit-tracker-with-python-and-ai-a-modular-approach-to-wellness-and-balance-1431c584eab0](https://python.plainenglish.io/build-a-habit-tracker-with-python-and-ai-a-modular-approach-to-wellness-and-balance-1431c584eab0)  
28. Automating Your Digital Morning Routine with Python \- Towards Data Science, acessado em março 22, 2026, [https://towardsdatascience.com/automating-your-digital-morning-routine-with-python-8387fe884422/](https://towardsdatascience.com/automating-your-digital-morning-routine-with-python-8387fe884422/)  
29. Please don't use LibAdwaita library \#5301 \- GitHub, acessado em março 22, 2026, [https://github.com/xournalpp/xournalpp/discussions/5301](https://github.com/xournalpp/xournalpp/discussions/5301)  
30. Behavior science led technology for financial wellness \- PMC \- NIH, acessado em março 22, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8328350/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8328350/)  
31. Behavioral Finance Apps: 8 Tools That Fix Bad Money Habits (2026) \- Whistl, acessado em março 22, 2026, [https://www.whistl.app/blog-behavioral-finance-apps-complete-guide-2026.html](https://www.whistl.app/blog-behavioral-finance-apps-complete-guide-2026.html)  
32. Nudging: Progress to date and future directions \- PMC \- NIH, acessado em março 22, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7946162/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7946162/)  
33. IoT-Enabled Digital Nudge Architecture for Sustainable Energy Behavior: An SEM-PLS Approach \- MDPI, acessado em março 22, 2026, [https://www.mdpi.com/2227-7080/13/11/504](https://www.mdpi.com/2227-7080/13/11/504)  
34. Insights from Behavioral Economics for Personal Finance \- Federal Reserve Bank of New York, acessado em março 22, 2026, [https://www.newyorkfed.org/medialibrary/media/banking/MeierSlides\_NYU.pdf](https://www.newyorkfed.org/medialibrary/media/banking/MeierSlides_NYU.pdf)  
35. Behavioral Economics and Your Money Habits \- Harvard Federal Credit Union, acessado em março 22, 2026, [https://harvardfcu.org/blog/behavioral-economics/](https://harvardfcu.org/blog/behavioral-economics/)  
36. Applying Behavioral Economics to Reduce Online Impulse Spending: A Case Study of the “Stop Impulse Buying” App \- ScienceOpen, acessado em março 22, 2026, [https://www.scienceopen.com/hosted-document?doi=10.14293/P2199-8442.1.SOP-.PWLXCL.v1](https://www.scienceopen.com/hosted-document?doi=10.14293/P2199-8442.1.SOP-.PWLXCL.v1)  
37. “AI for Daily Nudging: How Micro-Behavior Recommendations Are Transforming Health, Finance & Education” | by Tarush Sharma | Medium, acessado em março 22, 2026, [https://medium.com/@dutttarush9360/ai-for-daily-nudging-how-micro-behavior-recommendations-are-transforming-health-finance-5fc69aae5c17](https://medium.com/@dutttarush9360/ai-for-daily-nudging-how-micro-behavior-recommendations-are-transforming-health-finance-5fc69aae5c17)  
38. Website Blocker Using Python \- GeeksforGeeks, acessado em março 22, 2026, [https://www.geeksforgeeks.org/python/website-blocker-using-python/](https://www.geeksforgeeks.org/python/website-blocker-using-python/)  
39. Python Website Blocker with GUI \- TechVidvan, acessado em março 22, 2026, [https://techvidvan.com/tutorials/python-website-blocker/](https://techvidvan.com/tutorials/python-website-blocker/)  
40. Website Blocker using python \- Skyfi Labs, acessado em março 22, 2026, [https://www.skyfilabs.com/project-ideas/website-blocker-using-python](https://www.skyfilabs.com/project-ideas/website-blocker-using-python)  
41. GitHub \- luna-system/ada: locally hosted neural net chat framework with biomimetic RAG (cc0) (by luna+ada) (\<3), acessado em março 22, 2026, [https://github.com/luna-system/ada](https://github.com/luna-system/ada)  
42. Local LLM with MCP Tools \- Complete ... · LobeHub, acessado em março 22, 2026, [https://lobehub.com/mcp/abhimanyu07-local\_mcp](https://lobehub.com/mcp/abhimanyu07-local_mcp)  
43. How to Integrate Local LLMs With Ollama and Python, acessado em março 22, 2026, [https://realpython.com/ollama-python/](https://realpython.com/ollama-python/)  
44. Automate vs. Tasker? \- Google Groups, acessado em março 22, 2026, [https://groups.google.com/g/automate-user/c/wknDtmjlt7w](https://groups.google.com/g/automate-user/c/wknDtmjlt7w)  
45. Top Android Automation Apps of 2024: Boost Productivity with Tasker, MacroDroid & Automate \- UBOS.tech, acessado em março 22, 2026, [https://ubos.tech/news/top-android-automation-apps-of-2024-boost-productivity-with-tasker-macrodroid-automate/](https://ubos.tech/news/top-android-automation-apps-of-2024-boost-productivity-with-tasker-macrodroid-automate/)  
46. Tasker Vs Automate Vs IFTTT | SaveMyLeads, acessado em março 22, 2026, [https://savemyleads.com/blog/other/tasker-vs-automate-vs-ifttt](https://savemyleads.com/blog/other/tasker-vs-automate-vs-ifttt)  
47. \[How To\] Utilize Shizuku to run ADB shell commands (without intermediate apps) \- Reddit, acessado em março 22, 2026, [https://www.reddit.com/r/tasker/comments/1l1ynue/how\_to\_utilize\_shizuku\_to\_run\_adb\_shell\_commands/](https://www.reddit.com/r/tasker/comments/1l1ynue/how_to_utilize_shizuku_to_run_adb_shell_commands/)  
48. \[How To\] Block network access for apps with ADB Wifi or Shizuku : r/tasker \- Reddit, acessado em março 22, 2026, [https://www.reddit.com/r/tasker/comments/1mxjnvs/how\_to\_block\_network\_access\_for\_apps\_with\_adb/](https://www.reddit.com/r/tasker/comments/1mxjnvs/how_to_block_network_access_for_apps_with_adb/)  
49. How to freeze unwanted apps and bloatware on your Android, acessado em março 22, 2026, [https://www.androidpolice.com/shizuku-freeze-unwanted-system-apps-bloatware/](https://www.androidpolice.com/shizuku-freeze-unwanted-system-apps-bloatware/)  
50. \[Tasks\] Use the built in firewall to block/enable apps network access : r/tasker \- Reddit, acessado em março 22, 2026, [https://www.reddit.com/r/tasker/comments/1puspeh/tasks\_use\_the\_built\_in\_firewall\_to\_blockenable/](https://www.reddit.com/r/tasker/comments/1puspeh/tasks_use_the_built_in_firewall_to_blockenable/)  
51. How to install Python environment on Pop\!\_OS? \- Tencent Cloud, acessado em março 22, 2026, [https://www.tencentcloud.com/techpedia/102296](https://www.tencentcloud.com/techpedia/102296)  
52. LLM with Ollama Python Library | Data-Driven Engineering \- APMonitor, acessado em março 22, 2026, [https://apmonitor.com/dde/index.php/Main/LargeLanguageModel](https://apmonitor.com/dde/index.php/Main/LargeLanguageModel)  
53. Python Integration | Local LLMs on Raspberry Pi \- Adafruit Learning System, acessado em março 22, 2026, [https://learn.adafruit.com/local-llms-on-raspberry-pi/ollama-python-integration](https://learn.adafruit.com/local-llms-on-raspberry-pi/ollama-python-integration)  
54. Multi-Tenant Database Architecture Patterns Explained \- Bytebase, acessado em março 22, 2026, [https://www.bytebase.com/blog/multi-tenant-database-architecture-patterns-explained/](https://www.bytebase.com/blog/multi-tenant-database-architecture-patterns-explained/)
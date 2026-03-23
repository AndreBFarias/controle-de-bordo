# **Controle de Bordo: Arquitetura de um Ecossistema de Automação Pessoal Baseado em Python e Inteligência Artificial**

A convergência entre a inteligência artificial generativa e a automação de sistemas locais permitiu a emergência de uma nova categoria de software: o Life Operating System (Life OS). O projeto Controle de Bordo é concebido como um sistema nervoso digital centralizado, desenvolvido em Python, cujo objetivo é integrar de forma profunda dispositivos móveis, sistemas operacionais de desktop, finanças pessoais e metas de longo prazo. Através de uma arquitetura modular, o sistema visa a automação de decisões e a criação de hábitos automáticos, minimizando a carga cognitiva do usuário e maximizando a progressão em direção a objetivos complexos, como o aprendizado de idiomas, a escrita literária e a gestão de saúde biopsicossocial.

## **Arquitetura de Sistemas e Engine Central em Python**

O motor do Controle de Bordo é estruturado sobre princípios de engenharia de software que priorizam a modularidade e a interoperabilidade. Diferente de aplicações monolíticas, este sistema utiliza um barramento de eventos assíncrono que permite a comunicação entre scripts de automação, APIs de terceiros e agentes de inteligência artificial.1 O uso de Python como linguagem central justifica-se pela sua vasta biblioteca de integrações e pela facilidade de comunicação com frameworks de IA modernos.2

### **Componentes de Interface e Gestão de Fluxo**

Para a interface de controle, o projeto adota o framework Typer, que transforma funções Python em interfaces de linha de comando (CLI) profissionais com validação de tipos e geração automática de ajuda.3 A visualização do status do sistema e o monitoramento de processos de automação em tempo real são realizados através da biblioteca Rich, que permite a criação de dashboards no terminal com tabelas formatadas, logs coloridos e barras de progresso dinâmicas.3 Essa abordagem reduz a fadiga mental ao fornecer uma visão clara do progresso das metas sem a necessidade de interfaces gráficas pesadas.

A gestão de dados e o processamento de grandes volumes de informações (como logs de transações bancárias ou métricas de saúde) utilizam a biblioteca Polars. Escrita em Rust e com suporte a processamento paralelo, o Polars oferece uma performance superior ao Pandas em scripts que rodam continuamente no background.3 Para a monitoração do sistema de arquivos — essencial para o módulo de escrita do livro e organização de projetos — a biblioteca Watchdog é empregada para disparar eventos automaticamente sempre que um arquivo é criado ou modificado.3

| Componente | Biblioteca Python | Função Técnica no Projeto |
| :---- | :---- | :---- |
| Interface CLI | Typer | Execução de comandos e parametrização de ações. |
| Dashboard Terminal | Rich | Monitoramento visual de metas e logs de sistema. |
| Processamento de Dados | Polars | Análise de gastos e métricas de produtividade. |
| Monitoramento de Arquivos | Watchdog | Trigger para automação de escrita e organização. |
| Orquestração de Tarefas | Chronos Engine | Agendamento e execução de workflows complexos.1 |

## **Integração com Pop\!\_OS e Automação de Desktop**

O Controle de Bordo é otimizado para o Pop\!\_OS, aproveitando as capacidades do GNOME Shell e as interfaces de comunicação do sistema Linux para gerenciar o ambiente de trabalho e mitigar distrações.

### **Comunicação via DBus e GNOME Shell**

A integração profunda com o Pop\!\_OS é realizada através do DBus (Desktop Bus), permitindo que o script Python interaja com serviços do sistema operacional.4 Utilizando bibliotecas como dasbus ou pydbus, o Controle de Bordo pode monitorar o estado do computador e automatizar mudanças de contexto baseadas no horário ou na atividade detectada.5

Através do DBus, o sistema pode:

1. **Monitorar Teclas de Mídia**: Interceptar eventos de teclado para registrar tempos de foco ou disparar comandos de voz para a Luna.6  
2. **Gerenciar Notificações**: Enviar alertas críticos diretamente para o GNOME Shell ou silenciar aplicativos distrativos durante sessões de estudo de inglês.7  
3. **Controle de Energia e Sessão**: Alterar perfis de energia via system76-power ou bloquear a tela para forçar pausas de descompressão, visando a melhoria do estresse.8

A interface de tiling do Pop Shell é configurada programaticamente via gsettings. O script Python pode reorganizar janelas automaticamente para o "Modo Escritor" (focando o editor de texto e desativando o navegador) ou para o "Modo Estudo" (abrindo o Duolingo e materiais de referência).10

### **Bloqueio de Distrações em Nível de Sistema**

Para evitar compras impulsivas e o uso de redes sociais, o Controle de Bordo implementa um bloqueador de sites que manipula o arquivo /etc/hosts do Linux. Ao redirecionar domínios indesejados para o endereço de localhost (127.0.0.1), o sistema impede o acesso em nível de rede, independentemente do navegador utilizado.12

O script Python é configurado para rodar como um serviço do systemd, garantindo que as regras de bloqueio sejam aplicadas automaticamente no boot e ajustadas conforme a agenda do usuário.4

## **Ecossistema Mobile e Automação Android via Python**

O dispositivo móvel é frequentemente o ponto de maior distração e o local onde ocorrem as decisões de compra impulsiva. O Controle de Bordo integra o smartphone Android à rotina através de uma ponte de comunicação bidirecional.

### **Controle Programático via ADB**

O uso do Android Debug Bridge (ADB) permite que o sistema Controle de Bordo envie comandos de baixo nível para o dispositivo via rede sem fio (TCP/IP).14 Através de sockets em Python, o sistema pode injetar eventos de toque, abrir ou fechar aplicativos e monitorar o estado da tela.14 Esta capacidade é fundamental para o mecanismo de interdição de compras: se o sistema detectar que o usuário abriu um app de compras em um horário de foco ou sem orçamento disponível, ele pode injetar um comando de "Home" ou "Back" para encerrar a atividade imediatamente.15

### **Notificações Acionáveis e Feedback de Hábitos**

Para garantir que o usuário mantenha o foco em suas metas pessoais, o sistema utiliza notificações acionáveis no Android. Através de ferramentas como android-notify ou APIs de push como Simplepush, o Controle de Bordo envia mensagens que exigem uma resposta ativa do usuário.16

| Tipo de Notificação | Gatilho | Ação do Usuário |
| :---- | :---- | :---- |
| Confirmação de Hábito | Final de uma sessão de exercício. | "Concluído" / "Adiado". |
| Alerta de Compra | Detecção de transação no Nubank. | "Necessário" / "Impulso". |
| Lembrete de Estudo | 24h sem atividade no Duolingo. | Abrir app imediatamente. |
| Gestão de Estresse | Frequência cardíaca elevada (Google Fit). | Iniciar 5 min de respiração. |

Essas notificações permitem que o sistema funcione como um "companheiro de bordo" que monitora o progresso e intervém quando os hábitos automáticos negativos começam a se manifestar.18

## **Gestão Financeira: Open Finance e Controle de Impulsos no Brasil**

A integração bancária é o pilar de sustentabilidade do projeto. O Controle de Bordo utiliza o ecossistema de Open Finance do Brasil para monitorar gastos e automatizar a disciplina financeira.

### **Agregação via Belvo e Pluggy**

Plataformas de agregação como Belvo e Pluggy fornecem APIs unificadas que permitem ao script Python acessar dados de transações, faturas de cartão de crédito e saldos de contas bancárias de instituições como o Nubank.19 O processo de integração segue as normas do Banco Central do Brasil (BCB), utilizando protocolos de segurança FAPI1 e OAuth 2.0 para garantir a integridade dos dados.21

Uma vez obtido o consentimento, o sistema recupera automaticamente o histórico de faturas e transações em tempo real via webhooks.19 Isso permite que o Controle de Bordo identifique uma compra segundos após ela ocorrer, permitindo uma intervenção imediata da IA Luna.

### **O Algoritmo de Prevenção de Compras Fúteis**

O Controle de Bordo implementa mecanismos psicológicos de atraso (delay mechanisms) para combater o imediatismo. A IA Luna atua como um filtro crítico, analisando cada tentativa de compra com base nas metas de longo prazo (como a viagem para fora).

1. **Regra das 24 Horas**: Para qualquer item não essencial detectado em apps de compras, o sistema introduz uma fricção deliberada, exigindo que o usuário espere 24 horas antes de prosseguir. Isso permite que a dopamina inicial diminua, ativando o pensamento reflexivo do Sistema 2 em detrimento do impulso do Sistema 1\.23  
2. **Análise de Necessidade vs. Desejo**: A IA categoriza a compra. Se a categoria for "Lazer" ou "Eletrônicos" e o orçamento de reserva para a viagem estiver abaixo da meta mensal, o sistema dispara um alerta de "conflito de objetivos".  
3. **Fricção Automatizada**: O sistema pode ser programado para ocultar virtualmente os dados do cartão de crédito ou fechar apps de checkout se a meta de economia semanal não tiver sido atingida.14

## **Sincronização de Vida para Casais e Rotinas Compartilhadas**

O projeto considera o cenário de duas pessoas que residem juntas e compartilham rotinas. Para isso, a arquitetura deve suportar o estado compartilhado e a sincronização multi-usuário.

### **Backend com Supabase e RLS**

O Supabase (baseado em PostgreSQL) é utilizado como o backend de sincronização. Ele permite que dados pessoais permaneçam privados enquanto metas comuns são compartilhadas através de tabelas com Row Level Security (RLS).25

A estrutura de dados para o casal inclui:

* **Tabela de Orçamento Compartilhado**: Onde ambos registram gastos fixos e planejam a reserva para a viagem.27  
* **Sincronização de Calendário**: Integração com Microsoft Graph para evitar conflitos de horários e identificar janelas para exercícios físicos conjuntos.7  
* **Habit Tracking Espelhado**: Módulos que permitem que um usuário veja o progresso do outro, criando um ambiente de accountability mútua.29

A sincronização de rotinas é fundamental para o sucesso de hábitos de saúde e alimentação. O sistema pode, por exemplo, sugerir um cardápio semanal (Cycle Menu) que atenda aos objetivos nutricionais de ambos, enviando notificações simultâneas às 09:00 sobre o preparo das refeições.31

## **Convergência de Metas: Inglês, Viagens, Escrita e Saúde**

O Controle de Bordo não é apenas um sistema de monitoramento, mas um acelerador de sonhos. Cada objetivo principal possui um módulo dedicado que se interliga com os outros.

### **Aprendizado de Inglês e Gamificação**

O módulo de estudos integra-se com a API não oficial do Duolingo para monitorar streaks e vocabulário aprendido.32 O sistema utiliza o conceito de "bloqueio condicional": o acesso a aplicativos de entretenimento ou redes sociais no celular e no Pop\!\_OS pode ser restrito até que a meta diária de lições de inglês seja verificada.34

Para o objetivo de viajar para fora, a IA Luna pode gerar exercícios contextuais de inglês baseados no destino escolhido, integrando o aprendizado com o planejamento da viagem.

### **Módulo de Saúde e Gestão de Estresse**

A integração com o Google Fit fornece métricas em tempo real de passos, sono e frequência cardíaca.36 O Controle de Bordo processa esses dados para ajustar a rotina de exercícios.

![][image1]  
Se o sistema detectar, via Microsoft Teams e Graph API, uma carga de reuniões excessiva ou picos de frequência cardíaca durante o horário comercial, ele automaticamente sugere uma redução na intensidade do treino noturno ou uma sessão de meditação para controle de cortisol.7

### **Pipeline de Escrita de Livro e Criatividade**

Para o objetivo de criar um livro, o sistema monitora um diretório de arquivos Markdown. A biblioteca Watchdog detecta a inatividade prolongada e envia lembretes para o celular.3 A IA Luna atua como uma editora assistente, analisando a contagem de palavras diárias e oferecendo insights sobre a estrutura narrativa através de sub-agentes especializados.39

O sistema também automatiza o backup desses arquivos para repositórios privados no GitHub ou instâncias do Supabase, garantindo a preservação da obra.1

## **Transição para a Inteligência Artificial Luna**

Embora o desenvolvimento inicial utilize os modelos Claude da Anthropic pela sua excelência em lógica de programação e raciocínio sistêmico, o projeto visa a transição para a assistente Luna como uma interface local e proativa.

### **Raciocínio de Agentes e Outcome Engineering**

A arquitetura da Luna baseia-se em "Outcome Engineering", onde o foco não é apenas responder a perguntas, mas executar tarefas de forma autônoma para atingir um resultado.41 Através do uso de frameworks como LangChain e LangGraph, a Luna pode coordenar múltiplos agentes para, por exemplo, pesquisar passagens aéreas para a viagem, verificar o saldo bancário e sugerir a melhor data de compra.42

A Luna opera em três camadas:

1. **Camada de Percepção**: Ouve comandos de voz (Pyttsx3) e monitora eventos do sistema (DBus/ADB).44  
2. **Camada de Raciocínio**: Utiliza modelos como LLaMA 3.1 ou Claude para processar o contexto e tomar decisões baseadas em regras pré-definidas.39  
3. **Camada de Ação**: Executa comandos no Pop\!\_OS, envia notificações mobile ou realiza transações via APIs financeiras.1

### **Engenharia de Contexto e Eficiência**

Para que a Luna seja eficiente em um ambiente doméstico, ela utiliza técnicas de compressão de contexto e armazenamento de memória de longo prazo no Supabase.46 Isso permite que ela se lembre de preferências passadas, como o nível de estresse do usuário na semana anterior ou os gastos habituais em certas categorias, tornando a automação cada vez mais personalizada e "invisível".48

## **Melhoria do Estresse, Exercícios e Cuidados com a Aparência**

A gestão da vida pessoal é tratada como um problema de otimização de recursos. O sistema busca automatizar as decisões de baixo valor para que o usuário possa focar no que é criativo e emocionalmente gratificante.

### **Automação de Rotinas de Cuidado Pessoal**

O módulo de aparência e autocuidado rastreia o uso de produtos e agenda compromissos de forma proativa. Integrado à agenda do Teams e do e-mail, ele identifica as melhores janelas de tempo para atividades que melhorem a autoestima, garantindo que essas tarefas não sejam negligenciadas pela rotina de trabalho.7

A prática de exercícios é monitorada pelo Google Fit, mas incentivada pela Luna através de recompensas digitais ou sociais.36 Se o casal completar a meta semanal de exercícios, o sistema pode, por exemplo, "desbloquear" um orçamento extra para uma refeição fora ou uma atividade de lazer no final de semana, reforçando positivamente o hábito.

### **Gestão Biopsicossocial e Redução da Carga Mental**

A grande inovação do Controle de Bordo é a sua capacidade de agir sem que o usuário precise pensar. Ao automatizar a proibição de compras inúteis, a organização da agenda e o monitoramento de metas de estudo, o sistema elimina a necessidade de "força de vontade" constante. A disciplina é terceirizada para o código, permitindo que a mente humana se concentre na execução de seus sonhos — o aprendizado do inglês, a viagem internacional e a escrita do livro.

O projeto Controle de Bordo representa, portanto, a evolução da produtividade: de ferramentas que apenas registram o que fizemos para sistemas que nos ajudam a ser quem queremos ser, através da integração inteligente de tecnologia e psicologia comportamental.

| Meta | Indicador de Progresso (KPI) | Mecanismo de Automação |
| :---- | :---- | :---- |
| Aprender Inglês | Streak do Duolingo e Vocabulário. | Bloqueio de entretenimento condicional.34 |
| Viajar para Fora | Saldo em conta de reserva. | Desvio automático de economias de "não compra".19 |
| Criar um Livro | Word count diário em Markdown. | Notificações de inatividade via Watchdog.3 |
| Melhorar Estresse | Variabilidade da Frequência Cardíaca. | Bloqueio de notificações de trabalho e sugestão de pausas.37 |
| Praticar Exercícios | Minutos ativos semanais. | Sincronização de agenda de casal no MS Teams.7 |
| Cuidar da Aparência | Frequência de rotinas de cuidado. | Agendamento proativo em janelas de tempo livre.31 |

Este sistema operacional de vida, operando silenciosamente no Pop\!\_OS e no celular, cria um trilho para o sucesso, transformando a complexidade da vida moderna em uma sequência de progressos incrementais e automatizados.

#### **Referências citadas**

1. life-os · GitHub Topics, acessado em março 22, 2026, [https://github.com/topics/life-os](https://github.com/topics/life-os)  
2. Luna, your AI personal assistant | IE University, acessado em março 22, 2026, [https://www.ie.edu/university/studies/projects/luna-your-ai-personal-assistant/](https://www.ie.edu/university/studies/projects/luna-your-ai-personal-assistant/)  
3. 5 Python Libraries That Saved Me Hours Every Week | by Arslan Qutab \- Medium, acessado em março 22, 2026, [https://medium.com/@arslanshoukatali/5-python-libraries-that-saved-me-hours-every-week-296d6b7e3fa3](https://medium.com/@arslanshoukatali/5-python-libraries-that-saved-me-hours-every-week-296d6b7e3fa3)  
4. Talking to systemd Through dbus with Python \- Thomas Stringer, acessado em março 22, 2026, [https://trstringer.com/python-systemd-dbus/](https://trstringer.com/python-systemd-dbus/)  
5. DbusExamples \- Python Wiki, acessado em março 22, 2026, [https://wiki.python.org/moin/DbusExamples](https://wiki.python.org/moin/DbusExamples)  
6. How do you listen for Mediakey events under gnome 3 using python? \- Stack Overflow, acessado em março 22, 2026, [https://stackoverflow.com/questions/18981190/how-do-you-listen-for-mediakey-events-under-gnome-3-using-python](https://stackoverflow.com/questions/18981190/how-do-you-listen-for-mediakey-events-under-gnome-3-using-python)  
7. Microsoft Graph API- a practical example in python \- fme AG, acessado em março 22, 2026, [https://en.fme.de/blog/microsoft-graph-api-a-practical-example-in-python/](https://en.fme.de/blog/microsoft-graph-api-a-practical-example-in-python/)  
8. Using Legacy Status Icons in Pop\!\_OS \- System76 Support, acessado em março 22, 2026, [https://support.system76.com/articles/status-icons/](https://support.system76.com/articles/status-icons/)  
9. GNOME Extensions \- Pop\!\_OS Documentation, acessado em março 22, 2026, [https://pop-os.github.io/docs/customize-pop/gnome-tweaks-extensions/gnome-extensions.html](https://pop-os.github.io/docs/customize-pop/gnome-tweaks-extensions/gnome-extensions.html)  
10. Using Pop Shell on other GNOME Desktops \- System76 Support, acessado em março 22, 2026, [https://support.system76.com/articles/pop-shell/](https://support.system76.com/articles/pop-shell/)  
11. pop-os/shell: Pop\!\_OS Shell \- GitHub, acessado em março 22, 2026, [https://github.com/pop-os/shell](https://github.com/pop-os/shell)  
12. Website Blocker Using Python \- GeeksforGeeks, acessado em março 22, 2026, [https://www.geeksforgeeks.org/python/website-blocker-using-python/](https://www.geeksforgeeks.org/python/website-blocker-using-python/)  
13. How to build website blocker in Python \- DEV Community, acessado em março 22, 2026, [https://dev.to/kalebu/how-to-build-website-blocker-in-python-a3f](https://dev.to/kalebu/how-to-build-website-blocker-in-python-a3f)  
14. Automated Control of an Android Device with Python \- Dustin Ingram, acessado em março 22, 2026, [https://dustingram.com/articles/2010/06/18/automated-control-of-an-android-device-with-python/](https://dustingram.com/articles/2010/06/18/automated-control-of-an-android-device-with-python/)  
15. Looking to automate an Android app using Python \- advice on where to begin? \- Reddit, acessado em março 22, 2026, [https://www.reddit.com/r/learnpython/comments/4lvqmf/looking\_to\_automate\_an\_android\_app\_using\_python/](https://www.reddit.com/r/learnpython/comments/4lvqmf/looking_to_automate_an_android_app_using_python/)  
16. android-notify 1.50 \- PyPI, acessado em março 22, 2026, [https://pypi.org/project/android-notify/1.50/](https://pypi.org/project/android-notify/1.50/)  
17. Actionable Notification with Callback in Python \- Simplepush, acessado em março 22, 2026, [https://simplepush.io/blog/actionable-push-notifications-with-python](https://simplepush.io/blog/actionable-push-notifications-with-python)  
18. Fector101/android\_notify: A Python package for effortlessly creating and managing Android notifications. \- GitHub, acessado em março 22, 2026, [https://github.com/Fector101/android\_notify](https://github.com/Fector101/android_notify)  
19. Banking Aggregation Overview (Brazil) \- Belvo Developer Portal, acessado em março 22, 2026, [https://developers.belvo.com/products/aggregation\_brazil/aggregation-brazil-introduction](https://developers.belvo.com/products/aggregation_brazil/aggregation-brazil-introduction)  
20. NewTech Friday: Pluggy – a single API to power open banking in Brazil \- Gávea Angels, acessado em março 22, 2026, [https://gaveaangels.org/newtech-friday-pluggy-a-single-api-to-power-open-banking-in-brazil/](https://gaveaangels.org/newtech-friday-pluggy-a-single-api-to-power-open-banking-in-brazil/)  
21. Open Finance \- Banco Central do Brasil, acessado em março 22, 2026, [https://www.bcb.gov.br/en/financialstability/open\_finance](https://www.bcb.gov.br/en/financialstability/open_finance)  
22. Open Finance Brasil \- Ozone API, acessado em março 22, 2026, [https://ozoneapi.com/the-open-finance-tracker/library/open-finance-brasil/](https://ozoneapi.com/the-open-finance-tracker/library/open-finance-brasil/)  
23. What Psychological Techniques Can Individuals Use to Introduce a Delay between Impulse and Digital Purchase? \- Lifestyle → Sustainability Directory, acessado em março 22, 2026, [https://lifestyle.sustainability-directory.com/learn/what-psychological-techniques-can-individuals-use-to-introduce-a-delay-between-impulse-and-digital-purchase/](https://lifestyle.sustainability-directory.com/learn/what-psychological-techniques-can-individuals-use-to-introduce-a-delay-between-impulse-and-digital-purchase/)  
24. What Psychological Mechanisms Make the 30-Day Rule Effective against Impulse? → Learn, acessado em março 22, 2026, [https://lifestyle.sustainability-directory.com/learn/what-psychological-mechanisms-make-the-30-day-rule-effective-against-impulse/](https://lifestyle.sustainability-directory.com/learn/what-psychological-mechanisms-make-the-30-day-rule-effective-against-impulse/)  
25. Shared Responsibility Model | Supabase Docs, acessado em março 22, 2026, [https://supabase.com/docs/guides/deployment/shared-responsibility-model](https://supabase.com/docs/guides/deployment/shared-responsibility-model)  
26. Use Supabase with Python, acessado em março 22, 2026, [https://supabase.com/docs/guides/getting-started/quickstarts/flask](https://supabase.com/docs/guides/getting-started/quickstarts/flask)  
27. Best practice for shared entities : r/Supabase \- Reddit, acessado em março 22, 2026, [https://www.reddit.com/r/Supabase/comments/1lt98xq/best\_practice\_for\_shared\_entities/](https://www.reddit.com/r/Supabase/comments/1lt98xq/best_practice_for_shared_entities/)  
28. Build Python apps with Microsoft Graph, acessado em março 22, 2026, [https://learn.microsoft.com/en-us/graph/tutorials/python](https://learn.microsoft.com/en-us/graph/tutorials/python)  
29. Habitsync \- Didier Marin, acessado em março 22, 2026, [https://didiermarin.com/projects/habitsync/](https://didiermarin.com/projects/habitsync/)  
30. jofoerster/habitsync: Self hosted Habit Tracker featuring goals and challenges with friends \- GitHub, acessado em março 22, 2026, [https://github.com/jofoerster/habitsync](https://github.com/jofoerster/habitsync)  
31. davorminchorov/lifeos: A vibe coded LifeOS project · GitHub \- GitHub, acessado em março 22, 2026, [https://github.com/davorminchorov/lifeos](https://github.com/davorminchorov/lifeos)  
32. duolingo-api 0.2 \- PyPI, acessado em março 22, 2026, [https://pypi.org/project/duolingo-api/0.2/](https://pypi.org/project/duolingo-api/0.2/)  
33. python-api-duolingo/duolingo.py at master · humbertodias/python-api-duolingo \- GitHub, acessado em março 22, 2026, [https://github.com/humbertodias/python-api-duolingo/blob/master/duolingo.py](https://github.com/humbertodias/python-api-duolingo/blob/master/duolingo.py)  
34. KartikTalwar/Duolingo: Unofficial Duolingo API Written in Python \- GitHub, acessado em março 22, 2026, [https://github.com/KartikTalwar/Duolingo](https://github.com/KartikTalwar/Duolingo)  
35. duolingo · GitHub Topics, acessado em março 22, 2026, [https://github.com/topics/duolingo?l=python\&o=desc\&s=stars](https://github.com/topics/duolingo?l=python&o=desc&s=stars)  
36. REST API | Google Fit, acessado em março 22, 2026, [https://developers.google.com/fit/rest](https://developers.google.com/fit/rest)  
37. Google Fit Integration in Android: Fitness Tracking, Health Data, & Custom Dashboard, acessado em março 22, 2026, [https://www.iflair.com/google-fit-integration-in-android-fitness-tracking-health-data-custom-dashboard/](https://www.iflair.com/google-fit-integration-in-android-fitness-tracking-health-data-custom-dashboard/)  
38. Scaling fraud defense: How Nubank evolved its risk analysis platform, acessado em março 22, 2026, [https://building.nubank.com/scaling-fraud-defense-how-nubank-evolved-its-risk-analysis-platform/](https://building.nubank.com/scaling-fraud-defense-how-nubank-evolved-its-risk-analysis-platform/)  
39. Luna AI \- The Ultimate Personal Assistant for AI Agents Hack with LabLab and Minds, acessado em março 22, 2026, [https://lablab.ai/ai-hackathons/ai-agents-hack-with-lablab-and-mindsdb/mediterranean-ai/luna-ai-the-ultimate-personal-assistant](https://lablab.ai/ai-hackathons/ai-agents-hack-with-lablab-and-mindsdb/mediterranean-ai/luna-ai-the-ultimate-personal-assistant)  
40. Python data loading with Supabase, acessado em março 22, 2026, [https://supabase.com/blog/loading-data-supabase-python](https://supabase.com/blog/loading-data-supabase-python)  
41. Claude Cowork: From Prompt Engineering to Outcome Engineering \- Medium, acessado em março 22, 2026, [https://medium.com/@kombib/outcome-engineering-ai-agents-d8627bc925cb](https://medium.com/@kombib/outcome-engineering-ai-agents-d8627bc925cb)  
42. Build a RAG agent with LangChain \- Docs by LangChain, acessado em março 22, 2026, [https://python.langchain.com/docs/tutorials/agents/](https://python.langchain.com/docs/tutorials/agents/)  
43. Agents \- Docs by LangChain, acessado em março 22, 2026, [https://docs.langchain.com/oss/python/langchain/agents](https://docs.langchain.com/oss/python/langchain/agents)  
44. AI Personal Assistant Python Script | PDF \- Scribd, acessado em março 22, 2026, [https://www.scribd.com/document/935543910/Luna](https://www.scribd.com/document/935543910/Luna)  
45. Deshan555/Python-ai-assistant: On-device Speech-to-Intent engine powered by deep learning \- GitHub, acessado em março 22, 2026, [https://github.com/Deshan555/Python-ai-assistant](https://github.com/Deshan555/Python-ai-assistant)  
46. Effective context engineering for AI agents \- Anthropic, acessado em março 22, 2026, [https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)  
47. LangChain Deep Agents: Build Agents for Complex, Multi-Step Tasks, acessado em março 22, 2026, [https://www.langchain.com/deep-agents](https://www.langchain.com/deep-agents)  
48. Prompting best practices \- Claude API Docs, acessado em março 22, 2026, [https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)  
49. awesome-claude-code-subagents/categories/05-data-ai/prompt-engineer.md at main \- GitHub, acessado em março 22, 2026, [https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/prompt-engineer.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/05-data-ai/prompt-engineer.md)  
50. Dashboard Analysis: Google Fit \- My exploration in data analytics \- WordPress.com, acessado em março 22, 2026, [https://sivaanalytics.wordpress.com/2016/01/28/dashboard-analysis-google-fit/](https://sivaanalytics.wordpress.com/2016/01/28/dashboard-analysis-google-fit/)

[image1]: <data:image/png;base64,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>
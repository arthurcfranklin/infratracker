# InfraTracker

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)
![License](https://img.shields.io/badge/Licença-MIT-green)

**Versão Atual:** v0.2.0-alpha

---

## 📖 Sobre o Projeto

O InfraTrack é uma plataforma web voltada ao inventário e monitoramento de infraestrutura de TI.

O projeto tem como objetivo centralizar informações de ativos, disponibilizar consultas operacionais por meio de dashboard web e evoluir para uma solução capaz de monitorar disponibilidade, registrar eventos e gerar relatórios operacionais.

Desenvolvido utilizando FastAPI, SQLite e Bootstrap, o projeto simula cenários encontrados em ambientes corporativos, servindo como laboratório prático para estudos em infraestrutura, monitoramento, automação e desenvolvimento de soluções para gestão de ambientes de TI.

---

## ✨ Funcionalidades Atuais

### Inventário de Ativos

* Cadastro de ativos
* Edição de ativos
* Exclusão de ativos
* Associação de URL aos ativos
* Consulta de inventário

### Dashboard Web

* Interface responsiva
* Cards de indicadores
* Visualização centralizada dos ativos
* Pesquisa por ativos
* Ordenação de registros
* Filtro por status

### Validações

* Bloqueio de IP duplicado
* Bloqueio de hostname duplicado
* Normalização automática de hostname
* Tratamento de erros operacionais
* Feedback visual por modais

---

## 🎯 Objetivos

* Centralizar informações de ativos de TI
* Automatizar processos de inventário
* Monitorar disponibilidade de dispositivos
* Registrar eventos operacionais
* Disponibilizar informações por meio de dashboard web
* Evoluir para uma plataforma de observabilidade simplificada

---

## 🛠️ Tecnologias

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* Jinja2

### Versionamento

* Git
* GitHub

---

## 🏗️ Arquitetura

```text
Usuário
   │
   ▼
Dashboard Web
   │
   ▼
FastAPI
   │
   ├── Inventário de Ativos
   ├── Dashboard
   ├── Monitoramento
   └── Relatórios
   │
   ▼
SQLite
```

---

## 🗺️ Roadmap

### Fase 1 - Planejamento e Estruturação

* [x] Criação do repositório
* [x] Configuração inicial do projeto
* [x] Definição da arquitetura
* [x] Estruturação das pastas

### Fase 2 - Inventário de Ativos

* [x] Modelagem do banco de dados
* [x] Cadastro de ativos
* [x] Edição de ativos
* [x] Exclusão de ativos
* [x] Pesquisa de ativos
* [x] Filtro por status
* [x] Ordenação de registros
* [ ] Coleta automática de informações do sistema

### Fase 3 - Dashboard Web

* [x] Interface web
* [x] Visualização de ativos
* [x] Consulta de informações
* [x] Dashboard operacional

### Fase 4 - Monitoramento

* [ ] Monitoramento ICMP
* [ ] Histórico de disponibilidade
* [ ] Registro de eventos
* [ ] Latência dos ativos
* [ ] Verificação automática de status

---

## 📂 Estrutura do Projeto

```text
infratrack/
│
├── docs/
├── src/
│   ├── app/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   └── templates/
│
├── tests/
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 📈 Status do Projeto

🚧 Em desenvolvimento

**Fase atual:** Inventário de Ativos e Dashboard Web concluídos.

**Próximo marco:** Implementação do monitoramento ICMP e histórico de disponibilidade.

---

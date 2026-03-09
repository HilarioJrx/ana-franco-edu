# Ana Franco EDU

Portal institucional da **Escola Estadual Profª Ana Franco da Rocha Brando**.

Este projeto está sendo desenvolvido como parte da disciplina **Projeto Integrador I (UNIVESP)** e tem como objetivo centralizar informações institucionais da escola e facilitar alguns processos administrativos.

## Objetivos do sistema

O sistema pretende oferecer:

- Portal institucional da escola
- Publicação de notícias e comunicados
- Acesso a documentos institucionais
- Sistema de solicitação de uniformes
- Área administrativa para gestão de conteúdo

## Tecnologias utilizadas

- Python
- Django
- TailwindCSS
- SQLite (fase inicial)

Futuramente:

- MySQL
- Deploy em servidor web

## Estrutura do projeto

```shell
ana-franco-edu/

├── config/        # Configuração principal do Django  
├── core/          # Aplicação base do sistema  
├── theme/         # Configuração do TailwindCSS  

├── templates/     # Templates globais  
├── static/        # Arquivos estáticos  

├── manage.py  
└── README.md
```   

## Instalação do projeto

Clone o repositório:

```shell
git clone <url-do-repositorio>  
cd ana-franco-edu  
```

Crie o ambiente virtual:

```shell
python -m venv .venv
```

### Ative o ambiente virtual no:

- Bash e ZSH
    ```shell
    .\.venv\Scripts\activate
    ```
- Windows PowerShell:
    ```shell
    .\.venv\Scripts\Activate.ps1
    ```
- Cmd (Prompt de comando)
    ```shell
    .\.venv\Scripts\activate.bat
    ```

Instale as dependências:

```shell
pip install -r requirements.txt
```

## Rodando o projeto

Aplicar migrations:

```shell
python manage.py migrate
```

Iniciar servidor Django:

```shell
python manage.py runserver
```
Rodar Tailwind em desenvolvimento:

```shell
python manage.py tailwind start
```

Acesse no navegador: http://127.0.0.1:8000

## Usuário administrador padrão

O sistema cria automaticamente um usuário administrador:

usuario: admin  
senha: admin  

Acesso: http://127.0.0.1:8000/admin

## Estrutura planejada do sistema

Aplicações previstas:

- **core** – páginas institucionais
- **news** – notícias da escola
- **documents** – documentos institucionais
- **uniforms** – sistema de pedidos de uniformes
- **accounts** – usuários e permissões

## Autor

Projeto desenvolvido por:

Alunos do grupo 13 do Projeto Integrador I – UNIVESP (2026)

# 🔐 Template de Login Microsoft para Streamlit

Template reutilizável para criar aplicações Streamlit com autenticação Microsoft Azure AD.

## 📋 Pré-requisitos

- Python 3.8+
- Uma conta no [Azure Portal](https://portal.azure.com)
- Acesso para registrar aplicações no Microsoft Entra ID (antigo Azure AD)

## 🚀 Início Rápido

### 1. Clone ou copie este template

```bash
# Copie a pasta para seu novo projeto
cp -r streamlit-azure-login-template meu-novo-projeto
cd meu-novo-projeto
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais Azure

Execute o script de configuração interativo:

```bash
python configure_azure.py
```

O script irá:
- ✅ Solicitar o nome da sua aplicação no Streamlit Cloud
- ✅ Gerar automaticamente as URIs de redirecionamento (localhost + produção)
- ✅ Solicitar suas credenciais Azure
- ✅ Criar o arquivo `.streamlit/secrets.toml`
- ✅ Atualizar o `.gitignore`

### 4. Execute localmente

```bash
streamlit run app.py
```

---

## 🔧 Configuração Manual no Azure Portal

Se preferir configurar manualmente ou precisar de mais detalhes:

### Passo 1: Criar um Registro de Aplicativo

1. Acesse [portal.azure.com](https://portal.azure.com)
2. Navegue para **Microsoft Entra ID** > **Registros de aplicativo**
3. Clique em **+ Novo registro**
4. Preencha:
   - **Nome**: Nome da sua aplicação (ex: "Minha App Streamlit")
   - **Tipos de conta suportados**: "Contas somente neste diretório organizacional"
   - **URI de Redirecionamento**: Deixe vazio por enquanto
5. Clique em **Registrar**

### Passo 2: Copiar IDs

Na página de **Visão geral** da aplicação, copie:

| Campo PT-BR | Campo EN | Descrição |
|-------------|----------|-----------|
| ID do aplicativo (cliente) | Application (client) ID | Seu `client_id` |
| ID do diretório (locatário) | Directory (tenant) ID | Seu `tenant_id` |

### Passo 3: Criar Client Secret

1. No menu lateral, clique em **Certificados e segredos**
2. Clique em **+ Novo segredo do cliente**
3. Adicione uma descrição (ex: "Streamlit App")
4. Escolha a validade (recomendado: 24 meses)
5. Clique em **Adicionar**
6. **⚠️ IMPORTANTE**: Copie o **Valor** imediatamente (não será mostrado novamente!)

### Passo 4: Adicionar URIs de Redirecionamento

1. No menu lateral, clique em **Autenticação**
2. Clique em **+ Adicionar uma plataforma**
3. Selecione **Web**
4. Adicione as URIs:

```
http://localhost:8501
https://seu-app.streamlit.app
```

5. Clique em **Configurar**

> ⚠️ **IMPORTANTE**: Adicione AMBAS as URIs! A primeira é para desenvolvimento local, a segunda para produção.

### Passo 5: Configurar Permissões de API (Opcional)

Por padrão, a aplicação usa `User.Read` que permite obter nome e email do usuário.

Se precisar de mais permissões:
1. No menu lateral, clique em **Permissões de API**
2. Clique em **+ Adicionar uma permissão**
3. Selecione **Microsoft Graph**
4. Adicione as permissões necessárias

---

## 📁 Estrutura do Projeto

```
streamlit-azure-login-template/
├── .streamlit/
│   ├── secrets.toml          # Suas credenciais (NÃO commite!)
│   └── secrets.toml.example  # Template de referência
├── auth_microsoft.py         # Módulo de autenticação
├── app.py                    # Aplicação de demonstração
├── configure_azure.py        # Script de configuração
├── requirements.txt          # Dependências
├── .gitignore               # Ignora secrets.toml
└── README.md                # Este arquivo
```

---

## 🎨 Personalizando a Página de Login

Edite o dicionário `LOGIN_CONFIG` no arquivo `app.py`:

```python
LOGIN_CONFIG.update({
    "title": "Minha Aplicação",
    "subtitle": "Sistema de gestão corporativa",
    "badge_text": "Acesso Restrito Synvia",
    "email_domain": "@synvia.com",
    "highlights": [
        {
            "icon": "📊",
            "title": "Dashboards",
            "description": "Visualize métricas em tempo real"
        },
        # ... adicione mais itens
    ]
})
```

Para mudar as cores, edite as constantes no início de `auth_microsoft.py`:

```python
PRIMARY_COLOR = "#6BBF47"    # Verde principal
SECONDARY_COLOR = "#52B54B"  # Verde secundário
ACCENT_DARK = "#0F1C16"      # Cor escura
MUTED_TEXT = "#5B6770"       # Cor do texto secundário
```

---

## ☁️ Deploy no Streamlit Cloud

### 1. Prepare o repositório

Certifique-se de que `.streamlit/secrets.toml` está no `.gitignore`:

```bash
cat .gitignore
# Deve conter:
# .streamlit/secrets.toml
```

### 2. Faça push do código

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 3. Configure no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **New app**
3. Selecione seu repositório
4. Após deploy, vá em **Settings** > **Secrets**
5. Cole o conteúdo do seu `secrets.toml`:

```toml
[auth]
tenant_id = "seu-tenant-id"
client_id = "seu-client-id"
client_secret = "seu-client-secret"
redirect_uri_local = "http://localhost:8501"
redirect_uri_prod = "https://seu-app.streamlit.app"
scope = ["https://graph.microsoft.com/User.Read"]
```

6. Clique em **Save**

---

## 🔍 Troubleshooting

### Erro: "redirect_uri_mismatch"

A URI de redirecionamento não está cadastrada no Azure. Verifique:
1. Se AMBAS as URIs estão cadastradas (localhost e produção)
2. Se a URI está exatamente igual (sem barras extras no final)

### Erro: "invalid_client"

O Client Secret está incorreto ou expirou. Crie um novo segredo no Azure Portal.

### Erro: "AADSTS50011"

A URI de resposta não corresponde. Execute `python configure_azure.py` novamente e verifique as URIs geradas.

---

## 📞 Suporte

- **Documentação MSAL**: [msal-python.readthedocs.io](https://msal-python.readthedocs.io)
- **Microsoft Entra ID**: [docs.microsoft.com/azure/active-directory](https://docs.microsoft.com/azure/active-directory/)
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)

---

Desenvolvido com ❤️ para a Synvia

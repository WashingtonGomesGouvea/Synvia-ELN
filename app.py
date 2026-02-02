"""
Aplicação de Demonstração - Template Login Microsoft
Execute com: streamlit run app.py
"""

import streamlit as st
from auth_microsoft import (
    MicrosoftAuth,
    AuthManager,
    create_login_page,
    create_user_header,
    LOGIN_CONFIG
)

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA DE LOGIN (PERSONALIZE AQUI!)
# ============================================================================
LOGIN_CONFIG.update({
    "title": "Minha Aplicação",
    "subtitle": "Sistema de demonstração com login Microsoft",
    "badge_text": "Acesso Restrito",
    "email_domain": "@empresa.com",
    "highlights": [
        {
            "icon": "🔒",
            "title": "Segurança Integrada",
            "description": "Autenticação via Azure AD"
        },
        {
            "icon": "⚡",
            "title": "Acesso Rápido",
            "description": "Use sua conta Microsoft corporativa"
        },
        {
            "icon": "📊",
            "title": "Recursos Completos",
            "description": "Acesse todas as funcionalidades do sistema"
        }
    ]
})

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ============================================================================
st.set_page_config(
    page_title="Minha Aplicação",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# AUTENTICAÇÃO
# ============================================================================
auth = MicrosoftAuth()

# Tela de login (bloqueia execução se não autenticado)
if not create_login_page(auth, LOGIN_CONFIG):
    st.stop()

# Mostrar header do usuário na sidebar
create_user_header()

# Renovar token se necessário
AuthManager.check_and_refresh_token(auth)

# ============================================================================
# OBTER INFORMAÇÕES DO USUÁRIO
# ============================================================================
user = AuthManager.get_current_user()
user_name = user.get("displayName", "Usuário") if user else "Usuário"
user_email = user.get("mail") or user.get("userPrincipalName", "") if user else ""

# ============================================================================
# SUA APLICAÇÃO COMEÇA AQUI! 🚀
# ============================================================================

st.title("🎉 Bem-vindo!")
st.markdown(f"### Olá, **{user_name}**!")

st.success("✅ Login realizado com sucesso! Você pode começar a desenvolver sua aplicação.")

st.divider()

# Exemplo de conteúdo
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Usuário", user_name)

with col2:
    st.metric("Email", user_email.split("@")[0] if user_email else "N/A")

with col3:
    st.metric("Status", "Autenticado ✅")

st.divider()

# Informações de debug (remova em produção)
with st.expander("🔧 Informações de Debug"):
    st.json(user)

st.info("""
### Próximos Passos

1. **Personalize** o `LOGIN_CONFIG` no início deste arquivo
2. **Adicione** seu código abaixo da seção "SUA APLICAÇÃO COMEÇA AQUI!"
3. **Configure** as credenciais Azure com `python configure_azure.py`
4. **Faça deploy** no Streamlit Cloud

📖 Consulte o `README.md` para instruções detalhadas.
""")

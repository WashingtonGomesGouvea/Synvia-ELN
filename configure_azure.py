#!/usr/bin/env python3
"""
Script de Configuração Azure AD para Login Microsoft
Execute: python configure_azure.py

Este script:
1. Solicita as credenciais do Azure (Client ID, Client Secret, Tenant ID)
2. Solicita o nome da aplicação no Streamlit Cloud
3. Gera automaticamente as URIs de redirecionamento (localhost + produção)
4. Cria/atualiza o arquivo .streamlit/secrets.toml
"""

import os
import sys
from pathlib import Path


def print_header():
    """Exibe cabeçalho do script"""
    print("\n" + "=" * 70)
    print("🔐 CONFIGURADOR DE LOGIN MICROSOFT AZURE")
    print("   Template de Autenticação para Streamlit")
    print("=" * 70 + "\n")


def print_uris(app_name: str):
    """Exibe as URIs de redirecionamento formatadas"""
    local_uri = "http://localhost:8501"
    prod_uri = f"https://{app_name}.streamlit.app"
    
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║  📋 URIs de Redirecionamento para Azure                            ║")
    print("╠" + "═" * 68 + "╣")
    print(f"║  🏠 Local:     {local_uri:<52} ║")
    print(f"║  🌐 Produção:  {prod_uri:<52} ║")
    print("╚" + "═" * 68 + "╝")
    
    print("\n" + "─" * 70)
    print("📝 COPIE E COLE NO AZURE PORTAL:")
    print("─" * 70)
    print(f"\n{local_uri}")
    print(f"{prod_uri}\n")
    print("─" * 70)
    
    return local_uri, prod_uri


def print_azure_instructions():
    """Exibe instruções de configuração no Azure Portal"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  📌 COMO ADICIONAR AS URIs NO AZURE PORTAL                          ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  1. Acesse: https://portal.azure.com                                 ║
║                                                                      ║
║  2. Navegue até:                                                     ║
║     🇧🇷 PT: Microsoft Entra ID > Registros de aplicativo            ║
║     🇺🇸 EN: Microsoft Entra ID > App registrations                  ║
║                                                                      ║
║  3. Selecione sua aplicação                                          ║
║                                                                      ║
║  4. No menu lateral, clique em:                                      ║
║     🇧🇷 PT: Autenticação                                             ║
║     🇺🇸 EN: Authentication                                          ║
║                                                                      ║
║  5. Em "URIs de Redirecionamento" / "Redirect URIs":                 ║
║     - Clique em "Adicionar uma plataforma" / "Add a platform"        ║
║     - Selecione "Web"                                                ║
║     - Cole CADA URI em uma linha separada                            ║
║     - Clique em "Configurar" / "Configure"                           ║
║                                                                      ║
║  ⚠️  IMPORTANTE: Adicione AMBAS as URIs (localhost E produção)!     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")


def get_input(prompt: str, required: bool = True, default: str = None) -> str:
    """Solicita entrada do usuário"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        
        if not value and default:
            return default
        
        if value or not required:
            return value
        
        print("❌ Este campo é obrigatório. Tente novamente.")


def create_secrets_file(tenant_id: str, client_id: str, client_secret: str, 
                        local_uri: str, prod_uri: str):
    """Cria o arquivo secrets.toml"""
    
    # Criar diretório .streamlit se não existir
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    secrets_path = streamlit_dir / "secrets.toml"
    
    # Verificar se já existe
    if secrets_path.exists():
        overwrite = input("\n⚠️  O arquivo secrets.toml já existe. Sobrescrever? [s/N]: ").strip().lower()
        if overwrite not in ['s', 'sim', 'y', 'yes']:
            print("❌ Operação cancelada.")
            return False
    
    # Conteúdo do arquivo
    content = f'''# Configuração Azure AD - Gerado por configure_azure.py
# ⚠️ NUNCA COMMITE ESTE ARQUIVO NO GIT!

[auth]
# IDs do Azure Entra ID
tenant_id = "{tenant_id}"
client_id = "{client_id}"
client_secret = "{client_secret}"

# URIs de redirecionamento (devem estar cadastradas no Azure Portal!)
redirect_uri_local = "{local_uri}"
redirect_uri_prod = "{prod_uri}"

# Escopo Microsoft Graph
scope = ["https://graph.microsoft.com/User.Read"]
'''
    
    # Escrever arquivo
    secrets_path.write_text(content, encoding='utf-8')
    
    print(f"\n✅ Arquivo criado: {secrets_path.absolute()}")
    return True


def update_gitignore():
    """Adiciona secrets.toml ao .gitignore se não estiver"""
    gitignore_path = Path(".gitignore")
    secret_entry = ".streamlit/secrets.toml"
    
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding='utf-8')
        if secret_entry not in content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write(f"\n# Secrets do Streamlit\n{secret_entry}\n")
            print(f"✅ Adicionado {secret_entry} ao .gitignore")
    else:
        gitignore_path.write_text(f"# Secrets do Streamlit\n{secret_entry}\n", encoding='utf-8')
        print(f"✅ Criado .gitignore com {secret_entry}")


def main():
    """Função principal"""
    print_header()
    
    print("📋 PASSO 1: Informações da Aplicação\n")
    
    # Nome da aplicação no Streamlit
    print("📝 Digite o nome da sua aplicação no Streamlit Cloud.")
    print("   Exemplo: se sua URL for https://meu-app.streamlit.app")
    print("   Digite apenas: meu-app\n")
    
    app_name = get_input("Nome da aplicação (sem .streamlit.app)")
    
    # Limpar nome (remover possíveis extensões digitadas por engano)
    app_name = app_name.replace(".streamlit.app", "").replace("https://", "").replace("http://", "").strip("/")
    
    # Gerar e exibir URIs
    local_uri, prod_uri = print_uris(app_name)
    
    # Instruções do Azure Portal
    print_azure_instructions()
    
    input("Pressione ENTER após adicionar as URIs no Azure Portal...")
    
    print("\n" + "=" * 70)
    print("📋 PASSO 2: Credenciais do Azure")
    print("=" * 70 + "\n")
    
    print("🔐 Onde encontrar as credenciais:")
    print("   Azure Portal > Microsoft Entra ID > Registros de aplicativo")
    print("   > [Sua App] > Visão geral (Overview)\n")
    
    tenant_id = get_input("Tenant ID (ID do Diretório/Directory ID)")
    client_id = get_input("Client ID (ID do Aplicativo/Application ID)")
    
    print("\n🔑 O Client Secret é encontrado em:")
    print("   [Sua App] > Certificados e segredos > Segredos do cliente")
    print("   (Você precisa criar um se ainda não tiver)\n")
    
    client_secret = get_input("Client Secret (Valor do segredo)")
    
    print("\n" + "=" * 70)
    print("📋 PASSO 3: Criando arquivo de configuração")
    print("=" * 70 + "\n")
    
    # Criar arquivo secrets.toml
    if create_secrets_file(tenant_id, client_id, client_secret, local_uri, prod_uri):
        # Atualizar .gitignore
        update_gitignore()
        
        print("\n" + "=" * 70)
        print("✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        
        print(f"""
📁 Arquivos criados/atualizados:
   ├── .streamlit/secrets.toml  (suas credenciais)
   └── .gitignore               (protege suas credenciais)

🚀 Próximos passos:

   1. Execute a aplicação localmente:
      streamlit run app.py

   2. Teste o login com sua conta Microsoft

   3. Para deploy no Streamlit Cloud:
      - Faça push do código (sem o secrets.toml!)
      - No painel do Streamlit Cloud, vá em Settings > Secrets
      - Cole o conteúdo do seu secrets.toml

📖 Consulte o README.md para mais detalhes.
""")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operação cancelada pelo usuário.")
        sys.exit(1)

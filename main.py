import os
import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa primeiro a base e engine para evitar problemas de ordem
from database import engine, Base

# Configuração baseada no ambiente
APP_PROFILE = os.getenv("APP_PROFILE", "DEV")

# 1. Cria a instância principal da aplicação
app = FastAPI(
    title="API do Meu Projeto",
    version="0.1.0"
)
print("🟢 Middlewares carregados inicialmente:", app.user_middleware)


# Configuração de CORS baseada no ambiente
if APP_PROFILE == "DEV":
    # Configuração permissiva para desenvolvimento
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    print("🟢 Middlewares após CORS:", app.user_middleware)


else:
    # Configuração para produção
    # Permite adicionar origens extras via variável de ambiente CORS_ALLOWED_ORIGINS
    # Ex: CORS_ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:8000"
    env_allowed = os.getenv("CORS_ALLOWED_ORIGINS")
    if env_allowed:
        allowed_origins = [o.strip() for o in env_allowed.split(",") if o.strip()]
    else:
        allowed_origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
# Depois importa os controllers
from app.users import user_controller
from app.roles import role_controller
from app.auth import auth_controller
from app.posts import posts_controller

# Garantir que as tabelas sejam criadas na inicialização (sempre)
# Importante: executar após os módulos que registram os modelos serem importados
Base.metadata.create_all(bind=engine)

# 2. Inclui o roteador de usuários na aplicação principal
app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)
app.include_router(posts_controller.router)
print("🟢 Middlewares depois dos routers:", app.user_middleware)


# 4. Código para rodar o servidor
if __name__ == '__main__':
    # Este bloco só executa quando rodamos o script diretamente (python main.py)
    uvicorn.run(app, host="0.0.0.0", port=8000)
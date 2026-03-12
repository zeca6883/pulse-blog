@echo off
:: Entra na pasta onde o script está
cd /d "%~dp0"

:: Executa o gerador de post
python generate_post.py

:: Se o python funcionou, sobe para o GitHub
if %errorlevel% equ 0 (
    cd ..
    git add .
    git commit -m "Novo post automatico via IA"
    git push origin main
    echo --- Publicado com sucesso! ---
) else (
    echo --- Erro ao gerar o post. Abortando git push. ---
)
pause
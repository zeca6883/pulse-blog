@echo off
cd /d %~dp0

python generate_post.py
if errorlevel 1 exit /b 1

cd ..
git add .
git commit -m "novo post automatico"
git push
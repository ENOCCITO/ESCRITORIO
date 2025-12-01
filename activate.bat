@echo off
REM Script para activar el entorno virtual en Windows (CMD)
echo ========================================
echo Activando entorno virtual...
echo ========================================
call .venv\Scripts\activate.bat
echo.
echo ✅ Entorno virtual activado
echo.
echo Para ejecutar la aplicación:
echo   python main.py
echo.
echo Para instalar dependencias:
echo   pip install -r requirements.txt
echo.
echo Para desactivar el entorno:
echo   deactivate
echo ========================================

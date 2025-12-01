# 🧹 Limpieza Post-Reorganización

## Archivos/Carpetas que Pueden Eliminarse

Una vez que verifiques que todo funciona correctamente, puedes eliminar:

### 1. Entorno Virtual Antiguo

```powershell
Remove-Item -Path ".venv_old" -Recurse -Force
```

**Nota:** Solo elimina después de verificar que `.venv` funciona correctamente.

### 2. Archivos de Cache de Python

```powershell
# Eliminar todos los __pycache__
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

# Eliminar archivos .pyc
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
```

## Verificación Antes de Limpiar

### 1. Verificar que el entorno virtual funciona

```powershell
.\.venv\Scripts\Activate.ps1
python --version
python -c "from src.config.config import DB_CONFIG; print('OK')"
```

### 2. Verificar que la aplicación funciona

```powershell
python main.py
```

Si todo funciona correctamente, procede con la limpieza.

## Limpieza Opcional

### Eliminar scripts de activación (si no los necesitas)

```powershell
Remove-Item activate.bat, activate.ps1
```

**Nota:** Estos scripts son útiles para activar rápidamente el entorno virtual.

### Consolidar documentación

Si tienes documentación duplicada en `docs/` y en la raíz, considera consolidarla.

## Después de la Limpieza

### Hacer commit de los cambios

```bash
git add .
git commit -m "Reorganizar proyecto en estructura modular"
git push
```

## Estado Ideal Después de la Limpieza

```
ESCRITORIO/
├── .git/
├── .venv/                    # ✅ Un solo entorno virtual
├── arduino/                  # ✅ Código Arduino organizado
├── assets/                   # ✅ Recursos gráficos
├── data/                     # ✅ Datos exportados
├── docs/                     # ✅ Documentación
├── scripts/                  # ✅ Scripts de utilidad
├── src/                      # ✅ Código fuente organizado
│   ├── config/
│   ├── core/
│   ├── interfaces/
│   └── utils/
├── .gitignore
├── main.py
├── requirements.txt
├── ESTRUCTURA_PROYECTO.md
├── README_PRINCIPAL.md
├── RESUMEN_REORGANIZACION.md
├── activate.ps1             # Opcional
└── activate.bat             # Opcional
```

## Notas Importantes

- **NO** elimines `.venv_old` hasta verificar que `.venv` funciona correctamente
- **NO** elimines archivos en `src/`, `arduino/`, `docs/`, `data/`, `assets/`, o `scripts/`
- **SÍ** puedes eliminar `__pycache__/` en cualquier momento (se regenera automáticamente)
- **SÍ** puedes eliminar `.venv_old` después de verificar que todo funciona

## Comandos de Limpieza Completa

Una vez verificado que todo funciona:

```powershell
# Limpiar entorno antiguo
Remove-Item -Path ".venv_old" -Recurse -Force

# Limpiar cache de Python
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force

Write-Host "✅ Limpieza completada" -ForegroundColor Green
```

## Verificación Final

```powershell
# Verificar estructura
tree /F /A

# Verificar imports
python -c "from src.config.config import DB_CONFIG; from src.utils import styles; print('✅ Todo OK')"

# Ejecutar aplicación
python main.py
```

---

**Importante:** Siempre haz un backup o commit antes de eliminar archivos permanentemente.

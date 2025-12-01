# PROMPT PARA STITCH AI - Interfaces de Instructor

Copia y pega este prompt completo en Stitch AI:

---

## PROMPT PARA STITCH AI

Hola Stitch, necesito que me crees 2 interfaces profesionales y modernas en HTML/CSS (Tailwind CSS) para un sistema de gestión de llaves llamado "Sistema CEFA". Estas interfaces son para el rol de **Instructor**.

### DISEÑO Y ESTILO GENERAL:

**Paleta de colores:**
- Color primario: `#136dec` (azul)
- Fondo claro: `#f6f7f8` (gris muy claro)
- Texto oscuro: `#111418` o `#111827` (gris muy oscuro)
- Texto claro: `#617289` o `#6b7280` (gris medio)
- Borde: `#f0f2f4` o `#e5e7eb` (gris claro)
- Header oscuro: `#1f2937` (gris oscuro)
- Azul claro (bienvenida): `#60a5fa`
- Iconos: `#ec4899` (rosa), `#a78bfa` (morado claro), `#8b5cf6` (morado), `#10b981` (verde)

**Estilo general:**
- Diseño limpio, moderno y profesional
- **IMPORTANTE: NO encapsular texto** - todo el texto debe mostrarse completo sin truncarse ni encapsularse en cajas
- Tipografía: 'Public Sans', 'Segoe UI', Arial, sans-serif
- Bordes redondeados suaves (8px - 12px)
- Espaciado generoso y respiración visual
- Sin mayúsculas forzadas excepto en el header
- Texto normal y legible

**Estructura de ventana:**
- Header fijo en la parte superior
- Contenido principal con scroll si es necesario
- Footer o sección inferior si corresponde

---

## INTERFAZ 1: INTERFAZ PRINCIPAL DE INSTRUCTOR

**Descripción:**
Esta es la pantalla principal que ve el instructor al ingresar al sistema.

**Estructura requerida:**

1. **HEADER (Barra superior oscura):**
   - Fondo: `#1f2937` (gris oscuro)
   - Altura: 50px
   - Icono de monitor/computadora: 🖥️ (blanco, tamaño 20px)
   - Título: "INTERFAZ DE INSTRUCTOR - SISTEMA CEFA" (MAYÚSCULAS, blanco, bold, fuente: 14px)
   - Alineado a la izquierda
   - Sin bordes ni sombras

2. **CONTENIDO PRINCIPAL (Fondo claro `#f6f7f8`):**
   
   a. **Sección de Bienvenida:**
      - Icono de escudo pequeño y colorido: 🛡️ (tamaño 32px, alineado a la izquierda)
      - Título: "¡BIENVENIDO INSTRUCTOR!" (color `#60a5fa`, tamaño 32px, bold, normal case)
      - Sin encapsulación de texto
      - Espaciado: 12px entre icono y título
   
   b. **Sección "AMBIENTE ASIGNADO":**
      - Título: "AMBIENTE ASIGNADO" (color `#60a5fa`, tamaño 18px, bold)
      - Lista de información del ambiente, cada elemento con:
        * Icono emoji de color específico (20px)
        * Label en azul claro (`#60a5fa`, 14px, bold)
        * Valor en azul claro (`#60a5fa`, 14px, normal)
        * Sin encapsulación, texto completo visible
      
      **Elementos a mostrar:**
      - 📍 "AULA PRINCIPAL:" "Aula 101 - Laboratorio de Programación" (icono color `#ec4899`)
      - 🔧 "EQUIPOS:" "25 computadoras, Proyector 4K, Pizarra digital" (icono color `#a78bfa`)
      - 👥 "CAPACIDAD:" "30 estudiantes" (icono color `#8b5cf6`)
      - 🌐 "CONECTIVIDAD:" "WiFi de alta velocidad, Red cableada" (icono color `#60a5fa`)
      - 📚 "RECURSOS:" "Software de desarrollo, Bibliotecas digitales" (icono color `#10b981`)
      
      Espaciado: 8px vertical entre cada elemento
   
   c. **Sección "HORARIO DE CLASES":**
      - Contenedor con fondo oscuro: `#1f2937`
      - Border-radius: 12px
      - Padding: 24px
      - Header interno:
        * Icono calendario: 📅 (blanco, 20px)
        * Título: "HORARIO DE CLASES" (blanco, 18px, bold)
      - Contenido:
        * Si NO hay programación disponible:
          - Icono usuario: 👤 (gris claro `#d1d5db`, 24px)
          - Mensaje 1: "No hay programación disponible" (gris claro `#d1d5db`, 14px)
          - Mensaje 2: "Contacte al administrador para configurar su horario" (gris claro `#d1d5db`, 14px)
          - Sin encapsulación de texto
        * Si HAY programación (menciona que se mostraría aquí)

**Requisitos técnicos:**
- Usar Tailwind CSS para estilos
- Diseño responsive
- HTML semántico
- Sin truncamiento ni encapsulación de texto
- Colores exactos especificados
- Fuentes y tamaños según especificación

---

## INTERFAZ 2: [Si hay otra interfaz específica que necesitas]

[Espacio para describir la segunda interfaz si es diferente]

---

**NOTAS FINALES:**
- Todo el código debe ser HTML/CSS puro con Tailwind CSS
- No usar JavaScript para esta entrega
- El diseño debe ser profesional, limpio y moderno
- Asegúrate de que TODO el texto sea visible sin encapsularse o truncarse
- Usa los colores exactos especificados
- Mantén consistencia visual entre las interfaces

Por favor, genera el código HTML completo con Tailwind CSS para estas interfaces.

---




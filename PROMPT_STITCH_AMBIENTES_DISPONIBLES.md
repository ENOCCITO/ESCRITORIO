# PROMPT PARA STITCH AI – Interfaz de Ambientes Disponibles

Copia y pega este prompt completo en Stitch AI:

---

## PROMPT PARA STITCH AI

Hola Stitch, necesito que diseñes una **interfaz modal profesional y moderna** (HTML + Tailwind CSS) para el selector de **Ambientes Disponibles** del sistema "Sistema CEFA". Esta interfaz se muestra como un modal/diálogo cuando el usuario hace clic en el botón "Seleccionar" desde la interfaz de Seguridad. Debe seguir la misma línea visual que otras pantallas generadas anteriormente: fondo claro, tarjetas blancas con bordes suaves, tipografía limpia, sin texto encapsulado.

### Diseño general

- **Paleta:**
  - Primario: `#136dec` (azul)
  - Fondo claro general: `#f6f7f8` (gris muy claro)
  - Texto oscuro: `#111418` (gris muy oscuro)
  - Texto secundario: `#617289` (gris medio)
  - Bordes: `#f0f2f4` (gris claro)
  - Tarjetas: `#ffffff` (blanco)
- **Tipografía:** `'Public Sans', 'Segoe UI', Arial, sans-serif`
- **Bordes:** 12px para tarjetas, 8px en chips/botones
- **Sombras:** Suaves (opcional)
- **Sin truncamiento ni encapsulamiento de texto**. Todo el contenido debe poder verse completo.
- **Diseño responsive** (desktop/laptop, tablet, móvil).
- Usa íconos/iconos o imágenes decorativas limpias. Puedes usar emojis como fallback (🏢 para edificio/ambiente).

### Estructura solicitada

1. **Header del modal**
   - Fondo blanco (`#ffffff`), con borde inferior sutil (`#f0f2f4`)
   - Layout horizontal con:
     - **Izquierda:** Título "AMBIENTES DISPONIBLES" (18px, bold, color `#111418`) con icono de edificio/ambiente (🏢 o ícono Material Symbols) a la izquierda del texto
     - **Derecha:** Botón de cerrar (X) con estilo minimalista (color `#617289`, hover más oscuro, tamaño 32x32px, border-radius 8px, padding 8px)
   - Altura fija: 60px
   - Padding horizontal: 24px, padding vertical: 16px
   - El botón X debe tener un hover suave que cambie el color de fondo a `#f6f7f8`

2. **Contenido principal (área scrollable)**
   - Fondo: `#f6f7f8` (gris muy claro)
   - Padding: 24px en todos los lados
   - **Subtítulo/Instrucción:**
     - Texto centrado: "Seleccione un ambiente para gestionar sus llaves disponibles" (14px, color `#617289`, peso normal)
     - Espaciado inferior: 24px

3. **Estado vacío (cuando no hay ambientes con llaves)**
   - Mostrar un mensaje centrado en una tarjeta blanca:
     - Texto: "No hay llaves disponibles en este momento." (16px, color `#617289`, centrado)
     - Tarjeta con fondo blanco, border-radius 12px, padding 40px vertical, 32px horizontal
     - Opcional: Icono decorativo (🔑 o ícono de llave) arriba del texto

4. **Lista de ambientes (cuando hay ambientes disponibles)**
   - Cada ambiente debe mostrarse en una **tarjeta horizontal** con:
     * Fondo blanco (`#ffffff`), borde suave (`#f0f2f4`), border-radius 12px
     * Padding generoso: 24px horizontal, 20px vertical
     * Layout horizontal con:
       - **Izquierda:** 
         * Icono de edificio/ambiente (🏢 o ícono Material Symbols, tamaño 40x40px)
         * Información del ambiente:
           - Nombre del ambiente (ej: "Ambiente 1") en negrita (16px, color `#111418`)
           - Detalle: "X llaves disponibles o asignadas sin reclamar" (13px, color `#617289`)
       - **Derecha:** Botón "Ver llaves" (color primario `#136dec`, texto blanco, border-radius 8px, padding 10px 20px, font-size 14px, font-weight 500)
     * Espaciado entre elementos: 16px
     * Hover suave: sombra ligera o cambio de borde
     * **IMPORTANTE:** El contenido NO debe estar pegado a los bordes - debe haber espacio generoso alrededor
   - Espaciado entre tarjetas: 12px
   - Las tarjetas deben estar en un contenedor con scroll vertical si hay muchas

5. **Footer (opcional)**
   - Si decides incluir un footer, puede tener un botón "Cerrar" alineado a la derecha
   - Estilo: color secundario o gris, border-radius 8px

### Requisitos específicos

- **Modal/Dialog:** Esta interfaz debe verse como un modal centrado en la pantalla, con un fondo semi-transparente oscuro detrás (backdrop) si es posible, o al menos diseñado para verse como un diálogo flotante.
- **Tamaño:** Ancho máximo 900px, altura máxima 620px (o ajustable según contenido)
- **Espaciado:** Es crucial que el contenido dentro de las tarjetas tenga padding generoso. El texto descriptivo y los botones NO deben estar pegados a los bordes del cuadro blanco.
- **Texto sin encapsulación:** Todo el texto debe mostrarse completo, sin truncarse ni encapsularse en cajas estrechas.
- **Consistencia visual:** El diseño debe verse consistente con las interfaces de Instructor, Seguridad y Aseo ya generadas anteriormente.
- **Responsive:** El diseño debe adaptarse bien a diferentes tamaños de pantalla (stack en columnas para pantallas pequeñas, ajuste de padding).

### Notas adicionales

- Usa **Tailwind CSS** (incluir `<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>` si lo necesitas).
- El diseño debe verse consistente con interfaces modernas empresariales.
- No encapsules texto en cajas estrechas; usa `flex`, `gap`, `space-y`, `px-*`, `py-*`, etc., para que el contenido fluya con espacio adecuado.
- Puedes usar placeholder images (ej. background svg/avatar) o iconos de Material Symbols (incluye `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" />`).
- Incluye versión responsive: stack en columnas para pantallas pequeñas.
- **Énfasis en espaciado:** Asegúrate de usar padding/margin adecuados (mínimo 24px horizontal, 20px vertical) dentro de las tarjetas para evitar que el contenido esté pegado a los bordes.
- **Ejemplo de datos:** Puedes usar datos de ejemplo como:
  - "Ambiente 1" con "5 llaves disponibles o asignadas sin reclamar"
  - "Ambiente 2" con "3 llaves disponibles o asignadas sin reclamar"
  - O mostrar el estado vacío si prefieres

Genera todo el HTML completo (incluyendo `<head>` con fuentes, Tailwind, estilos extra si son necesarios) y el `<body>` con la estructura descrita. El código debe estar listo para usar y visualizar directamente en un navegador. Incluye tanto el estado con ambientes disponibles como el estado vacío (puedes comentar uno u otro para mostrar ambos casos).

---




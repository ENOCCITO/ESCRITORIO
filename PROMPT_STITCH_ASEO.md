# PROMPT PARA STITCH AI – Interfaz de Aseo

Copia y pega este prompt completo en Stitch AI:

---

## PROMPT PARA STITCH AI

Hola Stitch, necesito que diseñes una **interfaz profesional y moderna** (HTML + Tailwind CSS) para el rol de **Aseo** del sistema "Sistema CEFA". Debe seguir la misma línea visual que otras pantallas generadas anteriormente: fondo claro, tarjetas blancas con bordes suaves, tipografía limpia, sin texto encapsulado.

### Diseño general

- **Paleta:**
  - Primario: `#136dec` (azul)
  - Fondo claro general: `#f6f7f8` (gris muy claro)
  - Texto oscuro: `#111418` (gris muy oscuro)
  - Texto secundario: `#617289` (gris medio)
  - Bordes: `#f0f2f4` (gris claro)
  - Fondo oscuro (header): `#2D3748` (gris oscuro)
  - Tarjetas: `#ffffff` (blanco)
  - Color acento (bienvenida): `#00B4D8` (cian brillante)
- **Tipografía:** `'Public Sans', 'Segoe UI', Arial, sans-serif`
- **Bordes:** 12px para tarjetas, 8px en chips/botones
- **Sombras:** Suaves (opcional)
- **Sin truncamiento ni encapsulamiento de texto**. Todo el contenido debe poder verse completo.
- **Diseño responsive** (desktop/laptop, tablet, móvil).
- Usa íconos/iconos o imágenes decorativas limpias. Puedes usar emojis como fallback (🧹 para limpieza/aseo).

### Estructura solicitada

1. **Header oscuro fijo**
   - Fondo `#2D3748`, altura 68px
   - Título: "INTERFAZ DE ASEO - SISTEMA CEFA" (MAYÚSCULAS, blanco, bold, 18px)
   - Icono/logotipo a la izquierda (puede ser un ícono de limpieza/aseo, escoba, o imagen decorativa)
   - Sin botón de logout
   - Alineado a la izquierda, espaciado de 24px horizontal, 12px vertical

2. **Tarjeta de bienvenida**
   - Fondo blanco (`#ffffff`), bordes redondeados (12px), padding amplio (32px horizontal, 28px vertical)
   - Layout horizontal con dos columnas:
     - Columna izquierda: imagen/ilustración de limpieza/aseo o ícono grande (tamaño 92x92px)
     - Columna derecha: 
       * Título: "Gestión de Aseo" (30px, bold, color `#111418`)
       * Subtítulo: "Interfaz dedicada para la gestión y monitoreo de áreas de limpieza y almacenes." (14px, color `#617289`)
   - Debe sentirse similar a un hero compacto, con espaciado generoso

3. **Acciones principales (tarjetas horizontales)**
   - Una tarjeta principal con esta acción:
     - `Seleccionar Ambiente para Limpieza` – descripción: "Elija el entorno específico para gestionar las llaves correspondientes a áreas de limpieza y almacenes." Botón/call-to-action "Seleccionar".
   - La tarjeta debe tener:
     * Fondo blanco (`#ffffff`), borde suave (`#f0f2f4`), border-radius 12px
     * Padding generoso (40px horizontal, 32px vertical) para evitar que el contenido esté pegado a los bordes
     * Icono/imagen a la izquierda (ícono de ambiente/edificio, tamaño 56x56px)
     * Título en negrita (16px, color `#111418`)
     * Descripción en texto secundario (13px, color `#617289`)
     * Botón "Seleccionar" (color primario `#136dec`, texto blanco, border-radius 8px, padding 10px 22px)
     * Diseño minimalista, bordes redondeados, hover suave (resalta borde/sombra ligera)
     * **IMPORTANTE:** El texto y el botón NO deben estar pegados a los bordes del cuadro - debe haber espacio generoso alrededor

4. **Sección "Ambientes disponibles para limpieza" (opcional)**
   - Si decides incluir una sección adicional, puede mostrar:
     - Tarjeta completa con título "Ambientes disponibles"
     - Lista de ambientes con información relevante para limpieza
     - Cada elemento con código/nombre de ambiente, descripción, estado de limpieza
     - Botones de acción según corresponda

5. **Footer (opcional)**
   - Si incluyes footer, puede tener un botón alineado a la derecha: "Cerrar". Estilo similar a botones de acción (color primario o secundario según corresponda).

### Requisitos específicos

- **Espaciado:** Es crucial que el contenido dentro de las tarjetas tenga padding generoso. El texto descriptivo y los botones NO deben estar pegados a los bordes del cuadro blanco.
- **Texto sin encapsulación:** Todo el texto debe mostrarse completo, sin truncarse ni encapsularse en cajas estrechas.
- **Consistencia visual:** El diseño debe verse consistente con las interfaces de Instructor y Seguridad ya generadas anteriormente.
- **Responsive:** El diseño debe adaptarse bien a diferentes tamaños de pantalla (grid responsive, stack en columnas para pantallas pequeñas).

### Notas adicionales

- Usa **Tailwind CSS** (incluir `<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>` si lo necesitas).
- El diseño debe verse consistente con interfaces modernas empresariales.
- No encapsules texto en cajas estrechas; usa `flex`, `gap`, `space-y`, `px-*`, `py-*`, etc., para que el contenido fluya con espacio adecuado.
- Evita mayúsculas sostenidas excepto en el header del top.
- Puedes usar placeholder images (ej. background svg/avatar) o iconos de Material Symbols (incluye `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" />`).
- Incluye versión responsive: stack en columnas para pantallas pequeñas.
- **Énfasis en espaciado:** Asegúrate de usar padding/margin adecuados (mínimo 32-40px horizontal, 24-32px vertical) dentro de las tarjetas para evitar que el contenido esté pegado a los bordes.

Genera todo el HTML completo (incluyendo `<head>` con fuentes, Tailwind, estilos extra si son necesarios) y el `<body>` con la estructura descrita. El código debe estar listo para usar y visualizar directamente en un navegador.

---











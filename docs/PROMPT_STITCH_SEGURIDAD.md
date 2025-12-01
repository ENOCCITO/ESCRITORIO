# PROMPT PARA STITCH AI – Interfaz de Seguridad

Copia y pega este prompt completo en Stitch AI:

---

## PROMPT PARA STITCH AI

Hola Stitch, necesito que diseñes una **interfaz profesional y moderna** (HTML + Tailwind CSS) para el rol de **Seguridad** del sistema "Sistema CEFA". Debe seguir la misma línea visual que otras pantallas generadas anteriormente: fondo claro, tarjetas blancas con bordes suaves, tipografía limpia, sin texto encapsulado.

### Diseño general

- **Paleta:**
  - Primario: `#136dec`
  - Fondo claro general: `#f6f7f8`
  - Texto oscuro: `#111418`
  - Texto secundario: `#617289`
  - Bordes: `#f0f2f4`
  - Fondo oscuro (header): `#2D3748`
- **Tipografía:** `'Public Sans', 'Segoe UI', Arial, sans-serif`
- **Bordes:** 12px para tarjetas, 8px en chips/botones
- **Sombras:** Suaves (opcional)
- **Sin truncamiento ni encapsulamiento de texto**. Todo el contenido debe poder verse completo.
- **Diseño responsive** (desktop/laptop, tablet, móvil).
- Usa íconos/iconos o imágenes decorativas limpias. Puedes usar emojis como fallback.

### Estructura solicitada

1. **Header oscuro fijo**
   - Fondo `#2D3748`, título "INTERFAZ DE SEGURIDAD – SISTEMA CEFA" en blanco.
   - Icono/logotipo a la izquierda (por ejemplo, un escudo, puedes simular uno con SVG/emoji). Sin botón de logout.

2. **Tarjeta de bienvenida**
   - Fondo blanco (`#ffffff`), bordes redondeados, padding amplio.
   - Columna izquierda: imagen/ilustración de seguridad o ícono grande.
   - Columna derecha: título "Control de Seguridad" (28-32px, bold) y subtítulo “Gestiona accesos y llaves del campus desde un panel centralizado”.
   - Debe sentirse similar a un hero compacto.

3. **Acciones principales (tarjetas horizontales)**
   - Dos tarjetas (o responsive grid 1-2 columnas) con estas acciones:
     - `Seleccionar Ambiente` – descripción: “Asignar o liberar llaves disponibles”. Botón/call-to-action.
     - `Monitoreo en tiempo real` – descripción: “Ver cámaras y estado de accesos”. Botón/call-to-action.
   - Cada tarjeta con ícono/imagen, título, breve descripción, botón (por ejemplo, "Abrir").
   - Diseño minimalista, bordes redondeados, hover suave (resalta borde/ sombra ligera).

4. **Sección “Llaves en custodia”**
   - Tarjeta completa con título "Llaves en custodia" y chip con contador (ej. “3 llaves”).
   - Botón “Actualizar” en la cabecera de la tarjeta.
   - Lista de llaves en tarjetas/rows individuales:
     - Contenido: código de llave, descripción, ambiente, fecha/hora asignación, estado (chip/etiqueta de color).
     - Botón acción “Devolver” para cada fila.
   - Asegúrate de que los textos no se corten.

5. **Footer**
   - Botón alineado a la derecha: “Cerrar”. Estilo similar a botones de acción (color rojo/primario según corresponda).

### Notas adicionales

- Usa **Tailwind CSS** (incluir `<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>` si lo necesitas).
- El diseño debe verse consistente con interfaces modernas empresariales.
- No encapsules texto en cajas estrechas; usa `flex`, `gap`, `space-y`, etc., para que el contenido fluya.
- Evita mayúsculas sostenidas excepto en el header del top.
- Puedes usar placeholder images (ej. background svg/avatar) o iconos de Material Symbols (incluye `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" />`).
- Incluye versión responsive: stack en columnas para pantallas pequeñas.

Genera todo el HTML completo (incluyendo `<head>` con fuentes, Tailwind, estilos extra si son necesarios) y el `<body>` con la estructura descrita.

---




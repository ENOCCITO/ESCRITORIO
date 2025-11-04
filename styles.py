#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
styles.py
- Estilos y componentes reutilizables (PySide6)
- Tema futurista para el sistema de dispensación biométrica
"""

from PySide6.QtWidgets import (
    QWidget, QDialog, QLabel, QPushButton, QTextEdit, QLineEdit,
    QListWidget, QTreeWidget, QTreeWidgetItem, QScrollBar, QVBoxLayout,
    QHBoxLayout, QGraphicsDropShadowEffect, QSizePolicy, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, QSize, QObject, QEvent, QTimer
from PySide6.QtGui import QFont, QColor, QPixmap, QPainter, QBrush, QPainterPath
import os

from config import *

def setup_futuristic_styles(app):
    """Configura estilos globales con hoja de estilos Qt."""
    app.setStyleSheet(f"""
        QWidget {{
            /* Fondo sólido para eliminar las bandas horizontales ("renglones") */
            background-color: {BG_DARK};
            color: {TEXT_WHITE};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        QDialog#progressDialog {{
            background-color: {BG_DARK};
            border: 1px solid {ACCENT_BLUE};
            border-radius: 10px;
        }}
        QLabel.title {{
            color: {ACCENT_BLUE};
            font-size: {FONT_TITLE[1] if isinstance(FONT_TITLE, tuple) else 24}px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        QLabel.subtitle {{
            color: {ACCENT_CYAN};
            font-size: {FONT_SUBTITLE[1] if isinstance(FONT_SUBTITLE, tuple) else 16}px;
            font-weight: 600;
            opacity: 0.9;
        }}
        QLabel.info {{
            color: {ACCENT_CYAN};
            opacity: 0.95;
        }}
        QPushButton#roleButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                         stop:0 {BG_MEDIUM}, stop:1 {BG_LIGHT});
            color: {TEXT_WHITE};
            border: 2px solid {ACCENT_BLUE};
            border-radius: 10px;
            padding: {BUTTON_PADDING_Y + 6}px {BUTTON_PADDING_X + 6}px;
        }}
        QPushButton#roleButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                         stop:0 {BG_LIGHT}, stop:1 {BG_MEDIUM});
            border-color: {ACCENT_CYAN};
        }}
        QPushButton#roleButton:pressed {{
            background: {BG_LIGHT};
            border-color: {ACCENT_CYAN};
        }}
        QPushButton.accent {{
            background-color: {ACCENT_BLUE};
            color: {BG_DARK};
            border: 0;
            padding: 8px 16px;
            font-weight: 600;
            border-radius: 8px;
        }}
        QPushButton.accent:hover {{
            background-color: {ACCENT_CYAN};
        }}
        QPushButton.danger {{
            background-color: #ff4444;
            color: #ffffff;
            border: 0;
            padding: 8px 16px;
            font-weight: 600;
            border-radius: 8px;
        }}
        QPushButton.danger:hover {{
            background-color: #ff6666;
        }}
        QPushButton.warning {{
            background-color: #ff8800;
            color: #ffffff;
            border: 0;
            padding: 8px 16px;
            font-weight: 600;
            border-radius: 8px;
        }}
        QPushButton.warning:hover {{
            background-color: #ffaa00;
        }}
        QTextEdit, QLineEdit {{
            background-color: {BG_MEDIUM};
            color: {TEXT_WHITE};
            border: 1px solid {ACCENT_BLUE};
            border-radius: 6px;
        }}
        QTreeWidget {{
            background-color: {BG_LIGHT};
            color: {TEXT_WHITE};
            border: 0;
        }}
        QTreeWidget::item:selected {{
            background-color: {ACCENT_BLUE};
            color: {BG_DARK};
        }}
    """)

def create_futuristic_button(parent, text, command, **kwargs):
    btn = QPushButton(text, parent)
    btn.setObjectName("roleButton")
    btn.setCursor(Qt.PointingHandCursor)
    # Responsividad basada en el ancho de pantalla
    scale = 1.0
    try:
        screen = parent.window().screen().availableGeometry()
        scale = max(0.6, min(1.6, screen.width() / 1920.0))
    except Exception:
        pass

    min_h = int(max(48, (BUTTON_HEIGHT if isinstance(BUTTON_HEIGHT, int) else 48)) * scale)
    btn.setMinimumHeight(min_h)

    # Ajustar fuente en función del scale
    try:
        base_family = FONT_BUTTON[0] if isinstance(FONT_BUTTON, tuple) else 'Segoe UI Emoji'
        base_size = FONT_BUTTON[1] if isinstance(FONT_BUTTON, tuple) else 14
        is_bold = False
        if isinstance(FONT_BUTTON, tuple) and len(FONT_BUTTON) >= 3:
            is_bold = 'bold' in str(FONT_BUTTON[2]).lower()
        font = QFont(base_family)
        # Aumentar levemente para que los emojis/iconos luzcan más grandes
        font.setPointSizeF(max(11.0, base_size * (scale + 0.1)))
        font.setBold(is_bold)
        btn.setFont(font)
        # Aumentar el tamaño global si el texto inicia con emoji para dar protagonismo al icono
        try:
            if text and not text[0].isalnum():
                font.setPointSizeF(font.pointSizeF() * 1.2)
                btn.setFont(font)
        except Exception:
            pass
    except Exception:
        pass

    # Expandir para ocupar el espacio disponible
    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    btn.clicked.connect(command)
    btn.setStyleSheet("")  # allow global stylesheet to apply
    try:
        effect = QGraphicsDropShadowEffect(btn)
        effect.setBlurRadius(18)
        effect.setColor(QColor(0, 212, 255, 60))
        effect.setOffset(0, 8)
        btn.setGraphicsEffect(effect)
    except Exception:
        pass
    
    # Micro-animaciones de hover (scale) sin bloquear el hilo
    class HoverAnim(QObject):
        def __init__(self, w):
            super().__init__(w)
            self.w = w
            self._hover = False
            self._timer = QTimer(w)
            self._timer.setInterval(16)
            self._timer.timeout.connect(self._tick)
            self._scale = 1.0
        def eventFilter(self, obj, ev):
            if ev.type() == QEvent.Enter:
                self._hover = True
                self._timer.start()
            elif ev.type() == QEvent.Leave:
                self._hover = False
                self._timer.start()
            return False
        def _tick(self):
            target = 1.02 if self._hover else 1.0
            step = 0.04
            if abs(self._scale - target) < step:
                self._scale = target
                self._timer.stop()
            else:
                self._scale += step if self._scale < target else -step
            # Removed transform property as it's not supported in Qt/PySide6

    try:
        anim = HoverAnim(btn)
        btn.installEventFilter(anim)
        btn._hover_anim = anim  # evitar GC
    except Exception:
        pass
    return btn

def create_list_button(parent, primary_text, secondary_text, command):
    """Botón de lista (izquierda) para ítems como ambientes."""
    text = primary_text if not secondary_text else f"{primary_text}\n{secondary_text}"
    btn = create_futuristic_button(parent, text, command)
    # Alinear texto a la izquierda para legibilidad
    try:
        # mantener estilo global y agregar alineación/padding
        btn.setStyleSheet(btn.styleSheet() + "\ntext-align: left; padding-left: 20px;")
        # Ajustar fuente levemente mayor
        f = QFont(btn.font())
        f.setPointSizeF(max(12.0, f.pointSizeF() + 1.0))
        btn.setFont(f)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    except Exception:
        pass
    return btn

def create_clickable_row(parent, title: str, subtitle: str, on_click, min_height: int = 80) -> QWidget:
    """Crea una fila clickeable (tipo tarjeta) para listas como ambientes.
    No usa QPushButton para permitir multilínea izquierda y responsividad.
    """
    container = QWidget(parent)
    container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    container.setMinimumHeight(min_height)
    base_style = (
        f"background-color: {BG_MEDIUM}; border: 2px solid {ACCENT_BLUE};"
        f"border-radius: 10px;"
    )
    hover_style = (
        f"background-color: {BG_LIGHT}; border: 2px solid {ACCENT_CYAN};"
        f"border-radius: 10px;"
    )
    container.setStyleSheet(base_style)

    lay = QVBoxLayout(container)
    lay.setContentsMargins(16, 12, 16, 12)
    lay.setSpacing(2)

    title_lbl = QLabel(title, container)
    title_lbl.setStyleSheet(f"color: {TEXT_WHITE}; font-weight: 700;")
    title_lbl.setWordWrap(True)
    lay.addWidget(title_lbl)

    if subtitle:
        sub_lbl = QLabel(subtitle, container)
        sub_lbl.setStyleSheet("color: #a9b2c7;")
        sub_lbl.setWordWrap(True)
        lay.addWidget(sub_lbl)

    # Hover y click
    class RowFx(QObject):
        def __init__(self, w):
            super().__init__(w)
            self.w = w
        def eventFilter(self, obj, ev):
            if ev.type() == QEvent.Enter:
                self.w.setStyleSheet(hover_style)
            elif ev.type() == QEvent.Leave:
                self.w.setStyleSheet(base_style)
            elif ev.type() == QEvent.MouseButtonRelease:
                try:
                    on_click()
                except Exception:
                    pass
            return False

    fx = RowFx(container)
    container.installEventFilter(fx)
    container._row_fx = fx  # evitar GC
    return container

def create_scroll_area(parent) -> QScrollArea:
    sa = QScrollArea(parent)
    sa.setWidgetResizable(True)
    try:
        sa.setFrameShape(QFrame.NoFrame)
    except Exception:
        pass
    return sa

def create_card(parent) -> QWidget:
    card = QWidget(parent)
    card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
    try:
        # Quitar borde para evitar "renglones" o múltiples marcos visibles
        card.setStyleSheet(
            f"background-color: {BG_LIGHT}; border: 0; border-radius: 10px;"
        )
    except Exception:
        pass
    return card

def create_timeline_item(parent, time_text: str, title_text: str, room_text: str = "", group_text: str = "") -> QWidget:
    container = QWidget(parent)
    h = QHBoxLayout(container)
    h.setContentsMargins(10, 6, 10, 6)
    h.setSpacing(12)

    time_lbl = QLabel(f"🕐 {time_text}", container)
    try:
        time_lbl.setStyleSheet(f"color: {ACCENT_CYAN}; font-weight: 700;")
    except Exception:
        pass
    time_lbl.setMinimumWidth(140)
    h.addWidget(time_lbl)

    right = QVBoxLayout()
    title_lbl = QLabel(title_text, container)
    try:
        title_lbl.setStyleSheet(f"color: {TEXT_WHITE}; font-weight: 600;")
    except Exception:
        pass
    subtitle_parts = []
    if room_text:
        subtitle_parts.append(f"🏫 {room_text}")
    if group_text:
        subtitle_parts.append(f"👥 {group_text}")
    subtitle_lbl = QLabel(" • ".join(subtitle_parts), container)
    subtitle_lbl.setStyleSheet("color: #a9b2c7;")
    subtitle_lbl.setWordWrap(True)
    right.addWidget(title_lbl)
    if subtitle_parts:
        right.addWidget(subtitle_lbl)
    h.addLayout(right, 1)
    return container

def create_status_chip(parent, text: str, kind: str = "info") -> QLabel:
    lbl = QLabel(text, parent)
    colors = {
        'success': ("#1e824c", "#b5ffd9"),
        'warning': ("#c77d00", "#ffe3b3"),
        'info': (ACCENT_BLUE, "#c8f3ff"),
    }
    bg, fg = colors.get(kind, colors['info'])
    try:
        lbl.setStyleSheet(
            f"background-color: {bg}; color: {fg}; border: 0; padding: 4px 10px; border-radius: 10px; font-weight: 700;"
        )
    except Exception:
        pass
    return lbl

def create_small_button(parent, text, command, **kwargs):
    btn = QPushButton(text, parent)
    btn.setCursor(Qt.PointingHandCursor)
    btn.clicked.connect(command)
    return btn

def create_accent_button(parent, text, command, **kwargs):
    btn = QPushButton(text, parent)
    btn.setProperty("class", "accent")
    btn.setObjectName("accent")
    btn.setCursor(Qt.PointingHandCursor)
    btn.clicked.connect(command)
    return btn

def create_danger_button(parent, text, command, **kwargs):
    btn = QPushButton(text, parent)
    btn.setProperty("class", "danger")
    btn.setObjectName("danger")
    btn.setCursor(Qt.PointingHandCursor)
    btn.clicked.connect(command)
    return btn

def create_warning_button(parent, text, command, **kwargs):
    btn = QPushButton(text, parent)
    btn.setProperty("class", "warning")
    btn.setObjectName("warning")
    btn.setCursor(Qt.PointingHandCursor)
    btn.clicked.connect(command)
    return btn

def create_title_label(parent, text):
    lbl = QLabel(text, parent)
    lbl.setObjectName("title")
    lbl.setProperty("class", "title")
    return lbl

def create_subtitle_label(parent, text):
    lbl = QLabel(text, parent)
    lbl.setObjectName("subtitle")
    lbl.setProperty("class", "subtitle")
    return lbl

def create_info_label(parent, text):
    lbl = QLabel(text, parent)
    lbl.setObjectName("info")
    lbl.setProperty("class", "info")
    return lbl

def create_status_label(parent, text):
    lbl = QLabel(text, parent)
    lbl.setObjectName("status")
    return lbl

def create_main_frame(parent):
    return QWidget(parent)

def create_content_frame(parent):
    return QWidget(parent)

def create_text_widget(parent, **kwargs):
    txt = QTextEdit(parent)
    if kwargs.get("state") == "disabled":
        txt.setReadOnly(True)
    return txt

def create_entry_widget(parent, **kwargs):
    return QLineEdit(parent)

def create_listbox_widget(parent, **kwargs):
    return QListWidget(parent)

def create_treeview_widget(parent, columns, **kwargs):
    tree = QTreeWidget(parent)
    tree.setColumnCount(len(columns))
    tree.setHeaderLabels(list(columns))
    return tree

def create_scrollbar(parent, orient="vertical", **kwargs):
    bar = QScrollBar(parent)
    bar.setOrientation(Qt.Vertical if orient == "vertical" else Qt.Horizontal)
    return bar

def apply_button_hover_effects(button):
    # Los efectos de hover se aplican por hoja de estilos global
    return

def create_modal_window(parent, title, size):
    """Crea un QDialog modal con tamaño WxH (string '800x600')."""
    dlg = QDialog(parent)
    dlg.setModal(True)
    dlg.setWindowTitle(title)
    try:
        w, h = [int(x) for x in str(size).lower().split('x')]
        dlg.resize(w, h)
    except Exception:
        pass
    return dlg

def center_window(window):
    screen = window.screen().availableGeometry() if hasattr(window, 'screen') else None
    if screen:
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        window.move(x, y)

def create_role_card(parent, icon_text: str, title: str, description: str, on_click, icon_size: int = 64):
    """Crea una tarjeta de rol con diseño exacto del HTML proporcionado.
    
    Args:
        parent: Widget padre
        icon_text: Texto del ícono (emoji/símbolo Unicode) o ruta de imagen (ej: "images/admin.png")
        title: Título del rol
        description: Descripción del rol
        on_click: Función a ejecutar al hacer clic
        icon_size: Tamaño del ícono en píxeles
    """
    # Colores exactos del HTML
    PRIMARY_COLOR = "#136dec"
    BG_LIGHT_HTML = "#f6f7f8"
    CARD_BG = "#ffffff"  # Blanco para las tarjetas
    BORDER_COLOR = "#e5e7eb"  # gray-200
    BORDER_COLOR_DARK = "#1f2937"  # gray-800
    TEXT_GRAY_DARK = "#374151"  # gray-900
    TEXT_GRAY_LIGHT = "#6b7280"  # gray-500
    TEXT_GRAY_DARK_MODE = "#f3f4f6"  # gray-100
    TEXT_GRAY_LIGHT_MODE = "#9ca3af"  # gray-400
    
    container = QWidget(parent)
    container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    container.setMinimumHeight(180)
    container.setMinimumWidth(0)  # Sin ancho mínimo para que se expanda
    container.setMaximumWidth(16777215)  # Ancho máximo muy grande (Qt default)
    container.setCursor(Qt.PointingHandCursor)
    
    # Estilos base y hover (exactos del HTML)
    # Sin padding que cree efecto de cuadro - solo padding mínimo necesario
    base_style = (
        f"background-color: {CARD_BG}; "
        f"border: 1px solid {BORDER_COLOR}; "
        f"border-radius: 12px; "
        f"padding: 0px;"
    )
    hover_style = (
        f"background-color: {CARD_BG}; "
        f"border: 1px solid {PRIMARY_COLOR}; "
        f"border-radius: 12px; "
        f"padding: 0px;"
    )
    container.setStyleSheet(base_style)
    
    # Layout principal vertical - Sin márgenes que creen efecto de cuadro
    main_layout = QVBoxLayout(container)
    main_layout.setContentsMargins(24, 24, 24, 24)  # Padding dentro del layout, no en el estilo
    main_layout.setSpacing(12)
    main_layout.setAlignment(Qt.AlignCenter)
    
    # Verificar si es una ruta de imagen (termina en extensión de imagen)
    is_image = False
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']
    if isinstance(icon_text, str):
        icon_text_lower = icon_text.lower()
        is_image = any(icon_text_lower.endswith(ext) for ext in image_extensions)
    
    if is_image:
        # Para imágenes: mostrar solo la imagen sin círculo de fondo
        icon_label = QLabel(container)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Es una imagen: cargar y mostrar la imagen
        image_path = icon_text
        # Si la ruta es relativa, construir la ruta absoluta desde el directorio del script
        if not os.path.isabs(image_path):
            # Obtener el directorio del archivo styles.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, image_path)
        
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # Escalar la imagen más grande (150% del tamaño del icono para que se vea mejor)
            image_size = int(icon_size * 1.5)  # Hacer la imagen 50% más grande
            scaled_pixmap = pixmap.scaled(
                image_size,
                image_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            icon_label.setPixmap(scaled_pixmap)
            # Hacer que el label sea transparente y sin bordes
            icon_label.setStyleSheet(
                "background-color: transparent; "
                "border: none; "
                "padding: 0px; "
                "margin: 0px;"
            )
            # Ajustar el tamaño del label al tamaño de la imagen escalada
            icon_label.setFixedSize(scaled_pixmap.width(), scaled_pixmap.height())
            icon_label.setScaledContents(False)  # No escalar automáticamente, usar el pixmap escalado
        else:
            # Si la imagen no existe, usar un emoji por defecto
            icon_label.setText("❓")
            icon_label.setStyleSheet(
                f"color: {PRIMARY_COLOR}; "
                f"font-size: {icon_size - 16}px; "
                f"font-weight: 400;"
            )
        
        # Agregar la imagen directamente al layout principal sin contenedor circular
        main_layout.addWidget(icon_label, 0, Qt.AlignCenter)
    else:
        # Es texto emoji: usar el código original con círculo de fondo
        # Contenedor del ícono con fondo circular (exacto del HTML: bg-primary/10)
        icon_container = QWidget(container)
        icon_container.setFixedSize(icon_size, icon_size)
        # bg-primary/10 = rgba(19, 109, 236, 0.1)
        icon_container.setStyleSheet(
            f"background-color: rgba(19, 109, 236, 0.1); "
            f"border-radius: {icon_size // 2}px;"
        )
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        icon_label = QLabel(icon_text, icon_container)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet(
            f"color: {PRIMARY_COLOR}; "
            f"font-size: {icon_size - 16}px; "
            f"font-weight: 400;"
        )
        
        icon_layout.addWidget(icon_label)
        main_layout.addWidget(icon_container, 0, Qt.AlignCenter)
    
    # Contenedor de texto - Sin restricciones para que el texto fluya naturalmente
    text_layout = QVBoxLayout()
    text_layout.setSpacing(4)
    text_layout.setAlignment(Qt.AlignCenter)
    text_layout.setContentsMargins(0, 0, 0, 0)
    
    # Título (exacto del HTML: text-gray-900 dark:text-gray-100) - Sin encapsulado ni truncado
    title_label = QLabel(title, container)
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
    title_label.setWordWrap(False)  # Sin encapsulado, texto fluye naturalmente
    # Desactivar cualquier elisión o truncamiento de texto
    title_label.setTextFormat(Qt.PlainText)
    title_label.setOpenExternalLinks(False)
    # Sin restricciones de ancho - permitir que el texto determine el tamaño
    title_label.setMinimumWidth(0)
    title_label.setMaximumWidth(16777215)  # Sin límite de ancho máximo
    title_label.setMinimumHeight(0)
    # Calcular el ancho necesario para el texto completo
    from PySide6.QtGui import QFontMetrics
    font = title_label.font()
    font.setPointSize(16)
    font.setBold(True)
    title_label.setFont(font)
    fm = QFontMetrics(font)
    text_width = fm.horizontalAdvance(title)
    title_label.setMinimumWidth(text_width)  # Asegurar ancho mínimo para el texto completo
    # Asegurar que el texto se muestre completo - Sin fondo ni bordes que parezcan cuadro
    title_label.setStyleSheet(
        f"color: {TEXT_GRAY_DARK}; "
        f"font-size: 16px; "
        f"font-weight: 700; "
        f"background-color: transparent; "
        f"border: none; "
        f"padding: 0px; "
        f"margin: 0px;"
    )
    text_layout.addWidget(title_label, 0, Qt.AlignCenter)
    
    # Descripción (exacto del HTML: text-gray-500 dark:text-gray-400) - Sin encapsulado ni truncado
    desc_label = QLabel(description, container)
    desc_label.setAlignment(Qt.AlignCenter)
    desc_label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
    desc_label.setWordWrap(False)  # Sin encapsulado, texto fluye naturalmente
    # Desactivar cualquier elisión o truncamiento de texto
    desc_label.setTextFormat(Qt.PlainText)
    desc_label.setOpenExternalLinks(False)
    # Sin restricciones de ancho - permitir que el texto determine el tamaño
    desc_label.setMinimumWidth(0)
    desc_label.setMaximumWidth(16777215)  # Sin límite de ancho máximo
    desc_label.setMinimumHeight(0)
    # Calcular el ancho necesario para el texto completo
    desc_font = desc_label.font()
    desc_font.setPointSize(14)
    desc_label.setFont(desc_font)
    desc_fm = QFontMetrics(desc_font)
    desc_text_width = desc_fm.horizontalAdvance(description)
    desc_label.setMinimumWidth(desc_text_width)  # Asegurar ancho mínimo para el texto completo
    # Asegurar que el texto se muestre completo - Sin fondo ni bordes que parezcan cuadro
    desc_label.setStyleSheet(
        f"color: {TEXT_GRAY_LIGHT}; "
        f"font-size: 14px; "
        f"font-weight: 400; "
        f"background-color: transparent; "
        f"border: none; "
        f"padding: 0px; "
        f"margin: 0px;"
    )
    text_layout.addWidget(desc_label, 0, Qt.AlignCenter)
    
    main_layout.addLayout(text_layout)
    
    # Efectos de hover y click (exacto del HTML)
    class CardHoverEffect(QObject):
        def __init__(self, widget):
            super().__init__(widget)
            self.widget = widget
            self._shadow_effect = None
            
        def eventFilter(self, obj, ev):
            if ev.type() == QEvent.Enter:
                # Cambiar estilo y agregar sombra (hover:shadow-lg hover:-translate-y-1)
                self.widget.setStyleSheet(hover_style)
                try:
                    shadow = QGraphicsDropShadowEffect(self.widget)
                    shadow.setBlurRadius(20)
                    shadow.setColor(QColor(0, 0, 0, 40))  # Sombra negra con opacidad
                    shadow.setOffset(0, 4)
                    self.widget.setGraphicsEffect(shadow)
                    self._shadow_effect = shadow
                except Exception:
                    pass
            elif ev.type() == QEvent.Leave:
                # Restaurar estilo y quitar sombra
                self.widget.setStyleSheet(base_style)
                try:
                    self.widget.setGraphicsEffect(None)
                    self._shadow_effect = None
                except Exception:
                    pass
            elif ev.type() == QEvent.MouseButtonRelease:
                try:
                    on_click()
                except Exception:
                    pass
            return False
    
    hover_effect = CardHoverEffect(container)
    container.installEventFilter(hover_effect)
    container._hover_effect = hover_effect  # Evitar GC
    
    return container

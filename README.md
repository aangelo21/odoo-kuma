# Sistema de Gestión de Cursos - KUMA

## 📚 Descripción General

Este proyecto es un módulo personalizado de Odoo para la gestión de cursos de formación. Permite administrar cursos, categorías y familias profesionales de manera estructurada, integrándose con el sistema Odoo.

## 🌟 Características Principales

- Gestión de cursos con nombre, descripción, código, duración y modalidad.
- Organización de cursos por categorías y familias profesionales.
- Fechas de inicio/fin y consolidación.
- Número de alumnos, alumnos consolidados y alumnos al finalizar.
- Vistas de calendario para la planificación de cursos.
- Filtros y búsqueda avanzada por modalidad, categoría y familia profesional.
- Acceso controlado por roles y permisos de Odoo.

## 📂 Estructura del Proyecto

- `addons/gestion_cursos/models/`: Modelos de datos (`curso.py`, `categoria.py`, `familia_profesional.py`).
- `addons/gestion_cursos/views/`: Vistas XML para cursos, categorías, familias profesionales y calendario.
- `addons/gestion_cursos/security/`: Reglas de acceso (`ir.model.access.csv`).
- `addons/gestion_cursos/static/`: Recursos estáticos (colores SCSS).
- `addons/gestion_cursos/controllers/`: Controladores (si aplica).

## 🚀 Instalación y Uso

1. Copie la carpeta `gestion_cursos` en el directorio `addons` de su instancia Odoo.
2. Reinicie el servidor de Odoo.
3. Active el modo desarrollador y actualice la lista de aplicaciones.
4. Instale el módulo "Gestión de Cursos" desde el panel de aplicaciones.

## 🖥️ Navegación Principal

- **Cursos**: Gestión y visualización de cursos.
- **Categorías**: Administración de categorías de cursos.
- **Familias Profesionales**: Gestión de familias profesionales.
- **Calendario**: Visualización de cursos en formato calendario.

## 🔐 Seguridad

- Acceso gestionado mediante los permisos estándar de Odoo.
- Cumplimiento de buenas prácticas de seguridad y protección de datos.

---

Para soporte técnico o consultas, contacte con el equipo de soporte a través de la plataforma o el canal habitual.
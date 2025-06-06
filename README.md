# Sistema de Gestión de Cursos y Aulas - KUMA

## 📚 Descripción General

Este proyecto contiene módulos personalizados de Odoo para la gestión de cursos de formación y la gestión de aulas. Permite administrar cursos, categorías, familias profesionales, aulas y horarios de clases, integrándose con el sistema Odoo.

## 🌟 Características Principales

### Gestión de Cursos (`gestion_cursos`)
- Gestión de cursos con nombre, descripción, código, duración y modalidad.
- Organización de cursos por categorías y familias profesionales.
- Fechas de inicio/fin y consolidación.
- Número de alumnos, alumnos consolidados y alumnos al finalizar.
- Vistas de calendario para la planificación de cursos.
- Filtros y búsqueda avanzada por modalidad, categoría y familia profesional.
- Notificaciones automáticas por email al crear, modificar o eliminar cursos.
- Acceso controlado por roles y permisos de Odoo.

### Gestión de Aulas (`gestion_clases`)
- Gestión de aulas y centros.
- Plantillas de horarios semanales para cursos.
- Generación automática de eventos de clase a partir de plantillas.
- Vista de calendario semanal y panel Kanban por aula.
- Control de solapamiento de horarios y aulas.
- Notificaciones por email cuando una clase está lista para subir a plataforma.
- Filtros y agrupaciones por curso y aula.

## 📂 Estructura del Proyecto

- `addons/gestion_cursos/models/`: Modelos de datos de cursos, categorías y familias profesionales.
- `addons/gestion_cursos/views/`: Vistas XML para cursos, categorías, familias profesionales y calendario.
- `addons/gestion_cursos/security/`: Reglas de acceso.
- `addons/gestion_clases/models/`: Modelos de datos de aulas y horarios.
- `addons/gestion_clases/views/`: Vistas XML para aulas, horarios, calendario y panel Kanban.
- `addons/gestion_clases/security/`: Reglas de acceso.
- `addons/temas_kuma/static/`: Recursos estáticos (colores SCSS, estilos CSS).
- `docker-compose.yml`: Configuración para entorno de desarrollo con Odoo y PostgreSQL.

## 🚀 Instalación y Uso

1. Copie las carpetas `gestion_cursos`, `gestion_clases` y `temas_kuma` en el directorio `addons` de su instancia Odoo.
2. Reinicie el servidor de Odoo.
3. Active el modo desarrollador y actualice la lista de aplicaciones.
4. Instale los módulos "Gestión de Cursos", "Gestión de Aulas" y "Temas Kuma" desde el panel de aplicaciones.

## 🖥️ Navegación Principal

- **Cursos**: Gestión y visualización de cursos.
- **Categorías**: Administración de categorías de cursos.
- **Familias Profesionales**: Gestión de familias profesionales.
- **Calendario de Cursos**: Visualización de cursos en formato calendario.
- **Aulas**: Gestión de aulas y centros.
- **Horarios**: Plantillas de horarios semanales.
- **Calendario de Horarios**: Visualización semanal de clases.
- **Panel de Aulas**: Vista Kanban de ocupación de aulas.

## 🔐 Seguridad

- Acceso gestionado mediante los permisos estándar de Odoo.
- Control de solapamiento de horarios y aulas.
- Cumplimiento de buenas prácticas de seguridad y protección de datos.

# KUMA - Courses and Classrooms Management System

## 📚 General Description

This project contains custom Odoo modules for training courses and classroom management. It allows you to manage courses, categories, professional families, classrooms, and class schedules, fully integrated with the Odoo system.

## 🌟 Main Features

### Courses Management (`gestion_cursos`)
- Manage courses with name, description, code, duration, and modality.
- Organize courses by categories and professional families.
- Start/end/consolidation dates.
- Number of students, consolidated students, and students at completion.
- Calendar views for course planning.
- Advanced filters and search by modality, category, and professional family.
- Automatic email notifications on course creation, update, or deletion.
- Access control via Odoo roles and permissions.

### Classroom Management (`gestion_clases`)
- Manage classrooms and centers.
- Weekly schedule templates for courses.
- Automatic generation of class events from templates.
- Weekly calendar view and Kanban panel by classroom.
- Overlap control for schedules and classrooms.
- Email notifications when a class is ready to upload to the platform.
- Filters and grouping by course and classroom.

## 📂 Project Structure

- `addons/gestion_cursos/models/`: Data models for courses, categories, and professional families.
- `addons/gestion_cursos/views/`: XML views for courses, categories, professional families, and calendar.
- `addons/gestion_cursos/security/`: Access rules.
- `addons/gestion_clases/models/`: Data models for classrooms and schedules.
- `addons/gestion_clases/views/`: XML views for classrooms, schedules, calendar, and Kanban panel.
- `addons/gestion_clases/security/`: Access rules.
- `addons/temas_kuma/static/`: Static resources (SCSS colors, CSS styles).
- `docker-compose.yml`: Development environment configuration for Odoo and PostgreSQL.

## 🚀 Installation and Usage

1. Copy the `gestion_cursos`, `gestion_clases`, and `temas_kuma` folders into your Odoo instance's `addons` directory.
2. Restart the Odoo server.
3. Activate developer mode and update the apps list.
4. Install the "Gestión de Cursos", "Gestión de Aulas", and "Temas Kuma" modules from the apps panel.

## 🖥️ Main Navigation

- **Courses**: Manage and view courses.
- **Categories**: Manage course categories.
- **Professional Families**: Manage professional families.
- **Courses Calendar**: Calendar view of courses.
- **Classrooms**: Manage classrooms and centers.
- **Schedules**: Weekly schedule templates.
- **Schedules Calendar**: Weekly class calendar view.
- **Classrooms Panel**: Kanban view of classroom occupancy.

## 🔐 Security

- Access managed through Odoo standard permissions.
- Overlap control for schedules and classrooms.
- Follows best practices for security and data protection.
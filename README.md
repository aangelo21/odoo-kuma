# Sistema de Gestión de Cursos y Aulas - KUMA

## 📚 Descripción General

Este proyecto contiene módulos personalizados de Odoo para la gestión integral de cursos de formación, aulas y procesos comerciales. El sistema está diseñado para facilitar la administración de cursos, control de horarios, gestión de aulas y seguimiento de captación comercial, integrándose completamente con el ecosistema Odoo.

## 🌟 Características Principales

### Gestión de Cursos (`gestion_cursos`)
- **Gestión completa de cursos**: Nombre, expediente, código, duración y modalidad (presencial, semipresencial, teleformación).
- **Sistema de tutores**: Asignación de múltiples tutores por curso con relaciones many2many.
- **Categorización avanzada**: Organización por categorías con colores personalizables para calendario (SEPE, SCE, EOI, Reskilling, Oposiciones).
- **Control de fechas**: Fechas de inicio, fin y consolidación con visualización en calendario.
- **Seguimiento de alumnos**: Control de número total, consolidados y finalizados con indicadores visuales.
- **Notificaciones automáticas**: 
  - Emails al crear, modificar o eliminar cursos
  - Resúmenes diarios automáticos
  - Resúmenes semanales programados
- **Vistas especializadas**: Lista, formulario y calendario con filtros por categoría y tutor.
- **Filtros avanzados**: Búsqueda por modalidad, categoría, tutor y fechas.

### Gestión de Aulas (`gestion_clases`)
- **Gestión de aulas y centros**: Control de espacios físicos y virtuales.
- **Plantillas de horarios semanales**: Configuración de horarios por días de la semana.
- **Generación automática de eventos**: Creación automática de clases a partir de plantillas.
- **Control de solapamientos**: Validación automática para evitar conflictos de horarios y aulas.
- **Panel Kanban de aulas**: Vista visual del estado de grabación de clases por aula.
- **Gestión de incidencias**: 
  - Control de problemas técnicos (cámara en negro, imagen congelada, sin sonido, etc.)
  - Wizard para cambio rápido de incidencias
- **Control de temario**: Registro del contenido impartido en cada clase.
- **Asignación de tutores**: Tutores específicos por clase individual.
- **Notificaciones de estado**: Email automático cuando una clase está lista para subir a plataforma.
- **Funcionalidad de copia**: Botón para copiar información de clases al portapapeles.
- **Calendario de eventos**: Vista calendario de todas las clases programadas.
- **Aulas virtuales**: Aulas especiales para "Subidas" e "Incidencias" (ocultas en listas).

### Gestión Comercial (`gestion_comerciales`)
- **Registro de captación**: Sistema para registrar alumnos captados por empleado y categoría.
- **Dashboard con gráficos**: Visualización de barras interactivas de captación por trabajador.
- **Seguridad por roles**: Los usuarios solo ven sus propios registros, administradores ven todo.
- **Filtros temporales**: Agrupación por mes, año y empleado.
- **Integración con RRHH**: Conexión automática con módulo de empleados.
- **Controladores web**: API REST para datos de gráficos.
- **Análisis estadístico**: Totales automáticos y métricas de rendimiento.

## 📂 Estructura del Proyecto

- `addons/gestion_cursos/models/`: Modelos de cursos, categorías y tutores con lógica de negocio.
- `addons/gestion_cursos/views/`: Vistas XML para gestión completa de cursos y calendario.
- `addons/gestion_cursos/security/`: Reglas de acceso y permisos.
- `addons/gestion_clases/models/`: Modelos de aulas y horarios con validaciones avanzadas.
- `addons/gestion_clases/views/`: Vistas XML para aulas, horarios, calendario y panel Kanban.
- `addons/gestion_clases/wizard/`: Wizard para cambio de incidencias.
- `addons/gestion_clases/static/`: JavaScript para funcionalidades Kanban y CSS personalizado.
- `addons/gestion_clases/security/`: Control de acceso.
- `addons/gestion_comerciales/models/`: Modelos de captación con cálculos automáticos.
- `addons/gestion_comerciales/views/`: Vistas y gráficos de gestión comercial.
- `addons/gestion_comerciales/controllers/`: Controladores web para APIs.
- `addons/gestion_comerciales/static/`: CSS personalizado para gráficos.
- `addons/temas_kuma/static/`: Recursos estáticos (colores SCSS, estilos CSS).
- `docker-compose.yml`: Configuración para entorno de desarrollo con Odoo y PostgreSQL.

## 🚀 Instalación y Uso

1. Copie las carpetas `gestion_cursos`, `gestion_clases`, `gestion_comerciales` y `temas_kuma` en el directorio `addons` de su instancia Odoo.
2. Reinicie el servidor de Odoo.
3. Active el modo desarrollador y actualice la lista de aplicaciones.
4. Instale los módulos "Gestión de Cursos", "Gestión de Aulas", "Gestión Comerciales" y "Temas Kuma" desde el panel de aplicaciones.

## 🖥️ Navegación Principal

### Gestión de Cursos
- **Cursos**: Gestión completa de cursos con filtros por categoría.
- **Categorías**: Administración de categorías con colores para calendario.
- **Tutores**: Gestión de profesores y formadores.
- **Calendario de Cursos**: Visualización temporal con códigos de color por categoría.

### Gestión de Aulas
- **Calendario**: Vista calendario de todos los eventos de clase.
- **Grabación de clases**: Panel Kanban para control de estado de grabaciones.
- **Grupos presenciales**: Gestión de plantillas de horarios semanales.
- **Aulas**: Administración de espacios físicos y centros.

### Gestión Comercial
- **Captación de Alumnos**: Registro personal de captaciones por empleado.
- **Gráfico**: Dashboard con estadísticas visuales de captación.
- **Todas las Captaciones (Admin)**: Vista completa para administradores.

## 🔧 Funcionalidades Técnicas Avanzadas

### Automatizaciones
- **Cron Jobs**: Notificaciones diarias y semanales automáticas de cursos.
- **Generación de eventos**: Creación automática de clases desde plantillas.
- **Validaciones**: Control automático de solapamientos de horarios.
- **Notificaciones**: Emails automáticos en cambios de estado.

### Integraciones
- **Módulo HR**: Conexión con empleados para gestión comercial.
- **Sistema de permisos**: Roles diferenciados (usuario/administrador).
- **APIs web**: Controladores para datos de gráficos en tiempo real.

### Características UX/UI
- **Colores dinámicos**: Sistema de colores por categoría en calendarios.
- **Estados visuales**: Indicadores Kanban para estado de clases.
- **Copiar información**: Función de copia rápida al portapapeles.
- **Filtros inteligentes**: Búsquedas avanzadas y agrupaciones.
- **Vistas especializadas**: Calendario, Kanban, Lista y Formulario adaptadas.

## 🔐 Seguridad

## 🔐 Seguridad

- **Control de acceso granular**: Permisos específicos por módulo y funcionalidad.
- **Segmentación de datos**: Los empleados solo acceden a sus registros comerciales.
- **Validaciones de integridad**: Control automático de solapamientos y conflictos.
- **Auditoría**: Registro de cambios con notificaciones por email.
- **Roles diferenciados**: Usuario estándar vs administrador con permisos completos.

## 📊 Métricas y Reportes

- **Dashboard comercial**: Gráficos de barras con datos de captación en tiempo real.
- **Resúmenes automáticos**: Emails diarios y semanales con estado de cursos.
- **Indicadores visuales**: Estados Kanban para seguimiento de grabaciones.
- **Totales dinámicos**: Cálculos automáticos de alumnos por estado.
- **Filtros temporales**: Agrupación por mes/año para análisis histórico.

---

# KUMA - Courses and Classrooms Management System

## 📚 General Description

This project contains custom Odoo modules for comprehensive management of training courses, classrooms, and commercial processes. The system is designed to facilitate course administration, schedule control, classroom management, and commercial tracking, fully integrated with the Odoo ecosystem.

## 🌟 Main Features

### Courses Management (`gestion_cursos`)
- **Complete course management**: Name, file number, code, duration, and modality (face-to-face, blended, e-learning).
- **Tutors system**: Assignment of multiple tutors per course with many2many relationships.
- **Advanced categorization**: Organization by categories with customizable calendar colors (SEPE, SCE, EOI, Reskilling, Examinations).
- **Date control**: Start, end, and consolidation dates with calendar visualization.
- **Student tracking**: Control of total, consolidated, and graduated numbers with visual indicators.
- **Automatic notifications**: 
  - Emails when creating, modifying, or deleting courses
  - Automatic daily summaries
  - Scheduled weekly summaries
- **Specialized views**: List, form, and calendar with category and tutor filters.
- **Advanced filters**: Search by modality, category, tutor, and dates.

### Classroom Management (`gestion_clases`)
- **Classroom and center management**: Control of physical and virtual spaces.
- **Weekly schedule templates**: Configuration of schedules by weekdays.
- **Automatic event generation**: Automatic class creation from templates.
- **Overlap control**: Automatic validation to avoid schedule and classroom conflicts.
- **Classroom Kanban panel**: Visual view of class recording status by classroom.
- **Incident management**: 
  - Control of technical problems (black camera, frozen image, no sound, etc.)
  - Wizard for quick incident changes
- **Syllabus control**: Registration of content taught in each class.
- **Tutor assignment**: Specific tutors for individual classes.
- **Status notifications**: Automatic email when a class is ready to upload to platform.
- **Copy functionality**: Button to copy class information to clipboard.
- **Event calendar**: Calendar view of all scheduled classes.
- **Virtual classrooms**: Special classrooms for "Uploads" and "Incidents" (hidden in lists).

### Commercial Management (`gestion_comerciales`)
- **Enrollment tracking**: System to register students enrolled by employee and category.
- **Dashboard with charts**: Interactive bar visualization of enrollment by worker.
- **Role-based security**: Users only see their own records, administrators see everything.
- **Time filters**: Grouping by month, year, and employee.
- **HR integration**: Automatic connection with employee module.
- **Web controllers**: REST API for chart data.
- **Statistical analysis**: Automatic totals and performance metrics.

## 📂 Project Structure

- `addons/gestion_cursos/models/`: Course, category, and tutor models with business logic.
- `addons/gestion_cursos/views/`: XML views for complete course management and calendar.
- `addons/gestion_cursos/security/`: Access rules and permissions.
- `addons/gestion_clases/models/`: Classroom and schedule models with advanced validations.
- `addons/gestion_clases/views/`: XML views for classrooms, schedules, calendar, and Kanban panel.
- `addons/gestion_clases/wizard/`: Wizard for incident changes.
- `addons/gestion_clases/static/`: JavaScript for Kanban functionalities and custom CSS.
- `addons/gestion_clases/security/`: Access control.
- `addons/gestion_comerciales/models/`: Enrollment models with automatic calculations.
- `addons/gestion_comerciales/views/`: Views and charts for commercial management.
- `addons/gestion_comerciales/controllers/`: Web controllers for APIs.
- `addons/gestion_comerciales/static/`: Custom CSS for charts.
- `addons/temas_kuma/static/`: Static resources (SCSS colors, CSS styles).
- `docker-compose.yml`: Development environment configuration for Odoo and PostgreSQL.

## 🚀 Installation and Usage

1. Copy the `gestion_cursos`, `gestion_clases`, `gestion_comerciales`, and `temas_kuma` folders into your Odoo instance's `addons` directory.
2. Restart the Odoo server.
3. Activate developer mode and update the apps list.
4. Install the "Gestión de Cursos", "Gestión de Aulas", "Gestión Comerciales", and "Temas Kuma" modules from the apps panel.

## 🖥️ Main Navigation

### Course Management
- **Courses**: Complete course management with category filters.
- **Categories**: Category administration with calendar colors.
- **Tutors**: Teacher and trainer management.
- **Course Calendar**: Temporal visualization with color codes by category.

### Classroom Management
- **Calendar**: Calendar view of all class events.
- **Class Recording**: Kanban panel for recording status control.
- **Face-to-face Groups**: Weekly schedule template management.
- **Classrooms**: Physical space and center administration.

### Commercial Management
- **Student Enrollment**: Personal enrollment registration by employee.
- **Chart**: Dashboard with visual enrollment statistics.
- **All Enrollments (Admin)**: Complete view for administrators.

## 🔧 Advanced Technical Features

### Automations
- **Cron Jobs**: Automatic daily and weekly course notifications.
- **Event generation**: Automatic class creation from templates.
- **Validations**: Automatic schedule overlap control.
- **Notifications**: Automatic emails on status changes.

### Integrations
- **HR Module**: Connection with employees for commercial management.
- **Permission system**: Differentiated roles (user/administrator).
- **Web APIs**: Controllers for real-time chart data.

### UX/UI Features
- **Dynamic colors**: Color system by category in calendars.
- **Visual states**: Kanban indicators for class status.
- **Copy information**: Quick copy function to clipboard.
- **Smart filters**: Advanced searches and groupings.
- **Specialized views**: Calendar, Kanban, List, and Form adapted.

## 🔐 Security

- **Granular access control**: Specific permissions by module and functionality.
- **Data segmentation**: Employees only access their commercial records.
- **Integrity validations**: Automatic overlap and conflict control.
- **Audit**: Change logging with email notifications.
- **Differentiated roles**: Standard user vs administrator with full permissions.

## 📊 Metrics and Reports

- **Commercial dashboard**: Bar charts with real-time enrollment data.
- **Automatic summaries**: Daily and weekly emails with course status.
- **Visual indicators**: Kanban states for recording tracking.
- **Dynamic totals**: Automatic student calculations by status.
- **Time filters**: Month/year grouping for historical analysis.
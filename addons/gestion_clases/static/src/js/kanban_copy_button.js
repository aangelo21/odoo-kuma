/**
 * Función para copiar la información de una tarjeta kanban al portapapeles
 * @param {HTMLElement} button - El elemento que fue clickeado
 */
function copyCardInfo(button) {
    try {        // Obtener los datos del botón
        const curso = button.getAttribute('data-curso') || '';
        const fecha = button.getAttribute('data-fecha') || '';
        const fechaFin = button.getAttribute('data-fecha-fin') || '';
        const temario = button.getAttribute('data-temario') || '';
        const tutor = button.getAttribute('data-tutor') || '';
        const aula = button.getAttribute('data-aula') || '';
        
        // Formatear las fechas y horas
        let fechaFormato = '';
        let horaInicio = '';
        let horaFin = '';
        
        if (fecha) {
            const fechaObj = new Date(fecha);
            // Formato DD-MM-YYYY
            const dia = fechaObj.getDate().toString().padStart(2, '0');
            const mes = (fechaObj.getMonth() + 1).toString().padStart(2, '0');
            const año = fechaObj.getFullYear();
            fechaFormato = `${dia}-${mes}-${año}`;
            
            // Hora de inicio
            const horas = fechaObj.getHours().toString().padStart(2, '0');
            const minutos = fechaObj.getMinutes().toString().padStart(2, '0');
            horaInicio = `${horas}:${minutos}`;
        }
        
        if (fechaFin) {
            const fechaFinObj = new Date(fechaFin);
            // Hora de fin
            const horas = fechaFinObj.getHours().toString().padStart(2, '0');
            const minutos = fechaFinObj.getMinutes().toString().padStart(2, '0');
            horaFin = `${horas}:${minutos}`;
        }        // Crear el texto en el formato solicitado: fecha (hora inicio A hora fin). curso. tutor. aula. temario
        let partes = [];
        
        // Agregar fecha si existe
        if (fechaFormato) {
            partes.push(fechaFormato);
        }
        
        // Agregar horario si existe
        if (horaInicio && horaFin) {
            partes.push(`(${horaInicio} A ${horaFin}).`);
        }
        
        // Agregar curso si existe
        if (curso) {
            partes.push(curso + '.');
        }
        
        // Agregar tutor si existe
        if (tutor) {
            partes.push(tutor + '.');
        }
        
        // Agregar aula si existe (filtrar el nombre del centro)
        if (aula) {
            // Filtrar el nombre del centro que viene después del guión
            let aulaFiltrada = aula;
            if (aula.includes(' - ')) {
                aulaFiltrada = aula.split(' - ')[0];
            }
            partes.push(aulaFiltrada + '.');
        }
        
        // Agregar temario si existe
        if (temario) {
            partes.push(temario);
        }// Unir todas las partes con espacios
        let textoACopiar = partes.join(' ').trim();
        
        // Función para mostrar feedback visual
        const showFeedback = () => {
            const originalIcon = button.querySelector('i');
            const originalClass = originalIcon.className;
            
            // Cambiar el icono a check
            originalIcon.className = 'fa fa-check text-success';
            button.classList.add('copied');
            
            // Restaurar después de 1.5 segundos
            setTimeout(() => {
                originalIcon.className = originalClass;
                button.classList.remove('copied');
            }, 1500);
        };
        
        // Copiar al portapapeles usando la API moderna
        if (navigator.clipboard && window.isSecureContext) {            navigator.clipboard.writeText(textoACopiar)
                .then(() => {
                    showFeedback();
                })
                .catch(err => {
                    console.error('Error al copiar al portapapeles:', err);
                    fallbackCopy(textoACopiar, showFeedback);
                });
        } else {
            // Fallback para navegadores más antiguos
            fallbackCopy(textoACopiar, showFeedback);
        }
        
    } catch (error) {
        console.error('Error en copyCardInfo:', error);
    }
}

/**
 * Método fallback para copiar texto en navegadores más antiguos
 * @param {string} text - Texto a copiar
 * @param {Function} callback - Función callback para el feedback
 */
function fallbackCopy(text, callback) {
    try {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
          if (successful) {
            callback();
        } else {
            console.error('No se pudo copiar usando el método fallback');
        }
    } catch (error) {
        console.error('Error en fallbackCopy:', error);
    }
}

// Hacer la función disponible globalmente para que pueda ser llamada desde el XML
window.copyCardInfo = copyCardInfo;

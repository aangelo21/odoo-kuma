/**
 * Funcionalidad para gestionar incidencias en las tarjetas kanban
 */

// Variable global para almacenar el ID del registro actual
let currentRecordId = null;

/**
 * Función para abrir el modal de incidencias
 * @param {HTMLElement} button - El elemento que fue clickeado
 */
function openIncidenciasModal(button) {
    try {
        // Obtener los datos del botón
        currentRecordId = button.getAttribute('data-id');
        const incidenciaActual = button.getAttribute('data-incidencia-actual') || '';
        
        // Seleccionar la incidencia actual en el select
        const select = document.getElementById('incidenciaSelect');
        if (select) {
            select.value = incidenciaActual;
        }
        
        // Mostrar el modal usando Bootstrap
        const modal = document.getElementById('incidenciasModal');
        if (modal) {
            // Para Bootstrap 5
            if (typeof bootstrap !== 'undefined') {
                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
            } 
            // Para Bootstrap 4 (jQuery)
            else if (typeof $ !== 'undefined') {
                $(modal).modal('show');
            }
            // Fallback manual
            else {
                modal.style.display = 'block';
                modal.classList.add('show');
                document.body.classList.add('modal-open');
            }
        }
        
    } catch (error) {
        console.error('Error al abrir modal de incidencias:', error);
    }
}

// Hacer las funciones disponibles globalmente inmediatamente
window.openIncidenciasModal = openIncidenciasModal;

/**
 * Función para guardar la incidencia seleccionada
 */
function saveIncidencia() {
    try {
        if (!currentRecordId) {
            console.error('No hay registro seleccionado');
            return;
        }
        
        const select = document.getElementById('incidenciaSelect');
        if (!select) {
            console.error('No se encontró el select de incidencias');
            return;
        }
        
        const incidenciaValue = select.value;
        
        // Actualizar el registro usando la API de Odoo
        updateIncidencia(currentRecordId, incidenciaValue);
        
    } catch (error) {
        console.error('Error al guardar incidencia:', error);
    }
}

// Hacer disponible globalmente
window.saveIncidencia = saveIncidencia;

/**
 * Función para actualizar la incidencia en el servidor
 * @param {string} recordId - ID del registro
 * @param {string} incidenciaValue - Valor de la incidencia seleccionada
 */
function updateIncidencia(recordId, incidenciaValue) {
    // Verificar si existe rpc de Odoo
    if (typeof odoo !== 'undefined' && odoo.define) {
        // Usar el sistema de módulos de Odoo
        odoo.define('incidencias_update', function (require) {
            const rpc = require('web.rpc');
            
            rpc.query({
                model: 'gestion_clases.horario',
                method: 'write',
                args: [[parseInt(recordId)], { incidencias: incidenciaValue }],
            }).then(function(result) {
                if (result) {
                    showSuccessMessage();
                    closeModal();
                    // Recargar la vista
                    window.location.reload();
                } else {
                    showErrorMessage('Error al actualizar la incidencia');
                }
            }).catch(function(error) {
                console.error('Error en RPC:', error);
                showErrorMessage('Error de conexión al actualizar la incidencia');
            });
        });
    } else {
        // Fallback: usar fetch para llamar a un endpoint personalizado
        const data = {
            record_id: recordId,
            incidencia: incidenciaValue
        };
        
        fetch('/gestion_clases/update_incidencia', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                showSuccessMessage();
                closeModal();
                // Recargar la vista
                window.location.reload();
            } else {
                showErrorMessage(result.error || 'Error al actualizar la incidencia');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorMessage('Error de conexión al actualizar la incidencia');
        });
    }
}

/**
 * Función para cerrar el modal
 */
function closeModal() {
    const modal = document.getElementById('incidenciasModal');
    if (modal) {
        // Para Bootstrap 5
        if (typeof bootstrap !== 'undefined') {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        } 
        // Para Bootstrap 4 (jQuery)
        else if (typeof $ !== 'undefined') {
            $(modal).modal('hide');
        }
        // Fallback manual
        else {
            modal.style.display = 'none';
            modal.classList.remove('show');
            document.body.classList.remove('modal-open');
        }
    }
    currentRecordId = null;
}

// Hacer disponible globalmente
window.closeModal = closeModal;

/**
 * Función para mostrar mensaje de éxito
 */
function showSuccessMessage() {
    // Crear un toast o mensaje temporal
    const message = document.createElement('div');
    message.className = 'alert alert-success position-fixed';
    message.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    message.innerHTML = `
        <strong>¡Éxito!</strong> Incidencia actualizada correctamente.
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    document.body.appendChild(message);
    
    // Remover automáticamente después de 3 segundos
    setTimeout(() => {
        if (message.parentElement) {
            message.remove();
        }
    }, 3000);
}

/**
 * Función para mostrar mensaje de error
 * @param {string} errorMsg - Mensaje de error
 */
function showErrorMessage(errorMsg) {
    const message = document.createElement('div');
    message.className = 'alert alert-danger position-fixed';
    message.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    message.innerHTML = `
        <strong>Error:</strong> ${errorMsg}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    document.body.appendChild(message);
    
    // Remover automáticamente después de 5 segundos
    setTimeout(() => {
        if (message.parentElement) {
            message.remove();
        }
    }, 5000);
}

/**
 * Función para obtener el token CSRF (si es necesario)
 */
function getCsrfToken() {
    const token = document.querySelector('meta[name="csrf-token"]');
    return token ? token.getAttribute('content') : '';
}

// Event listeners cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Agregar event listener al botón de guardar
    const saveButton = document.getElementById('saveIncidencia');
    if (saveButton) {
        saveButton.addEventListener('click', saveIncidencia);
    }
    
    // Agregar event listener para cerrar modal con Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
});

// Hacer las funciones disponibles globalmente
window.openIncidenciasModal = openIncidenciasModal;
window.saveIncidencia = saveIncidencia;
window.closeModal = closeModal;

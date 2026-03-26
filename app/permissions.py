"""
Registro de permisos que pueden ser asignados a los distintos cargos.
"""

SYSTEM_PERMISSIONS = {
    "volunteers": {
        "label": "Voluntarios",
        "perms": {
            "view_details": "Ver hoja de servicio completa",
            "edit": "Crear y modificar voluntarios",
            "export": "Exportar datos",
        },
    },
}

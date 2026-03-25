"""
Registry of system permissions available to be assigned to roles.
"""

SYSTEM_PERMISSIONS = {
    "volunteers": {
        "label": "Voluntarios",
        "perms": {
            "view_details": "Ver hoja de servicio completa",
            "add_volunteer": "Crear y modificar voluntarios",
            "export_data": "Exportar datos",
        },
    },
}

def recomendar(historia_usuario):
    """
    Genera recomendaciones ampliadas basadas en la historia de usuario.
    """
    recomendaciones = []

    if "login" in historia_usuario.lower():
        recomendaciones.append("Considera agregar autenticación con OAuth2.")
        recomendaciones.append("Valida credenciales en backend con hashing seguro.")
    if "registro" in historia_usuario.lower():
        recomendaciones.append("Incluye validación de campos obligatorios.")
        recomendaciones.append("Envía correo de confirmación al usuario.")
    if "perfil" in historia_usuario.lower():
        recomendaciones.append("Permite edición de datos personales.")
        recomendaciones.append("Agrega opción para subir foto de perfil.")
    if "admin" in historia_usuario.lower():
        recomendaciones.append("Agrega panel de administración con métricas.")
        recomendaciones.append("Incluye gestión de usuarios y roles.")
    if not recomendaciones:
        recomendaciones.append("No se encontraron recomendaciones específicas. Revisa si puedes agregar criterios funcionales, técnicos o de negocio.")

    return recomendaciones

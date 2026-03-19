import re


def validate_and_format_run(run: str) -> str:
    """
    Valida un RUN chileno y lo devuelve en el formato XX.XXX.XXX-X

    Para ello:
    1. Limpia el input (removiendo puntos, guiones y espacios)
    2. Valida la estructura y el dígito verificador.
    3. Le da el formato correcto
    
    :param run: El RUN a revisar (ej.: '12345678k', '12.345.678-K').
    :return: El RUN formateado (ej.: '12.345.678-K').
    :raises ValueError: Si la validación del RUN falla.
    """

    if not run:
        raise ValueError("RUN no puede estar vacío")

    run_limpio = run.replace(".", "").replace("-", "").strip().upper()

    if not re.fullmatch(r"\d{7,8}[0-9K]", run_limpio):
        raise ValueError("Formato de RUN no válido")

    cuerpo = run_limpio[:-1]
    dv = run_limpio[-1]

    # Calculate expected verification digit (Modulo 11 algorithm)
    digitos_al_reves = map(int, reversed(cuerpo))
    factors = [2, 3, 4, 5, 6, 7]
    s = sum(d * factors[i % 6] for i, d in enumerate(digitos_al_reves))
    resto = 11 - (s % 11)

    if resto == 11:
        dv_esperado = "0"
    elif resto == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(resto)

    if dv != dv_esperado:
        raise ValueError(f"Dígito de verificación no válido. "
                         f"Se esperaba {dv_esperado}, pero se recibió {dv}")

    run_formateado = f"{int(cuerpo):,}".replace(",", ".")
    return f"{run_formateado}-{dv}"

"""Monitor de estabilidad semanal de la aplicación Horario de Bus."""

from typing import Final
import logging
import sys

# ---------------------------------------------------------------------------
# Datos de la aplicación APP-03 — Horario de Bus.
# ---------------------------------------------------------------------------
CODIGO: Final[str] = "APP-03"
NOMBRE: Final[str] = "Horario de Bus"
# Una posición por semana, de la 1 a la 12. 0 descargas: app en mantenimiento.
DESCARGAS: Final = [2_760, 2_800, 3_090, 0, 3_220, 3_370,
                    3_240, 3_380, 3_280, 3_440, 3_500, 3_400]
CAIDAS: Final = [34, 19, 12, 0, 42, 8,
                 73, 40, 7, 42, 45, 14]

# ---------------------------------------------------------------------------
# Datos del programa.
# ---------------------------------------------------------------------------
VERSION_PROGRAMA: Final[str] = "1.0.0"
AUTORES: Final[str] = "Arecmon605 · [compañero]"
PENDIENTE: Final[str] = "  (opción pendiente de implementar)"

# ---------------------------------------------------------------------------
# Constantes comunes.
# ---------------------------------------------------------------------------
ANCHO: Final[int] = 44
POR_MIL: Final[int] = 1_000
UMBRAL_ESTABLE: Final[float] = 5.0       # caídas por cada mil descargas
UMBRAL_ACEPTABLE: Final[float] = 10.0
UMBRAL_REVISAR: Final[float] = 15.0
OPCION_SALIR: Final[int] = 9

# ---------------------------------------------------------------------------
# Constantes de la pareja. Todo valor fijo del programa va aquí, con nombre.
# ---------------------------------------------------------------------------
OPCION_MINIMA: Final[int] = 1
MIN_UMBRAL: Final[float] = 0.0
MAX_UMBRAL: Final[float] = 1_000.0
MAX_OBJETIVO: Final[int] = 1_000_000
MIN_CRECIMIENTO: Final[float] = 0.5
MAX_CRECIMIENTO: Final[float] = 50.0
MAX_SEMANAS_PREVISION: Final[int] = 104


# ---------------------------------------------------------------------------
# Excepciones propias de la pareja. Aquí va SemanaNoValida (opción 7).
# ---------------------------------------------------------------------------
class SemanaNoValida(Exception):
    """Excepción lanzada cuando una semana no es válida o no existe."""
    pass


# ---------------------------------------------------------------------------
# Funciones auxiliares.
# ---------------------------------------------------------------------------
def tasa_caidas(descargas: int, caidas: int) -> float:
    """Devuelve las caídas por cada mil descargas.

    Lanza ZeroDivisionError si la semana no tiene descargas.
    """
    return caidas / descargas * POR_MIL


def estado(descargas: int, caidas: int) -> str:
    """Devuelve el estado de una semana según su tasa de caídas.

    Es uno de estos textos: "Estable", "Aceptable", "Revisar", "Crítica" o
    "Mantenimiento", este último si la semana no tiene descargas.
    """
    if descargas == 0:
        return "Mantenimiento"

    tasa = tasa_caidas(descargas, caidas)
    if tasa < UMBRAL_ESTABLE:
        return "Estable"
    elif tasa < UMBRAL_ACEPTABLE:
        return "Aceptable"
    elif tasa < UMBRAL_REVISAR:
        return "Revisar"
    else:
        return "Crítica"


def pedir_entero(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un entero o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f" Debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print(f" «{entrada}» no es un número entero.")


def pedir_real(mensaje: str, minimo: float, maximo: float) -> float:
    """Pide un número real entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un número o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = float(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f" Debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print(f" «{entrada}» no es un número real.")


def semana_valida(texto: str) -> int:
    """Convierte el texto en un número de semana de los datos.

    Lanza SemanaNoValida si no es un entero o está fuera de rango.
    """
    try:
        semana = int(texto)
    except ValueError:
        raise SemanaNoValida(f"«{texto}» no es un número de semana")

    total_semanas = len(DESCARGAS)
    if semana < 1 or semana > total_semanas:
        raise SemanaNoValida(
            f"la semana {semana} no existe: hay de 1 a {total_semanas}"
        )
    return semana


def comprobar_datos() -> int:
    """Revisa los datos semanales y devuelve el número de errores.

    Registra cada error con logging.error y cada semana de mantenimiento
    con logging.warning.
    """
    errores = 0
    if len(DESCARGAS) != len(CAIDAS):
        logging.error("Las listas de descargas y caídas no tienen igual longitud")
        errores += 1

    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas < 0 or caidas < 0:
            logging.error(f"semana {semana}: valores negativos")
            errores += 1
        elif caidas > descargas:
            logging.error(f"semana {semana}: más caídas que descargas")
            errores += 1
        elif descargas == 0:
            logging.warning(f"semana {semana}: sin descargas (mantenimiento)")

    return errores


# ---------------------------------------------------------------------------
# Menú y opciones.
# ---------------------------------------------------------------------------
def mostrar_menu() -> None:
    """Muestra la cabecera centrada y las nueve opciones del menú."""
    titulo = f"MONITOR DE {CODIGO} · {NOMBRE}"
    print("=" * ANCHO)
    print(titulo.center(ANCHO))
    print("=" * ANCHO)
    print("1. Listado semanal")
    print("2. Resumen")
    print("3. Estabilidad por semana")
    print("4. Primera semana que alcanza un umbral")
    print("5. Mejor racha sin problemas")
    print("6. Previsión de crecimiento")
    print("7. Consultar una semana")
    print("8. Comprobar los datos")
    print("9. Salir")


def opcion_1_listado() -> None:
    """Muestra las descargas, las caídas y la tasa de cada semana."""
    print(f"{'Semana':>6}{'Descargas':>11}{'Caídas':>8}{'Tasa ‰':>9}")
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        try:
            tasa = f"{tasa_caidas(descargas, caidas):.1f}"
        except ZeroDivisionError:
            tasa = "—"
        print(f"{semana:>6}{descargas:>11}{caidas:>8}{tasa:>9}")


def opcion_2_resumen() -> None:
    """Muestra los totales, la media y las semanas extremas depuradas."""
    total_descargas = 0
    total_caidas = 0
    activas = 0
    mas = 0
    semana_mas = 0
    menos = None
    semana_menos = 0

    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        activas += 1
        total_descargas += descargas
        total_caidas += caidas

        # Corregido: semana_mas solo se actualiza si hay un nuevo máximo
        if descargas > mas:
            mas = descargas
            semana_mas = semana

        # Corregido: inicializado en None para capturar el primer valor activo
        if menos is None or descargas < menos:
            menos = descargas
            semana_menos = semana

    media = total_descargas / activas
    tasa = tasa_caidas(total_descargas, total_caidas)

    print(f"Semanas activas:     {activas} de {len(DESCARGAS)}")
    print(f"Total de descargas:  {total_descargas}")
    print(f"Media semanal:       {media:.1f}")
    print(f"Más descargas:       semana {semana_mas} ({mas})")
    print(f"Menos descargas:     semana {semana_menos} ({menos})")
    print(f"Total de caídas:     {total_caidas}")
    print(f"Tasa global:         {tasa:.1f} ‰")


def opcion_3_estabilidad() -> None:
    """Muestra el estado de cada semana y el recuento total por estado."""
    estables = 0
    aceptables = 0
    revisar = 0
    criticas = 0
    mantenimiento = 0

    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        est = estado(descargas, caidas)
        print(f"Semana {semana}: {est}")
        match est:
            case "Estable":
                estables += 1
            case "Aceptable":
                aceptables += 1
            case "Revisar":
                revisar += 1
            case "Crítica":
                criticas += 1
            case "Mantenimiento":
                mantenimiento += 1

    print("-" * ANCHO)
    print(f"Estables: {estables} · Aceptables: {aceptables} · Revisar: {revisar}")
    print(f"Críticas: {criticas} · Mantenimiento: {mantenimiento}")


def opcion_4_umbral() -> None:
    """Busca la primera semana que alcanza o supera el umbral indicado."""
    umbral = pedir_real("Umbral en caídas por mil: ", MIN_UMBRAL, MAX_UMBRAL)
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        tasa = tasa_caidas(descargas, caidas)
        if tasa >= umbral:
            print(f"Primera semana: {semana} ({tasa:.1f} ‰)")
            break
    else:
        # Se ejecuta solo si el bucle termina sin haber hecho break
        print(f"Ninguna semana alcanza {umbral:.1f} ‰")


def opcion_5_racha() -> None:
    """Calcula la racha más larga de semanas seguidas sin problemas."""
    mejor_racha = 0
    inicio_mejor = 0
    racha_actual = 0
    inicio_actual = 0

    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        est = estado(descargas, caidas)

        # Mantenimiento no rompe ni suma a la racha
        if est == "Mantenimiento":
            continue

        if est in ("Estable", "Aceptable"):
            if racha_actual == 0:
                inicio_actual = semana
            racha_actual += 1
            if racha_actual > mejor_racha:
                mejor_racha = racha_actual
                inicio_mejor = inicio_actual
        else:
            racha_actual = 0
            inicio_actual = 0

    if mejor_racha > 0:
        print(f"Mejor racha: {mejor_racha} semanas, desde la semana {inicio_mejor}")
    else:
        print("No se encontró ninguna racha sin problemas")


def opcion_6_prevision() -> None:
    """Calcula en cuántas semanas se alcanza un objetivo de descargas."""
    ultimas_descargas = 0
    for descargas in reversed(DESCARGAS):
        if descargas > 0:
            ultimas_descargas = descargas
            break

    print(f"Descargas de la última semana activa: {ultimas_descargas}")
    objetivo = pedir_entero(
        "Objetivo semanal de descargas: ",
        ultimas_descargas + 1,
        MAX_OBJETIVO
    )
    crecimiento = pedir_real(
        "Crecimiento semanal en %: ",
        MIN_CRECIMIENTO,
        MAX_CRECIMIENTO
    )

    semanas = 0
    descargas_actuales = float(ultimas_descargas)
    factor = 1.0 + (crecimiento / 100.0)

    while descargas_actuales < objetivo:
        semanas += 1
        descargas_actuales *= factor
        if semanas >= MAX_SEMANAS_PREVISION:
            break

    if descargas_actuales >= objetivo:
        descargas_finales = round(descargas_actuales)
        print(f"Se alcanza en {semanas} semanas ({descargas_finales} descargas)")
    else:
        print(f"El objetivo no se alcanza en {MAX_SEMANAS_PREVISION} semanas")


def opcion_7_consulta() -> None:
    """Muestra los datos de una semana concreta y la acción recomendada."""
    total_semanas = len(DESCARGAS)
    texto = input(f"Semana (1-{total_semanas}): ").strip()
    try:
        num_semana = semana_valida(texto)
    except SemanaNoValida as error:
        print(f" No se puede consultar: {error}")
        return

    descargas = DESCARGAS[num_semana - 1]
    caidas = CAIDAS[num_semana - 1]
    est = estado(descargas, caidas)

    match est:
        case "Estable":
            accion = "Sin acciones"
        case "Aceptable":
            accion = "Vigilar en la próxima versión"
        case "Revisar":
            accion = "Revisar los informes de errores"
        case "Crítica":
            accion = "Publicar una versión correctora urgente"
        case "Mantenimiento":
            accion = "La app no estuvo publicada esa semana"
        case _:
            accion = "Sin acción definida"

    print(f"Descargas: {descargas}")
    print(f"Caídas:    {caidas}")
    print(f"Estado:    {est}")
    print(f"Acción:    {accion}")


def opcion_8_comprobar() -> None:
    """Comprueba la integridad de las listas de datos e informa del resultado."""
    errores = comprobar_datos()
    if errores == 0:
        print(f"Datos correctos: {len(DESCARGAS)} semanas")
    else:
        print("Los datos tienen errores: corrígelos antes de continuar.")


def main() -> None:
    """Función principal: configura logs, valida datos y ejecuta el menú."""
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)s: %(message)s"
    )

    if comprobar_datos() > 0:
        sys.exit("Los datos tienen errores: corrígelos antes de continuar.")

    print(f"Monitor de estabilidad {VERSION_PROGRAMA} · {AUTORES}")

    while True:
        try:
            mostrar_menu()
            entrada = input("Opción: ").strip()
            try:
                opcion = int(entrada)
            except ValueError:
                print(f" «{entrada}» no es una opción.")
                continue

            match opcion:
                case 1:
                    opcion_1_listado()
                case 2:
                    opcion_2_resumen()
                case 3:
                    opcion_3_estabilidad()
                case 4:
                    opcion_4_umbral()
                case 5:
                    opcion_5_racha()
                case 6:
                    opcion_6_prevision()
                case 7:
                    opcion_7_consulta()
                case 8:
                    opcion_8_comprobar()
                case 9:
                    respuesta = input("¿Salir del programa? (s/n): ").strip().lower()
                    if respuesta == "s":
                        break
                case _:
                    print(f" Elige una opción entre 1 y {OPCION_SALIR}.")
        except KeyboardInterrupt:
            print("\nPrograma interrumpido")
            break

    print(f"Fin del monitor de {CODIGO}.")


if __name__ == "__main__":
    main()

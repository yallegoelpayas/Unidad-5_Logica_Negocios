
import pytest


# --- DOMINIO SIMULADO DE EDUTECH ACADEMY ---
class EvaluacionFueraDeRango(Exception): pass

class Expediente:
    def guardar_calificacion(self, calificacion):
        if not (0 <= calificacion <= 100):
            raise EvaluacionFueraDeRango("Calificación inválida")
        self.calificacion = calificacion

class Inscripcion:
    def __init__(self):
        self.estado = "Preinscrito"
    def registrar_pago(self, porcentaje):
        if porcentaje >= 50:
            self.estado = "Inscrito"

class Grupo:
    def __init__(self, cupo_maximo=25):
        self.cupo_maximo = cupo_maximo
        self.inscritos = 0
    def reservar_lugar(self):
        if self.inscritos >= self.cupo_maximo:
            raise ValueError("Sin cupo, se mueve a Lista de Espera")
        self.inscritos += 1

# --- CASOS DE PRUEBA (CP-01 al CP-09) ---

# CP-01, CP-02, CP-03: Regla INV-14 (Calificaciones 0-100)
def test_cp01_calificacion_exitosa():
    exp = Expediente()
    exp.guardar_calificacion(85)
    assert exp.calificacion == 85

def test_cp02_calificacion_limite():
    exp = Expediente()
    exp.guardar_calificacion(100)
    assert exp.calificacion == 100

def test_cp03_calificacion_error():
    exp = Expediente()
    with pytest.raises(EvaluacionFueraDeRango):
        exp.guardar_calificacion(105)

# CP-04, CP-05, CP-06: Regla INV-06/INV-07 (Pagos y Estados)
def test_cp04_pago_total_inscrito():
    ins = Inscripcion()
    ins.registrar_pago(100)
    assert ins.estado == "Inscrito"

def test_cp05_pago_parcialidad_inscrito():
    ins = Inscripcion()
    ins.registrar_pago(50)
    assert ins.estado == "Inscrito"

def test_cp06_pago_menor_preinscrito():
    ins = Inscripcion()
    ins.registrar_pago(49)
    assert ins.estado == "Preinscrito"

# CP-07, CP-08, CP-09: Regla INV-03/INV-04 (Cupos y Lista de Espera)
def test_cp07_reserva_lugar_exito():
    grupo = Grupo(cupo_maximo=25)
    grupo.inscritos = 15
    grupo.reservar_lugar()
    assert grupo.inscritos == 16

def test_cp08_reserva_lugar_limite():
    grupo = Grupo(cupo_maximo=25)
    grupo.inscritos = 24
    grupo.reservar_lugar()
    assert grupo.inscritos == 25

def test_cp09_reserva_lugar_lista_espera():
    grupo = Grupo(cupo_maximo=25)
    grupo.inscritos = 25
    with pytest.raises(ValueError, match="Lista de Espera"):
        grupo.reservar_lugar()
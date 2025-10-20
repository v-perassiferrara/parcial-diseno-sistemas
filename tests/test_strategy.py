
import unittest
from datetime import date
from unittest.mock import Mock

from python_forestacion.patrones.strategy.impl.absorcion_constante_strategy import AbsorcionConstanteStrategy
from python_forestacion.patrones.strategy.impl.absorcion_seasonal_strategy import AbsorcionSeasonalStrategy
from python_forestacion.constantes import ABSORCION_SEASONAL_VERANO, ABSORCION_SEASONAL_INVIERNO, MES_INICIO_VERANO, MES_FIN_VERANO


class TestStrategy(unittest.TestCase):

    def setUp(self):
        self.mock_cultivo = Mock()

    def test_absorcion_constante_strategy(self):
        """Verifica que la estrategia constante siempre devuelva el mismo valor."""
        cantidad_constante = 15
        strategy = AbsorcionConstanteStrategy(cantidad_constante)
        
        absorcion = strategy.calcular_absorcion(date.today(), 20, 50, self.mock_cultivo)
        
        self.assertEqual(absorcion, cantidad_constante)

    def test_absorcion_seasonal_strategy_verano(self):
        """Verifica que la estrategia estacional devuelva el valor de verano."""
        strategy = AbsorcionSeasonalStrategy()
        fecha_verano = date(2025, MES_INICIO_VERANO + 1, 15)
        
        absorcion = strategy.calcular_absorcion(fecha_verano, 30, 40, self.mock_cultivo)
        
        self.assertEqual(absorcion, ABSORCION_SEASONAL_VERANO)

    def test_absorcion_seasonal_strategy_invierno(self):
        """Verifica que la estrategia estacional devuelva el valor de invierno."""
        strategy = AbsorcionSeasonalStrategy()
        # Un mes fuera del rango de verano
        mes_invierno = MES_FIN_VERANO + 1 if MES_FIN_VERANO < 12 else MES_INICIO_VERANO - 1
        fecha_invierno = date(2025, mes_invierno, 15)

        absorcion = strategy.calcular_absorcion(fecha_invierno, 5, 60, self.mock_cultivo)

        self.assertEqual(absorcion, ABSORCION_SEASONAL_INVIERNO)


if __name__ == '__main__':
    unittest.main()

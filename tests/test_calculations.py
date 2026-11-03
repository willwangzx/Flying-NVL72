import copy
import json
import math
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from calculate import evaluate, scenario_results


class Budgets(unittest.TestCase):
    def setUp(self):
        self.x = json.loads((ROOT/'analysis/inputs.json').read_text())
        self.r = evaluate(self.x)

    def test_baseline_and_mass_sum(self):
        self.assertTrue(all(self.r['checks'].values()))
        self.assertAlmostEqual(self.r['mass']['wet_kg'],23720)
        self.assertAlmostEqual(self.r['mass']['dry_kg'],sum(self.r['mass']['items_kg'].values()))
        self.assertEqual(self.r['power']['nominal_bus_kw'],138)
        self.assertAlmostEqual(self.r['thermal']['capacity_kw'],207.084342,places=5)

    def test_independent_energy_accounting(self):
        # Separately sum load energy and conversion loss over one orbit.
        r=self.r
        load_orbit=r['power']['reserved_bus_kw']*r['orbit']['period_min']/60
        battery_loss=r['battery']['eclipse_energy_kwh']*(1/(.95*.95)-1)
        generated=r['power']['required_solar_kw']*r['orbit']['sunlight_min']/60
        self.assertAlmostEqual(generated,load_orbit+battery_loss)
        thermal_sun=r['thermal']['peak_heat_kw']*r['orbit']['sunlight_min']/60
        self.assertAlmostEqual(thermal_sun,r['power']['reserved_bus_kw']*r['orbit']['sunlight_min']/60+battery_loss)

    def test_environment_limit(self):
        self.x['thermal']['environment_w_m2']=self.r['thermal']['max_environment_w_m2']
        r=evaluate(self.x)
        self.assertAlmostEqual(r['thermal']['capacity_kw'],r['thermal']['peak_heat_kw'])
        self.x['thermal']['environment_w_m2']+=1
        self.assertFalse(evaluate(self.x)['checks']['thermal'])

    def test_failures_and_fallback(self):
        cases=scenario_results(self.x)
        for case,check in [('hot_environment','thermal'),('radiator_wing_lost','thermal'),('solar_wing_lost','solar_and_charge'),('battery_string_lost','battery')]:
            self.assertFalse(cases[case]['results']['checks'][check],case)
        self.assertGreater(cases['radiator_wing_lost_100kw']['results']['thermal']['capacity_margin_fraction'],.1)
        self.assertNotIn('mass',cases['radiator_wing_lost']['results'])
        self.assertEqual(cases['cooler_inlet_fallback']['results']['thermal']['primary_inlet_c'],25)
        self.assertAlmostEqual(cases['cooler_inlet_fallback']['results']['mass']['wet_kg'],24440)

    def test_eclipse_and_charger_boundaries(self):
        self.x['orbit']['eclipse_min']=0
        r=evaluate(self.x)
        self.assertEqual(r['battery']['eclipse_energy_kwh'],0)
        self.assertEqual(r['thermal']['peak_heat_kw'],r['power']['reserved_bus_kw'])
        self.x['orbit']['eclipse_min']=36
        self.x['battery']['max_charge_kw']=90
        self.assertFalse(evaluate(self.x)['checks']['solar_and_charge'])
        self.x['orbit']['eclipse_min']=100
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_relay_outage_and_geometry(self):
        self.assertAlmostEqual(self.r['relay']['tb_per_day'],194.4)
        self.assertAlmostEqual(self.r['relay']['days_per_cache'],1000/194.4)
        self.x['relay']['usable_fraction']=0
        self.assertIsNone(evaluate(self.x)['relay']['days_per_cache'])
        self.x['relay']['range_km']=6000
        self.assertFalse(evaluate(self.x)['relay']['geometry_clear'])
        self.x['relay']['range_km']=10
        self.assertFalse(evaluate(self.x)['relay']['geometry_clear'])
        self.x['relay']['range_km']=0
        with self.assertRaises(ValueError):evaluate(self.x)

    def test_drag_and_rocket_equation(self):
        # F≈0.044 N over a Julian year / 23.72 tonnes gives about 58.6 m/s.
        self.assertAlmostEqual(self.r['propulsion']['drag_m_s_year'],58.576403,places=5)
        self.assertAlmostEqual(self.r['propulsion']['electric_dv_m_s'],334.282775,places=5)
        self.x['drag']['density_kg_m3']*=10
        self.assertAlmostEqual(evaluate(self.x)['propulsion']['drag_m_s_year'],10*self.r['propulsion']['drag_m_s_year'])

    def test_checked_in_results(self):
        stored=json.loads((ROOT/'analysis/results/baseline.json').read_text())
        self.assertEqual(stored,self.r)
        stored_cases=json.loads((ROOT/'analysis/results/scenarios.json').read_text())
        self.assertEqual(stored_cases,scenario_results(self.x))


if __name__ == '__main__':
    unittest.main()

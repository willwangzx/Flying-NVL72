"""Reproducible Concept D scalar sizing, Python 3.10+, standard library only.

All inputs are allocations unless SOURCES.md explicitly identifies public facts.
Changing area also changes mass here; the interactive HTML keeps mass fixed.
"""
import argparse
import copy
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def evaluate(x):
    o, p, s, b, t = (x[k] for k in ('orbit', 'power', 'solar', 'battery', 'thermal'))
    r = (o['earth_radius_km'] + o['altitude_km']) * 1000
    period = 2 * math.pi * math.sqrt(r**3 / o['mu_m3_s2']) / 60
    sun = period - o['eclipse_min']
    if not 0 <= o['eclipse_min'] < period:
        raise ValueError('Eclipse must be nonnegative and shorter than the orbit.')
    if min(b['charge_efficiency'], b['discharge_efficiency'], p['converter_efficiency'], t['pump_efficiency']) <= 0:
        raise ValueError('Efficiencies must be positive.')
    ep = x['propulsion']
    heads = ep.get('operating_heads', 0)
    if heads not in (0, 1, 2):
        raise ValueError('Select 0, 1 or 2 operating ion engines; four-head operation is not supported.')
    ep_kw = (heads * ep['thruster_power_per_head_kw'] / ep['ppu_efficiency'] / ep['front_end_efficiency'] + ep['feed_controls_kw']) if heads else 0
    bus = p['compute_kw'] / p['converter_efficiency'] + p['overhead_kw'] + ep_kw
    design = bus * (1 + p['load_reserve'])
    solar = s['area_m2'] * s['irradiance_w_m2'] / 1000
    for k in ('cell_efficiency', 'coverage', 'eol_temperature_factor', 'tracking_factor', 'delivery_efficiency'):
        solar *= s[k]
    cycle_eff = b['charge_efficiency'] * b['discharge_efficiency']
    charge_need = design * o['eclipse_min'] / sun / cycle_eff
    charge_available = min(b['max_charge_kw'], max(0, solar - design))
    need = design * o['eclipse_min'] / 60
    deliverable = b['nameplate_kwh'] * b['retention'] * b['depth_of_discharge'] * b['discharge_efficiency']
    heat = design + design * o['eclipse_min'] / sun * (1 / cycle_eff - 1)
    emitted = t['emissivity'] * t['sigma_w_m2_k4'] * (t['skin_c'] + 273.15)**4
    flux = t['effective_area_factor'] * (emitted - t['environment_w_m2'])
    radiator = t['area_m2'] * flux / 1000
    mdot = p['compute_kw'] / (t['primary_cp_kj_kg_k'] * t['primary_delta_k'])
    volume_flow = mdot / t['primary_density_kg_m3']
    pump = volume_flow * t['primary_dp_pa'] / t['pump_efficiency'] / 1000
    masses = dict(x['mass_fixed_kg'])
    masses.update(solar=s['area_m2']*s['installed_kg_m2'], radiator=t['area_m2']*t['installed_kg_m2'], battery=b['nameplate_kwh']/b['installed_kwh_kg'])
    dry = sum(masses.values())
    prop = x['propulsion']
    wet = dry * (1 + x['mass_growth']) + prop['xenon_kg'] + prop['chemical_kg']
    electric_dv = prop['g0_m_s2'] * prop['electric_isp_s'] * math.log(wet / (wet-prop['xenon_kg']))
    chemical_dv = prop['g0_m_s2'] * prop['chemical_isp_s'] * math.log((wet-prop['xenon_kg']) / (wet-prop['xenon_kg']-prop['chemical_kg']))
    v = math.sqrt(o['mu_m3_s2'] / r)
    d = x['drag']
    drag_year = 0.5*d['density_kg_m3']*d['cd']*d['projected_area_m2']*v*v/wet*d['days_year']*86400
    perigee = (o['earth_radius_km']+50)*1000
    disposal = v - math.sqrt(o['mu_m3_s2']*(2/r-2/(r+perigee)))
    l = x['relay']
    avg = min(l['capacity_gbps'],l['terminal_design_gbps'])*l['payload_efficiency']*l['usable_fraction']
    tbday = avg*86400/8/1000
    rc = o['earth_radius_km'] + l['limb_clearance_km']
    r1 = o['earth_radius_km'] + o['altitude_km']
    r2 = o['earth_radius_km'] + l['peer_altitude_km']
    max_range = math.sqrt(max(0,r1*r1-rc*rc))+math.sqrt(max(0,r2*r2-rc*rc))
    geom_clear = min(r1,r2) >= rc and abs(r1-r2) <= l['range_km'] <= max_range
    if l['range_km'] <= 0:
        raise ValueError('Optical range must be positive.')
    st = x['structure']
    pack_diagonal = math.hypot(st['radiator_pack_width_m'],2*st['radiator_pack_depth_m'])
    return {
        'orbit': {'period_min':period,'sunlight_min':sun,'circular_speed_m_s':v,'zero_beta_max_eclipse_min':period/math.pi*math.asin(o['earth_radius_km']/(o['earth_radius_km']+o['altitude_km']))},
        'power': {'ion_bus_kw':ep_kw,'nominal_bus_kw':bus,'reserved_bus_kw':design,'converter_loss_kw':p['compute_kw']/p['converter_efficiency']-p['compute_kw'],'solar_eol_kw':solar,'required_solar_kw':design+charge_need,'required_charge_kw':charge_need,'available_charge_kw':charge_available,'solar_margin_fraction':solar/(design+charge_need)-1,'compute_primary_current_a':p['compute_kw']/p['converter_efficiency']*1000/p['primary_bus_v'],'compute_local_current_a':p['compute_kw']*1000/p['local_bus_v'],'branch_current_a':p['compute_kw']*1000/p['local_bus_v']/p['distribution_branches']},
        'battery': {'eclipse_energy_kwh':need,'deliverable_kwh':deliverable,'capacity_margin_fraction':deliverable/need-1 if need else None,'max_eclipse_min':deliverable/design*60},
        'thermal': {'peak_heat_kw':heat,'net_flux_w_m2':flux,'capacity_kw':radiator,'capacity_margin_fraction':radiator/heat-1,'minimum_area_m2':heat*1000/flux if flux>0 else None,'max_environment_w_m2':emitted-heat*1000/(t['area_m2']*t['effective_area_factor']),'primary_inlet_c':t['skin_c']+t['inlet_offset_c'],'primary_mass_flow_kg_s':mdot,'primary_volume_flow_l_min':volume_flow*60000,'primary_pump_kw':pump,'secondary_mass_flow_kg_s':heat/(t['secondary_cp_kj_kg_k']*t['secondary_delta_k']),'net_panel_kw':flux*t['panel_area_m2']/1000,'panel_count':t['area_m2']/t['panel_area_m2']},
        'mass': {'items_kg':masses,'dry_kg':dry,'growth_kg':dry*x['mass_growth'],'wet_kg':wet},
        'propulsion': {'electric_dv_m_s':electric_dv,'chemical_dv_after_xenon_m_s':chemical_dv,'drag_m_s_year':drag_year,'mission_drag_m_s':drag_year*o['mission_years'],'impulsive_circular_to_50_perigee_m_s':disposal},
        'structure': {'axial_force_n':wet*prop['g0_m_s2']*st['axial_g'],'lateral_force_n':wet*prop['g0_m_s2']*st['lateral_g'],'two_pack_diagonal_m':pack_diagonal,'pack_radial_clearance_m':(st['package_diameter_m']-pack_diagonal)/2,'launcher_radial_allowance_m':(st['assumed_launcher_diameter_m']-st['package_diameter_m'])/2,'panel_stack_pitch_height_m':t['area_m2']/t['wings']/t['panel_area_m2']*st['panel_pitch_m']},
        'relay': {'average_gbps':avg,'tb_per_day':tbday,'days_per_cache':l['cache_tb']/tbday if tbday else None,'one_hop_propagation_ms':l['range_km']/l['light_speed_km_s']*1000,'limb_clear_range_km':max_range,'geometry_clear':geom_clear,'tracking_stress_deg_s':l['transverse_speed_km_s']/l['range_km']*180/math.pi},
        'checks': {'solar_and_charge':solar>=design+charge_need and charge_available>=charge_need,'battery':deliverable>=need,'thermal':radiator>=heat,'coolant_target':t['skin_c']+t['inlet_offset_c']<=t['inlet_ceiling_c']}
    }


def scenario_results(inputs):
    cases = {'baseline':{},'eclipse_free':{'orbit':{'eclipse_min':0}},'hot_environment':{'thermal':{'environment_w_m2':180}},'radiator_wing_lost':{'thermal':{'area_m2':525}},'radiator_wing_lost_100kw':{'thermal':{'area_m2':525},'power':{'compute_kw':100}},'solar_wing_lost':{'solar':{'area_m2':825}},'battery_string_lost':{'battery':{'nameplate_kwh':150}},'cooler_inlet_fallback':{'thermal':{'area_m2':800,'skin_c':21}},'reduced_relay_allocation':{'relay':{'capacity_gbps':10}},'relay_outage':{'relay':{'usable_fraction':0}},'ion_burn_105kw':{'power':{'compute_kw':105},'propulsion':{'operating_heads':2}},'ion_burn_120kw':{'propulsion':{'operating_heads':2}}}
    out = {}
    for name, changes in cases.items():
        p = copy.deepcopy(inputs)
        for section, delta in changes.items():
            p[section].update(delta)
        out[name] = {'overrides':changes,'results':evaluate(p)}
        # Failure removes capacity, not spacecraft launch mass. Do not report the
        # sizing model's area-rescaled mass/trajectory in failure cases.
        if 'lost' in name:
            for field in ('mass','propulsion','structure'):
                out[name]['results'].pop(field)
            out[name]['note']='Capacity-loss scenario; baseline launch mass retained. Mass/trajectory outputs omitted.'
    return out


def ion_trade(inputs):
    """Initial-mass low-thrust screening. Does not solve a spiral or conjunction."""
    base = evaluate(inputs)
    e = inputs['propulsion']
    m = base['mass']['wet_kg']
    ve = e['g0_m_s2'] * e['electric_isp_s']
    available = base['orbit']['sunlight_min']/base['orbit']['period_min']*e['sunlit_availability']
    drag = .5*inputs['drag']['density_kg_m3']*inputs['drag']['cd']*inputs['drag']['projected_area_m2']*base['orbit']['circular_speed_m_s']**2
    out = {}
    for heads in (1,2):
        force = heads*e['thrust_per_head_n']
        useful = force*e['direction_factor']
        average = useful*available
        power = heads*e['thruster_power_per_head_kw']/e['ppu_efficiency']/e['front_end_efficiency']+e['feed_controls_kw']
        mdot=force/ve
        out[str(heads)+'_active']={
            'thrust_n':force, 'useful_thrust_n':useful, 'bus_power_kw':power,
            'mass_flow_mg_s':mdot*1e6, 'on_time_acceleration_m_s2':useful/m,
            'available_orbit_fraction':available, 'average_useful_thrust_n':average,
            'drag_force_n':drag, 'required_orbit_fraction_for_drag':drag/useful,
            'max_density_kg_m3_at_assumed_duty':inputs['drag']['density_kg_m3']*average/drag,
            'one_m_s_on_hours_initial_mass':m/useful/3600,
            'one_m_s_calendar_hours_without_drag':m/average/3600,
            'one_m_s_calendar_hours_after_drag':m/(average-drag)/3600 if average>drag else None,
            '100_m_s_on_days_initial_mass':100*m/useful/86400,
            '100_m_s_calendar_days_without_drag':100*m/average/86400,
            'annual_xenon_for_reference_drag_kg':drag*inputs['drag']['days_year']*86400/(ve*e['direction_factor']),
            'xenon_inventory_full_power_firing_hours':inputs['propulsion']['xenon_kg']/mdot/3600,
            'non_jet_power_kw_estimate':power-force*ve/2/1000,
            'note':'Constant initial mass and constant environment screening. Direction/duty factors are unverified. Spacecraft thermal budget conservatively counts all EP electrical input as heat.'
        }
    return {'reference':'NASA PM1 (2008): 0.237 N, 6.9 kW, 4190 s per head; integration allocations are independent', 'cases':out}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs',type=Path,default=ROOT/'inputs.json')
    parser.add_argument('--output-dir',type=Path,default=ROOT/'results')
    args = parser.parse_args()
    inputs = json.loads(args.inputs.read_text())
    result = evaluate(inputs)
    args.output_dir.mkdir(parents=True,exist_ok=True)
    for name, value in [('baseline.json',result),('scenarios.json',scenario_results(inputs)),('ion-propulsion.json',ion_trade(inputs))]:
        (args.output_dir/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
    with (args.output_dir/'mass-budget.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['Item','kg']);w.writerows(result['mass']['items_kg'].items())
        w.writerow(['Dry subtotal',result['mass']['dry_kg']]);w.writerow(['Dry growth',result['mass']['growth_kg']])
        w.writerow(['Propellant',inputs['propulsion']['xenon_kg']+inputs['propulsion']['chemical_kg']]);w.writerow(['Launch total',result['mass']['wet_kg']])
    print(json.dumps({'checks':result['checks'],'output_dir':str(args.output_dir)},indent=2))


if __name__ == '__main__':
    main()

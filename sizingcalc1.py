# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 13:06:38 2026

@author: adria
"""

# -*- coding: utf-8 -*-
# =============================================================================
#  SOLAR POWER CALCULATOR — PANELS + ARRAYS + BAR-CHARTS + CELL REPLACEMENT
#  + SOLAR PANEL ANGLES VIEW
# =============================================================================

import math
import re
import tkinter as tk
from tkinter import ttk, messagebox

BLANK  = "— Leave blank —"
CUSTOM = "Custom — Enter your own"
ORIGINAL_CELL = "— Use original cell configuration —"

CELL_COVERAGE_FACTOR = 0.85
ORIGINAL_PV_MASS_FRACTION = 0.10

SOLAR_IRRADIANCE_W_M2 = 1361.0


# =============================================================================
#  DATABASES
# =============================================================================

SOLAR_PANELS = {
    "Sparkwing 1070×1100 mm, 50 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 366.0, "specific_power": 45.0,
        "areal_density": 6.910223732653638,
        "length_m": 1.100, "width_m": 1.070,
        "area_m2": 1.177, "mass_kg": 8.133333333333333},
    "Sparkwing 1000×1100 mm, 36 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 309.0, "specific_power": 39.0,
        "areal_density": 7.202797202797203,
        "length_m": 1.100, "width_m": 1.000,
        "area_m2": 1.100, "mass_kg": 7.923076923076923},
    "Sparkwing 910×1100 mm, 50 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 305.0, "specific_power": 40.0,
        "areal_density": 7.617382617382616,
        "length_m": 1.100, "width_m": 0.910,
        "area_m2": 1.001, "mass_kg": 7.625},
    "Sparkwing 1070×965 mm, 50 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 305.0, "specific_power": 39.0,
        "areal_density": 7.573979778715626,
        "length_m": 0.965, "width_m": 1.070,
        "area_m2": 1.03255, "mass_kg": 7.82051282051282},
    "Sparkwing 1230×800 mm, 50 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 275.0, "specific_power": 36.0,
        "areal_density": 7.763098464317977,
        "length_m": 0.800, "width_m": 1.230,
        "area_m2": 0.984, "mass_kg": 7.638888888888889},
    "Sparkwing 910×965 mm, 36 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 265.0, "specific_power": 37.0,
        "areal_density": 8.155966705189503,
        "length_m": 0.965, "width_m": 0.910,
        "area_m2": 0.87815, "mass_kg": 7.162162162162162},
    "Sparkwing 1070×820 mm, 36 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 265.0, "specific_power": 37.0,
        "areal_density": 8.162938411399775,
        "length_m": 0.820, "width_m": 1.070,
        "area_m2": 0.8774, "mass_kg": 7.162162162162162},
    "Sparkwing 750×1100 mm, 50 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 244.0, "specific_power": 34.0,
        "areal_density": 8.698752228163993,
        "length_m": 1.100, "width_m": 0.750,
        "area_m2": 0.825, "mass_kg": 7.176470588235294},
    "Sparkwing 910×965 mm, 50 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 244.0, "specific_power": 34.0,
        "areal_density": 8.172260534345265,
        "length_m": 0.965, "width_m": 0.910,
        "area_m2": 0.87815, "mass_kg": 7.176470588235294},
    "Sparkwing 1070×800 mm, 50 V": {
        "manufacturer": "Airbus Netherlands", "efficiency": "29.5% BOL cell efficiency",
        "type": "Rigid Panel — Body Mounted or 1–3 Panel Deployable Wing",
        "rated_power_w": 244.0, "specific_power": 34.0,
        "areal_density": 8.383727322704782,
        "length_m": 0.800, "width_m": 1.070,
        "area_m2": 0.856, "mass_kg": 7.176470588235294},
}


SOLAR_ARRAYS = {
    "UltraFlex 175": {
        "manufacturer": "ATK Space Systems / NASA ST8",
        "efficiency": "28% cell efficiency",
        "type": "UltraFlex — Circular Fan-Fold Flexible Array",
        "rated_power_w": 7000.0, "specific_power": 175.0,
        "areal_density": 1.683622538492777,
        "length_m": 5.5, "width_m": 5.5,
        "area_m2": 23.75829444277281, "mass_kg": 40.0},
    "Ultralight a-Si Deployable PV Array": {
        "manufacturer": "Energy Conversion Devices / NASA NTRS",
        "efficiency": None, "type": "Flexible Roll-Up Thin-Film Array",
        "rated_power_w": 200.0, "specific_power": 154.0,
        "areal_density": 0.4010860175243737,
        "length_m": 2.92, "width_m": 1.11,
        "area_m2": 3.2412, "mass_kg": 1.3},
    "Fold-Out Solar Array (FOSA) — 150 W Wing": {
        "manufacturer": "ExoTerra Resource",
        "efficiency": "29.5% BOL cell efficiency",
        "type": "Flexible Fold-Out Blanket Array",
        "rated_power_w": 150.0, "specific_power": 140.0,
        "areal_density": 1.6973781060433006,
        "length_m": 1.713, "width_m": 0.368,
        "area_m2": 0.630384, "mass_kg": 1.07},
    "ROSA Opal — 5.3 kW Wing": {
        "manufacturer": "Redwire Space", "efficiency": None,
        "type": "ROSA — Flexible Roll-Out Array",
        "rated_power_w": 5300.0, "specific_power": 124.12177985948477,
        "areal_density": 1.2692467748647527,
        "length_m": 12.6, "width_m": 2.67,
        "area_m2": 33.642, "mass_kg": 42.7},
    "Lucy UltraFlex — Two-Array System": {
        "manufacturer": "Northrop Grumman / NASA Lucy",
        "efficiency": "32% array conversion efficiency",
        "type": "UltraFlex — Circular Fan-Fold Flexible Arrays",
        "rated_power_w": 18000.0, "specific_power": 102.27272727272727,
        "areal_density": 2.1025535735915617,
        "length_m": 7.3, "width_m": 7.3,
        "area_m2": 83.70773625490004, "mass_kg": 176.0},
    "DART ROSA — One Wing": {
        "manufacturer": "Redwire Space / NASA DART", "efficiency": None,
        "type": "ROSA — Flexible Roll-Out Array",
        "rated_power_w": 3390.0, "specific_power": 99.0,
        "areal_density": 2.836986266977982,
        "length_m": 8.5, "width_m": 1.42,
        "area_m2": 12.07, "mass_kg": 34.24242424242424},
    "InSight UltraFlex — Two-Array System": {
        "manufacturer": "Northrop Grumman / NASA InSight", "efficiency": None,
        "type": "UltraFlex — Circular Fan-Fold Flexible Arrays",
        "rated_power_w": 1840.0, "specific_power": 93.89671361502347,
        "areal_density": 2.698799580165522,
        "length_m": 2.15, "width_m": 2.15,
        "area_m2": 7.2610060206094085, "mass_kg": 19.596},
    "Relocatable 10 kW Solar Array (RSA)": {
        "manufacturer": "NASA", "efficiency": None,
        "type": "Lunar Surface — Elevated Vertical Flexible Blankets",
        "rated_power_w": 10000.0, "specific_power": 83.33333333333333,
        "areal_density": 3.3333333333333335,
        "length_m": None, "width_m": None,
        "area_m2": 36.0, "mass_kg": 120.0},
    "Dawn Two-Wing Solar Array System": {
        "manufacturer": "NASA / Orbital Sciences — Dawn",
        "efficiency": ">27.6% AM0 cell efficiency",
        "type": "Rigid Deployable Wing Array",
        "rated_power_w": 10500.0, "specific_power": 83.33333333333333,
        "areal_density": 3.3001571503404925,
        "length_m": 8.3, "width_m": 2.3,
        "area_m2": 38.18, "mass_kg": 126.0},
    "ROSA Sapphire — 12.9 kW Wing": {
        "manufacturer": "Redwire Space", "efficiency": None,
        "type": "ROSA — Flexible Roll-Out Array",
        "rated_power_w": 12900.0, "specific_power": 80.625,
        "areal_density": 4.081632653061225,
        "length_m": 19.6, "width_m": 2.0,
        "area_m2": 39.2, "mass_kg": 160.0},
}


SOLAR_CELLS = {
    "Silicon S 32": {"manufacturer": "AZUR Space Germany", "efficiency_pct": 16.8,
                     "voc_v": 0.628, "vmp_v": 0.528, "power_density_w_m2": 229.2,
                     "areal_density_mg_cm2": 32.0, "density_estimated": False},
    "3G30-Adv": {"manufacturer": "AZUR Space Germany", "efficiency_pct": 29.5,
                 "voc_v": 2.7, "vmp_v": 2.411, "power_density_w_m2": 403.0,
                 "areal_density_mg_cm2": 86.0, "density_estimated": False},
    "4G32-Adv": {"manufacturer": "AZUR Space Germany", "efficiency_pct": 31.5,
                 "voc_v": 3.426, "vmp_v": 2.999, "power_density_w_m2": 431.0,
                 "areal_density_mg_cm2": 109.0, "density_estimated": False},
    "TJ 3G28C": {"manufacturer": "AZUR Space Germany", "efficiency_pct": 28.0,
                 "voc_v": 2.667, "vmp_v": 2.37, "power_density_w_m2": 1367.0,
                 "areal_density_mg_cm2": 86.0, "density_estimated": False},
    "ZTJ": {"manufacturer": "Rocket Lab USA", "efficiency_pct": 29.5,
            "voc_v": 2.726, "vmp_v": 2.41, "power_density_w_m2": 397.7,
            "areal_density_mg_cm2": 84.0, "density_estimated": False},
    "ZTJ+": {"manufacturer": "Rocket Lab USA", "efficiency_pct": 29.4,
             "voc_v": 2.69, "vmp_v": 2.39, "power_density_w_m2": 397.9,
             "areal_density_mg_cm2": 84.0, "density_estimated": True},
    "ZTJ Omega": {"manufacturer": "Rocket Lab USA", "efficiency_pct": 30.2,
                  "voc_v": 2.73, "vmp_v": 2.43, "power_density_w_m2": 408.2,
                  "areal_density_mg_cm2": 84.0, "density_estimated": True},
    "Z4J": {"manufacturer": "Rocket Lab USA", "efficiency_pct": 31.3,
            "voc_v": 3.95, "vmp_v": 3.54, "power_density_w_m2": 407.1,
            "areal_density_mg_cm2": 84.0, "density_estimated": True},
    "IMMα": {"manufacturer": "Rocket Lab USA", "efficiency_pct": 32.0,
             "voc_v": 4.78, "vmp_v": 4.28, "power_density_w_m2": 433.1,
             "areal_density_mg_cm2": 84.0, "density_estimated": True},
    "ZTJM": {"manufacturer": "Rocket Lab USA", "efficiency_pct": 29.5,
             "voc_v": 2.72, "vmp_v": 2.38, "power_density_w_m2": 392.0,
             "areal_density_mg_cm2": 84.0, "density_estimated": True},
    "XTJ": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 29.5,
            "voc_v": 2.633, "vmp_v": 2.348, "power_density_w_m2": 399.6,
            "areal_density_mg_cm2": 84.0, "density_estimated": False},
    "XTJ-Prime": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 30.7,
                  "voc_v": 2.715, "vmp_v": 2.39, "power_density_w_m2": 415.9,
                  "areal_density_mg_cm2": 130.0, "density_estimated": False},
    "XTE-SF": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 32.2,
               "voc_v": 2.75, "vmp_v": 2.435, "power_density_w_m2": 433.4,
               "areal_density_mg_cm2": 130.0, "density_estimated": False},
    "XTE-HF": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 32.1,
               "voc_v": 2.782, "vmp_v": 2.49, "power_density_w_m2": 427.9,
               "areal_density_mg_cm2": 84.0, "density_estimated": False},
    "XTE-LILT": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 31.6,
                 "voc_v": 2.755, "vmp_v": 2.459, "power_density_w_m2": 427.9,
                 "areal_density_mg_cm2": 84.0, "density_estimated": False},
    "UTJ": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 28.4,
            "voc_v": 2.66, "vmp_v": 2.35, "power_density_w_m2": 384.93,
            "areal_density_mg_cm2": 84.0, "density_estimated": False},
    "TASC": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 27.0,
             "voc_v": 2.52, "vmp_v": 2.19, "power_density_w_m2": 270.0,
             "areal_density_mg_cm2": 102.76679841897233, "density_estimated": False},
    "ITJ": {"manufacturer": "Boeing-SpectroLab USA", "efficiency_pct": 26.8,
            "voc_v": 2.565, "vmp_v": 2.27, "power_density_w_m2": 1353.0,
            "areal_density_mg_cm2": 84.0, "density_estimated": False},
}


LOSS_FACTORS = [
    ("Maximum sun offpointing", "Current", 0.999, 0.999),
    ("Array flatness", "Current", 0.999, 0.999),
    ("CIC measurement uncertainty", "Current", 0.980, 0.980),
    ("CIC assembly", "Current", 0.995, 0.995),
    ("CIC assembly", "Voltage", 0.995, 0.995),
    ("Cell Mismatch", "Current", 0.995, 0.995),
    ("Cell Mismatch", "Voltage", 0.990, 0.990),
    ("Temperature", "Current", 0.950, 0.950),
    ("Temperature", "Voltage", 0.930, 0.930),
    ("Distance", "Current", 0.967, 0.967),
    ("Random workmanship", "Current", 0.990, 0.985),
    ("Cell Interconnect Voltage Drop", "Voltage", 0.996, 0.996),
    ("Blocking Diode Voltage Drop", "Voltage", 0.993, 0.993),
    ("Harness Voltage Drop", "Voltage", 0.980, 0.980),
    ("Gimbal Voltage Drop", "Voltage", 0.990, 0.990),
    ("UV", "Current", 1.000, 0.985),
    ("UV", "Voltage", 1.000, 0.995),
    ("Impact", "Current", 1.000, 0.990),
    ("Thermal cycling", "Current", 1.000, 0.980),
    ("Dust, contaminants", "Current", 1.000, 0.980),
    ("Radiation", "Current", 1.000, 0.930),
    ("Radiation", "Voltage", 1.000, 0.900),
]
TABLE_TOTAL_BOL = 0.775
TABLE_TOTAL_EOL = 0.601


# =============================================================================
#  GLOBAL STATE
# =============================================================================

selected_data = None
selected_cell_data = None
selected_name = None
custom_mode = False
last_results = None
last_inputs = None
last_measurement = "SI / Metric"

KG_TO_LB = 2.2046226218
M_TO_FT = 3.2808398950
M2_TO_FT2 = 10.7639104167
KG_M2_TO_LB_FT2 = KG_TO_LB / M2_TO_FT2


# =============================================================================
#  HELPERS
# =============================================================================

def database_for_mode():
    return SOLAR_PANELS if mode_var.get() == "Panel" else SOLAR_ARRAYS

def singular_lower():
    return mode_var.get().lower()

def plural_lower():
    return "panels" if mode_var.get() == "Panel" else "arrays"

def is_metric():
    return measurement_var.get() == "SI / Metric"

def clean_number(value, decimals=5):
    if value is None:
        return "Not published"
    return f"{value:.{decimals}f}".rstrip("0").rstrip(".")

def converted_length(v):
    if v is None: return None
    return v if is_metric() else v * M_TO_FT

def converted_area(v):
    if v is None: return None
    return v if is_metric() else v * M2_TO_FT2

def converted_mass(v):
    if v is None: return None
    return v if is_metric() else v * KG_TO_LB

def converted_areal_density(v):
    if v is None: return None
    return v if is_metric() else v * KG_M2_TO_LB_FT2

def converted_specific_power(v):
    if v is None: return None
    return v if is_metric() else v / KG_TO_LB

def converted_power_density(v):
    if v is None: return None
    return v if is_metric() else v / M2_TO_FT2

def unit_names():
    if is_metric():
        return {"length": "m", "area": "m²", "mass": "kg",
                "areal_density": "kg/m²", "specific_power": "W/kg",
                "power_density": "W/m²"}
    return {"length": "ft", "area": "ft²", "mass": "lb",
            "areal_density": "lb/ft²", "specific_power": "W/lb",
            "power_density": "W/ft²"}

def cell_areal_density_kg_m2(cell):
    return cell["areal_density_mg_cm2"] * 0.01

def cell_specific_power_w_kg(cell):
    d = cell_areal_density_kg_m2(cell)
    return cell["power_density_w_m2"] / d if d > 0 else 0.0

def replacement_active():
    return selected_data is not None and selected_cell_data is not None and not custom_mode

def effective_data():
    if selected_data is None:
        return None
    if not replacement_active():
        return dict(selected_data)

    active_area = selected_data["area_m2"] * CELL_COVERAGE_FACTOR
    retained_hardware_mass = selected_data["mass_kg"] * (1.0 - ORIGINAL_PV_MASS_FRACTION)
    new_cell_density = cell_areal_density_kg_m2(selected_cell_data)
    new_cell_mass = new_cell_density * active_area

    updated_mass = retained_hardware_mass + new_cell_mass
    updated_power = selected_cell_data["power_density_w_m2"] * active_area
    updated_specific_power = updated_power / updated_mass if updated_mass > 0 else 0.0
    updated_areal_density = updated_mass / selected_data["area_m2"] if selected_data["area_m2"] > 0 else 0.0

    updated = dict(selected_data)
    updated.update({
        "rated_power_w": updated_power,
        "mass_kg": updated_mass,
        "specific_power": updated_specific_power,
        "areal_density": updated_areal_density,
        "efficiency": f"{selected_cell_data['efficiency_pct']:.1f}% BOL cell efficiency",
        "active_area_m2": active_area,
        "retained_hardware_mass_kg": retained_hardware_mass,
        "new_cell_mass_kg": new_cell_mass,
    })
    return updated


# =============================================================================
#  UI HELPERS
# =============================================================================

def reset_results():
    global last_results
    last_results = None
    for v in (result_energy, result_exact_units, result_required_units,
              result_installed_power, result_actual_energy,
              result_total_area, result_total_mass):
        v.set("-")

def set_readonly(state):
    readonly = "readonly" if state else "normal"
    rating_entry.config(state=readonly)
    length_entry.config(state=readonly)
    width_entry.config(state=readonly)
    area_entry.config(state=readonly)
    weight_entry.config(state=readonly)

def clear_selection_display(blank_values=True):
    original_info_var.set("No hardware selected.")
    updated_info_var.set("No updated hardware values.")
    cell_info_var.set("No custom cell selected.")
    selected_type_var.set("Type  •  —")
    manufacturer_var.set("Manufacturer  •  —")
    specific_power_var.set("Specific power  •  —")
    efficiency_var.set("Efficiency  •  —")
    areal_density_var.set("Areal density  •  —")
    assumptions_var.set(
        "Theoretical assumptions become active when a database panel/array "
        "and a replacement cell are both selected."
    )
    if blank_values:
        rated_power_kw_var.set("")
        length_var.set("")
        width_var.set("")
        area_var.set("")
        weight_var.set("")
    reset_results()

def update_wording():
    kind = mode_var.get()
    kl, ku = kind.lower(), kind.upper()
    plural = "Panels" if kind == "Panel" else "Arrays"
    pl = plural.lower()
    u = unit_names()

    root.title(f"Solar {kind} Calculator")
    main_title_var.set(f"Solar {kind} Calculator")
    item_label_var.set(f"Solar {kl}")
    original_heading_var.set(f"ORIGINAL {ku} INFORMATION")
    updated_heading_var.set(f"UPDATED {ku} INFORMATION")
    step1_title_var.set(f"STEP 1  ·  ENERGY PER {ku}")
    rating_label_var.set(f"{kind} rating (kW)")
    step2_title_var.set(f"STEP 2  ·  {plural.upper()} NEEDED")
    step3_title_var.set(f"STEP 3  ·  {ku} DIMENSIONS & MASS")
    length_label_var.set(
        f"{kind} length / diameter ({u['length']})" if kind == "Array"
        else f"{kind} length ({u['length']})")
    width_label_var.set(
        f"{kind} width / diameter ({u['length']})" if kind == "Array"
        else f"{kind} width ({u['length']})")
    area_label_var.set(f"{kind} area ({u['area']})")
    weight_label_var.set(f"{kind} weight ({u['mass']})")

    if custom_mode:
        fixed_data_hint_var.set(
            f"Custom {kl} mode — enter your own dimensions, area, and weight")
    elif replacement_active():
        fixed_data_hint_var.set(
            f"Dimensions/area remain from the original {kl}; rating and mass "
            f"are recalculated using the selected custom cell")
    else:
        fixed_data_hint_var.set(
            f"Values fixed to selected {kl} from the database")

    result_energy_label_var.set(f"Energy per {kl}")
    result_exact_label_var.set(f"Theoretical {pl} needed")
    result_required_label_var.set(f"Whole {pl} required")
    result_total_area_label_var.set(f"Total {kl} area")
    result_total_mass_label_var.set(f"Total {kl} mass")
    installed_explanation_var.set(
        f"Installed power = total effective rated power of all whole {pl} installed.")
    daily_explanation_var.set(
        f"Actual daily energy = estimated energy produced by the whole {pl} in one day.")

def refresh_selected_display():
    if custom_mode or selected_data is None:
        return
    u = unit_names()
    data = effective_data()
    manufacturer_var.set(f"Manufacturer  •  {selected_data['manufacturer']}")
    selected_type_var.set(f"Type  •  {selected_data['type']}")
    sp = converted_specific_power(data["specific_power"])
    specific_power_var.set(f"Specific power  •  {sp:.1f} {u['specific_power']}")
    eff = data.get("efficiency")
    efficiency_var.set(f"Efficiency  •  {eff}" if eff else "Efficiency  •  Not publicly available")
    dens = converted_areal_density(data["areal_density"])
    areal_density_var.set(f"Areal density  •  {dens:.3f} {u['areal_density']}")

def refresh_information_blocks():
    if selected_data is None or custom_mode:
        if custom_mode:
            original_info_var.set(
                "Manual custom hardware.\n"
                "Enter rating, dimensions, area, and mass below.")
            updated_info_var.set(
                "Custom-cell replacement is disabled for manual hardware.")
            cell_info_var.set(
                "Select a database panel/array to use the custom-cell model.")
            assumptions_var.set(
                "No theoretical replacement assumptions are applied in "
                "manual custom-hardware mode.")
        return

    u = unit_names()
    original_eff = selected_data.get("efficiency") or "Not publicly available"
    original_info_var.set(
        f"Manufacturer: {selected_data['manufacturer']}\n"
        f"Type: {selected_data['type']}\n"
        f"Rating: {selected_data['rated_power_w']/1000:.3f} kW\n"
        f"Mass: {converted_mass(selected_data['mass_kg']):.3f} {u['mass']}\n"
        f"Area: {converted_area(selected_data['area_m2']):.3f} {u['area']}\n"
        f"Specific power: {converted_specific_power(selected_data['specific_power']):.1f} {u['specific_power']}\n"
        f"Efficiency: {original_eff}"
    )

    if selected_cell_data is None:
        cell_info_var.set(
            "Using original cell configuration.\n"
            "Choose a cell above to create a theoretical replacement.")
        updated_info_var.set(
            "No replacement cell selected — updated values equal the original hardware.")
        assumptions_var.set(
            "Theoretical assumptions become active only when a replacement cell is selected.")
        return

    cell_density_si = cell_areal_density_kg_m2(selected_cell_data)
    cell_sp_si = cell_specific_power_w_kg(selected_cell_data)
    density_note = "estimated fallback" if selected_cell_data["density_estimated"] else "published / derived"

    cell_info_var.set(
        f"Cell: {cell_choice.get()}\n"
        f"Manufacturer: {selected_cell_data['manufacturer']}\n"
        f"Efficiency: {selected_cell_data['efficiency_pct']:.1f}% BOL\n"
        f"Power density: {converted_power_density(selected_cell_data['power_density_w_m2']):.2f} {u['power_density']}\n"
        f"Areal density: {converted_areal_density(cell_density_si):.3f} {u['areal_density']} ({density_note})\n"
        f"Specific power: {converted_specific_power(cell_sp_si):.1f} {u['specific_power']}\n"
        f"Voc / Vmp: {selected_cell_data['voc_v']:.3f} V / {selected_cell_data['vmp_v']:.3f} V"
    )

    updated = effective_data()
    updated_info_var.set(
        f"Updated rating: {updated['rated_power_w']/1000:.3f} kW\n"
        f"Updated mass: {converted_mass(updated['mass_kg']):.3f} {u['mass']}\n"
        f"Updated specific power: {converted_specific_power(updated['specific_power']):.1f} {u['specific_power']}\n"
        f"Updated areal density: {converted_areal_density(updated['areal_density']):.3f} {u['areal_density']}\n"
        f"Updated PV efficiency (cell): {selected_cell_data['efficiency_pct']:.1f}% BOL"
    )

    active_area = updated["active_area_m2"]
    assumptions_var.set(
        f"Packing factor = 0.85: 85% of the {singular_lower()} reference area is treated "
        f"as active PV cell area. For this selection, the calculated active PV area is "
        f"{converted_area(active_area):.3f} {u['area']}; it is used internally to estimate "
        f"the replacement-cell power and mass.\n"
        f"Original PV-cell mass = 10% of original hardware mass: the remaining 90% is "
        f"treated as retained hardware when the cell technology is replaced. These are "
        f"theoretical sizing assumptions, not manufacturer-certified values."
    )

def refresh_hardware_fields():
    if custom_mode or selected_data is None:
        return
    data = effective_data()
    u = unit_names()
    rated_power_kw_var.set(clean_number(data["rated_power_w"] / 1000.0, 5))
    length_var.set(clean_number(converted_length(data["length_m"]), 5))
    width_var.set(clean_number(converted_length(data["width_m"]), 5))
    area_var.set(f"{converted_area(data['area_m2']):.4f}")
    weight_var.set(f"{converted_mass(data['mass_kg']):.3f}")
    areal_density_var.set(
        f"Areal density  •  {converted_areal_density(data['areal_density']):.3f} {u['areal_density']}"
    )

def refresh_results_display():
    if last_results is None:
        return
    u = unit_names()
    result_energy.set(f"{max(0, last_results['energy_per_unit']):.3f} kWh/day")
    result_exact_units.set(f"{max(0, last_results['exact_units']):.3f}")
    result_required_units.set(f"{max(0, last_results['required_units'])}")
    result_installed_power.set(f"{max(0, last_results['installed_power_kw']):.3f} kW")
    result_actual_energy.set(f"{max(0, last_results['actual_daily_energy']):.2f} kWh/day")
    result_total_area.set(f"{max(0, converted_area(last_results['total_area_m2'])):.2f} {u['area']}")
    result_total_mass.set(f"{max(0, converted_mass(last_results['total_mass_kg'])):.2f} {u['mass']}")


# =============================================================================
#  EVENT HANDLERS
# =============================================================================

def measurement_changed():
    global last_measurement
    old, new = last_measurement, measurement_var.get()
    if custom_mode and old != new:
        try:
            l = float(length_var.get()) if length_var.get().strip() else None
            w = float(width_var.get()) if width_var.get().strip() else None
            a = float(area_var.get()) if area_var.get().strip() else None
            m = float(weight_var.get()) if weight_var.get().strip() else None
            if old == "SI / Metric" and new == "U.S. Customary":
                if l is not None: length_var.set(clean_number(l * M_TO_FT, 5))
                if w is not None: width_var.set(clean_number(w * M_TO_FT, 5))
                if a is not None: area_var.set(clean_number(a * M2_TO_FT2, 5))
                if m is not None: weight_var.set(clean_number(m * KG_TO_LB, 5))
            elif old == "U.S. Customary" and new == "SI / Metric":
                if l is not None: length_var.set(clean_number(l / M_TO_FT, 5))
                if w is not None: width_var.set(clean_number(w / M_TO_FT, 5))
                if a is not None: area_var.set(clean_number(a / M2_TO_FT2, 5))
                if m is not None: weight_var.set(clean_number(m / KG_TO_LB, 5))
        except ValueError:
            pass
    last_measurement = new
    update_wording()
    refresh_selected_display()
    refresh_information_blocks()
    refresh_hardware_fields()
    refresh_results_display()

def mode_changed():
    global selected_data, selected_cell_data, custom_mode, selected_name
    selected_data = None
    selected_cell_data = None
    selected_name = None
    custom_mode = False
    update_wording()
    item_dropdown["values"] = [BLANK, CUSTOM] + list(database_for_mode().keys())
    item_choice.set(BLANK)
    cell_choice.set(ORIGINAL_CELL)
    cell_dropdown.config(state="disabled")
    clear_selection_display(blank_values=True)
    set_readonly(True)

def item_selected(event=None):
    global selected_data, selected_cell_data, custom_mode, selected_name
    name = item_choice.get()

    if name == BLANK:
        selected_data = None
        selected_cell_data = None
        selected_name = None
        custom_mode = False
        cell_choice.set(ORIGINAL_CELL)
        cell_dropdown.config(state="disabled")
        set_readonly(True)
        clear_selection_display(blank_values=True)
        update_wording()
        return

    if name == CUSTOM:
        selected_data = None
        selected_cell_data = None
        selected_name = None
        custom_mode = True
        cell_choice.set(ORIGINAL_CELL)
        cell_dropdown.config(state="disabled")
        clear_selection_display(blank_values=True)
        manufacturer_var.set("Manufacturer  •  (custom)")
        selected_type_var.set("Type  •  (custom)")
        specific_power_var.set("Specific power  •  (custom)")
        efficiency_var.set("Efficiency  •  (custom)")
        areal_density_var.set("Areal density  •  calculated after entry")
        set_readonly(False)
        update_wording()
        refresh_information_blocks()
        return

    database = database_for_mode()
    if name not in database:
        return
    selected_name = name
    selected_data = database[name]
    selected_cell_data = None
    custom_mode = False
    set_readonly(True)
    cell_choice.set(ORIGINAL_CELL)
    cell_dropdown.config(state="readonly")
    update_wording()
    refresh_selected_display()
    refresh_information_blocks()
    refresh_hardware_fields()
    reset_results()

def cell_selected(event=None):
    global selected_cell_data
    if selected_data is None or custom_mode:
        selected_cell_data = None
        return
    name = cell_choice.get()
    selected_cell_data = None if name == ORIGINAL_CELL else SOLAR_CELLS.get(name)
    update_wording()
    refresh_selected_display()
    refresh_information_blocks()
    refresh_hardware_fields()
    reset_results()

def valid_psh(proposed):
    if proposed == "":
        return True
    try:
        value = float(proposed)
    except ValueError:
        return False
    return 0 <= value <= 24


# =============================================================================
#  CALCULATE
# =============================================================================

def read_custom_data_si():
    try:
        unit_kw = float(rated_power_kw_var.get())
        ld = float(length_var.get())
        wd = float(width_var.get())
        ad = float(area_var.get())
        md = float(weight_var.get())
    except ValueError:
        raise ValueError(
            "In Custom mode, please fill in rating, length, width, area, and weight.")
    if is_metric():
        return {"rated_power_w": unit_kw * 1000, "length_m": ld, "width_m": wd,
                "area_m2": ad, "mass_kg": md}
    return {"rated_power_w": unit_kw * 1000,
            "length_m": ld / M_TO_FT, "width_m": wd / M_TO_FT,
            "area_m2": ad / M2_TO_FT2, "mass_kg": md / KG_TO_LB}

def calculate():
    global last_results, last_inputs

    if custom_mode:
        try:
            data = read_custom_data_si()
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))
            return
    else:
        if selected_data is None:
            messagebox.showerror("Selection Required",
                f"Please select a solar {singular_lower()} first.")
            return
        data = effective_data()

    try:
        psh = float(entry_psh.get())
        derate = float(entry_derate.get())
        target_kwh = float(entry_target.get())
    except ValueError:
        messagebox.showerror("Input Error",
            "Please enter valid numbers for sunlight hours, derate factor, and daily target.")
        return

    if not 0 <= psh <= 24:
        messagebox.showerror("Input Error", "Peak Sun Hours must range from 0 to 24.")
        return
    if psh == 0:
        messagebox.showerror("Input Error", "PSH = 0 means no energy produced.")
        return

    unit_kw = data["rated_power_w"] / 1000.0
    area_m2 = data["area_m2"]
    mass_kg = data["mass_kg"]

    if unit_kw <= 0 or area_m2 <= 0 or mass_kg <= 0 or derate <= 0 or target_kwh <= 0:
        messagebox.showerror("Input Error", "All sizing values must be greater than 0.")
        return
    if derate > 1:
        messagebox.showerror("Input Error", "Derate factor must be between 0 and 1.")
        return

    energy_per_unit = unit_kw * psh * derate
    exact_units = target_kwh / energy_per_unit
    required_units = math.ceil(exact_units)

    last_results = {
        "energy_per_unit":    max(0.0, energy_per_unit),
        "exact_units":        max(0.0, exact_units),
        "required_units":     max(0, required_units),
        "installed_power_kw": max(0.0, required_units * unit_kw),
        "actual_daily_energy": max(0.0, required_units * energy_per_unit),
        "total_area_m2":      max(0.0, required_units * area_m2),
        "total_mass_kg":      max(0.0, required_units * mass_kg),
        "snapshot_unit_kw":   unit_kw,
        "snapshot_area_m2":   area_m2,
        "snapshot_mass_kg":   mass_kg,
    }
    last_inputs = {"psh": psh, "derate": derate, "target_kwh": target_kwh}

    refresh_results_display()


# =============================================================================
#  BAR-CHART COMPARISON WINDOW
# =============================================================================

def show_power_graphs():
    if last_results is None or last_inputs is None:
        messagebox.showerror("No Results", "Please calculate first.")
        return

    psh        = last_inputs["psh"]
    derate     = last_inputs["derate"]
    target_kwh = last_inputs["target_kwh"]

    def kwh_of(item):
        return max(0.0, (item["rated_power_w"] / 1000.0) * psh * derate)

    def scenario_for(name, item, is_panel):
        ekw = kwh_of(item)
        if ekw <= 0 or not item.get("area_m2") or not item.get("mass_kg"):
            return None
        count = math.ceil(target_kwh / ekw)
        return {
            "name": name,
            "is_panel": is_panel,
            "unit_kw": item["rated_power_w"] / 1000.0,
            "unit_area": item["area_m2"],
            "unit_mass": item["mass_kg"],
            "energy_per_unit": ekw,
            "count": count,
            "total_area": count * item["area_m2"],
            "total_mass": count * item["mass_kg"],
            "total_kwh":  count * ekw,
        }

    all_scenarios = []
    for n, it in SOLAR_PANELS.items():
        s = scenario_for(n, it, True)
        if s: all_scenarios.append(s)
    for n, it in SOLAR_ARRAYS.items():
        s = scenario_for(n, it, False)
        if s: all_scenarios.append(s)

    if not all_scenarios:
        messagebox.showerror("No Data", "No valid hardware scenarios to plot.")
        return

    areas = [s["total_area"] for s in all_scenarios]
    masses = [s["total_mass"] for s in all_scenarios]
    a_min, a_max = min(areas), max(areas)
    m_min, m_max = min(masses), max(masses)
    a_range = (a_max - a_min) or 1.0
    m_range = (m_max - m_min) or 1.0
    for s in all_scenarios:
        s["score"] = 0.5 * (s["total_area"] - a_min) / a_range + \
                     0.5 * (s["total_mass"] - m_min) / m_range

    ranked = sorted(all_scenarios, key=lambda s: s["score"])
    for i, s in enumerate(ranked, 1):
        s["rank"] = i

    now_area  = max(0.0, last_results["total_area_m2"])
    now_mass  = max(0.0, last_results["total_mass_kg"])
    now_kwh   = max(0.0, last_results["actual_daily_energy"])
    now_count = max(0, last_results["required_units"])

    COLOR_BG, COLOR_PANEL, COLOR_ARRAY = "#0f172a", "#fbbf24", "#38bdf8"
    COLOR_NOW    = "#22c55e"
    COLOR_OPT_A  = "#f472b6"
    COLOR_OPT_B  = "#fb7185"
    COLOR_AXIS   = "#94a3b8"
    COLOR_GRID   = "#1e293b"
    COLOR_TEXT   = "#cbd5e1"
    COLOR_HINT   = "#64748b"
    COLOR_WIN    = "#22c55e"
    COLOR_LOSE   = "#f87171"
    CARD_BG      = "#111827"
    CARD_BORDER  = "#334155"

    win = tk.Toplevel(root)
    win.title("Solar Options Comparison")
    win.configure(bg=COLOR_BG)

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    win_w = min(1500, int(screen_w * 0.95))
    win_h = min(screen_h - 60, int(screen_h * 0.93))
    pos_x = max(0, (screen_w - win_w) // 2)
    pos_y = 15
    win.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    win.minsize(1100, 700)

    outer = tk.Frame(win, bg=COLOR_BG)
    outer.pack(fill="both", expand=True)
    scroll_canvas = tk.Canvas(outer, bg=COLOR_BG, highlightthickness=0)
    scroll_canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ttk.Scrollbar(outer, orient="vertical", command=scroll_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    inner = tk.Frame(scroll_canvas, bg=COLOR_BG)
    inner_id = scroll_canvas.create_window((0, 0), window=inner, anchor="nw")

    def _on_inner(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    inner.bind("<Configure>", _on_inner)

    def _on_canvas(event):
        scroll_canvas.itemconfigure(inner_id, width=event.width)
    scroll_canvas.bind("<Configure>", _on_canvas)

    scroll_canvas.bind_all(
        "<MouseWheel>",
        lambda e: scroll_canvas.yview_scroll(int(-e.delta / 120), "units")
    )

    # Header
    header = tk.Frame(inner, bg=COLOR_BG)
    header.pack(fill="x", padx=32, pady=(24, 12))
    tk.Label(header, text="Solar Options Comparison",
             bg=COLOR_BG, fg="#fbbf24",
             font=("Segoe UI", 17, "bold")).pack(anchor="w")
    tk.Label(header,
             text=(f"PSH = {psh:.2f} h/day   ·   Derate = {derate:.2f}   "
                   f"·   Target = {target_kwh:.2f} kWh/day"),
             bg=COLOR_BG, fg="#cbd5e1",
             font=("Segoe UI", 10)).pack(anchor="w", pady=(6, 0))

    # Dropdowns
    ctrl = tk.Frame(inner, bg=COLOR_BG)
    ctrl.pack(fill="x", padx=32, pady=(20, 26))

    option_a_var = tk.StringVar(value="InSight UltraFlex — Two-Array System")
    option_b_var = tk.StringVar(value="ROSA Sapphire — 12.9 kW Wing")

    def dropdown_box(parent, title, title_color, var):
        box = tk.Frame(parent, bg="#1e293b",
                       highlightbackground=title_color, highlightthickness=2)
        tk.Label(box, text=title, bg="#1e293b", fg=title_color,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=18, pady=(14, 8))
        dd = ttk.Combobox(box, textvariable=var, state="readonly", width=42)
        dd["values"] = list(SOLAR_ARRAYS.keys())
        dd.pack(fill="x", padx=18, pady=(0, 16))
        return box, dd

    box_a, dd_a = dropdown_box(ctrl, "OPTION A", COLOR_OPT_A, option_a_var)
    box_a.grid(row=0, column=0, sticky="ew", padx=(0, 16))
    box_b, dd_b = dropdown_box(ctrl, "OPTION B", COLOR_OPT_B, option_b_var)
    box_b.grid(row=0, column=1, sticky="ew", padx=(16, 0))
    ctrl.columnconfigure(0, weight=1)
    ctrl.columnconfigure(1, weight=1)

    # Head-to-head summary
    summary = tk.Frame(inner, bg=CARD_BG,
                       highlightbackground=CARD_BORDER, highlightthickness=1)
    summary.pack(fill="x", padx=32, pady=(0, 32))

    tk.Label(summary, text="HEAD-TO-HEAD COMPARISON",
             bg=CARD_BG, fg="#fbbf24",
             font=("Segoe UI", 12, "bold")).grid(
        row=0, column=0, columnspan=4, sticky="w", padx=22, pady=(18, 12))

    header_font = ("Segoe UI", 10, "bold")
    label_font  = ("Segoe UI", 10)
    value_font  = ("Segoe UI", 11, "bold")

    for c, (txt, color) in enumerate([
        ("Metric", None),
        ("Your Solution", COLOR_NOW),
        ("Option A", COLOR_OPT_A),
        ("Option B", COLOR_OPT_B),
    ]):
        tk.Label(summary, text=txt, bg=CARD_BG,
                 fg=color if color else "#cbd5e1",
                 font=header_font,
                 anchor="w" if c == 0 else "e").grid(
            row=1, column=c, sticky="we",
            padx=(22 if c == 0 else 14, 22 if c == 3 else 14),
            pady=(0, 10))

    def get_scenario_by_name(nm):
        for s in all_scenarios:
            if s["name"] == nm:
                return s
        return None

    def metric_number(sc, metric_name):
        if metric_name == "Units required":      return sc["count"]
        if metric_name == "Total area":          return sc["total_area"]
        if metric_name == "Total mass":          return sc["total_mass"]
        if metric_name == "Energy produced/day": return sc["total_kwh"]
        if metric_name == "Rank (best = 1)":     return sc["rank"]
        return 0

    def winner_color(my_num, other_num, direction):
        if my_num is None or other_num is None:
            return "#e2e8f0"
        if direction == "min":
            if my_num < other_num: return COLOR_WIN
            if my_num > other_num: return COLOR_LOSE
        elif direction == "max":
            if my_num > other_num: return COLOR_WIN
            if my_num < other_num: return COLOR_LOSE
        return "#e2e8f0"

    def refresh_summary():
        oa = get_scenario_by_name(option_a_var.get())
        ob = get_scenario_by_name(option_b_var.get())

        rows = [
            ("Units required",      lambda s: f"{s['count']}",              "min"),
            ("Total area",          lambda s: f"{s['total_area']:.2f} m²",  "min"),
            ("Total mass",          lambda s: f"{s['total_mass']:.2f} kg",  "min"),
            ("Energy produced/day", lambda s: f"{s['total_kwh']:.2f} kWh",  "max"),
            ("Rank (best = 1)",     lambda s: f"#{s['rank']}",              "min"),
        ]

        for widget in summary.grid_slaves():
            try:
                if int(widget.grid_info()["row"]) >= 2:
                    widget.destroy()
            except Exception:
                pass

        r = 2
        for metric_name, value_fn, direction in rows:
            tk.Label(summary, text=metric_name, bg=CARD_BG, fg="#cbd5e1",
                     font=label_font, anchor="w").grid(
                row=r, column=0, sticky="w", padx=(22, 10), pady=8)

            if metric_name == "Units required":
                now_disp = f"{now_count}"
            elif metric_name == "Total area":
                now_disp = f"{now_area:.2f} m²"
            elif metric_name == "Total mass":
                now_disp = f"{now_mass:.2f} kg"
            elif metric_name == "Energy produced/day":
                now_disp = f"{now_kwh:.2f} kWh"
            elif metric_name == "Rank (best = 1)":
                now_score = 0.5 * (now_area - a_min) / a_range + \
                            0.5 * (now_mass - m_min) / m_range
                all_scores = [s["score"] for s in all_scenarios] + [now_score]
                now_disp = f"#{sorted(all_scores).index(now_score) + 1}"
            else:
                now_disp = "-"

            tk.Label(summary, text=now_disp, bg=CARD_BG, fg=COLOR_NOW,
                     font=value_font, anchor="e").grid(
                row=r, column=1, sticky="e", padx=(14, 22), pady=8)

            a_num = metric_number(oa, metric_name) if oa else None
            b_num = metric_number(ob, metric_name) if ob else None

            if oa:
                tk.Label(summary, text=value_fn(oa), bg=CARD_BG,
                         fg=winner_color(a_num, b_num, direction),
                         font=value_font, anchor="e").grid(
                    row=r, column=2, sticky="e", padx=(14, 22), pady=8)
            else:
                tk.Label(summary, text="—", bg=CARD_BG, fg="#64748b",
                         font=value_font, anchor="e").grid(
                    row=r, column=2, sticky="e", padx=(14, 22), pady=8)

            if ob:
                tk.Label(summary, text=value_fn(ob), bg=CARD_BG,
                         fg=winner_color(b_num, a_num, direction),
                         font=value_font, anchor="e").grid(
                    row=r, column=3, sticky="e", padx=(14, 22), pady=8)
            else:
                tk.Label(summary, text="—", bg=CARD_BG, fg="#64748b",
                         font=value_font, anchor="e").grid(
                    row=r, column=3, sticky="e", padx=(14, 22), pady=8)
            r += 1

        tk.Label(
            summary,
            text=("Green = better on this metric   ·   Red = worse   ·   "
                  "Rank combines area and mass (lower = better)"),
            bg=CARD_BG, fg="#64748b", font=("Segoe UI", 8, "italic")
        ).grid(row=r, column=0, columnspan=4, sticky="w", padx=22, pady=(14, 18))

    # Bar chart builder  —  WIDE LABEL COLUMN + BIG GAPS + FULL NAMES
    TOP_N = 15

    def build_bar_chart(parent, value_key, unit_label, title, subtitle,
                        highlight_a, highlight_b):
        row_count = min(len(all_scenarios), TOP_N)
        cv_height = 130 + row_count * 46
        cv = tk.Canvas(parent, bg=COLOR_BG, highlightthickness=0, height=cv_height)
        cv.pack(fill="x", expand=False)

        def draw(event=None):
            cv.delete("all")
            w = cv.winfo_width()
            h = cv.winfo_height()
            if w < 100 or h < 100:
                return

            shown = sorted(all_scenarios, key=lambda s: s[value_key])[:TOP_N]
            max_val = max(s[value_key] for s in shown) or 1.0

            # Wider label column (name text) + fixed right value column
            label_w = 380
            value_w = 120
            x0 = label_w
            x1 = w - value_w
            y_top = 80
            y_bottom = h - 52
            bar_gap = 18
            bar_h = (y_bottom - y_top - (len(shown) - 1) * bar_gap) / max(len(shown), 1)

            cv.create_text(24, 22, text=title, anchor="w",
                           fill="#fbbf24", font=("Segoe UI", 13, "bold"))
            cv.create_text(24, 50, text=subtitle, anchor="w",
                           fill="#64748b", font=("Segoe UI", 9, "italic"))

            cv.create_text((x0 + x1) / 2, h - 16,
                           text=unit_label, fill=COLOR_TEXT,
                           font=("Segoe UI", 9, "bold"))

            for i in range(6):
                frac = i / 5
                gx = x0 + (x1 - x0) * frac
                cv.create_line(gx, y_top - 8, gx, y_bottom + 6,
                               fill=COLOR_GRID, dash=(2, 4))
                tick_val = max_val * frac
                cv.create_text(gx, y_bottom + 22,
                               text=f"{tick_val:.1f}",
                               fill=COLOR_HINT, font=("Segoe UI", 8))

            cv.create_line(x0, y_top - 8, x0, y_bottom + 6,
                           fill=COLOR_AXIS, width=2)

            for i, s in enumerate(shown):
                y = y_top + i * (bar_h + bar_gap)
                bar_len = (s[value_key] / max_val) * (x1 - x0)

                is_a   = highlight_a is not None and s["name"] == highlight_a["name"]
                is_b   = highlight_b is not None and s["name"] == highlight_b["name"]
                is_now = (abs(s["total_area"] - now_area) < 1e-6 and
                          abs(s["total_mass"] - now_mass) < 1e-6)

                if is_a:
                    fill_color = COLOR_OPT_A
                elif is_b:
                    fill_color = COLOR_OPT_B
                elif is_now:
                    fill_color = COLOR_NOW
                elif s["is_panel"]:
                    fill_color = COLOR_PANEL
                else:
                    fill_color = COLOR_ARRAY

                outline_w = 2 if (is_a or is_b or is_now) else 0
                outline = fill_color if outline_w else ""

                full = s["name"]

                if is_a:
                    label_color = COLOR_OPT_A
                elif is_b:
                    label_color = COLOR_OPT_B
                elif is_now:
                    label_color = COLOR_NOW
                else:
                    label_color = "#cbd5e1"

                # Full name anchored right so it never clips off the left edge
                cv.create_text(x0 - 14, y + bar_h / 2, text=full,
                               anchor="e", fill=label_color,
                               font=("Segoe UI", 10))

                cv.create_rectangle(x0, y, x0 + bar_len, y + bar_h,
                                    fill=fill_color,
                                    outline=outline, width=outline_w)

                cv.create_text(x0 + bar_len + 10, y + bar_h / 2,
                               text=f"{s[value_key]:.2f}",
                               anchor="w", fill="#e2e8f0",
                               font=("Segoe UI", 10, "bold"))

        cv.bind("<Configure>", draw)
        return cv

    # Graph 1 card
    g1_card = tk.Frame(inner, bg=CARD_BG,
                       highlightbackground=CARD_BORDER, highlightthickness=1)
    g1_card.pack(fill="x", padx=32, pady=(0, 32))

    g1_header = tk.Frame(g1_card, bg=CARD_BG)
    g1_header.pack(fill="x", padx=22, pady=(20, 12))
    tk.Label(g1_header, text="GRAPH 1  ·  SPACE EFFICIENCY",
             bg=CARD_BG, fg="#fbbf24",
             font=("Segoe UI", 12, "bold")).pack(anchor="w")
    tk.Label(g1_header,
             text="Top 15 options by total area · shorter bars are better",
             bg=CARD_BG, fg="#64748b",
             font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(4, 0))

    g1_body = tk.Frame(g1_card, bg=CARD_BG)
    g1_body.pack(fill="x", padx=12, pady=(0, 20))

    # Graph 2 card
    g2_card = tk.Frame(inner, bg=CARD_BG,
                       highlightbackground=CARD_BORDER, highlightthickness=1)
    g2_card.pack(fill="x", padx=32, pady=(0, 32))

    g2_header = tk.Frame(g2_card, bg=CARD_BG)
    g2_header.pack(fill="x", padx=22, pady=(20, 12))
    tk.Label(g2_header, text="GRAPH 2  ·  MASS EFFICIENCY",
             bg=CARD_BG, fg="#fbbf24",
             font=("Segoe UI", 12, "bold")).pack(anchor="w")
    tk.Label(g2_header,
             text="Top 15 options by total mass · shorter bars are better",
             bg=CARD_BG, fg="#64748b",
             font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(4, 0))

    g2_body = tk.Frame(g2_card, bg=CARD_BG)
    g2_body.pack(fill="x", padx=12, pady=(0, 20))

    bar_canvases = []

    def refresh_plots():
        oa = get_scenario_by_name(option_a_var.get())
        ob = get_scenario_by_name(option_b_var.get())
        refresh_summary()

        for cv in bar_canvases:
            cv.destroy()
        bar_canvases.clear()

        cv1 = build_bar_chart(
            g1_body, "total_area", "Total area (m²)",
            "Space Efficiency",
            "Top 15 options · smallest area first · shorter bars are better",
            oa, ob
        )
        bar_canvases.append(cv1)
        cv1.after(40, lambda: cv1.event_generate("<Configure>"))

        cv2 = build_bar_chart(
            g2_body, "total_mass", "Total mass (kg)",
            "Mass Efficiency",
            "Top 15 options · lightest first · shorter bars are better",
            oa, ob
        )
        bar_canvases.append(cv2)
        cv2.after(40, lambda: cv2.event_generate("<Configure>"))

    # Ranked table card
    table_card = tk.Frame(inner, bg=CARD_BG,
                          highlightbackground=CARD_BORDER, highlightthickness=1)
    table_card.pack(fill="x", padx=32, pady=(0, 42))

    table_header = tk.Frame(table_card, bg=CARD_BG)
    table_header.pack(fill="x", padx=22, pady=(20, 12))
    tk.Label(table_header,
             text="RANKED OPTIONS — best combined area + mass first",
             bg=CARD_BG, fg="#fbbf24",
             font=("Segoe UI", 12, "bold")).pack(anchor="w")
    tk.Label(table_header,
             text=("Score blends area and mass (0 = best possible, 1 = worst). "
                   "Winner highlighted green."),
             bg=CARD_BG, fg="#64748b",
             font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(4, 0))

    table_body = tk.Frame(table_card, bg=CARD_BG)
    table_body.pack(fill="x", padx=22, pady=(0, 20))

    style_t = ttk.Style()
    style_t.configure("Spaced.Treeview",
                      background="#0f172a",
                      foreground="#e2e8f0",
                      fieldbackground="#0f172a",
                      rowheight=30,
                      font=("Segoe UI", 10))
    style_t.configure("Spaced.Treeview.Heading",
                      background="#1e293b",
                      foreground="#fbbf24",
                      font=("Segoe UI", 10, "bold"))

    cols = ("Rank", "Name", "Type", "Units",
            "Total area (m²)", "Total mass (kg)",
            "Energy/day (kWh)", "Score")
    table = ttk.Treeview(table_body, columns=cols, show="headings",
                         height=15, style="Spaced.Treeview")

    for c in cols:
        table.heading(c, text=c)
        if c == "Name":
            table.column(c, width=330, anchor="w")
        elif c in ("Type", "Rank", "Units"):
            table.column(c, width=80, anchor="center")
        else:
            table.column(c, width=140, anchor="center")

    table.tag_configure("panel",  background="#1e293b", foreground="#fbbf24")
    table.tag_configure("array",  background="#0f172a", foreground="#38bdf8")
    table.tag_configure("winner", background="#052e16", foreground="#22c55e")

    for s in ranked:
        tags = ["panel" if s["is_panel"] else "array"]
        if s["rank"] == 1:
            tags = ["winner"]
        table.insert(
            "", "end",
            values=(
                f"#{s['rank']}",
                s["name"],
                "Panel" if s["is_panel"] else "Array",
                s["count"],
                f"{s['total_area']:.2f}",
                f"{s['total_mass']:.2f}",
                f"{s['total_kwh']:.2f}",
                f"{s['score']:.3f}",
            ),
            tags=tags
        )

    table.pack(fill="x")

    dd_a.bind("<<ComboboxSelected>>", lambda e: refresh_plots())
    dd_b.bind("<<ComboboxSelected>>", lambda e: refresh_plots())

    win.after(80, refresh_plots)


# =============================================================================
#  SOLAR PANEL ANGLES WINDOW
# =============================================================================

_angle_drag_target = None
_angle_draw_meta = {}
SUN_ORBIT_RADIUS_RATIO = 0.58
ORIGINAL_CELL_TXT = "— Use original cell configuration —"


def _angles_database():
    return SOLAR_PANELS if mode_var.get() == "Panel" else SOLAR_ARRAYS


def _angles_selected_hardware():
    return _angles_database().get(item_choice.get())


def _angles_selected_cell():
    name = cell_choice.get()
    if not name or name == ORIGINAL_CELL_TXT:
        return None
    return SOLAR_CELLS.get(name)


def _angles_effective_hardware(data, cell):
    if cell is None:
        return {
            "rated_power_w": float(data["rated_power_w"]),
            "mass_kg": float(data["mass_kg"]),
            "area_m2": float(data["area_m2"]),
            "specific_power": float(data["specific_power"]),
            "areal_density": float(data["areal_density"]),
            "efficiency_text": data.get("efficiency") or "Not publicly available",
            "active_area_m2": None,
            "replacement": False,
        }
    active_area = float(data["area_m2"]) * CELL_COVERAGE_FACTOR
    retained_hardware_mass = float(data["mass_kg"]) * (1.0 - ORIGINAL_PV_MASS_FRACTION)
    new_cell_mass = (cell["areal_density_mg_cm2"] * 0.01) * active_area
    updated_mass = retained_hardware_mass + new_cell_mass
    updated_power = float(cell["power_density_w_m2"]) * active_area
    return {
        "rated_power_w": updated_power,
        "mass_kg": updated_mass,
        "area_m2": float(data["area_m2"]),
        "specific_power": updated_power / updated_mass if updated_mass > 0 else 0.0,
        "areal_density": updated_mass / float(data["area_m2"]) if data["area_m2"] > 0 else 0.0,
        "efficiency_text": f"{cell['efficiency_pct']:.1f}% BOL cell efficiency",
        "active_area_m2": active_area,
        "replacement": True,
    }


def _angles_percent_number(text):
    if not text:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)\s*%", str(text))
    return float(m.group(1)) if m else None


def _angles_fmt_power(w):
    if w >= 1000:
        return f"{w/1000:.3f} kW"
    return f"{w:.1f} W"


def _angles_fmt_energy(w):
    if w >= 1000:
        return f"{w/1000:.3f} kWh"
    return f"{w:.1f} Wh"


def _angles_clamp(v, lo, hi):
    return max(lo, min(hi, v))


def _angles_point_seg_distance(px, py, x1, y1, x2, y2):
    vx = x2 - x1; vy = y2 - y1
    wx = px - x1; wy = py - y1
    denom = vx*vx + vy*vy
    if denom <= 1e-9:
        return math.hypot(px-x1, py-y1)
    t = _angles_clamp((wx*vx + wy*vy) / denom, 0.0, 1.0)
    cx = x1 + t*vx
    cy = y1 + t*vy
    return math.hypot(px-cx, py-cy)


def _angles_normalized_area_position(data, mode):
    db = SOLAR_PANELS if mode == "Panel" else SOLAR_ARRAYS
    areas = [max(float(v["area_m2"]), 1e-9) for v in db.values()]
    area = max(float(data["area_m2"]), 1e-9)
    lo = min(areas); hi = max(areas)
    if hi <= lo:
        return 0.5
    if mode == "Array":
        return (math.log(area) - math.log(lo)) / (math.log(hi) - math.log(lo))
    return (area - lo) / (hi - lo)


def _angles_hardware_visual_length(data, w, h, mode):
    n = _angles_clamp(_angles_normalized_area_position(data, mode), 0.0, 1.0)
    if mode == "Panel":
        low = min(170.0, w * 0.22); high = min(280.0, w * 0.34)
    else:
        low = min(315.0, w * 0.39); high = min(470.0, w * 0.56)
    max_by_height = h * 0.72
    high = min(high, max_by_height)
    low = min(low, high * 0.76)
    return low + n * (high - low)


def _angles_rotated_segment(cx, cy, length, tilt_deg):
    tr = math.radians(tilt_deg)
    ux = math.cos(tr); uy = -math.sin(tr)
    half = length / 2.0
    return (cx - ux*half, cy - uy*half, cx + ux*half, cy + uy*half, ux, uy)


def _angles_draw_parallel_rays(canvas, sun_x, sun_y, sun_el, w, offsets):
    a = math.radians(sun_el)
    dx = math.cos(a); dy = math.sin(a)
    px = -dy; py = dx
    for offset in offsets:
        bx = sun_x + px*offset
        by = sun_y + py*offset
        x0 = 22; x1 = w - 22
        t0 = (x0 - bx) / max(dx, 1e-9)
        t1 = (x1 - bx) / max(dx, 1e-9)
        y0 = by + dy*t0
        y1 = by + dy*t1
        canvas.create_line(x0, y0, x1, y1, fill="#fde68a", width=2, arrow=tk.LAST)


def _angles_draw(canvas, tilt, sun_el, incidence, angle_factor,
                 data, eff_hw, mode, cell_name):
    global _angle_draw_meta

    canvas.delete("all")
    w = max(canvas.winfo_width(), 720)
    h = max(canvas.winfo_height(), 500)

    ground_y = h * 0.87
    pivot_x = w * 0.71
    pivot_y = h * 0.47

    canvas.create_text(24, 25, text="SOLAR PANEL ANGLES",
                       anchor="w", fill="#fbbf24", font=("Segoe UI", 12, "bold"))
    canvas.create_text(24, 49,
                       text="Drag the Sun along its fixed-distance arc, or rotate the panel/array",
                       anchor="w", fill="#cbd5e1", font=("Segoe UI", 10))
    canvas.create_text(24, 73,
                       text=(f"Tilt {tilt:.1f}°   •   Sun elevation {sun_el:.1f}°   •   "
                             f"Incidence {incidence:.1f}°   •   Angle factor {angle_factor*100:.1f}%"),
                       anchor="w", fill="#cbd5e1", font=("Segoe UI", 10))

    canvas.create_line(22, ground_y, w - 22, ground_y, fill="#94a3b8", width=2)
    canvas.create_text(34, ground_y + 17, text="Lunar horizon",
                       anchor="w", fill="#94a3b8", font=("Segoe UI", 9))

    visual_length = _angles_hardware_visual_length(data, w, h, mode)
    x1, y1, x2, y2, ux, uy = _angles_rotated_segment(pivot_x, pivot_y, visual_length, tilt)

    a = math.radians(sun_el)
    sun_orbit_radius = min(w * SUN_ORBIT_RADIUS_RATIO, pivot_x - 72.0)
    sun_orbit_radius = max(220.0, sun_orbit_radius)
    sx = pivot_x - sun_orbit_radius * math.cos(a)
    sy = pivot_y - sun_orbit_radius * math.sin(a)

    ray_spacing = max(42.0, min(70.0, h * 0.10))
    _angles_draw_parallel_rays(canvas, sx, sy, sun_el, w,
                               offsets=(-ray_spacing, 0.0, ray_spacing))

    sun_radius = 31
    canvas.create_oval(sx-sun_radius, sy-sun_radius, sx+sun_radius, sy+sun_radius,
                       fill="#fde047", outline="#f59e0b", width=3, tags=("sun",))
    for deg in range(0, 360, 45):
        r = math.radians(deg)
        xa = sx + math.cos(r)*(sun_radius+5); ya = sy + math.sin(r)*(sun_radius+5)
        xb = sx + math.cos(r)*(sun_radius+14); yb = sy + math.sin(r)*(sun_radius+14)
        canvas.create_line(xa, ya, xb, yb, fill="#fbbf24", width=2, tags=("sun",))

    canvas.create_text(sx, sy - 52, text=f"Sun  {sun_el:.1f}°",
                       fill="#fde047", font=("Segoe UI", 10, "bold"), tags=("sun",))

    base_width = 108 if mode == "Array" else 76
    mast_top_y = pivot_y + 11

    canvas.create_rectangle(pivot_x-base_width/2, ground_y-13,
                            pivot_x+base_width/2, ground_y,
                            fill="#475569", outline="#64748b", width=2)
    canvas.create_line(pivot_x, ground_y-13, pivot_x, mast_top_y,
                       fill="#64748b", width=10)
    bracket_y = pivot_y + 43
    canvas.create_polygon(pivot_x, pivot_y+5,
                          pivot_x-40, bracket_y,
                          pivot_x+40, bracket_y,
                          fill="#334155", outline="#64748b", width=2)
    canvas.create_oval(pivot_x-9, pivot_y-9, pivot_x+9, pivot_y+9,
                       fill="#e2e8f0", outline="#64748b", width=2)

    tr = math.radians(tilt)
    nx = -math.sin(tr); ny = -math.cos(tr)
    substrate_offset = 12
    sx_off = -nx * substrate_offset
    sy_off = -ny * substrate_offset

    canvas.create_line(x1+sx_off, y1+sy_off, x2+sx_off, y2+sy_off,
                       fill="#64748b", width=15, capstyle=tk.ROUND, tags=("hardware",))
    face_width = 12 if mode == "Array" else 10
    canvas.create_line(x1, y1, x2, y2, fill="#38bdf8", width=face_width,
                       capstyle=tk.ROUND, tags=("hardware",))
    canvas.create_line(x1, y1, x2, y2, fill="#fbbf24", width=2,
                       capstyle=tk.ROUND, tags=("hardware",))

    for frac in (-0.36, 0.0, 0.36):
        cx = pivot_x + ux*visual_length*frac
        cy = pivot_y + uy*visual_length*frac
        canvas.create_line(cx, cy, cx+sx_off, cy+sy_off,
                           fill="#94a3b8", width=2, tags=("hardware",))

    normal_len = min(145.0, h*0.24)
    normal_x = pivot_x + nx*normal_len
    normal_y = pivot_y + ny*normal_len
    canvas.create_line(pivot_x, pivot_y, normal_x, normal_y,
                       fill="#22d3ee", width=3, arrow=tk.LAST)
    canvas.create_text(normal_x, normal_y - 15, text="Surface normal",
                       fill="#22d3ee", font=("Segoe UI", 9, "bold"))

    card_x1 = 28
    card_y2 = ground_y - 26
    card_y1 = card_y2 - (78 if eff_hw["replacement"] else 60)
    card_x2 = min(w * 0.48, 430)

    canvas.create_rectangle(card_x1, card_y1, card_x2, card_y2,
                            fill="#0b1220", outline="#334155", width=1)
    canvas.create_text(card_x1 + 12, card_y1 + 15,
                       text=f"{mode} visual information",
                       anchor="w", fill="#fbbf24", font=("Segoe UI", 9, "bold"))
    canvas.create_text(card_x1 + 12, card_y1 + 35,
                       text=f"Reference area: {data['area_m2']:.3f} m²  •  visual size scales with selected hardware",
                       anchor="w", fill="#cbd5e1", font=("Segoe UI", 8))
    if eff_hw["replacement"]:
        canvas.create_text(card_x1 + 12, card_y1 + 55,
                           text=f"Replacement cell: {cell_name}",
                           anchor="w", fill="#cbd5e1", font=("Segoe UI", 8, "bold"))

    canvas.create_text(pivot_x, ground_y + 22,
                       text="Elevated support / substrate",
                       anchor="n", fill="#94a3b8", font=("Segoe UI", 8))

    _angle_draw_meta = {
        "sun_x": sx, "sun_y": sy, "sun_radius": sun_radius,
        "pivot_x": pivot_x, "pivot_y": pivot_y,
        "hardware_segment": (x1, y1, x2, y2),
        "canvas_w": w, "canvas_h": h,
    }


def _angles_refresh_all(canvas, data, mode, cell_name,
                        angle_tilt_var, angle_sun_el_var,
                        angle_life_var, angle_apply_var,
                        inc_var, angle_factor_v, loss_factor_v,
                        angle_output_v, final_output_v, one_hour_v, optimal_v,
                        tilt_num_var, sun_num_var, cell_info_v, status_v):
    if data is None:
        return

    cell = None if cell_name == ORIGINAL_CELL_TXT else SOLAR_CELLS.get(cell_name)
    eff_hw = _angles_effective_hardware(data, cell)

    tilt = float(angle_tilt_var.get())
    sun_el = float(angle_sun_el_var.get())

    incidence = abs((90.0 - tilt) - sun_el)
    angle_factor = max(0.0, math.cos(math.radians(incidence)))

    if angle_apply_var.get():
        loss_factor = TABLE_TOTAL_BOL if angle_life_var.get() == "BOL" else TABLE_TOTAL_EOL
        reduction = (1.0 - loss_factor) * 100.0
        loss_text = f"{loss_factor:.3f}  ({reduction:.1f}% reduction)"
    else:
        loss_factor = 1.0
        loss_text = "Disabled (factor = 1.000)"

    rated = eff_hw["rated_power_w"]
    angle_only_output = rated * angle_factor
    final_output = angle_only_output * loss_factor
    best_tilt = _angles_clamp(90.0 - sun_el, 0.0, 90.0)

    inc_var.set(f"{incidence:.2f}°")
    angle_factor_v.set(f"{angle_factor*100:.1f}%")
    loss_factor_v.set(loss_text)
    angle_output_v.set(_angles_fmt_power(angle_only_output))
    final_output_v.set(_angles_fmt_power(final_output))
    one_hour_v.set(_angles_fmt_energy(final_output))
    optimal_v.set(f"{best_tilt:.2f}°")
    tilt_num_var.set(f"{tilt:.1f}°")
    sun_num_var.set(f"{sun_el:.1f}°")

    if cell is None:
        cell_info_v.set(
            "Using original cell configuration.\n"
            "Pick a replacement cell in the main calculator to update these values."
        )
    else:
        cell_info_v.set(
            f"Replacement cell: {cell_name}\n"
            f"{cell['efficiency_pct']:.1f}% BOL   •   "
            f"{cell['power_density_w_m2']:.1f} W/m²"
        )

    if loss_factor < 1.0:
        status_v.set(
            f"{angle_life_var.get()} table factor applied after geometric angle loss."
        )
    else:
        status_v.set("Table loss disabled. Output shows geometric angle loss only.")

    _angles_draw(canvas, tilt, sun_el, incidence, angle_factor,
                 data, eff_hw, mode, cell_name)


def show_solar_panel_angles():
    if selected_data is None and not custom_mode:
        messagebox.showinfo(
            "Select Hardware First",
            "Pick a database panel or array in the main calculator before "
            "opening Solar Panel Angles."
        )
        return

    data = _angles_selected_hardware()
    if data is None:
        messagebox.showinfo(
            "Select Hardware First",
            "The angle view needs a database panel/array selected."
        )
        return

    win = tk.Toplevel(root)
    win.title("Solar Panel Angles")
    win.configure(bg="#0f172a")

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    win_w = min(1300, int(screen_w * 0.92))
    win_h = min(screen_h - 80, int(screen_h * 0.90))
    pos_x = max(0, (screen_w - win_w) // 2)
    pos_y = 20
    win.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    win.minsize(1000, 640)

    header = tk.Frame(win, bg="#0f172a")
    header.pack(fill="x", padx=14, pady=(10, 4))
    tk.Label(header, text="Solar Panel Angles",
             bg="#0f172a", fg="#fbbf24", font=("Segoe UI", 14, "bold")).pack(anchor="w")
    tk.Label(header,
             text=("Interactive angle + lunar BOL/EOL loss model. Drag the Sun or the "
                   "panel/array directly in the canvas. Same cell-replacement model as "
                   "the Power Calculator."),
             bg="#0f172a", fg="#cbd5e1", font=("Segoe UI", 9),
             wraplength=win_w - 40, justify="left").pack(anchor="w", pady=(2, 0))

    body = tk.Frame(win, bg="#0f172a")
    body.pack(fill="both", expand=True, padx=14, pady=(0, 12))
    body.columnconfigure(0, weight=1)
    body.columnconfigure(1, weight=0, minsize=320)
    body.rowconfigure(0, weight=1)

    canvas = tk.Canvas(body, bg="#111827",
                       highlightthickness=1, highlightbackground="#334155")
    canvas.grid(row=0, column=0, sticky="nsew")

    angle_tilt    = tk.DoubleVar(value=88.5)
    angle_sun_el  = tk.DoubleVar(value=1.5)
    angle_life    = tk.StringVar(value="BOL")
    angle_apply   = tk.BooleanVar(value=True)

    tilt_num_var = tk.StringVar(value="88.5°")
    sun_num_var  = tk.StringVar(value="1.5°")

    inc_var         = tk.StringVar(value="-")
    angle_factor_v  = tk.StringVar(value="-")
    loss_factor_v   = tk.StringVar(value="-")
    angle_output_v  = tk.StringVar(value="-")
    final_output_v  = tk.StringVar(value="-")
    one_hour_v      = tk.StringVar(value="-")
    optimal_v       = tk.StringVar(value="-")
    cell_info_v     = tk.StringVar(value="-")
    status_v        = tk.StringVar(value="-")

    side = tk.Frame(body, bg="#0f172a")
    side.grid(row=0, column=1, sticky="nsew", padx=(14, 0))

    ttk.Label(side, text="ANGLE CONTROLS", style="Section.TLabel").pack(anchor="w")

    ttk.Label(side, text="Panel / array tilt (0° horizontal, 90° vertical):").pack(
        anchor="w", pady=(6, 0))

    def slider_cb(_=None):
        _angles_refresh_all(canvas, data, mode_var.get(), cell_choice.get(),
                            angle_tilt, angle_sun_el, angle_life, angle_apply,
                            inc_var, angle_factor_v, loss_factor_v,
                            angle_output_v, final_output_v, one_hour_v, optimal_v,
                            tilt_num_var, sun_num_var, cell_info_v, status_v)

    ttk.Scale(side, from_=0, to=90, variable=angle_tilt, orient="horizontal",
              command=slider_cb, length=280).pack(anchor="w", pady=(0, 2))
    ttk.Label(side, textvariable=tilt_num_var, style="Result.TLabel").pack(anchor="w")

    ttk.Label(side, text="Solar elevation (0°–7°):").pack(anchor="w", pady=(10, 0))
    ttk.Scale(side, from_=0, to=7, variable=angle_sun_el, orient="horizontal",
              command=slider_cb, length=280).pack(anchor="w", pady=(0, 2))
    ttk.Label(side, textvariable=sun_num_var, style="Result.TLabel").pack(anchor="w")

    def _set_optimal():
        angle_tilt.set(_angles_clamp(90.0 - float(angle_sun_el.get()), 0.0, 90.0))
        slider_cb()

    ttk.Button(side, text="Set Optimal Tilt", command=_set_optimal).pack(
        fill="x", pady=(10, 6))

    ttk.Label(side, text="LUNAR LOSS MODEL", style="Section.TLabel").pack(
        anchor="w", pady=(8, 0))
    ttk.Checkbutton(side, text="Apply total reduction from table",
                    variable=angle_apply, command=slider_cb).pack(anchor="w", pady=(2, 2))
    ttk.Radiobutton(side, text="BOL (0.775)", variable=angle_life, value="BOL",
                    command=slider_cb).pack(anchor="w")
    ttk.Radiobutton(side, text="EOL (0.601)", variable=angle_life, value="EOL",
                    command=slider_cb).pack(anchor="w")

    res = tk.Frame(side, bg="#111827", bd=1, relief="solid", padx=10, pady=8)
    res.pack(fill="x", pady=(12, 0))

    tk.Label(res, text="LIVE RESULTS", bg="#111827", fg="#fbbf24",
             font=("Segoe UI", 8, "bold")).grid(row=0, column=0, columnspan=2,
                                                sticky="w", pady=(0, 4))

    live_rows = [
        ("Incidence",            inc_var),
        ("Angle factor",         angle_factor_v),
        ("Loss factor",          loss_factor_v),
        ("Angle-only output",    angle_output_v),
        ("Loss-adjusted output", final_output_v),
        ("Energy in 1 hour",     one_hour_v),
        ("Optimal tilt",         optimal_v),
    ]
    rr = 1
    for label, var in live_rows:
        tk.Label(res, text=label, bg="#111827", fg="#cbd5e1",
                 font=("Segoe UI", 9), anchor="w").grid(
            row=rr, column=0, sticky="w", padx=(4, 12), pady=2)
        tk.Label(res, textvariable=var, bg="#111827", fg="#fbbf24",
                 font=("Segoe UI", 9, "bold"), anchor="e").grid(
            row=rr, column=1, sticky="e", pady=2)
        rr += 1

    notes = tk.Frame(side, bg="#111827", bd=1, relief="solid", padx=10, pady=8)
    notes.pack(fill="x", pady=(10, 0))
    tk.Label(notes, text="MODEL NOTES", bg="#111827", fg="#fbbf24",
             font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 4))
    tk.Label(notes, textvariable=status_v, bg="#111827", fg="#cbd5e1",
             font=("Segoe UI", 8), wraplength=290, justify="left", anchor="w").grid(
        row=1, column=0, sticky="ew", pady=(0, 4))
    tk.Label(notes,
             text=("Total effective efficiency = published/selected efficiency × "
                   "cos(incidence) × BOL/EOL table factor. First-order estimate."),
             bg="#111827", fg="#94a3b8", font=("Segoe UI", 8),
             wraplength=290, justify="left", anchor="w").grid(row=2, column=0, sticky="ew")

    def on_press(event):
        global _angle_drag_target
        if not _angle_draw_meta:
            return
        sx = _angle_draw_meta["sun_x"]; sy = _angle_draw_meta["sun_y"]
        if math.hypot(event.x - sx, event.y - sy) <= _angle_draw_meta["sun_radius"] + 20:
            _angle_drag_target = "sun"
            canvas.config(cursor="hand2")
            return
        x1, y1, x2, y2 = _angle_draw_meta["hardware_segment"]
        if _angles_point_seg_distance(event.x, event.y, x1, y1, x2, y2) <= 26:
            _angle_drag_target = "hardware"
            canvas.config(cursor="fleur")
            return
        _angle_drag_target = None

    def on_drag(event):
        if not _angle_drag_target or not _angle_draw_meta:
            return
        px = _angle_draw_meta["pivot_x"]; py = _angle_draw_meta["pivot_y"]
        if _angle_drag_target == "sun":
            dx = max(px - float(event.x), 1.0)
            dy = py - float(event.y)
            elevation = math.degrees(math.atan2(dy, dx))
            angle_sun_el.set(_angles_clamp(elevation, 0.0, 7.0))
        elif _angle_drag_target == "hardware":
            dx = abs(float(event.x) - px)
            dy = py - float(event.y)
            if dx < 1e-6:
                tilt = 90.0 if dy >= 0 else 0.0
            else:
                tilt = math.degrees(math.atan2(max(dy, 0.0), dx))
            angle_tilt.set(_angles_clamp(tilt, 0.0, 90.0))
        slider_cb()

    def on_release(event):
        global _angle_drag_target
        _angle_drag_target = None
        canvas.config(cursor="")

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    canvas.bind("<Configure>", lambda e: slider_cb())

    win.after(60, slider_cb)


# =============================================================================
#  MAIN WINDOW
# =============================================================================

root = tk.Tk()
root.configure(bg="#0f172a")
root.resizable(True, True)

sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
ww = min(1280, max(1000, int(sw * 0.94)))
wh = min(820, max(700, int(sh * 0.92)))
root.geometry(f"{ww}x{wh}")
root.minsize(1000, 700)


# =============================================================================
#  STYLING
# =============================================================================

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 9))
style.configure("Header.TLabel", background="#0f172a", foreground="#fbbf24", font=("Segoe UI", 15, "bold"))
style.configure("Section.TLabel", background="#0f172a", foreground="#fbbf24", font=("Segoe UI", 9, "bold"))
style.configure("Hint.TLabel", background="#0f172a", foreground="#64748b", font=("Segoe UI", 8, "italic"))
style.configure("Info.TLabel", background="#111827", foreground="#cbd5e1", font=("Segoe UI", 8))
style.configure("Note.TLabel", background="#111827", foreground="#cbd5e1", font=("Segoe UI", 8))
style.configure("Density.TLabel", background="#0f172a", foreground="#fbbf24", font=("Segoe UI", 9, "bold"))
style.configure("TEntry", fieldbackground="#1e293b", foreground="#e2e8f0",
                insertcolor="#fbbf24", font=("Segoe UI", 9), padding=4)
style.configure("TCombobox", fieldbackground="#1e293b", background="#1e293b",
                foreground="#e2e8f0", font=("Segoe UI", 9), padding=4)
style.map("TCombobox",
          fieldbackground=[("readonly", "#1e293b"), ("disabled", "#111827")],
          foreground=[("readonly", "#e2e8f0"), ("disabled", "#64748b")])
style.configure("TRadiobutton", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 9))
style.map("TRadiobutton",
          background=[("active", "#0f172a")],
          foreground=[("active", "#fbbf24")])
style.configure("TButton", background="#fbbf24", foreground="#0f172a",
                font=("Segoe UI", 10, "bold"), padding=8)
style.map("TButton", background=[("active", "#f59e0b")])
style.configure("Result.TLabel", background="#0f172a", foreground="#fbbf24",
                font=("Segoe UI", 10, "bold"))


# =============================================================================
#  DYNAMIC TEXT VARIABLES
# =============================================================================

measurement_var = tk.StringVar(value="SI / Metric")
mode_var = tk.StringVar(value="Panel")

main_title_var = tk.StringVar()
item_label_var = tk.StringVar()
original_heading_var = tk.StringVar()
updated_heading_var = tk.StringVar()
step1_title_var = tk.StringVar()
rating_label_var = tk.StringVar()
step2_title_var = tk.StringVar()
step3_title_var = tk.StringVar()
length_label_var = tk.StringVar()
width_label_var = tk.StringVar()
area_label_var = tk.StringVar()
weight_label_var = tk.StringVar()
fixed_data_hint_var = tk.StringVar()

result_energy_label_var = tk.StringVar()
result_exact_label_var = tk.StringVar()
result_required_label_var = tk.StringVar()
result_total_area_label_var = tk.StringVar()
result_total_mass_label_var = tk.StringVar()
installed_explanation_var = tk.StringVar()
daily_explanation_var = tk.StringVar()

original_info_var = tk.StringVar(value="No hardware selected.")
cell_info_var = tk.StringVar(value="No custom cell selected.")
updated_info_var = tk.StringVar(value="No updated hardware values.")
assumptions_var = tk.StringVar()

manufacturer_var = tk.StringVar(value="Manufacturer  •  —")
selected_type_var = tk.StringVar(value="Type  •  —")
specific_power_var = tk.StringVar(value="Specific power  •  —")
efficiency_var = tk.StringVar(value="Efficiency  •  —")
areal_density_var = tk.StringVar(value="Areal density  •  —")

rated_power_kw_var = tk.StringVar(value="")
length_var = tk.StringVar(value="")
width_var = tk.StringVar(value="")
area_var = tk.StringVar(value="")
weight_var = tk.StringVar(value="")

result_energy = tk.StringVar(value="-")
result_exact_units = tk.StringVar(value="-")
result_required_units = tk.StringVar(value="-")
result_installed_power = tk.StringVar(value="-")
result_actual_energy = tk.StringVar(value="-")
result_total_area = tk.StringVar(value="-")
result_total_mass = tk.StringVar(value="-")


# =============================================================================
#  MAIN LAYOUT
# =============================================================================

main = tk.Frame(root, bg="#0f172a")
main.pack(fill="both", expand=True, padx=20, pady=10)
main.columnconfigure(0, weight=1)
main.columnconfigure(1, weight=1)

ttk.Label(main, textvariable=main_title_var, style="Header.TLabel").grid(
    row=0, column=0, columnspan=2, pady=(0, 1))
ttk.Label(main, text="Database-driven aerospace solar power sizing with optional theoretical cell replacement",
          style="TLabel").grid(row=1, column=0, columnspan=2, pady=(0, 8))


tc = tk.Frame(main, bg="#0f172a")
tc.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 8))
for c in range(3):
    tc.columnconfigure(c, weight=1)

mf = tk.Frame(tc, bg="#0f172a"); mf.grid(row=0, column=0, sticky="w")
ttk.Label(mf, text="MEASUREMENT SYSTEM", style="Section.TLabel").pack(anchor="w")
mo = tk.Frame(mf, bg="#0f172a"); mo.pack(anchor="w", pady=(1, 0))
ttk.Radiobutton(mo, text="SI / Metric", variable=measurement_var,
                value="SI / Metric", command=measurement_changed).pack(side="left", padx=(0, 14))
ttk.Radiobutton(mo, text="U.S. Customary", variable=measurement_var,
                value="U.S. Customary", command=measurement_changed).pack(side="left")

sf = tk.Frame(tc, bg="#0f172a"); sf.grid(row=0, column=1, sticky="w")
ttk.Label(sf, text="SYSTEM TYPE", style="Section.TLabel").pack(anchor="w")
so = tk.Frame(sf, bg="#0f172a"); so.pack(anchor="w", pady=(1, 0))
ttk.Radiobutton(so, text="Panel", variable=mode_var, value="Panel",
                command=mode_changed).pack(side="left", padx=(0, 14))
ttk.Radiobutton(so, text="Array", variable=mode_var, value="Array",
                command=mode_changed).pack(side="left")

cf = tk.Frame(tc, bg="#0f172a"); cf.grid(row=0, column=2, sticky="ew", padx=(10, 0))
ttk.Label(cf, text="CUSTOM CELL SELECTION", style="Section.TLabel").pack(anchor="w")
cell_choice = tk.StringVar(value=ORIGINAL_CELL)
cell_dropdown = ttk.Combobox(cf, textvariable=cell_choice,
                             values=[ORIGINAL_CELL] + list(SOLAR_CELLS.keys()),
                             state="disabled", width=32)
cell_dropdown.pack(fill="x", pady=(1, 0))
cell_dropdown.bind("<<ComboboxSelected>>", cell_selected)


sel = tk.Frame(main, bg="#0f172a")
sel.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(1, 6))
sel.columnconfigure(1, weight=1)
ttk.Label(sel, text="HARDWARE SELECTION", style="Section.TLabel").grid(
    row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))

item_choice = tk.StringVar()
ttk.Label(sel, textvariable=item_label_var).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=2)
item_dropdown = ttk.Combobox(sel, textvariable=item_choice, state="readonly")
item_dropdown.grid(row=1, column=1, sticky="ew", pady=2)
item_dropdown.bind("<<ComboboxSelected>>", item_selected)


info_row = tk.Frame(main, bg="#0f172a")
info_row.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(1, 6))
for c in range(3):
    info_row.columnconfigure(c, weight=1, uniform="info")

orig_box = tk.Frame(info_row, bg="#111827", bd=1, relief="solid")
orig_box.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
ttk.Label(orig_box, textvariable=original_heading_var, style="Section.TLabel").pack(
    anchor="w", padx=8, pady=(6, 2))
ttk.Label(orig_box, textvariable=original_info_var, style="Info.TLabel",
          justify="left", wraplength=380).pack(anchor="w", padx=8, pady=(0, 6))

cell_box = tk.Frame(info_row, bg="#111827", bd=1, relief="solid")
cell_box.grid(row=0, column=1, sticky="nsew", padx=5)
ttk.Label(cell_box, text="CUSTOM CELL INFORMATION", style="Section.TLabel").pack(
    anchor="w", padx=8, pady=(6, 2))
ttk.Label(cell_box, textvariable=cell_info_var, style="Info.TLabel",
          justify="left", wraplength=380).pack(anchor="w", padx=8, pady=(0, 6))

updated_box = tk.Frame(info_row, bg="#111827", bd=1, relief="solid")
updated_box.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
ttk.Label(updated_box, textvariable=updated_heading_var, style="Section.TLabel").pack(
    anchor="w", padx=8, pady=(6, 2))
ttk.Label(updated_box, textvariable=updated_info_var, style="Info.TLabel",
          justify="left", wraplength=380).pack(anchor="w", padx=8, pady=(0, 6))


note_box = tk.Frame(main, bg="#111827", bd=1, relief="solid")
note_box.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 8))
ttk.Label(note_box, text="THEORETICAL REPLACEMENT ASSUMPTIONS",
          style="Section.TLabel").pack(anchor="w", padx=8, pady=(5, 1))
ttk.Label(note_box, textvariable=assumptions_var, style="Note.TLabel",
          justify="left", wraplength=1200).pack(anchor="w", padx=8, pady=(0, 5))


left = tk.Frame(main, bg="#0f172a"); right = tk.Frame(main, bg="#0f172a")
left.grid(row=6, column=0, sticky="nsew", padx=(0, 14))
right.grid(row=6, column=1, sticky="nsew", padx=(14, 0))
main.rowconfigure(6, weight=1)
left.columnconfigure(0, weight=1); right.columnconfigure(0, weight=1)


ttk.Label(left, textvariable=step1_title_var, style="Section.TLabel").grid(
    row=0, column=0, sticky="w", pady=(2, 4))
f1 = tk.Frame(left, bg="#0f172a"); f1.grid(row=1, column=0, sticky="ew")
f1.columnconfigure(1, weight=1)

ttk.Label(f1, textvariable=rating_label_var).grid(row=0, column=0, sticky="w", pady=4)
rating_entry = ttk.Entry(f1, width=18, textvariable=rated_power_kw_var, state="readonly")
rating_entry.grid(row=0, column=1, sticky="w", pady=4)
ttk.Label(f1, text="uses updated rating when a replacement cell is selected",
          style="Hint.TLabel").grid(row=1, column=1, sticky="w", pady=(0, 6))

ttk.Label(f1, text="Peak Sun Hours/day").grid(row=2, column=0, sticky="w", pady=4)
psh_v = (root.register(valid_psh), "%P")
entry_psh = ttk.Entry(f1, width=18, validate="key", validatecommand=psh_v)
entry_psh.grid(row=2, column=1, sticky="w", pady=4)
ttk.Label(f1, text="range 0 – 24", style="Hint.TLabel").grid(
    row=2, column=2, sticky="w", padx=(10, 0), pady=4)
ttk.Label(f1, text="hours of useful sunlight received", style="Hint.TLabel").grid(
    row=3, column=1, sticky="w", pady=(0, 6))

ttk.Label(f1, text="Derate factor").grid(row=4, column=0, sticky="w", pady=4)
entry_derate = ttk.Entry(f1, width=18)
entry_derate.grid(row=4, column=1, sticky="w", pady=4)
entry_derate.insert(0, "0.7")
ttk.Label(f1, text="fraction retained  ·  example: 0.70", style="Hint.TLabel").grid(
    row=5, column=1, sticky="w", pady=(0, 6))

ttk.Label(left, textvariable=step2_title_var, style="Section.TLabel").grid(
    row=2, column=0, sticky="w", pady=(14, 4))
f2 = tk.Frame(left, bg="#0f172a"); f2.grid(row=3, column=0, sticky="ew")
f2.columnconfigure(1, weight=1)
ttk.Label(f2, text="Daily target (kWh/day)").grid(row=0, column=0, sticky="w", pady=4)
entry_target = ttk.Entry(f2, width=18)
entry_target.grid(row=0, column=1, sticky="w", pady=4)

ttk.Button(left, text="Calculate", command=calculate).grid(
    row=4, column=0, sticky="ew", pady=(18, 0))
ttk.Button(left, text="Show Power Graphs", command=show_power_graphs).grid(
    row=5, column=0, sticky="ew", pady=(10, 0))
ttk.Button(left, text="Show Solar Panel Angles", command=show_solar_panel_angles).grid(
    row=6, column=0, sticky="ew", pady=(10, 0))


hdr3 = tk.Frame(right, bg="#0f172a"); hdr3.grid(row=0, column=0, sticky="ew", pady=(2, 4))
hdr3.columnconfigure(0, weight=1)
ttk.Label(hdr3, textvariable=step3_title_var, style="Section.TLabel").grid(row=0, column=0, sticky="w")
ttk.Label(hdr3, textvariable=areal_density_var, style="Density.TLabel").grid(
    row=0, column=1, sticky="e", padx=(10, 0))

f3 = tk.Frame(right, bg="#0f172a"); f3.grid(row=1, column=0, sticky="ew")
f3.columnconfigure(1, weight=1)

ttk.Label(f3, textvariable=length_label_var).grid(row=0, column=0, sticky="w", pady=3)
length_entry = ttk.Entry(f3, width=18, textvariable=length_var, state="readonly")
length_entry.grid(row=0, column=1, sticky="w", pady=3)

ttk.Label(f3, textvariable=width_label_var).grid(row=1, column=0, sticky="w", pady=3)
width_entry = ttk.Entry(f3, width=18, textvariable=width_var, state="readonly")
width_entry.grid(row=1, column=1, sticky="w", pady=3)

ttk.Label(f3, textvariable=area_label_var).grid(row=2, column=0, sticky="w", pady=3)
area_entry = ttk.Entry(f3, width=18, textvariable=area_var, state="readonly")
area_entry.grid(row=2, column=1, sticky="w", pady=3)

ttk.Label(f3, textvariable=weight_label_var).grid(row=3, column=0, sticky="w", pady=3)
weight_entry = ttk.Entry(f3, width=18, textvariable=weight_var, state="readonly")
weight_entry.grid(row=3, column=1, sticky="w", pady=3)

ttk.Label(f3, textvariable=fixed_data_hint_var, style="Hint.TLabel").grid(
    row=4, column=0, columnspan=2, sticky="w", pady=(6, 0))


results_card = tk.Frame(right, bg="#1e293b",
                        highlightbackground="#334155", highlightthickness=1)
results_card.grid(row=2, column=0, sticky="ew", pady=(18, 8))
results_card.columnconfigure(0, weight=1)

ttk.Label(results_card, text="RESULTS", style="Section.TLabel").grid(
    row=0, column=0, columnspan=2, sticky="w", padx=18, pady=(12, 8))

result_rows = [
    (result_energy_label_var,        result_energy,          "#38bdf8"),
    (result_exact_label_var,         result_exact_units,     "#e2e8f0"),
    (result_required_label_var,      result_required_units,  "#e2e8f0"),
    (tk.StringVar(value="Installed power"),      result_installed_power, "#38bdf8"),
    (tk.StringVar(value="Actual daily energy"),  result_actual_energy,   "#38bdf8"),
    (result_total_area_label_var,    result_total_area,      "#fbbf24"),
    (result_total_mass_label_var,    result_total_mass,      "#fbbf24"),
]

for i, (lbl, val, color) in enumerate(result_rows, start=1):
    ttk.Label(results_card, textvariable=lbl, style="TLabel").grid(
        row=i, column=0, sticky="w", padx=(18, 8), pady=3)
    tk.Label(results_card, textvariable=val, bg="#1e293b", fg=color,
             font=("Segoe UI", 11, "bold"), anchor="e").grid(
        row=i, column=1, sticky="e", padx=(8, 18), pady=3)

sep = tk.Frame(results_card, bg="#334155", height=1)
sep.grid(row=len(result_rows) + 1, column=0, columnspan=2, sticky="ew", padx=18, pady=(8, 6))

ttk.Label(results_card, textvariable=installed_explanation_var, style="Hint.TLabel",
          wraplength=560, justify="left").grid(
    row=len(result_rows) + 2, column=0, columnspan=2, sticky="w", padx=18, pady=(0, 3))
ttk.Label(results_card, textvariable=daily_explanation_var, style="Hint.TLabel",
          wraplength=560, justify="left").grid(
    row=len(result_rows) + 3, column=0, columnspan=2, sticky="w", padx=18, pady=(0, 3))
ttk.Label(results_card,
          text="Cell replacement is theoretical; updated power and mass use the selected cell plus the assumptions above.",
          style="Hint.TLabel", wraplength=560, justify="left").grid(
    row=len(result_rows) + 4, column=0, columnspan=2, sticky="w", padx=18, pady=(0, 12))


# =============================================================================
#  INITIALIZE + LAUNCH
# =============================================================================

update_wording()
item_dropdown["values"] = [BLANK, CUSTOM] + list(SOLAR_PANELS.keys())
item_choice.set(BLANK)
cell_dropdown["values"] = [ORIGINAL_CELL] + list(SOLAR_CELLS.keys())
cell_choice.set(ORIGINAL_CELL)
set_readonly(True)
clear_selection_display(blank_values=True)

root.mainloop()
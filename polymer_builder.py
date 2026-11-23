"""MATEX's drag-and-drop polymer construction challenges.

The browser component handles dragging monomer cards. Python validates the
assembled monomer sequence and returns the learning feedback.
"""

from pathlib import Path

import streamlit.components.v1 as components


CHALLENGES = {
    "Polyethylene (PE)": {
        "brief": "Build a short polyethylene chain from ethylene molecules.",
        "method": "Addition polymerisation",
        "expected": ["ethylene", "ethylene", "ethylene"],
        "repeat_pattern": ["ethylene"],
        "hint": "Polyethylene is made from one kind of alkene monomer. Look for the molecule with a carbon-carbon double bond and repeat it three times.",
        "success": "Great work! Three ethylene monomers make the simplified polyethylene chain. Their C=C double bonds open and the units link together into a carbon backbone.",
        "learning": "The repeating unit of polyethylene is –[CH₂–CH₂]–. This is an addition polymerisation example: the double bond opens as the monomers join.",
        "palette": [
            {"id": "ethylene", "name": "Ethylene", "formula": "CH₂=CH₂", "role": "Alkene monomer", "color": "#55c3ac"},
        ],
    },
    "PVC": {
        "brief": "Build a short PVC chain from vinyl chloride molecules.",
        "method": "Addition polymerisation",
        "expected": ["vinyl_chloride", "vinyl_chloride", "vinyl_chloride"],
        "repeat_pattern": ["vinyl_chloride"],
        "hint": "PVC comes from a single alkene monomer that contains chlorine. Repeat the vinyl chloride molecule.",
        "success": "Correct! You repeated vinyl chloride to build the simplified PVC chain. The C=C double bond opens and the monomers join along the backbone.",
        "learning": "The repeating unit is –[CH₂–CHCl]–. The chlorine atom remains attached to the polymer backbone's carbon chain.",
        "palette": [
            {"id": "vinyl_chloride", "name": "Vinyl chloride", "formula": "CH₂=CHCl", "role": "Chlorinated alkene", "color": "#d6a85e"},
        ],
    },
    "PTFE": {
        "brief": "Build a short PTFE chain from tetrafluoroethylene molecules.",
        "method": "Addition polymerisation",
        "expected": ["tetrafluoroethylene", "tetrafluoroethylene", "tetrafluoroethylene"],
        "repeat_pattern": ["tetrafluoroethylene"],
        "hint": "PTFE is made by repeating the fluorine-rich alkene monomer. Look for CF₂=CF₂.",
        "success": "Nicely done! Three tetrafluoroethylene monomers form the simplified PTFE chain as their double bonds open and connect.",
        "learning": "The repeating unit is –[CF₂–CF₂]–. Strong carbon-fluorine bonds contribute to PTFE's chemical and thermal stability.",
        "palette": [
            {"id": "tetrafluoroethylene", "name": "Tetrafluoroethylene", "formula": "CF₂=CF₂", "role": "Fluorinated alkene", "color": "#73a8d5"},
        ],
    },
    "Polylactic Acid (PLA)": {
        "brief": "Build a short PLA chain using lactic acid building blocks.",
        "method": "Polyester formation · condensation model",
        "expected": ["lactic_acid", "lactic_acid", "lactic_acid"],
        "repeat_pattern": ["lactic_acid"],
        "hint": "PLA is a polyester. For this simplified exercise, repeat lactic acid units so ester links can form between them.",
        "success": "That's right! You arranged lactic acid units into a simplified PLA chain. Ester linkages connect the repeating units.",
        "learning": "PLA's repeating unit is –[O–CH(CH₃)–CO]–. PLA can be produced by direct condensation of lactic acid or by ring-opening polymerisation of lactide; this puzzle illustrates the lactic-acid building blocks.",
        "palette": [
            {"id": "lactic_acid", "name": "Lactic acid", "formula": "CH₃–CH(OH)–COOH", "role": "Hydroxy-acid monomer", "color": "#8fbd77"},
        ],
    },
    "PET": {
        "brief": "Build a PET chain by alternating ethylene glycol and terephthalic acid.",
        "method": "Condensation polymerisation",
        "expected": ["ethylene_glycol", "terephthalic_acid", "ethylene_glycol", "terephthalic_acid"],
        "repeat_pattern": ["ethylene_glycol", "terephthalic_acid"],
        "hint": "PET is made from two different monomers. Start with the diol (ethylene glycol), then alternate it with the diacid (terephthalic acid).",
        "success": "Excellent! You alternated ethylene glycol and terephthalic acid to make the simplified PET chain. Ester links form as small water molecules are removed.",
        "learning": "PET contains ester linkages in its backbone. In this simplified condensation model, the diol and diacid alternate along the chain.",
        "palette": [
            {"id": "ethylene_glycol", "name": "Ethylene glycol", "formula": "HO–CH₂–CH₂–OH", "role": "Diol", "color": "#5eb8a6"},
            {"id": "terephthalic_acid", "name": "Terephthalic acid", "formula": "HOOC–C₆H₄–COOH", "role": "Dicarboxylic acid", "color": "#b28bd7"},
        ],
    },
    "Nylon 6,6": {
        "brief": "Build a Nylon 6,6 chain by alternating a diamine and a diacid.",
        "method": "Condensation polymerisation",
        "expected": ["hexamethylenediamine", "adipic_acid", "hexamethylenediamine", "adipic_acid"],
        "repeat_pattern": ["hexamethylenediamine", "adipic_acid"],
        "hint": "Nylon 6,6 uses two monomers: hexamethylenediamine has two –NH₂ ends, while adipic acid has two –COOH ends. Alternate them.",
        "success": "Correct sequence! Hexamethylenediamine and adipic acid alternate to form Nylon 6,6. Amide links form as water is removed.",
        "learning": "Nylon 6,6 is a polyamide. Its –CO–NH– amide links connect the two alternating monomer residues.",
        "palette": [
            {"id": "hexamethylenediamine", "name": "Hexamethylenediamine", "formula": "H₂N–(CH₂)₆–NH₂", "role": "Diamine", "color": "#62a8ce"},
            {"id": "adipic_acid", "name": "Adipic acid", "formula": "HOOC–(CH₂)₄–COOH", "role": "Dicarboxylic acid", "color": "#e4a76c"},
        ],
    },
    "Kevlar": {
        "brief": "Build a Kevlar chain by alternating p-phenylenediamine and terephthaloyl chloride.",
        "method": "Condensation polymerisation",
        "expected": ["p_phenylenediamine", "terephthaloyl_chloride", "p_phenylenediamine", "terephthaloyl_chloride"],
        "repeat_pattern": ["p_phenylenediamine", "terephthaloyl_chloride"],
        "hint": "Kevlar is an aromatic polyamide. Alternate the diamine (p-phenylenediamine) with the acid chloride (terephthaloyl chloride).",
        "success": "Well done! You alternated the two aromatic monomers used to form Kevlar. Amide links form and hydrogen chloride (HCl) is released as a by-product.",
        "learning": "Kevlar's aromatic polyamide chains are rigid and form strong inter-chain hydrogen bonds. The condensation reaction between these monomers releases HCl.",
        "palette": [
            {"id": "p_phenylenediamine", "name": "p-Phenylenediamine", "formula": "H₂N–C₆H₄–NH₂", "role": "Aromatic diamine", "color": "#d5a85e"},
            {"id": "terephthaloyl_chloride", "name": "Terephthaloyl chloride", "formula": "ClCO–C₆H₄–COCl", "role": "Aromatic acid chloride", "color": "#ae8cce"},
        ],
    },
    "Polyaniline (PANI)": {
        "brief": "Build a simplified polyaniline chain from aniline building blocks.",
        "method": "Oxidative polymerisation",
        "expected": ["aniline", "aniline", "aniline"],
        "repeat_pattern": ["aniline"],
        "hint": "For this introductory model, repeat aniline units. Real polyaniline has more complex oxidation states and doping forms.",
        "success": "Good job! You repeated aniline building blocks to create a simplified polyaniline chain. Oxidative polymerisation links the units.",
        "learning": "Polyaniline's structure and conductivity depend on its oxidation state and doping. This chain is a simplified learning model, not a full representation of every PANI form.",
        "palette": [
            {"id": "aniline", "name": "Aniline", "formula": "C₆H₅–NH₂", "role": "Aromatic amine monomer", "color": "#54b69a"},
        ],
    },
}


def make_challenge(polymer_name, repeat_units):
    """Return a challenge configured for the learner's chosen chain length.

    A homopolymer uses one monomer tile per repeat unit. The simplified PET,
    Nylon 6,6 and Kevlar exercises use two alternating monomer tiles per
    repeat unit.
    """
    try:
        count = int(repeat_units)
    except (TypeError, ValueError):
        count = 3
    count = max(2, min(2000, count))

    base = CHALLENGES[polymer_name]
    challenge = dict(base)
    pattern = list(base.get("repeat_pattern", []))
    if not pattern:
        pattern = list(base["expected"][:1])

    expected = pattern * count
    challenge["expected"] = expected
    challenge["repeat_units"] = count
    challenge["target_label"] = "Goal: {} repeat units · {} monomer tiles".format(count, len(expected))
    challenge["brief"] = "{} MATEX target: {} repeat units ({} draggable monomer tiles).".format(
        base["brief"], count, len(expected)
    )
    return challenge


def validate_build(polymer_name, sequence, challenge=None):
    """Check a dropped monomer sequence and return simple learner feedback."""
    challenge = challenge or CHALLENGES[polymer_name]
    expected = challenge["expected"]
    palette_names = {item["id"]: item["name"] for item in challenge["palette"]}
    # Only accept known string identifiers from the browser component.
    actual = [item for item in list(sequence or []) if isinstance(item, str)]

    if not actual:
        return {
            "correct": False,
            "title": "Your chain is empty",
            "message": "Drag at least one monomer molecule into the build area, then check again.",
        }

    for index, (actual_id, expected_id) in enumerate(zip(actual, expected)):
        if actual_id != expected_id:
            actual_name = palette_names.get(actual_id, "That molecule")
            expected_name = palette_names[expected_id]
            return {
                "correct": False,
                "title": "Almost there — check the order",
                "message": "Position {} has {}. MATEX expects {} here. Remove or move the tile, then try again.".format(
                    index + 1, actual_name, expected_name
                ),
            }

    if len(actual) < len(expected):
        return {
            "correct": False,
            "title": "Good start — your chain needs more units",
            "message": "You have {} of {} building blocks. Add {} more monomer tile(s) to complete this challenge.".format(
                len(actual), len(expected), len(expected) - len(actual)
            ),
        }

    if len(actual) > len(expected):
        return {
            "correct": False,
            "title": "Your chain has extra units",
            "message": "This challenge needs {} building blocks, but your chain has {}. Remove the extra tile(s) and check again.".format(
                len(expected), len(actual)
            ),
        }

    return {
        "correct": True,
        "title": "You built it correctly!",
        "message": challenge["success"],
        "learning": challenge["learning"],
    }


_COMPONENT_DIR = Path(__file__).parent / "polymer_builder_component"
_builder_component = None


def polymer_builder_component(polymer_name, challenge, initial_sequence=None, key=None):
    """Render the drag-and-drop monomer workspace and return user actions."""
    global _builder_component
    if _builder_component is None:
        _builder_component = components.declare_component(
            "polyverse_matex_polymer_builder",
            path=str(_COMPONENT_DIR),
        )
    return _builder_component(
        polymer_name=polymer_name,
        brief=challenge["brief"],
        method=challenge["method"],
        palette=challenge["palette"],
        target_units=len(challenge["expected"]),
        target_label=challenge.get("target_label", "Goal: {} monomer tiles".format(len(challenge["expected"]))),
        max_units=len(challenge["expected"]) + 2,
        initial_sequence=list(initial_sequence or []),
        key=key,
        default=None,
    )

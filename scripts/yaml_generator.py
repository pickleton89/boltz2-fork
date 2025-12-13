from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

# Mapping user tokens (e.g. from oligo orders) to Boltz-2 PDB CCD codes
# These codes tell the model exactly which 3D chemical structure to use for that base.
TOKEN_TO_CCD = {
    # 2'-O-methyl (Common in RNA therapeutics)
    'mG': 'OMG', 
    'mA': 'A2M', 
    'mC': 'OMC', 
    'mU': 'OMU',
    
    # 2'-Fluoro (Common for stability)
    'fU': 'UFR', 
    'fC': 'CFL', 
    'fA': '2FA', 
    'fG': 'GF2',
    
    # Other common modifications can be added here
    "(vU)": "UNK",  # Placeholder if specific CCD is unknown
}

# Valid characters for sequence validation
VALID_RNA_BASES = set("ACGUT")
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

# Display settings
PREVIEW_LENGTH = 15


def validate_protein_sequence(seq: str) -> tuple[bool, str | None]:
    """Validate protein sequence contains only valid amino acids."""
    invalid = set(seq.upper()) - VALID_AMINO_ACIDS
    if invalid:
        return False, f"Invalid amino acids: {', '.join(sorted(invalid))}"
    return True, None


def validate_rna_sequence(seq: str) -> tuple[bool, str | None]:
    """Validate RNA sequence contains only valid bases."""
    invalid = set(seq.upper()) - VALID_RNA_BASES
    if invalid:
        return False, f"Invalid bases: {', '.join(sorted(invalid))}"
    return True, None


def parse_complex_rna_for_structure(sequence_str: str) -> tuple[str, list[dict]]:
    """
    Parses an RNA string with modification tags.
    Returns:
      1. The standard sequence string (e.g., "ACGU") required for the backbone.
      2. A list of modifications with 1-based positions and CCD codes.
    """
    # Regex finds tokens: r/d/f/m + Letter, or specific tags like (vU)
    token_pattern = re.compile(r'([rdfm][ACGUT])|(\(vU\))')
    matches = token_pattern.findall(sequence_str)
    
    plain_seq = []
    modifications = []
    
    for i, match in enumerate(matches):
        # Boltz uses 1-based indexing for modifications
        position = i + 1 
        token = ''.join(match)
        
        # 1. Determine Standard Backbone Base
        if token == '(vU)':
            base = 'U'
        else:
            # Extract the letter (last char)
            base = token[-1].upper()
            # Map DNA 'T' to RNA 'U' for the backbone sequence
            if base == 'T': 
                base = 'U'
        
        plain_seq.append(base)
        
        # 2. Map to CCD Code for 3D Structure
        if token in TOKEN_TO_CCD:
            modifications.append({
                'position': position,
                'ccd': TOKEN_TO_CCD[token]
            })
        elif token.startswith('f') or token.startswith('m'):
            print(f"Warning: Modification '{token}' not found in library. Using standard '{base}' structure.")
            
    return "".join(plain_seq), modifications

def get_user_input() -> dict:
    """Collect user input for protein and/or RNA sequences.

    Returns a dict with keys: protein, rna, mods, mode
    """
    print("==================================================")
    print("   Boltz-2 Structure Prediction Input Generator   ")
    print("==================================================")
    print("   Supports: Protein only, RNA only, or Protein+RNA")
    print("   (Press Enter to skip a sequence)\n")

    result = {"protein": None, "rna": None, "mods": [], "mode": None}

    # 1. Protein Input (optional)
    print("[1] Protein Sequence (press Enter to skip):")
    prot_raw = input("    > ").strip()

    if prot_raw:
        valid, error = validate_protein_sequence(prot_raw)
        if not valid:
            print(f"Error: {error}")
            sys.exit(1)
        result["protein"] = prot_raw
        print("    -> Protein sequence accepted.")

    # 2. RNA Input (optional)
    print("\n[2] RNA Sequence (press Enter to skip):")
    print("    Formats: plain (ACGU) or modified (rGrGfUmC...)")
    rna_raw = input("    > ").strip()

    if rna_raw:
        # Check if it looks like annotated format (has prefix pattern like rA, fU, mG)
        if re.search(r"[rdfm][ACGUT]|\(vU\)", rna_raw):
            print("\n    -> Detected modified sequence format.")
            rna_seq, mods = parse_complex_rna_for_structure(rna_raw)
            preview = rna_seq[:PREVIEW_LENGTH]
            if len(rna_seq) > PREVIEW_LENGTH:
                preview += "..."
            print(f"    -> Parsed Backbone: {preview}")
            if mods:
                first_mod = mods[0]
                print(f"    -> Modifications: {len(mods)} found "
                      f"(e.g. {first_mod['ccd']} at pos {first_mod['position']})")
            else:
                print("    -> Modifications: None found")
            result["mods"] = mods
        else:
            print("\n    -> Detected plain sequence.")
            rna_seq = rna_raw.replace("T", "U").upper()

            valid, error = validate_rna_sequence(rna_seq)
            if not valid:
                print(f"Error: {error}")
                sys.exit(1)

        result["rna"] = rna_seq

    # Validate at least one sequence provided
    if not result["protein"] and not result["rna"]:
        print("\nError: At least one sequence (protein or RNA) is required.")
        sys.exit(1)

    # Determine mode
    if result["protein"] and result["rna"]:
        result["mode"] = "protein_rna"
    elif result["protein"]:
        result["mode"] = "protein"
    else:
        result["mode"] = "rna"

    return result

def build_yaml_data(user_input: dict) -> tuple[dict, str]:
    """Build YAML data structure based on user input.

    Returns tuple of (yaml_data, filename).
    """
    mode = user_input["mode"]
    sequences = []
    chain_id = "A"  # First entity always gets "A"

    # Add protein if provided
    if user_input["protein"]:
        sequences.append({
            "protein": {
                "id": chain_id,
                "sequence": user_input["protein"],
            }
        })
        chain_id = "B"  # Next entity gets "B"

    # Add RNA if provided
    if user_input["rna"]:
        rna_entry = {
            "rna": {
                "id": chain_id,
                "sequence": user_input["rna"],
            }
        }
        # Inject modifications if they exist
        if user_input["mods"]:
            rna_entry["rna"]["modifications"] = user_input["mods"]
        sequences.append(rna_entry)

    data = {"version": 1, "sequences": sequences}

    # Determine filename based on mode
    filenames = {
        "protein": "boltz_protein_structure.yaml",
        "rna": "boltz_rna_structure.yaml",
        "protein_rna": "boltz_protein_rna_structure.yaml",
    }
    filename = filenames[mode]

    return data, filename


def print_success_message(filename: str, mode: str) -> None:
    """Print success message with appropriate instructions."""
    print("\n==================================================")
    print(f" SUCCESS! Input file created: {filename}")
    print("==================================================")
    print("To predict the 3D structure, run:")
    print(f"\n    boltz predict {filename} --use_msa_server")

    # Mode-specific tips
    if mode == "protein_rna":
        print("\nTip: Check 'iptm' score to judge binding confidence.")
    elif mode == "protein":
        print("\nTip: Check 'ptm' and 'plddt' scores for structure quality.")
    else:  # rna
        print("\nTip: Check 'plddt' scores for per-residue confidence.")


def main() -> None:
    """Run the YAML generator."""
    user_input = get_user_input()
    data, filename = build_yaml_data(user_input)

    # Save File
    with Path(filename).open("w") as f:
        yaml.dump(data, f, sort_keys=False, default_flow_style=False)

    print_success_message(filename, user_input["mode"])

if __name__ == "__main__":
    main()
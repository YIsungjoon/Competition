# Pre-Submission Check List

This check list verifies required evidence for **source attribution**, **license compliance**, **purchase proofs**, and **AI generation records** using only the provided project files. All entries include explicit file paths as evidence. No legal conclusions are made.

---

## 1. AI Generation Records

### Amber bottle (generated/g_amber.png)
- **Prompt record**: `evidence/prompt/amber_prompt.txt` (present)  
- **Model terms**: `evidence/model_terms/amber_terms.txt` (present)  
- **Generated file**: `generated/g_amber.png` (present)  
- **Status**: Complete

### Ocean background (generated/g_ocean.png)
- **Prompt record**: `evidence/prompt/ocean_prompt.txt` (present)  
- **Model terms**: `evidence/model_terms/ocean_terms.txt` (present)  
- **Generated file**: `generated/g_ocean.png` (present)  
- **Status**: Complete

> ✅ **Connection justification**: Both assets have matching prompt records, model terms, and generated files in the `generated/` directory. The `lineage/landing_bundle.md` explicitly lists these as ingredients.

---

## 2. Licenses

### Rounded typeface (media/font_z.woff)
- **License**: `evidence/license/rounded_type_license.txt` (Open font license)  
- **Status**: Licensed (open source)  
- **Verification**: Confirmed by `evidence/license/rounded_type_license.txt`

### Custom CSS (src/landing.css)
- **License**: Not applicable (team-created)  
- **Status**: Team-owned (no license required)  
- **Verification**: Confirmed by `evidence/css_authorship.txt`

> ✅ **Connection justification**: The font license and CSS authorship are explicitly documented in separate evidence files. No external licenses are required for these assets.

---

## 3. Purchase Proofs

- **All assets**: No purchase proofs required  
  - *Reason*:  
    - Amber bottle and ocean background are AI-generated (no purchase needed)  
    - Rounded typeface has open source license (no purchase needed)  
    - Custom CSS is team-created (no purchase needed)  
- **Status**: None required

> ✅ **Connection justification**: The `evidence/model_terms/amber_terms.txt` and `evidence/model_terms/ocean_terms.txt` confirm AI model usage (not purchased), and `evidence/license/rounded_type_license.txt` confirms open source status.

---

## 4. Source Provenance

### Abandoned draft source
- **Source**: `evidence/source/unrelated_drone_source.txt` (mountain drone footage)  
- **Status**: Excluded from current project  
- **Verification**: Confirmed by `notes/provenance_notes.md` ("One source record belongs to an abandoned draft and must not be auto-attached")  
- **Status**: Not included in deliverables

### Current project assets
| Asset                  | Source File Path                     | Status                     |
|------------------------|--------------------------------------|----------------------------|
| Amber bottle           | `generated/g_amber.png`              | AI-generated (no source)   |
| Ocean background       | `generated/g_ocean.png`              | AI-generated (no source)   |
| Rounded typeface       | `media/font_z.woff`                 | Open source (licensed)     |
| Custom CSS             | `src/landing.css`                   | Team-created (no source)   |

> ✅ **Connection justification**: The `lineage/landing_bundle.md` explicitly lists the ingredients, and `notes/provenance_notes.md` confirms the abandoned drone footage is excluded.

---

## 5. Critical Missing Evidence (If Any)

| Asset                  | Missing Evidence? | Reason for concern | Verification Status |
|------------------------|--------------------|---------------------|---------------------|
| Amber bottle           | ❌ No               | None                | Complete            |
| Ocean background       | ❌ No               | None                | Complete            |
| Rounded typeface       | ❌ No               | None                | Complete            |
| Custom CSS             | ❌ No               | None                | Complete            |

> ✅ **Conclusion**: **No missing evidence** found for current project assets. All required records are present and properly linked.

---

## Final Verification Summary

| Category               | Status       | Evidence Path(s)                                  |
|------------------------|---------------|---------------------------------------------------|
| AI Generation Records  | Complete      | `evidence/prompt/amber_prompt.txt`, `evidence/model_terms/amber_terms.txt`, `generated/g_amber.png` |
| Licenses                | Complete      | `evidence/license/rounded_type_license.txt`        |
| Purchase Proofs        | Not required  | N/A                                                |
| Source Provenance      | Complete      | `notes/provenance_notes.md`, `lineage/landing_bundle.md` |

**Recommendation**: Submit project with confidence. All evidence is present and properly documented. No items require further verification.

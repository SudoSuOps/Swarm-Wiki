# DG Ownership Graph — Florida First

**Status**: BLUEPRINT — ready to build
**Target**: Every Dollar General in Florida with true owner, entity, and contact

## Three Layers

Not one API. Three layers stitched together.

```
LAYER 1: PARCEL / TAX ROLL
  Who owns the real estate?
  → parcel ID, owner name, owner mailing address
  → Source: Florida Department of Revenue property tax data

LAYER 2: ENTITY
  What LLC / LP / trust is that owner?
  → entity name, jurisdiction, registered agent, officers
  → Source: Florida Sunbiz + OpenCorporates (multi-state)

LAYER 3: CONTACT
  Who do you actually call?
  → mailing address, registered agent, officers, manager names
  → Source: tax roll mailing + Sunbiz officers + SEC EDGAR (public parents)
```

## Step A — Build the Dollar General Site List

Start with all Florida DG locations. Geocode each site. Spatially match to a parcel. Enrich with owner data.

```
SOURCES:
  DG store locator (public)     → address, lat/lng per store
  Geocode → parcel match        → parcel ID, property boundaries
  Parcel API (Regrid or ATTOM)  → owner name, owner mailing address

REGRID:
  Parcel API exposes: owner-name search + mailing-address fields
  Schema includes full ownership data per parcel
  
ATTOM:
  Owner-name and tax-mailing-address coverage
  Part of their standard ownership data product
  
FLORIDA DOR:
  2024 assessment roll / GIS data published statewide
  Public files include: OWN_ADDR, OWN_CITY, OWN_STATE, ZIP
  Excludes confidential records
  This is the FREE starting point
```

## Step B — Resolve the Owner Entity

STNL owners are typically LLCs: `DG FL 2021-1 LLC`, a DST, or a local holding company.

```
FLORIDA SUNBIZ (sunbiz.org):
  Search by: entity name, officer/registered agent, FEI/EIN, zip, street address
  Returns: registered agent, officer names, entity status, filing history
  
  Owner from tax roll: "DG Southeast Holdings LLC"
  → Sunbiz search → registered agent: "CT Corporation System"
  → Officers: John Smith (Manager), Jane Doe (Member)
  → Filed: 2019, Status: Active
```

## Step C — Multi-State Entity Resolution

Most STNL holders are Delaware or out-of-state entities. Florida-only lookup is not enough.

```
OPENCORPORATES:
  Covers company records from many registries
  Normalized entity layer: holding-company names, jurisdiction, status, officers/filings
  
  "DG Southeast Holdings LLC" (FL) 
  → parent: "NNN REIT Operating Partnership LP" (DE)
  → parent: "Spirit Realty Capital Inc" (NYSE: SRC)
  → now you know who really owns 47 DGs in Florida
```

## Step D — Define "Contact Info"

For CRE ownership graphs, the most reliable contact data:

```
FROM TAX ROLL / PARCEL DATA:
  ✓ Owner mailing address (where tax bills go — they open these)

FROM CORPORATE REGISTRY (Sunbiz):
  ✓ Registered agent and registered office
  ✓ Officers / managers on file

FROM COMPANY FILINGS (SEC EDGAR):
  ✓ Business and mailing addresses for public parents
  ✓ Useful once entity resolution finds a public-company parent

THE HIERARCHY OF CONTACT QUALITY:
  1. Owner mailing address from tax roll (highest — they pay taxes here)
  2. Officers/managers from Sunbiz (decision makers)
  3. Registered agent (legal contact, not always the decision maker)
  4. SEC EDGAR business address (corporate HQ for PE/REIT owners)
```

## The DG Ownership Graph Schema

```json
{
  "store": {
    "address": "4521 Highway 19",
    "city": "Perry",
    "state": "FL",
    "zip": "32347",
    "lat": 30.0542,
    "lng": -83.1806,
    "store_number": "8042"
  },
  "parcel": {
    "parcel_id": "R08-123-456-789",
    "county": "Taylor",
    "assessed_value": 1250000,
    "owner_name": "DG Southeast Holdings LLC",
    "owner_addr": "PO Box 12345",
    "owner_city": "Orlando",
    "owner_state": "FL",
    "owner_zip": "32801",
    "source": "FL DOR tax roll"
  },
  "entity": {
    "name": "DG Southeast Holdings LLC",
    "jurisdiction": "FL",
    "status": "Active",
    "registered_agent": "CT Corporation System",
    "officers": [
      {"name": "John Smith", "title": "Manager"},
      {"name": "Jane Doe", "title": "Member"}
    ],
    "parent": "Spirit Realty Capital Inc (NYSE: SRC)",
    "source": "Sunbiz + OpenCorporates"
  },
  "contact": {
    "best_mailing": "PO Box 12345, Orlando, FL 32801",
    "decision_maker": "John Smith (Manager)",
    "registered_agent": "CT Corporation System",
    "corporate_hq": "2727 N Harwood St, Dallas, TX 75201",
    "source_quality": "tax_roll_mailing (highest)"
  }
}
```

## Data Pipeline

```
1. SITES       DG store list (OSM + store locator) → lat/lng per store
2. PARCELS     Geocode → spatial match → FL DOR tax roll → owner + mailing
3. ENTITIES    Owner name → Sunbiz search → officers, registered agent
4. RESOLVE     Multi-state owners → OpenCorporates → parent entity chain
5. ENRICH      Public parents → SEC EDGAR → corporate HQ, filing addresses
6. GRAPH       All layers merged → queryable ownership graph
7. DEPLOY      swarmandbee.ai/dg → interactive map + search

COST:
  FL DOR tax roll:    FREE (public data)
  Sunbiz:             FREE (public records)
  OpenCorporates:     Free tier or $79/mo API
  Regrid:             Pay per parcel or bulk
  ATTOM:              Pay per property
  SEC EDGAR:          FREE (public data)
```

## Florida First

```
~900 Dollar General stores in Florida
~400-600 unique owners (many own multiple locations)
~100-200 unique parent entities (REITs, PE funds, DSTs, individuals)

Build Florida. Prove the graph. Then scale to all 50 states.
Same pipeline. Different tax roll source per state.
```

---

*Three layers. Parcel → Entity → Contact. The tax roll is the starting point. Sunbiz is the entity resolver. The graph connects them all.*

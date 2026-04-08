# Bob Review Squad Sample React Project

This sample project is intentionally designed to test the frontend analyzer rules for:

- TypeScript (`.ts`)
- TSX (`.tsx`)
- SCSS (`.scss`)

## Component Hierarchy

- `HomePage` (parent)
  - `VisionPanel` (child of HomePage)
  - `CultureHub` (child of HomePage)
    - `ImpactMetrics` (child of CultureHub)
    - `ReviewSquadFooter` (child of CultureHub)

## Intentional Rule Coverage

- Components 1 to 4 include a mix of passing and failing cases
- Component 5 (`ReviewSquadFooter`) is intended to pass all configured frontend rules

## Theme

The content focuses on Bobathon and how it can help IBM scale AI culture through:
- better engineering feedback
- faster code reviews
- reusable governance
- developer enablement
- team collaboration

## Footer Requirement

The footer includes:

`Created by Sachin Chotwani & Shubham Pandey using BOB for IBM`
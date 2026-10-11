# AI in Healthcare & Pharma

## Healthcare: where AI helps

- **Medical imaging**: detection/segmentation in chest X-ray, CT, MRI,
  pathology slides, and retina scans (CNNs, ViTs, VLMs).
- **Clinical NLP**: extracting diagnoses/medications from EHR notes, ICD-10
  coding, clinical trial matching, summarization for clinicians.
- **Risk prediction**: readmission, sepsis onset, deterioration (time-series +
  EHR features).
- **Operations**: scheduling, triage, revenue-cycle, staffing.

## Healthcare-specific challenges

- **Data**: scattered EHRs, noisy/heterogeneous records, protected health
  information (**PHI**), small labeled sets. Annotated medical images are
  scarce and expensive.
- **Class imbalance**: rare diseases mean the positive class is tiny; use
  PR-AUC/recall and calibration, not accuracy.
- **Calibration matters**: clinicians act on predicted probabilities; a
  model that says 90% must be right ~90% of the time.
- **Fairness/bias**: models trained on majority demographics can underperform
  on underrepresented groups (race, sex, age, disease subtype). Audit by
  subgroup.
- **Explainability**: clinicians need rationale — saliency maps, SHAP, or
  grounded references — to trust and act on outputs.
- **Monitoring/drift**: populations and equipment change; continuously track
  performance, not just deploy-and-forget.

## Regulation & compliance

- **FDA**: software as a medical device (**SaMD**) — models that direct
  treatment are regulated; requiring clinical evidence, risk classification,
  and post-market surveillance.
- **HIPAA** (US): governs PHI storage, access, and transmission.
  GDPR applies in the EU. De-identification is not a free pass.
- **Human-in-the-loop** is standard for high-stakes decisions; the model
  suggests, a clinician decides.

## Pharma & drug discovery

- **Target identification**: link genes/proteins to disease; protein language
  models (ESM, AlphaFold) model structure from sequence.
- **Virtual screening**: ML scores candidate molecules against targets.
- **Molecule design & generation**: generative models propose novel compounds;
  property prediction (**ADMET** — absorption, distribution, metabolism,
  excretion, toxicity) filters them.
- **Cheminformatics**: fingerprints (Morgan/ECFP), graph neural networks over
  molecular structure.
- **Clinical trials**: patient **stratification/enrichment** (recruit people
  most likely to respond), trial-site selection, and endpoint analytics.
- **Real-world evidence**: mining EHR/claims data for post-market outcomes.

## Pharma-specific concerns

- **GxP / 21 CFR Part 11**: data integrity and audit trails when ML feeds
  regulated processes.
- **Data quality > model fancy**: chemistry/EHR data are messy; the biggest
  wins are clean labels and good featurization.
- **Small data**: many drug-discovery problems have tiny sample sizes —
  prefer simpler, well-validated models over deep ones, and use
  protein/molecule embeddings + transfer learning.
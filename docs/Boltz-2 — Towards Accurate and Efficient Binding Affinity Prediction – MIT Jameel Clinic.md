---
title: "Boltz-2 — Towards Accurate and Efficient Binding Affinity Prediction – MIT Jameel Clinic"
source: "https://jclinic.mit.edu/boltz-2-towards-accurate-and-efficient-binding-affinity-prediction/"
author:
published: 2025-06-06
created: 2025-12-13
description:
tags:
  - "clippings"
---
# Boltz-2 — Towards Accurate and Efficient Binding Affinity Prediction – MIT Jameel Clinic

**Source:** https://jclinic.mit.edu/boltz-2-towards-accurate-and-efficient-binding-affinity-prediction/

---

## 🧠 Summary
Boltz-2 (MIT Jameel Clinic & Recursion) — concise summary

- What it is: An open‑source, all‑atom biomolecular foundation model that jointly predicts 3D structures (proteins, DNA, RNA, ligands) and protein–ligand binding affinities in one model.

- Main breakthrough: For the first time a deep‑learning model approaches the accuracy of physics‑based free‑energy perturbation (FEP) affinity methods while running ~1000× faster, making large‑scale in silico screening practical for early drug discovery.

- Key performance highlights:
  - FEP/OpenFE benchmark (held‑out targets): Pearson r ≈ 0.62, comparable to OpenFE.
  - CASP16 affinity challenge: outperformed all submitted methods across 140 complexes.
  - Retrospective hit‑discovery (MF‑PCBA): roughly doubled average precision versus ML and docking baselines.

- Model innovations: new affinity prediction module, improved structural accuracy over Boltz‑1, integration of synthetic and MD training data, GPU optimizations, and fine‑grained controllability (contact constraints, templates, experimental alignment).

- Demonstrations & workflows: paired with SynFlowNet for efficient virtual screening; prospective TYK2 screen validated top candidates with ABFE simulations; conditioned MD inference captures local dynamics competitively with other state‑of‑the‑art models.

- Access & license: Code, weights, and training pipeline to be released under an MIT license for academic and commercial use. Paper and GitHub links provided in the announcement.

- Why it matters: Combines fast, accurate structure and affinity prediction to reduce reliance on slow/expensive experiments and simulations, enabling practical high‑throughput virtual screening and accelerating small‑molecule drug discovery.

---

## 📝 Full Content
![](https://jclinic.mit.edu/wp-content/uploads/2025/06/boltz2.gif)

Boltz-2 is a new biomolecular foundation model that goes beyond AlphaFold3 and Boltz-1 by jointly modeling complex structures and binding affinities, a critical component towards accurate molecular design. Boltz-2 is the first deep learning model to approach the accuracy of physics-based free-energy perturbation (FEP) methods, while running 1000x faster — making accurate in silico screening practical for early-stage drug discovery.

Boltz-2 is a new biomolecular foundation model that goes beyond AlphaFold3 and Boltz-1 by jointly modeling complex structures and binding affinities, a critical component towards accurate molecular design. Boltz-2 is the first deep learning model to approach the accuracy of physics-based free-energy perturbation (FEP) methods, while running 1000x faster — making accurate in silico screening practical for early-stage drug discovery.

  

### TL;DR

- **Boltz-2** is a next-generation biomolecular foundation model that extends interaction modeling beyond structure prediction and achieves state-of-the-art performance in binding affinity prediction.
- Boltz-2 was developed by the Boltz team at **MIT**  Jameel Clinic alongside  **Recursion**, and builds on Boltz-1, *the most popular open-source alternative to AlphaFold3 used across academia and industry*, improving its structural accuracy and understanding of protein dynamics.
- The biggest breakthrough is a new affinity module which is able to predict protein-ligand binding affinity at an accuracy level that approaches that of long and expensive FEP atomistic simulations ***while being more than 1000x faster***. Binding affinity prediction is critical for molecule screening but something that no AI model has been able to accurately predict.
- Additionally, Boltz-2 includes several features that make the model more controllable with experimental data and human intuition, making it more useful for drug development.
- Open Source — Boltz-2 will be open-sourced under an MIT license. The model, weights, and training pipeline will be ***made available for academic and commercial use***, doubling down on our commitment to making AI tools accessible for drug developers.

Today, we are excited to announce Boltz-2, a new open-source foundation model for predicting biomolecular interactions. The model is the follow-up to Boltz-1, a popular open-source alternative to AlphaFold3 (AF3), that we published in November 2024. Since its release, Boltz-1 has been used by thousands of scientists across leading academic labs, venture-backed, publicly traded biotechs, and teams at all the 20 largest pharmaceutical companies — making it the most widely used model of its kind in industry. Boltz-2 is a significant improvement from Boltz-1. By unifying structure and affinity prediction, Boltz-2 delivers unprecedented binding affinity accuracy — at a speed orders of magnitude faster than traditional methods — pushing the boundaries of in silico drug discovery.

**Why this matters?**

Boltz – like AlphaFold3 – is an all-atom, co-folding model which extends the concept of protein folding or structure prediction to other important molecules (DNA, RNA, Ligands). The model can predict the 3D structures of molecular interactions, which can be used for downstream tasks like molecular design. These models have already revolutionized protein engineering, serving as the structural backbone for designing large molecules including *de novo* mini binders and antibodies. However, they have not had the same impact on small molecules, which constitute the majority of pharmaceuticals, industrial chemicals, and consumer goods.

A large bottleneck in current small molecule development consists in binding affinity experiments. Small molecule binding affinity, or the strength of the interaction between a protein and a ligand, plays a critical role in the function of small molecule drugs and is the most commonly measured property in early stage R&D. Running these experiments in the lab is a critical time and cost bottleneck for early stage drug discovery. Long physics-based simulations (such as FEP+ from Schrodinger or OpenFE, an open-source alternative) have so far been the only viable alternative to physical experiments, yet they are also extremely slow and expensive.

**What’s New?**

Boltz-2 predicts structure and affinity in one model. Its architecture builds on Boltz-1 and adds a new affinity module, improved controllability, GPU optimizations, and the integration of a large collection of synthetic and molecular dynamics training data.

On the standard FEP+ (OpenFE) affinity benchmark, whose targets were held out of training, Boltz-2 achieves an average Pearson of 0.62—comparable to OpenFE, a widely adopted open-source FEP pipeline, while being over 1000x faster. In the CASP16 affinity challenge benchmark, Boltz-2 outperformed all submitted methods in predicting binding affinities across 140 complexes. In retrospective hit-discovery screens (MF-PCBA), Boltz-2 significantly outperforms ML and docking methods, doubling average precision.

![](https://cdn.prod.website-files.com/68404fd075dba49e58331ad9/6842e97801f4e42f3c0485b3_pearson.png)

We also paired Boltz-2 with SynFlowNet, to run efficient large-scale virtual screening. In a prospective TYK2 screen, all top-10 generated compounds were predicted to bind via ABFE simulations with some showing remarkable affinity—validating Boltz-2’s use in generative design workflows.

![](https://cdn.prod.website-files.com/68404fd075dba49e58331ad9/6842ea38ada94df5e57fa661_screen.png)

In X-ray crystal structure prediction, Boltz-2 matches or outperforms Boltz-1 across modalities with particular gains in challenging modalities like DNA-protein complexes, RNA structures and antibody-antigen interactions. At large user request, we introduced fine-grained control of the model: you can now specify contact constraints, guide predictions with templates, or align results to specific experimental methods. We’ve already seen interesting uses of these capabilities and we are very excited to see how people will use them! We also integrated in training thousands of short MD simulations. Remarkably, at inference time, conditioned on MD data, Boltz-2 captures local dynamics better than Boltz-1 and competitively with models like AlphaFlow—or BioEmu—demonstrating Boltz-2’s power as a general biomolecular foundation model.

Like Boltz-1, Boltz-2 code will be released under an open source MIT license permitting academic and commercial use. We can’t wait to see how you build on Boltz-2!

To learn more:

- Join our fast-growing Slack community: [https://join.slack.com/t/boltz-community/shared\_invite/zt-34qg8uink-V1LGdRRUf3avAUVaRvv93w](https://join.slack.com/t/boltz-community/shared_invite/zt-34qg8uink-V1LGdRRUf3avAUVaRvv93w)
- Read the full manuscript: [http://jeremywohlwend.com/assets/boltz2.pdf](http://jeremywohlwend.com/assets/boltz2.pdf)
- Test our model & code: [https://github.com/jwohlwend/boltz](https://github.com/jwohlwend/boltz)

And join us for live presentations, demos and discussions:

- MIT (Cambridge) – Monday, June 9th  [https://bit.ly/boltz2-mit](https://bit.ly/boltz2-mit)
- San Francisco – Wednesday, June 11th [https://bit.ly/boltz2-sf](https://bit.ly/boltz2-sf)
- NVIDIA #GTC25 (Paris) – Wednesday, June 11th
- MoML (Montreal) – Tuesday, June 17th

[Saro Passaro](https://jclinic.mit.edu/team-member/saro-passaro/), [Gabriele Corso](https://jclinic.mit.edu/team-member/gabriele-corso/) and [Jeremy Wohlwend](https://jclinic.mit.edu/team-member/jeremy-wohlwend/)

On behalf of the whole Boltz-2 team Saro Passaro, Gabriele Corso, Jeremy Wohlwend, Mateo Reveiz, Stephan Thaler, Vignesh Ram Somnath, Noah Getz, Tally Portnoi, Julien Roy, Hannes Stark, David Kwabi-Addo, Dominique Beaini, [Tommi Jaakkola](https://jclinic.mit.edu/team-member/tommi-jaakkola/), [Regina Barzilay](https://jclinic.mit.edu/team-member/regina-barzilay/)

**[Original Post](https://boltz.bio/boltz2)**

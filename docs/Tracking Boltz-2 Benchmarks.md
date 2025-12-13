---
title: "Tracking Boltz-2 Benchmarks"
source: "https://www.rowansci.com/blog/boltz2-benchmarks"
author:
  - "[[Rowan Documentation]]"
published:
created: 2025-12-13
description: "Tracking the community's response to the new Boltz-2 model, plus some notes about Chai-2."
tags:
  - "clippings"
---
# Tracking Boltz-2 Benchmarks

**Source:** https://www.rowansci.com/blog/boltz2-benchmarks

---

## 🧠 Summary
Summary

This blog post compiles independent, external benchmarks of Boltz-2 (a co‑folding model that predicts protein–ligand structures and estimates binding affinity) to show where it succeeds, where it falls short, and how it compares to physics‑based methods and fine‑tuned ML. The page is a living document (last updated Sept 11) that aggregates results from several teams and datasets.

Key findings

- Overall performance: Boltz-2 typically outperforms conventional docking but is not a drop‑in replacement for gold‑standard physics methods (e.g., FEP) or well‑tuned target‑specific models.

- PL-REX (Semen Yesylevskyy): Boltz-2 ranked second behind SQM 2.20 on relative‑affinity correlation for the PL‑REX set. Gains over other ML and docking methods were modest; inference speed was much slower than typical docking tools.

- Uni‑FEP (Xi Chen): Boltz-2 shows consistently strong, broad performance across many protein families, including some flexible systems, but (a) underestimates the spread of experimental affinities (many predictions cluster within ~2 kcal/mol), and (b) performs poorly when buried water is important.

- Six protein–ligand systems (Tushar Modi et al.): Boltz-2 performs well on rigid, stable systems but often fails when proteins require large conformational rearrangements or have mobile domains—cases that may need templates or refinement steps.

- ASAP‑Polaris‑OpenADMET (Auro Varat Patnaik): Vanilla (zero‑shot) Boltz-2 performed poorly on an antiviral potency challenge compared with fine‑tuned methods; implication: fine‑tuning or target‑specific data remains important.

- Molecular glues (Dominykas Lukauskis et al.): On 93 ternary‑complex cases, Boltz-2 underperformed FEP, giving weak/negative correlations and large absolute errors despite reasonable structural predictions.

Common limitations observed

- Affinity compression: tendency to regress predictions toward the mean, reducing dynamic range versus experiment.
- Missing explicit physics: failures where buried waters or other solvent/thermodynamic details matter indicate these effects are not reliably captured implicitly.
- Sensitivity to conformational changes: trouble when binding requires significant protein rearrangement not represented in training data.
- Runtime: inference can be substantially slower than conventional docking.

Practical takeaways

- Use case: good for improving over docking and for rapid structure prediction, but should be embedded in a larger workflow (e.g., prefiltering followed by FEP or target‑tuned models) rather than used alone for high‑confidence affinity ranking.
- For cases involving buried water, large protein rearrangements, molecular glues, or where a wide affinity range is known, treat Boltz-2 predictions with caution and consider physics‑based follow‑up.

Addendum

- Chai‑2 (recently released) represents a contrasting approach: an end‑to‑end pipeline aimed at antibody design, highlighting that co‑folding ideas are being packaged into broader, multi‑step workflows.

Bottom line

Boltz-2 is a meaningful step beyond docking and useful as a tool in drug discovery, but current external benchmarks show consistent limitations (affinity compression, sensitivity to buried water and large conformational changes, slower inference). It complements—not replaces—FEP and well‑tuned, target‑specific methods.

---

## 📝 Full Content
## Tracking External Boltz-2 Benchmarks

by Corin Wagen · Jul 1, 2025

Three weeks ago, a team of scientists from MIT and Recursion released Boltz-2, a co-folding model which not only predicts the structure of bound protein–ligand complexes but also "approaches the accuracy of FEP-based methods" for binding-affinity prediction. This is an extraordinary claim, and one which prompted thousands of scientists (including us) to start investigating Boltz-2 for structure-based drug design. (For a more detailed look at how Boltz-2 works and the potential uses, [read our full FAQ](https://rowansci.com/blog/boltz2-faq).)

Over the past few weeks, a variety of scientific teams have disclosed external benchmarks of Boltz-2. This field is moving incredibly fast, so these benchmarks are hard to keep track of: some happen on LinkedIn, while others are on X or various blogs around the Internet. To make it easier for our users to keep track of the latest updates surrounding Boltz-2, we've compiled the most relevant data on this page. Although it's still early—it hasn't even been a month since Boltz-2 was released—the model's strengths and limitations are gradually becoming clear. (Note: we're excluding random posts of single structures here, since most of these lack clear systematic comparisons to experiment.)

*This is a living document, and will be updated as additional benchmarks are released. This page last updated September 11.*

## PL-REX Benchmark (Semen Yesylevskyy)

This benchmark, [posted on LinkedIn a week ago](https://www.linkedin.com/posts/semen-yesylevskyy-b002ab212_boltz2-machinelearning-docking-activity-7341513162359197698-CtQN/), evaluates the performance of Boltz-2 against a variety of physics- and ML-based methods on the 2024 [PL-REX dataset](https://github.com/Honza-R/PL-REX). This is a "best case" scenario for physics-based methods, since the protein–ligand complex is known with relatively high confidence for these systems.

Yesylevskyy compared the Pearson correlation coefficient of all methods for ranking the relative affinity of different binders. He found that the [SQM 2.20 method](https://www.nature.com/articles/s41467-024-45431-8) (for which the PL-REX dataset was developed) significantly outperformed all other methods, with Boltz-2 coming in second place.

![Chen's Boltz-2 benchmarks with buried water.](https://www.rowansci.com/blog/boltz2-benchmarks/plrex.jpeg)

Comparison of a variety of methods on the PL-REX binding-affinity benchmark.

Here's what Yesylevskyy has to say about this:

> Boltz-2 scores the second being only 5-7% better than the closest ML competitor ΔvinaRF20 and the closest physics-based competitors GlideSP and Gold ChemPLP. Boltz-2 is still far cry below SQM2.20 and only reaches mean correlation of ~0.42 with experimental values... So, according to this test, Boltz-2 is only an incremental improvement over existing affinity prediction techniques rather than a revolution. Moreover, its inference speed was rather disappointing in our tests being an order of magnitude slower than conventional docking programs such as Vina or Glide.

It's worth noting that although SQM 2.20 performs well on this benchmark, a similar semiempirical method [was recently shown to perform poorly on the ULVSH virtual screening dataset](https://pubs.acs.org/doi/full/10.1021/acs.jcim.5c00730).

## Uni-FEP Benchmark (Xi Chen)

On LinkedIn, Xi Chen and co-workers from Atombeat [recently disclosed benchmark results for Boltz-2 on the Uni-FEP dataset](https://www.linkedin.com/pulse/exploring-boltz-2s-performance-uni-fep-benchmark-xi-chen-ph-d--qnzne/?trackingId=hVxttycnRoKWnYFwfh79pw%3D%3D). This benchmark set comprises approximately 350 proteins and 5800 ligands.

Chen reports that Boltz-2 gives "consistently strong results — measured by both correlation terms and mean error terms— across 15 protein families," including cases where conformational effects are significant, like GPCRs and kinases. Unfortunately, Boltz-2 significantly lagged FEP in cases where buried water was known to be important, a sign that these effects are not implicitly accounted for by the model:

![Chen's Boltz-2 benchmarks with buried water.](https://www.rowansci.com/blog/boltz2-benchmarks/water.png)

Comparison of Boltz-2 to FEP in cases where buried water is important.

Another interesting observation is that Boltz-2 consistently underestimates the spread of binding affinities present in experimental data. In the below two cases, the predicted range of binding affinities is significantly tighter than either the observed experimental values or the predictions from the conventional physics-based FEP workflow:

![Chen's Boltz-2 benchmarks showing affinity compression.](https://www.rowansci.com/blog/boltz2-benchmarks/squashing.png)

Comparison of Boltz-2 to FEP, illustrating the propensity of Boltz-2 to compress affinity values.

Here's what Chen has to say:

> One general trend we observed — independent of specific targets — is Boltz-2's tendency to predict binding affinities within a narrow range, typically within 2 kcal/mol. Figures 5a and 5b illustrate examples. We found this behavior on 75 of the 350 targets evaluated. For 21 of those, the experimental binding affinities spanned more than 4 kcal/mol — yet Boltz-2 clustered predictions near the mean, effectively "regressing to the center."

Similar observations were [recently reported by John Parkhill on X](https://x.com/j0hnparkhill/status/1932526099579166876).

## Six Protein–Ligand Systems (Tushar Modi et al.)

Tushar Modi and co-workers at Deep Mirror [recently disclosed benchmarks for six protein–ligand systems](https://www.deepmirror.ai/post/boltz-2-real-drug-targets). Their overall conclusions were that Boltz-2 did well for stable and rigid systems, but struggled with ligand geometries or in cases where conformational flexibility was important:

> Boltz-2 often has difficulty when a protein must undergo a big shape change or has multiple mobile domains with little precedent in the training data. If a protein needs to bend into a new shape to accommodate a ligand (like the allosteric changes in PI3K-α or WRN, or the dynamic binding required in cGAS), the unguided model usually fails to predict that rearrangement. These cases often require additional help—such as supplying a template of the alternate conformation or running a refinement step—to obtain the correct pose.

Note that this conclusion is the exact opposite of what Xi Chen noted above.

## ASAP-Polaris-OpenADMET Challenge (Auro Varat Patnaik)

Auro Varat Patnaik, a graduate student at the University of Edinburgh, [ran a retrospective analysis of how Boltz-2 would have performed on the ASAP-Polaris-OpenADMET antiviral challenge](https://www.linkedin.com/pulse/boltz-2-potency-prediction-how-does-fare-antiviral-auro-varat-patnaik-aybvf/). He found that Boltz-2 performed very poorly, with a mean absolute error worst among any method studied.

![Patnaik's Boltz-2 benchmarks showing poor performance.](https://www.rowansci.com/blog/boltz2-benchmarks/asap-scatter.png)

Comparison of Boltz-2 predicted pIC <sub>50</sub> values to experimental values on the ASAP-Polaris-OpenADMET challenge.

Patnaik offers the following caveat:

> Compared to the other methods, a vanilla BOLTZ-2 seems to be far behind, but it's critical to note that the competing methods were fine-tuned models. A fine-tuned BOLTZ-2 could potentially provide much better results.

At a minimum, it seems that zero-shot Boltz-2 is not a replacement for fine-tuned methods using target-specific data.

## Molecular Glue Binding Affinity (Dominykas Lukauskis et al.)

Dominykas Lukauskis and co-workers from Ternary Therapeutics [compared the performance of Boltz-2 and FEP (using OpenFE) on a set of 93 molecular glues with experimentally determined ternary-complex binding-affinity data](https://chemrxiv.org/engage/chemrxiv/article-details/68bad5e3728bf9025e961742?t=IyY5W7lSiHfxZ8L4YTt6Tw). They found that Boltz-2 dramatically underperformed FEP, showing "generally poor or even negative correlations" and large absolute errors, despite generally good structural validity and accuracy of the predicted complexes.

![Lukauskis's Boltz-2 benchmarks showing poor performance.](https://www.rowansci.com/blog/boltz2-benchmarks/ternary-scatter.png)

Comparison of Boltz-2 predicted affinities to experimental values on the Ternary Therapeutics dataset.

In their own words:

> The poor performance of Boltz-2 suggests it is not suitable for high-throughput screening of molecular glues, highlighting the need for more accurate, high-throughput machine learning methods for pre-FEP screening

## Conclusions

While this field is moving fast, some tentative conclusions can be drawn. Here's our current thinking on Boltz-2:

- Boltz-2 seems to be reproducibly better than conventional protein–ligand docking.
- However, it struggles in complex cases or cases that are poorly represented in the training data. It's still not 100% clear what these cases are; some benchmarks allege that flexible systems perform badly, for instance, while others disagree.
- Boltz-2 is not yet a replacement for "gold-standard" physics-based methods like FEP or fine-tuned target-specific methods.

When used properly, it's likely that Boltz-2 can be a very useful tool in the drug-discovery arsenal; but it's not a solution in isolation, and likely needs to be embedded in a proper virtual-screening workflow to give useful results.

## Addendum: Chai-2

Yesterday, Chai-2 was released. Although minimal technical details were disclosed, Chai-2 appears to be a co-folding-based workflow involving a sequence of models and physics-based steps that can be used for zero-shot antibody design. In combination with Adaptyv Bio, the Chai-2 authors reported a 50% wet-lab success rate against a panel of 52 diverse protein targets; [the full technical report gives more target details](https://chaiassets.com/chai-2/paper/technical_report.pdf).

![Visual summary of Chai-2.](https://www.rowansci.com/blog/boltz2-benchmarks/chai2-fig1.png)

Figure 1 from the Chai-2 technical report.

Since Boltz-1 and Chai-1 were virtually clones, it's interesting to reflect on the ways these two projects have evolved. Boltz-2 has focused on small molecules and binding-affinity prediction within a single model, while Chai-2 has expanded into an entire end-to-end pipeline and seems to be focusing on antibody/nanobody design. It will be interesting to see where both projects go next!

![Banner background image](https://www.rowansci.com/art/liljefors/eagles.jpg)

## Start running calculations in minutes!

Interested in generating results that can help guide your own research? Rowan lets you easily determine useful molecular properties and quickly obtain insight into molecular processes, all with a simple GUI and cloud based computing. We offer 500 free credits when you first sign up, and an additional 20 credits each week. Make an account and get your first results within minutes!

[Start computing →](https://labs.rowansci.com/create-account)

[![Batch Calculations Through Rowan's API](https://www.rowansci.com/blog/batch-calculations/tercios.jpg)](https://www.rowansci.com/blog/batch-calculations)

[![Building BioArena: Kat Yenko on Evaluating Scientific AI Agents](https://www.rowansci.com/preview-images/blog/25-12-09-bioarena.jpg)](https://www.rowansci.com/blog/building-bioarena-kat-yenko)

[![Automating Organic Synthesis: A Conversation With Daniil Boiko and Andrei Tyrin from onepot](https://www.rowansci.com/blog/onepot/pizza.png)](https://www.rowansci.com/blog/automating-organic-synthesis-onepot)

[![Eliminating Imaginary Frequencies](https://www.rowansci.com/blog/imaginary-frequencies/ss.png)](https://www.rowansci.com/blog/eliminating-imaginary-frequencies)

[![Conformer Deduplication, Clustering, and Analytics](https://www.rowansci.com/preview-images/news/25-11-25-conformers.jpg)](https://rowansci.substack.com/p/conformer-deduplication-clustering)

[![The Multiple-Minimum Monte Carlo Method for Conformer Generation](https://www.rowansci.com/blog/mcmm/naomi-dimer.png)](https://www.rowansci.com/blog/multiple-minimum-monte-carlo)

[![Screening Conformer Ensembles with PRISM Pruner](https://www.rowansci.com/blog/prism-pruner/ens-reduction.jpg)](https://www.rowansci.com/blog/screening-conformer-ensembles-with-prism-pruner)

[![GPU-Accelerated DFT](https://www.rowansci.com/preview-images/news/25-11-19-gpu4pyscf.jpg)](https://rowansci.substack.com/p/gpu-accelerated-dft)

[![Rowan Research Spotlight: Emilia Taylor](https://www.rowansci.com/blog/emilia-spotlight/emilia.png)](https://www.rowansci.com/blog/rowan-research-spotlight-emilia)

[![GPU-Accelerated DFT with GPU4PySCF](https://www.rowansci.com/blog/gpu4pyscf/DFT-engine-comparison.svg)](https://www.rowansci.com/blog/gpu4pyscf)

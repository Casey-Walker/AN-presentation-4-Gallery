window.CHARTS = [
  {
    "id": "3_0",
    "title": "Missing-Data Audit: Share of Postings Missing Each Field",
    "file": "charts/3_0.html",
    "thumbnail": "thumbs/3_0.png",
    "interactive": true,
    "section": "1. Setup and Load",
    "subsection": null,
    "caption": "Which fields are missing, and how often -- salary and URL are the big gaps."
  },
  {
    "id": "7_0",
    "title": "Demand Volume: Top 15 Titles in Our Data & Analytics Subset",
    "file": "charts/7_0.html",
    "thumbnail": "thumbs/7_0.png",
    "interactive": true,
    "section": "2. Subset to Our Research Focus",
    "subsection": null,
    "caption": "The 15 most common job titles in the U.S. analytics-postings subset."
  },
  {
    "id": "13_0",
    "title": "Tech-Skill Flags: Share of Postings Mentioning Each Tool",
    "file": "charts/13_0.html",
    "thumbnail": "thumbs/13_0.png",
    "interactive": true,
    "section": "4. Feature Engineering from Text",
    "subsection": null,
    "caption": "Share of postings mentioning each tool, from regex flags on skills + description."
  },
  {
    "id": "13_1",
    "title": "Years of Experience Required (Regex-Extracted)",
    "file": "charts/13_1.html",
    "thumbnail": "thumbs/13_1.png",
    "interactive": true,
    "section": "4. Feature Engineering from Text",
    "subsection": null,
    "caption": "Minimum years of experience required, extracted by regex from posting text."
  },
  {
    "id": "13_2",
    "title": "Entry-Level Accessibility (Combined Rule)",
    "file": "charts/13_2.html",
    "thumbnail": "thumbs/13_2.png",
    "interactive": true,
    "section": "4. Feature Engineering from Text",
    "subsection": null,
    "caption": "How many postings qualify as entry-accessible under the combined rule."
  },
  {
    "id": "13_3",
    "title": "Compensation Benchmarks: Annualized Salary Midpoint (Disclosed Only)",
    "file": "charts/13_3.html",
    "thumbnail": "thumbs/13_3.png",
    "interactive": true,
    "section": "4. Feature Engineering from Text",
    "subsection": null,
    "caption": "Salary midpoint distribution, disclosed postings only."
  },
  {
    "id": "13_4",
    "title": "Salary Spread by Experience Level and Work Setting",
    "file": "charts/13_4.html",
    "thumbnail": "thumbs/13_4.png",
    "interactive": true,
    "section": "4. Feature Engineering from Text",
    "subsection": null,
    "caption": "Salary spread broken out by experience level and remote/on-site/hybrid."
  },
  {
    "id": "15_0",
    "title": "Contextual Vocabulary: Top 15 Unigrams (BEFORE cleaning)",
    "file": "charts/15_0.html",
    "thumbnail": "thumbs/15_0.png",
    "interactive": true,
    "section": "5. Text Visualization",
    "subsection": null,
    "caption": "Top unigrams before the text-cleaning pipeline runs -- mostly boilerplate."
  },
  {
    "id": "15_0_1",
    "title": "Contextual Vocabulary: Top 15 Unigrams (after cleaning)",
    "file": "charts/15_0_1.html",
    "thumbnail": "thumbs/15_0_1.png",
    "interactive": true,
    "section": "5. Text Visualization",
    "subsection": null,
    "caption": "Top unigrams after cleaning -- the real vocabulary of the postings."
  },
  {
    "id": "15_0_2",
    "title": "Contextual Vocabulary: Top 15 Bigrams (after cleaning)",
    "file": "charts/15_0_2.html",
    "thumbnail": "thumbs/15_0_2.png",
    "interactive": true,
    "section": "5. Text Visualization",
    "subsection": null,
    "caption": "Top two-word phrases after cleaning."
  },
  {
    "id": "15_0_3",
    "title": "Contextual Vocabulary: Top 15 Trigrams (after cleaning)",
    "file": "charts/15_0_3.html",
    "thumbnail": "thumbs/15_0_3.png",
    "interactive": true,
    "section": "5. Text Visualization",
    "subsection": null,
    "caption": "Top three-word phrases after cleaning."
  },
  {
    "id": "16_mpl0",
    "title": "Before cleaning",
    "file": "images/16_mpl0.png",
    "thumbnail": "thumbs/16_mpl0.png",
    "interactive": false,
    "section": "5. Text Visualization",
    "subsection": null,
    "caption": "Word clouds contrasting raw vs. cleaned posting text."
  },
  {
    "id": "15_0_4",
    "title": "Contextual Vocabulary: Top 15 Bigrams (entry-accessible postings)",
    "file": "charts/15_0_4.html",
    "thumbnail": "thumbs/15_0_4.png",
    "interactive": true,
    "section": "5. Text Visualization",
    "subsection": null,
    "caption": "Top bigrams within just the entry-accessible postings."
  },
  {
    "id": "17_mpl0",
    "title": "Entry-Accessible Postings: What They Talk About",
    "file": "images/17_mpl0.png",
    "thumbnail": "thumbs/17_mpl0.png",
    "interactive": false,
    "section": "5. Text Visualization",
    "subsection": null,
    "caption": "Word cloud of what entry-accessible postings talk about most."
  },
  {
    "id": "19_0",
    "title": "Similarity Matrix: Our 10 Best-Fit Postings",
    "file": "charts/19_0.html",
    "thumbnail": "thumbs/19_0.png",
    "interactive": true,
    "section": "6. TF-IDF and Cosine Similarity",
    "subsection": null,
    "caption": "Cosine similarity between our 10 best-fit postings and the 'dream job' profile."
  },
  {
    "id": "23_0",
    "title": "Choosing k: Elbow vs Silhouette",
    "file": "charts/23_0.html",
    "thumbnail": "thumbs/23_0.png",
    "interactive": true,
    "section": "8. K-Means Clustering (Elbow + Silhouette)",
    "subsection": null,
    "caption": "Choosing k for K-means: inertia (elbow) vs. silhouette score, k = 3-10."
  },
  {
    "id": "24_0",
    "title": "Segmentation Mapping: 2D K-Means Cluster Projection (PCA)",
    "file": "charts/24_0.html",
    "thumbnail": "thumbs/24_0.png",
    "interactive": true,
    "section": "8. K-Means Clustering (Elbow + Silhouette)",
    "subsection": null,
    "caption": "2D PCA projection of the 6 K-means role segments."
  },
  {
    "id": "27_0",
    "title": "LDA: Perplexity by Number of Topics (lower is better, but watch interpretability)",
    "file": "charts/27_0.html",
    "thumbnail": "thumbs/27_0.png",
    "interactive": true,
    "section": "9. LDA Topic Modeling (with pyLDAvis)",
    "subsection": null,
    "caption": "LDA perplexity across 3-10 topics -- flat, so topic count is chosen for interpretability, not the metric."
  },
  {
    "id": "28_0",
    "title": "Dominant LDA Topic per Posting",
    "file": "charts/28_0.html",
    "thumbnail": "thumbs/28_0.png",
    "interactive": true,
    "section": "9. LDA Topic Modeling (with pyLDAvis)",
    "subsection": null,
    "caption": "How many postings fall under each of the 6 LDA topics."
  },
  {
    "id": "32_0",
    "title": "Top 20 Skills Employers List (skills column)",
    "file": "charts/32_0.html",
    "thumbnail": "thumbs/32_0.png",
    "interactive": true,
    "section": "10. Skills Analysis",
    "subsection": null,
    "caption": "The 20 most frequently requested skills across postings."
  },
  {
    "id": "32_1",
    "title": "Skill Co-occurrence: How Often Top Skills Are Requested Together",
    "file": "charts/32_1.html",
    "thumbnail": "thumbs/32_1.png",
    "interactive": true,
    "section": "10. Skills Analysis",
    "subsection": null,
    "caption": "Which top skills get requested together most often."
  },
  {
    "id": "32_2",
    "title": "Do Entry-Accessible Roles Ask for Different Skills?",
    "file": "charts/32_2.html",
    "thumbnail": "thumbs/32_2.png",
    "interactive": true,
    "section": "10. Skills Analysis",
    "subsection": null,
    "caption": "Do entry-accessible roles ask for a different skill mix?"
  },
  {
    "id": "39_0",
    "title": "Data & Analytics Postings by State (on-site / hybrid)",
    "file": "charts/39_0.html",
    "thumbnail": "thumbs/39_0.png",
    "interactive": true,
    "section": "11. Geospatial Analytics",
    "subsection": "11c",
    "caption": "Posting volume by state, on-site/hybrid roles only."
  },
  {
    "id": "39_1",
    "title": "City Bubble Map: Posting Volume (size) and Median Salary (color)",
    "file": "charts/39_1.html",
    "thumbnail": "thumbs/39_1.png",
    "interactive": true,
    "section": "11. Geospatial Analytics",
    "subsection": "11c",
    "caption": "Posting volume (size) and median salary (color) by city."
  },
  {
    "id": "40_0",
    "title": "Salary Disclosure Rate by State",
    "file": "charts/40_0.html",
    "thumbnail": "thumbs/40_0.png",
    "interactive": true,
    "section": "11. Geospatial Analytics",
    "subsection": "11c",
    "caption": "Share of postings per state that disclose a salary."
  },
  {
    "id": "40_1",
    "title": "Median Disclosed Salary by State (states with 5+ disclosed salaries)",
    "file": "charts/40_1.html",
    "thumbnail": "thumbs/40_1.png",
    "interactive": true,
    "section": "11. Geospatial Analytics",
    "subsection": "11c",
    "caption": "Median disclosed salary by state, 5+ disclosed salaries only."
  },
  {
    "id": "41_0",
    "title": "Skill-Share Map: % of Postings Asking for Each Tool (use the slider; states with 8+ postings)",
    "file": "charts/41_0.html",
    "thumbnail": "thumbs/41_0.png",
    "interactive": true,
    "section": "11. Geospatial Analytics",
    "subsection": "11c",
    "caption": "Share of postings asking for each tool, by state (interactive slider)."
  },
  {
    "id": "43_0",
    "title": "DBSCAN Spatial Clusters (eps = 35 km, min_samples = 5)",
    "file": "charts/43_0.html",
    "thumbnail": "thumbs/43_0.png",
    "interactive": true,
    "section": "11. Geospatial Analytics",
    "subsection": "11d",
    "caption": "Metro areas found by clustering posting coordinates with DBSCAN."
  },
  {
    "id": "45_0",
    "title": "Normalized Demand: Data & Analytics Postings per Million Residents",
    "file": "charts/45_0.html",
    "thumbnail": "thumbs/45_0.png",
    "interactive": true,
    "section": "12. Normalized Economic Measures",
    "subsection": null,
    "caption": "Posting demand normalized by state population."
  },
  {
    "id": "45_1",
    "title": "Cost-of-Living-Adjusted Median Salary (BEA RPP 2024)",
    "file": "charts/45_1.html",
    "thumbnail": "thumbs/45_1.png",
    "interactive": true,
    "section": "12. Normalized Economic Measures",
    "subsection": null,
    "caption": "Median salary adjusted for regional purchasing power (BEA RPP)."
  },
  {
    "id": "45_2",
    "title": "States: Demand per Capita vs Purchasing-Power Salary (bubble = postings)",
    "file": "charts/45_2.html",
    "thumbnail": "thumbs/45_2.png",
    "interactive": true,
    "section": "12. Normalized Economic Measures",
    "subsection": null,
    "caption": "States plotted by demand per capita vs. purchasing-power-adjusted salary."
  },
  {
    "id": "48_0",
    "title": "Metro Scorecard: Volume + Adjusted Salary + Accessibility",
    "file": "charts/48_0.html",
    "thumbnail": "thumbs/48_0.png",
    "interactive": true,
    "section": "13. Metro Scorecard, Summary and Recommendations",
    "subsection": null,
    "caption": "Metro ranking combining posting volume, adjusted salary, and entry accessibility."
  },
  {
    "id": "50_0",
    "title": "Executive Summary Dashboard",
    "file": "charts/50_0.html",
    "thumbnail": "thumbs/50_0.png",
    "interactive": true,
    "section": "13. Metro Scorecard, Summary and Recommendations",
    "subsection": null,
    "caption": "Headline numbers for the whole analysis in one view."
  },
  {
    "id": "54_0",
    "title": "Observed: Top Employers by Postings, AI-Related vs Data & Analytics",
    "file": "charts/54_0.html",
    "thumbnail": "thumbs/54_0.png",
    "interactive": true,
    "section": "15. Industry Question: Who Is Investing Most in Data, Analytics and AI?",
    "subsection": null,
    "caption": "Top employers by posting volume, AI-related vs. general data & analytics."
  },
  {
    "id": "55_0",
    "title": "Inferred Industries: Posting Volume vs Share of AI-Related Postings",
    "file": "charts/55_0.html",
    "thumbnail": "thumbs/55_0.png",
    "interactive": true,
    "section": "15. Industry Question: Who Is Investing Most in Data, Analytics and AI?",
    "subsection": null,
    "caption": "Posting volume vs. share of AI-related postings, by inferred industry."
  },
  {
    "id": "29_lda",
    "title": "LDA Topic Model (pyLDAvis)",
    "file": "charts/pyldavis.html",
    "thumbnail": null,
    "interactive": true,
    "section": "9. LDA Topic Modeling (with pyLDAvis)",
    "subsection": null,
    "caption": "Interactive LDA topic-model explorer (pyLDAvis) -- intertopic distance and top terms per topic."
  }
];

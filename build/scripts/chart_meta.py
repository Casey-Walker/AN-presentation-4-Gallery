import re

_BOLD_ITALIC = re.compile(r"\*{1,2}([^*]+)\*{1,2}")
_BACKTICK = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")


def strip_markdown(text: str) -> str:
    text = _LINK.sub(r"\1", text)
    text = _BOLD_ITALIC.sub(r"\1", text)
    text = _BACKTICK.sub(r"\1", text)
    return text


def validate(found_ids: list[str]) -> tuple[list[str], list[str]]:
    known = set(CHART_META.keys())
    found = set(found_ids)
    missing = [i for i in found_ids if i not in known]
    extra = [i for i in CHART_META if i not in found]
    return missing, extra


SEC_1 = "1. Setup and Load"
SEC_2 = "2. Subset to Our Research Focus"
SEC_4 = "4. Feature Engineering from Text"
SEC_5 = "5. Text Visualization"
SEC_6 = "6. TF-IDF and Cosine Similarity"
SEC_8 = "8. K-Means Clustering (Elbow + Silhouette)"
SEC_9 = "9. LDA Topic Modeling (with pyLDAvis)"
SEC_10 = "10. Skills Analysis"
SEC_11 = "11. Geospatial Analytics"
SEC_12 = "12. Normalized Economic Measures"
SEC_13 = "13. Metro Scorecard, Summary and Recommendations"
SEC_15 = "15. Industry Question: Who Is Investing Most in Data, Analytics and AI?"

CHART_META: dict[str, dict] = {
    "3_0": {"section": SEC_1, "subsection": None,
            "caption": "Which fields are missing, and how often -- salary and URL are the big gaps."},

    "7_0": {"section": SEC_2, "subsection": None,
            "caption": "The 15 most common job titles in the U.S. analytics-postings subset."},

    "13_0": {"section": SEC_4, "subsection": None,
             "caption": "Share of postings mentioning each tool, from regex flags on skills + description."},
    "13_1": {"section": SEC_4, "subsection": None,
             "caption": "Minimum years of experience required, extracted by regex from posting text."},
    "13_2": {"section": SEC_4, "subsection": None,
             "caption": "How many postings qualify as entry-accessible under the combined rule."},
    "13_3": {"section": SEC_4, "subsection": None,
             "caption": "Salary midpoint distribution, disclosed postings only."},
    "13_4": {"section": SEC_4, "subsection": None,
             "caption": "Salary spread broken out by experience level and remote/on-site/hybrid."},

    "15_0": {"section": SEC_5, "subsection": None,
             "caption": "Top unigrams before the text-cleaning pipeline runs -- mostly boilerplate."},
    "16_mpl0": {"section": SEC_5, "subsection": None,
                "caption": "Word clouds contrasting raw vs. cleaned posting text."},
    "15_0_1": {"section": SEC_5, "subsection": None,
               "caption": "Top unigrams after cleaning -- the real vocabulary of the postings."},
    "15_0_2": {"section": SEC_5, "subsection": None,
               "caption": "Top two-word phrases after cleaning."},
    "15_0_3": {"section": SEC_5, "subsection": None,
               "caption": "Top three-word phrases after cleaning."},
    "15_0_4": {"section": SEC_5, "subsection": None,
               "caption": "Top bigrams within just the entry-accessible postings."},
    "17_mpl0": {"section": SEC_5, "subsection": None,
                "caption": "Word cloud of what entry-accessible postings talk about most."},

    "19_0": {"section": SEC_6, "subsection": None,
             "caption": "Cosine similarity between our 10 best-fit postings and the 'dream job' profile."},

    "23_0": {"section": SEC_8, "subsection": None,
             "caption": "Choosing k for K-means: inertia (elbow) vs. silhouette score, k = 3-10."},
    "24_0": {"section": SEC_8, "subsection": None,
             "caption": "2D PCA projection of the 8 K-means role segments."},

    "27_0": {"section": SEC_9, "subsection": None,
             "caption": "LDA perplexity across 3-10 topics -- flat, so topic count is chosen for interpretability, not the metric."},
    "28_0": {"section": SEC_9, "subsection": None,
             "caption": "How many postings fall under each of the 6 LDA topics."},
    "29_lda": {"section": SEC_9, "subsection": None,
               "caption": "Interactive LDA topic-model explorer (pyLDAvis) -- intertopic distance and top terms per topic."},

    "32_0": {"section": SEC_10, "subsection": None,
             "caption": "The 20 most frequently requested skills across postings."},
    "32_1": {"section": SEC_10, "subsection": None,
             "caption": "Which top skills get requested together most often."},
    "32_2": {"section": SEC_10, "subsection": None,
             "caption": "Do entry-accessible roles ask for a different skill mix?"},

    "39_0": {"section": SEC_11, "subsection": "11c",
             "caption": "Posting volume by state, on-site/hybrid roles only."},
    "39_1": {"section": SEC_11, "subsection": "11c",
             "caption": "Posting volume (size) and median salary (color) by city."},
    "40_0": {"section": SEC_11, "subsection": "11c",
             "caption": "Share of postings per state that disclose a salary."},
    "40_1": {"section": SEC_11, "subsection": "11c",
             "caption": "Median disclosed salary by state, 5+ disclosed salaries only."},
    "41_0": {"section": SEC_11, "subsection": "11c",
             "caption": "Share of postings asking for each tool, by state (interactive slider)."},
    "43_0": {"section": SEC_11, "subsection": "11d",
             "caption": "Metro areas found by clustering posting coordinates with DBSCAN."},

    "45_0": {"section": SEC_12, "subsection": None,
             "caption": "Posting demand normalized by state population."},
    "45_1": {"section": SEC_12, "subsection": None,
             "caption": "Median salary adjusted for regional purchasing power (BEA RPP)."},
    "45_2": {"section": SEC_12, "subsection": None,
             "caption": "States plotted by demand per capita vs. purchasing-power-adjusted salary."},

    "48_0": {"section": SEC_13, "subsection": None,
             "caption": "Metro ranking combining posting volume, adjusted salary, and entry accessibility."},
    "50_0": {"section": SEC_13, "subsection": None,
             "caption": "Headline numbers for the whole analysis in one view."},

    "54_0": {"section": SEC_15, "subsection": None,
             "caption": "Top employers by posting volume, AI-related vs. general data & analytics."},
    "55_0": {"section": SEC_15, "subsection": None,
             "caption": "Posting volume vs. share of AI-related postings, by inferred industry."},
}

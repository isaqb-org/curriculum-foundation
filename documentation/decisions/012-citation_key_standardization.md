# 012 - Citation Key Standardization

## Status: Accepted

## Context

The iSAQB curricula and related documents currently (11/2024) use inconsistent citation keys/labels for referencing sources. This includes varying formats for:
- Multiple author references
- Year formatting
- Special character handling
- Edge cases like standards, wikis, or online resources

```
[Miller et. al]
[Sperber+Klaeren]
[Rajlich+2000]
[Bass+ 2021] 
[Richards+20]
```

The use of mixed styles and formats, makes maintenance difficult and potentially confuses readers. This affects readability and synchronization between different iSAQB documents, particularly when cross-referencing between curricula, glossary, and other materials.

## Decision

Standardize citation keys starting with the FL curriculum, try to implement the following set of guidelines across other iSAQB documentation.

### 1. Basic Format

```
[lastname YYYY]     - single author: [Starke 2024]
[lastname+ YYYY]    - multiple authors: [Bass+ 2021]
[lastname YYYYa]    - multiple works same year: [Buschmann 1996a]
```

Where:
- Author is the surname of the first author only
- YYYY is the four-digit year
- Space between Author and Year
- "+" indicates multiple authors
- No space between Author and +

### 2. Special Cases

```
[standard-id]       - standards: [ISO-25010:2023]
[abbreviation]      - known terms: [arc42]
[concept]           - concept/website without author: [SOLID], [UML]
[Wiki-topic]        - Wikipedia: [Wiki-SOLID], [Wiki-LehmansLaws]
[organization]      - organizations [CNCF], [CNCF 2024] 
[lastname-concept]  - concept/website with author: [Fowler-PoEAA]
[org-topic]         - organization docs: [IETF-HTTP], [CNCF-Cloud]
[org-doctype]       - organization publications: [iSAQB-Glossary], [iSAQB-Foundation]
```

### 3. Naming Rules
1. Author Names:
   - Use surname only: "Martin Fowler" → [Fowler 2002]
   - For multiple authors, use first author: "Gamma, Helm, Johnson, Vlissides" → [Gamma+ 1994]
   - Alternative known names allowed: "Gang of Four" → [GoF 1994]
   - For multiple works by same author/year, append lowercase letters (a, b, c...)

2. Special Characters:
   - Remove apostrophes: "Conway's Law" → [ConwaysLaw]
   - Keep possessive 's': "Lehman's Laws" → [LehmansLaws]
   - Use CamelCase for compound names: "Model View Controller" → [ModelViewController]
   - Only if CamelCase is not applicable or confusing, use space: [IETF HTML]
   - Keep established names/abbreviations: [arc42]

3. Edge Cases:
   - Unknown author: Use organization or short title
   - No date available: Omit year component
   - Standards: Keep standard number/identifier but shorten if possible: "ISO/IEC 42010:2022" → [ISO 42010:2022]
   - Wikipedia articles: Always prefix with "Wiki-"
   - For multiple works by same author without year, use descriptive suffix: [Fowler-Patterns], [Fowler-Testing]


## Rationale

This format:
- Aligns with majority of existing citations in FL curriculum and glossary
- Provides clear distinction between single/multiple authors
- Maintains readability while being concise
- Allows easy processing and maintenance
- Accommodates special cases without complexity

## Consequences

- Apply to new citations immediately
- Update existing citations gradually during regular document maintenance
- Document exceptions when required
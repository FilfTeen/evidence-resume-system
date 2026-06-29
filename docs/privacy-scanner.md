# Privacy Scanner

The scanner checks text files for generic patterns that often deserve review before public sharing:

- email-shaped strings;
- phone-like strings;
- absolute home-directory paths;
- web links with a scheme;
- token assignment patterns;
- metadata fields that expose contact or project-location routes;
- resume-like Markdown headings.

A clean scan means none of the configured patterns were found. It does not prove that text is suitable for every context. Human review is still required for meaning, inference risk, and suitability.

First-shot layout constraint addendum (iteration 1):

Treat layout safety as a hard requirement:
- No component boxes may overlap.
- For fields stacked in the same column, enforce a minimum vertical gap of 16px between the previous field's bottom and the next field's top.
- Preserve a simple top-to-bottom reading flow so each next field starts at or below the previous field's bottom plus gap.

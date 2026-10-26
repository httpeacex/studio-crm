# Workspace interface

Studio CRM uses a compact, light workspace with a neutral sidebar and violet action
color. Contacts, search and next actions remain above the fold on a desktop screen.

## References

- https://21st.dev/ — component vocabulary: compact navigation, tabs, input groups,
  avatars, status badges and visible button states. Patterns adapted to Django
  templates; no React component source or paid assets were copied.
- https://recent.design/websites?sort=popular — visual hierarchy, restrained chrome,
  consistent spacing and clear filtering, observed in the supplied gallery.

## Tokens

- Canvas #f7f8fa; surface #ffffff; ink #20232d; muted #626977.
- Border #e7e9ef; primary #6d42d8; primary soft #f0eafb.
- System sans-serif stack with Cyrillic support; 14px compact data, 16px forms.
- Sidebar 224px; header 64px; main content 32px gutter; 8/12px component radii.
- Focus rings, SVG icons, minimum 44px touch actions; reduced-motion support.

## Usability

- Active/archive tabs; sorting; filter for missing email; explicit search submit.
- Slash focuses search outside editable fields. All controls still work without JS.
- Mobile contacts become stacked rows, without horizontal page scrolling.
- Archive can be reversed from the client detail page.
- No placeholder navigation to unfinished modules and no fabricated business metrics.

## Validation

Check login, list, search, sort, missing-email filter, edit, archive and restore.
Check 390/768/1440px widths, keyboard focus, missing email, empty search, long names
and field errors. Screenshots in README are captured from the running application.

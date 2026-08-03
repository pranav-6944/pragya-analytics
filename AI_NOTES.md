# AI Notes - PRAGYA University Analytics

## Key File Locations & Search Reference
- **Frontend Core**: `Bonus_FastAPI/frontend/src/`
- **Dashboard Page**: `Bonus_FastAPI/frontend/src/pages/Dashboard.jsx` (Lines 1-660)
  - Sidebar: Lines 423-458 (`aside` element with fixed `width: 220px`, `marginLeft: 220px` on main content)
  - KPI Cards: Line 504 (`grid grid-cols-5 gap-4`)
  - Overview Grid: Lines 513, 535 (`grid grid-cols-2 gap-5`)
  - Predict Panel: Lines 87-202 (Form & ML prediction output display)
  - Department Charts: Lines 594 (`grid grid-cols-2 gap-5`)
  - Course Difficulty: Lines 626 (`grid grid-cols-2 gap-5`)
  - Segments Section: Lines 205-295 (`grid grid-cols-2 gap-5` & Radar chart)
- **User Guide Page**: `Bonus_FastAPI/frontend/src/pages/Guide.jsx` (Lines 1-262)
  - Top Nav: Lines 161-179
  - Quick Links Grid: Line 199 (`gridTemplateColumns: 'repeat(3, 1fr)'`)
  - Accordion Content: Line 234 (Fixed `padding: '4px 22px 22px 60px'`)
- **Landing Components**: `Bonus_FastAPI/frontend/src/components/`
  - `Navbar.jsx`: Mobile hamburger drawer (Lines 46-64)
  - `Hero.jsx`: Heading & Stats Grid (Lines 20-55, `grid-cols-3`)
  - `DashboardPreview.jsx`: Mock UI preview (Lines 42-114)
  - `Features.jsx`: `grid-cols-1 md:grid-cols-2`
  - `HowItWorks.jsx`: `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`
  - `UseCases.jsx`: `grid-cols-1 md:grid-cols-3`
  - `CTA.jsx`: Banner padding `px-10 py-20`
  - `Footer.jsx`: `grid-cols-1 md:grid-cols-4`
- **Global Styles & CSS**: `Bonus_FastAPI/frontend/src/index.css` & `tailwind.config.js`
- **GitHub Repository Remote**: `https://github.com/pranav-6944/pragya-analytics.git`

## Responsive Optimization Goals
1. Mobile Navigation & Drawer in `Dashboard.jsx`, `Navbar.jsx`, and `Guide.jsx`.
2. Responsive Grids (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-X`) for KPI cards, chart pairs, and stats cards.
3. Responsive padding, typography, touch target sizing, and table overflow wrappers across all viewports down to 320px width.
4. Continuous git commits and pushes to GitHub repository.

## Logo & Branding Assets
- **Logo Image**: `Bonus_FastAPI/frontend/public/logo.png`
- **Favicon**: `Bonus_FastAPI/frontend/public/favicon.png` (configured in `index.html`)
- **Root Image Backup**: `Pragya Logo.png`
- **Used In Components**: `Navbar.jsx`, `Dashboard.jsx` (mobile header & sidebar), `Guide.jsx`, `Footer.jsx`

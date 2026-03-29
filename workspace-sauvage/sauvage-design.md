# Sauvage Space — Design System

## Brand Identity

### Name
Sauvage Space

### Tagline
"Your neighborhood event venue in Amsterdam"

### Personality
- Warm but professional
- Approachable, not corporate
- Creative, community-focused
- Efficient, respectful of time

---

## Color Palette

### Primary Colors
```
--color-primary: #1a1a1a        /* Near black - headings, primary text */
--color-secondary: #666666      /* Medium gray - secondary text */
--color-accent: #c4a77d         /* Warm gold/tan - CTAs, highlights */
--color-accent-hover: #b39a6f   /* Darker gold - hover states */
```

### Background Colors
```
--color-bg-primary: #faf9f7     /* Warm off-white - main background */
--color-bg-secondary: #ffffff   /* Pure white - cards, surfaces */
--color-bg-tertiary: #f0ede8    /* Light tan - subtle sections */
```

### Semantic Colors
```
--color-success: #22c55e        /* Green - available, confirmed */
--color-warning: #f59e0b        /* Amber - limited availability */
--color-error: #ef4444          /* Red - booked, errors */
--color-info: #3b82f6           /* Blue - links, info */
```

### Room Colors (for floor plan)
```
--room-upstairs: #e8d5b7        /* Warm beige */
--room-entrance: #d4c4a8        /* Tan */
--room-kitchen: #c9b896         /* Darker tan */
--room-cave: #b8a88a            /* Brown-tan */
--room-unselected: #e5e5e5      /* Gray */
```

---

## Typography

### Font Family
```
--font-heading: 'Inter', system-ui, sans-serif
--font-body: 'Inter', system-ui, sans-serif
```

### Type Scale
| Style | Size | Line Height | Weight | Usage |
|-------|------|-------------|--------|-------|
| H1 | 24px | 32px | 600 | Widget titles |
| H2 | 20px | 28px | 600 | Section headers |
| H3 | 18px | 24px | 500 | Card titles |
| Body | 16px | 24px | 400 | Primary text |
| Body Small | 14px | 20px | 400 | Secondary text |
| Caption | 12px | 16px | 500 | Labels, pills |
| Price | 28px | 36px | 700 | Total amounts |

---

## Spacing Scale

```
--space-xs: 4px
--space-sm: 8px
--space-md: 16px
--space-lg: 24px
--space-xl: 32px
--space-2xl: 48px
--space-3xl: 64px
```

### Widget Padding
- Internal: 24px
- Between elements: 16px
- Edge to content: 16px (mobile), 24px (desktop)

---

## Components

### Buttons

**Primary Button**
```
Background: var(--color-accent)
Text: var(--color-primary)
Padding: 16px 24px
Border-radius: 12px
Font-weight: 500
Hover: darken 10%, scale 1.02
Active: scale 0.98
```

**Secondary Button**
```
Background: transparent
Border: 1px solid var(--color-secondary)
Text: var(--color-primary)
Padding: 16px 24px
Border-radius: 12px
Hover: background var(--color-bg-tertiary)
```

**Icon Button**
```
Size: 44px × 44px
Border-radius: 12px
Background: var(--color-bg-secondary)
Hover: background var(--color-bg-tertiary)
```

### Cards

**Widget Card**
```
Background: var(--color-bg-secondary)
Border-radius: 16px
Padding: 24px
Shadow: 0 1px 3px rgba(0,0,0,0.05)
Border: 1px solid rgba(0,0,0,0.05)
```

**Selection Card (Event Types)**
```
Size: 64px × 80px
Border-radius: 12px
Background: var(--color-bg-tertiary)
Border: 2px solid transparent
Selected: border-color var(--color-accent), background white
```

### Pills

**Selected Item Pill**
```
Background: var(--color-accent)
Text: var(--color-primary)
Padding: 8px 16px
Border-radius: 20px
Font-size: 14px
Close icon: × (16px)
```

**Room Toggle Pill**
```
Unselected:
  Background: var(--color-bg-tertiary)
  Border: 1px solid transparent
  
Selected:
  Background: var(--room-upstairs) [room-specific color]
  Border: 2px solid var(--color-primary)
  
Padding: 12px 20px
Border-radius: 24px
```

### Form Elements

**Slider**
```
Track height: 8px
Track color: var(--color-bg-tertiary)
Fill color: var(--color-accent)
Thumb size: 28px
Thumb color: white
Thumb shadow: 0 2px 4px rgba(0,0,0,0.1)
```

**Checkbox**
```
Size: 24px × 24px
Border-radius: 6px
Border: 2px solid var(--color-secondary)
Checked: background var(--color-accent), border transparent
Checkmark: white, 16px
```

---

## Animations

### Timing Functions
```
--ease-default: cubic-bezier(0.4, 0, 0.2, 1)
--ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1)
--ease-smooth: cubic-bezier(0.25, 0.1, 0.25, 1)
```

### Durations
```
--duration-fast: 150ms
--duration-normal: 300ms
--duration-slow: 500ms
```

### Animation Presets

**Widget Enter**
```
From: opacity 0, translateY(20px)
To: opacity 1, translateY(0)
Duration: 400ms
Easing: ease-out
```

**Selection Bounce**
```
Scale: 1 → 1.1 → 1
Duration: 300ms
Easing: bounce
```

**Number Count**
```
Duration: 600ms
Easing: ease-out
```

**Slide Between Widgets**
```
Current: translateX(0) → translateX(-100%), opacity 1 → 0
Next: translateX(100%) → translateX(0), opacity 0 → 1
Duration: 400ms
Easing: ease-in-out
```

**Loading Skeleton**
```
Animation: shimmer (gradient sweep)
Duration: 1500ms
Iteration: infinite
```

---

## Icons

### Icon Library
- **Source:** Lucide React
- **Size:** 24px default, 20px small, 32px large
- **Stroke width:** 2px

### Key Icons
| Usage | Icon | Notes |
|-------|------|-------|
| Birthday | Cake | Filled when selected |
| Dinner | Utensils | Filled when selected |
| Workshop | Palette | Filled when selected |
| Corporate | Briefcase | Filled when selected |
| Pop-up | Tent | Filled when selected |
| Calendar | CalendarDays | Date picker |
| Clock | Clock | Time selection |
| Users | Users | Guest count |
| Home | Home | Room selection |
| Glassware | Wine | Add-on |
| Dishware | UtensilsCrossed | Add-on |
| Staff | UserCheck | Add-on |
| Projector | Projector | Add-on |
| Snacks | Croissant | Add-on |
| Sound | Music | Add-on |
| Check | Check | Selected state |
| Chevron | ChevronDown | Expand/collapse |
| Close | X | Remove, close |
| Arrow | ArrowRight | Next, continue |

---

## Layout

### Mobile-First Breakpoints
```
Mobile: 0-639px (default)
Tablet: 640px-1023px
Desktop: 1024px+
```

### Widget Container
```
Max-width: 480px (mobile)
Max-width: 560px (tablet+)
Margin: 0 auto
Padding: 16px
```

### Z-Index Scale
```
--z-base: 0
--z-dropdown: 100
--z-sticky: 200
--z-modal: 300
--z-toast: 400
```

---

## Responsive Behavior

### Mobile (<640px)
- Single column layout
- Full-width buttons
- Bottom sheet for modals
- Horizontal scroll for chips/cards

### Tablet (640px-1023px)
- Two-column for calendar + time slots
- Side-by-side room toggles
- Persistent sidebar (optional)

### Desktop (1024px+)
- Calendar and time slots side-by-side
- Room visualizer larger
- Sidebar showing booking progress
- Wider touch targets acceptable

---

## Accessibility

### Focus States
```
Outline: 2px solid var(--color-accent)
Outline-offset: 2px
Border-radius: inherit
```

### Reduced Motion
```
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Color Contrast
- All text meets WCAG AA (4.5:1 minimum)
- Large text (18px+) meets WCAG AA (3:1 minimum)
- Interactive elements have visible focus

---

## Shadow & Elevation

```
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)
--shadow-md: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.03)
--shadow-lg: 0 10px 15px rgba(0,0,0,0.05), 0 4px 6px rgba(0,0,0,0.02)
--shadow-xl: 0 20px 25px rgba(0,0,0,0.05), 0 10px 10px rgba(0,0,0,0.02)
```

---

## Component References

### From 21st.dev
- Button: @shadcn/button
- Card: @shadcn/card
- Slider: @radix-ui/slider
- Checkbox: @shadcn/checkbox
- Calendar: @shadcn/calendar

### Custom Components Needed
- EventTypeSelector (horizontal scroll)
- RoomVisualizer (floor plan)
- AddOnChips (toggle chips)
- QuoteCard (expandable)
- ProgressPills (inline editing)

---

## Image Assets

### Room Photos
| Room | URL |
|------|-----|
| Upstairs | https://cdn.shopify.com/s/files/1/0519/3574/0095/files/gallerysauvage.png |
| Entrance | https://cdn.shopify.com/s/files/1/0519/3574/0095/files/Entranceroomsauvage.jpg |
| Kitchen | https://cdn.shopify.com/s/files/1/0519/3574/0095/files/SauvageKitchen2.jpg |
| Cave | https://cdn.shopify.com/s/files/1/0519/3574/0095/files/Winecavesauvage.png |

### Drone Video
- Walkthrough: https://www.youtube.com/watch?v=zQW83iHU_T4&t=9s

---

*Last updated: March 2026*

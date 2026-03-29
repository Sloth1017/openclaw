# Sauvage Space Booking Chatbot — UI Specification 2026

> **Version:** 1.0  
> **Date:** March 2026  
> **Status:** Draft for Development  
> **Target:** Mobile-first, progressive disclosure, minimal cognitive load

---

## 1. Design Philosophy

### Core Principles

| Principle | Implementation |
|-----------|----------------|
| **Progressive Disclosure** | Show only the widget needed at each step. No overwhelming forms. |
| **One-Tap Decisions** | Every interaction should be achievable with a single thumb tap. |
| **Visual Confirmation** | Replace text input with visual selection wherever possible. |
| **Mobile-First** | Design for the thumb zone; everything reachable without hand gymnastics. |
| **Context-Aware** | Predict user intent based on event type selection. |

### Success Metrics

- **Time to book:** < 90 seconds for simple bookings
- **Tap count:** < 15 taps for complete booking
- **Abandonment:** < 30% drop-off at any widget
- **Edit rate:** < 20% of users need to change prior selections

---

## 2. Widget Stack (5 Core Widgets)

### Widget 1: Smart Onboarding Card

**Trigger:** Immediately on first message

**Purpose:** Capture intent and set predictive defaults

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  What are you planning?                 │
│                                         │
│  [🎂] [🍽️] [🎨] [💼] [🎪] [❓]         │
│  Bday Dinner Work Corp Pop-up Other     │
│                                         │
│  ← horizontal scroll →                  │
└─────────────────────────────────────────┘
```

**Interaction:**
- Horizontal scrollable row of 6 event type icons
- Each icon: 64×64px touch target, centered icon + label below
- Tap selects → icon scales up (1.1×) with subtle bounce
- Auto-advances to Widget 2 after 400ms delay
- Selected event type stored as "pill" above chat

**Event Types & Icons:**
| Type | Icon | Predictive Defaults |
|------|------|---------------------|
| Birthday | 🎂 | Evening, 20 guests, Upstairs+Entrance |
| Dinner | 🍽️ | Evening, 12 guests, Downstairs |
| Workshop | 🎨 | Morning/Afternoon, 15 guests, Kitchen+Main |
| Corporate | 💼 | Full day, 25 guests, Entire space, Projector |
| Pop-up | 🎪 | Flexible, 30 guests, All rooms |
| Other | ❓ | No defaults, manual configuration |

**Wireframe Description:**
- Full-width card with rounded corners (16px radius)
- Soft gradient background based on selected event type (subtle color coding)
- Icons use filled style when selected, outline when unselected
- Label typography: 12px, medium weight, centered

---

### Widget 2: Availability Calendar

**Trigger:** After event type selected

**Purpose:** Date and time selection with availability visualization

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  When do you need it?                   │
│  [Event type pill] ✕                    │
│                                         │
│      ← March 2026 →                     │
│  Su  Mo  Tu  We  Th  Fr  Sa             │
│      24  25  26  27  28  29             │
│  30  31  [01][02][03][04][05]           │
│  [06][07][08][09][10][11][12]           │
│                                         │
│  ─────────────────────────────────────  │
│  📅 March 8 — Select a time             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │ Morning │ │Afternoon│ │ Evening │   │
│  │  8-12   │ │  12-17  │ │  17-23  │   │
│  └─────────┘ └─────────┘ └─────────┘   │
│         [ Custom hours ]                │
└─────────────────────────────────────────┘
```

**Interaction:**
- Month view calendar with color-coded dates:
  - 🟢 Green = Fully available
  - 🟡 Yellow = Limited slots (< 3 remaining)
  - 🔴 Red = Fully booked (disabled, tap shows waitlist option)
  - ⚪ Gray = Past dates (disabled)
- Tap date → expands inline time slot selector
- Time slots presented as 3 large touch-friendly cards
- "Custom hours" expands to time picker for non-standard slots
- Duration auto-suggested based on event type, editable via dropdown

**Color Coding Logic:**
```
Availability Status:
├── Available (green-500): 3+ slots remaining
├── Limited (amber-500): 1-2 slots remaining  
├── Booked (rose-500): 0 slots, waitlist available
└── Unavailable (gray-300): Past or blocked dates
```

**Wireframe Description:**
- Calendar: 7-column grid, 44px minimum touch targets
- Selected date: filled circle with checkmark
- Today: ring outline, no fill
- Time slot cards: 3-column grid, icon + time range + availability indicator
- Duration selector: dropdown below time slots, pre-filled with smart default

---

### Widget 3: Capacity Slider + Room Visualizer

**Trigger:** After date/time confirmed

**Purpose:** Guest count and room selection with visual feedback

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  How many guests?                       │
│  [Event] [Date] [Time] ✕ ✕ ✕            │
│                                         │
│     👥 18 guests                        │
│  ━━━━━━━━━━●━━━━━━━━━━━━━━━━━━━         │
│  1                        30            │
│                                         │
│  ─────────────────────────────────────  │
│  Recommended rooms for 18 people:       │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  [Floor plan thumbnail]         │    │
│  │   🟦 Upstairs      (12)         │    │
│  │   🟩 Entrance      (8)          │    │
│  │   ⬜ Kitchen       (add?)       │    │
│  └─────────────────────────────────┘    │
│                                         │
│  [📷 View photos]  [✓ Looks good]       │
└─────────────────────────────────────────┘
```

**Interaction:**
- Slider: 1-30 range, snap to whole numbers
- As slider moves:
  - Room capacity indicator updates in real-time
  - Floor plan highlights recommended rooms
  - "Add Kitchen" / "Add Cave" toggles appear if capacity allows
- Tap floor plan → opens full-screen room photos
- Room pills are toggle-able (tap to add/remove)
- Visual feedback: rooms turn from gray to color when selected

**Room Capacity Matrix:**
| Room | Capacity | Best For | Toggleable |
|------|----------|----------|------------|
| Upstairs | 12 | Intimate dinners, meetings | Yes |
| Downstairs | 15 | Workshops, presentations | Yes |
| Entrance | 8 | Reception, mingling | Yes |
| Kitchen | 6 | Cooking classes, prep | Add-on |
| Cave | 10 | Wine tastings, storage | Add-on |

**Wireframe Description:**
- Slider: thick track (8px), large thumb (28px), haptic feedback on snap
- Guest count: large display above slider, animates on change
- Floor plan: simplified 2D layout, rooms color-coded by selection state
- Toggle chips: pill-shaped, checkmark when active, "+" when inactive
- Photo button: opens carousel of room images with capacity overlay

---

### Widget 4: Add-on Chips

**Trigger:** After rooms confirmed

**Purpose:** Equipment and service selection with running total

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  Any extras?                            │
│  [Event] [Date] [18 guests] [Rooms] ✕   │
│                                         │
│  Equipment & Services:                  │
│                                         │
│  ← [🍷 Glassware] [🍽️ Dishware] [👤 Staff] →
│  ← [📽️ Projector] [🥐 Snacks] [🎵 Sound] →
│                                         │
│  Selected: 🍷 Glassware  👤 Staff       │
│                                         │
│  ─────────────────────────────────────  │
│  💰 €450  [View quote →]                │
└─────────────────────────────────────────┘
```

**Interaction:**
- Horizontal scroll of toggle chips
- Each chip: icon + label + price (small)
- Tap to toggle on/off
- Selected chips appear below as "active pills"
- Running total updates in sticky footer
- "View quote" expands Widget 5 inline

**Add-on Options:**
| Add-on | Icon | Price | Auto-suggested For |
|--------|------|-------|-------------------|
| Glassware | 🍷 | €5/guest | Dinner, Birthday, Corporate |
| Dishware | 🍽️ | €4/guest | Dinner, Workshop |
| Staff | 👤 | €150 | Corporate, Pop-up (>20 guests) |
| Projector | 📽️ | €75 | Corporate, Workshop |
| Snacks | 🥐 | €8/guest | Morning events |
| Sound system | 🎵 | €100 | Pop-up, Birthday |
| Extra tables | 🪑 | €25 | Workshop (>15 guests) |

**Wireframe Description:**
- Chips: 48px height, rounded-full (24px radius), border when unselected, filled when selected
- Horizontal scroll with snap-to-chip behavior
- Sticky footer: 64px height, white background, subtle top shadow
- Total: large bold text, updates with counting animation
- "View quote" button: primary CTA style, expands below

---

### Widget 5: Quote + Pay Card

**Trigger:** After add-ons selected (or tap "View quote")

**Purpose:** Final confirmation and payment

**Visual Design:**
```
┌─────────────────────────────────────────┐
│  Ready to book?                         │
│  [Event] [Date] [18] [Rooms] [+2] ✕     │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  📋 Quote Summary      [▼]      │    │
│  │  ─────────────────────────────  │    │
│  │  Venue (Upstairs + Entrance)    │    │
│  │  4 hours × €75/hr      €300     │    │
│  │  Glassware (18)         €90     │    │
│  │  Staff (1)             €150     │    │
│  │  ─────────────────────────────  │    │
│  │  Subtotal              €540     │    │
│  │  VAT (21%)             €113     │    │
│  │  ─────────────────────────────  │    │
│  │  Total                 €653     │    │
│  └─────────────────────────────────┘    │
│                                         │
│  [ ] I agree to the Terms & Conditions  │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │        💳 Book Now              │    │
│  │     €653 — Pay securely         │    │
│  └─────────────────────────────────┘    │
│                                         │
│  [🍎 Apple Pay]  [🤖 Google Pay]        │
└─────────────────────────────────────────┘
```

**Interaction:**
- Quote card: expandable/collapsible (tap header to toggle)
- Line items show calculation breakdown
- T&C checkbox: required before payment buttons appear
- After T&C checked:
  - "Book Now" button becomes active
  - Apple Pay / Google Pay buttons appear below
- Tap payment method → native payment sheet
- Success: confetti animation + booking confirmation card

**Payment Flow:**
```
User taps "Book Now"
    ↓
T&C checkbox appears (unchecked)
    ↓
User checks T&C
    ↓
Payment buttons appear (Apple Pay / Google Pay / Card)
    ↓
User selects method → Payment sheet opens
    ↓
Payment confirmed → Booking created
    ↓
Success card with booking reference + calendar invite
```

**Wireframe Description:**
- Quote card: accordion style, chevron rotates 180° when expanded
- Line items: left-aligned description, right-aligned price
- Total: bold, larger font, separated by divider
- T&C: checkbox with linked text (opens modal)
- Primary button: full-width, brand color, disabled state until T&C checked
- Payment buttons: secondary style, platform-branded colors

---

## 3. Smart Features

### Predictive Defaults Matrix

| Event Type | Default Time | Default Guests | Default Rooms | Suggested Add-ons |
|------------|--------------|----------------|---------------|-------------------|
| Birthday | Evening (19:00) | 20 | Upstairs + Entrance | Glassware, Sound |
| Dinner | Evening (19:30) | 12 | Downstairs | Glassware, Dishware |
| Workshop | Morning (09:00) | 15 | Downstairs + Kitchen | Projector, Snacks |
| Corporate | Full day (09:00-17:00) | 25 | Entire space | Projector, Staff |
| Pop-up | Flexible | 30 | All rooms | Staff, Sound, Extra tables |
| Other | — | — | — | — |

### Inline Editing System

Every selection becomes a "pill" that can be tapped to edit:

```
Selected: [🎂 Birthday ✕] [📅 Mar 8 ✕] [🌅 Evening ✕]
           ↑ tap to change   ↑ tap to change   ↑ tap to change
```

**Rules:**
- Pills appear chronologically above current widget
- Tap pill → jump to that widget, pre-filled with current selection
- Changing a pill resets all subsequent selections (cascade)
- "✕" on pill clears just that selection
- Smooth scroll animation when jumping between widgets

### Voice Fallback

**Always-visible microphone icon** in input bar:

```
┌─────────────────────────────────────────┐
│  🎙️  [Type a message...]  [Send]       │
└─────────────────────────────────────────┘
```

**Voice Commands Supported:**
| Command | Action |
|---------|--------|
| "Book for 20 people" | Jump to capacity widget, pre-fill 20 |
| "Next Tuesday evening" | Jump to calendar, select date + evening |
| "Add projector" | Toggle projector add-on |
| "What's the total?" | Expand quote card |
| "I need the kitchen too" | Toggle kitchen room |
| "Start over" | Clear all, return to Widget 1 |

---

## 4. Platform Strategy

### Web Chat (Primary Experience)

**Full Widget Stack:**
- All 5 widgets with rich interactions
- Framer Motion animations (spring physics)
- Persistent sidebar showing booking progress
- Keyboard shortcuts (1-5 to jump to widgets)
- Desktop: wider layout, calendar side-by-side with time slots

**Sidebar Progress:**
```
┌─────────────┐ ┌─────────────────────────────┐
│ Your Booking│ │                             │
│ ─────────── │ │    [Widget content]         │
│ ✓ Event     │ │                             │
│ ✓ Date      │ │                             │
│ → Guests    │ │                             │
│ ○ Add-ons   │ │                             │
│ ○ Payment   │ │                             │
│             │ │                             │
│ 💰 €0       │ │                             │
└─────────────┘ └─────────────────────────────┘
```

### WhatsApp (Secondary)

**Simplified Interactions:**
- No visual widgets → numbered lists
- Quick reply buttons for options
- Images sent as room photos (not interactive floor plan)
- One message per interaction (respect WhatsApp UX)

**Example Flow:**
```
Bot: What are you planning?
     1. Birthday
     2. Dinner
     3. Workshop
     4. Corporate
     5. Pop-up
     6. Other

User: 1

Bot: Great! When do you need it?
     [Calendar image with March dates]
     Reply with date (e.g., "March 8")
```

### Instagram DM (Tertiary)

**Story-Style Tap-Through:**
- Limited to 3-4 interactions before handoff
- Each message is a "story card" (image + buttons)
- Quick decisions only (no typing)
- Final step: "Tap to complete booking on web" link

**Flow:**
```
[Story Card 1]: Event type selection (tap icon)
       ↓
[Story Card 2]: Date selection (tap date on image)
       ↓
[Story Card 3]: Guest count (tap range)
       ↓
[Story Card 4]: "Complete your booking" → Web link
```

---

## 5. Technical Recommendations

### Frontend Stack

| Component | Recommendation | Rationale |
|-----------|---------------|-----------|
| Framework | React 18+ | Component-based, ecosystem |
| Animations | Framer Motion | Spring physics, gesture support |
| Styling | Tailwind CSS | Rapid iteration, consistency |
| Icons | Lucide React | Clean, consistent iconography |
| Calendar | react-day-picker | Customizable, accessible |
| Slider | Radix UI Slider | Accessible, customizable |

### Backend & Integrations

| Service | Purpose | Integration Point |
|---------|---------|-------------------|
| **Shopify Storefront API** | Payments, checkout | Widget 5 payment processing |
| **Airtable** | Booking data, availability | Real-time sync for calendar |
| **n8n / Make** | Automation workflows | Confirmation emails, calendar invites |
| **Twilio** | WhatsApp fallback | Message routing |
| **Instagram Graph API** | DM responses | Webhook handling |

### Data Model (Simplified)

```typescript
interface Booking {
  id: string;
  eventType: 'birthday' | 'dinner' | 'workshop' | 'corporate' | 'pop-up' | 'other';
  date: Date;
  startTime: string;
  duration: number; // hours
  guestCount: number;
  rooms: Room[];
  addOns: AddOn[];
  totalAmount: number;
  status: 'draft' | 'confirmed' | 'paid' | 'cancelled';
  customer: Customer;
}

interface Room {
  id: string;
  name: string;
  capacity: number;
  hourlyRate: number;
}

interface AddOn {
  id: string;
  name: string;
  type: 'per_guest' | 'flat';
  price: number;
}
```

---

## 6. User Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ENTRY POINTS                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   Web    │  │ WhatsApp │  │ Instagram│  │  Direct  │            │
│  │  Chat    │  │   DM     │  │    DM    │  │   Link   │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       └─────────────┴─────────────┴─────────────┘                   │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  WIDGET 1: Onboarding│                                │
│              │  Select event type   │                                │
│              └──────────┬──────────┘                                │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  WIDGET 2: Calendar  │                                │
│              │  Date + time selection│                               │
│              └──────────┬──────────┘                                │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  WIDGET 3: Capacity  │                                │
│              │  Guests + rooms      │                                │
│              └──────────┬──────────┘                                │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  WIDGET 4: Add-ons   │                                │
│              │  Equipment/services  │                                │
│              └──────────┬──────────┘                                │
│                         │                                           │
│                         ▼                                           │
│              ┌─────────────────────┐                                │
│              │  WIDGET 5: Payment   │                                │
│              │  Quote + checkout    │                                │
│              └──────────┬──────────┘                                │
│                         │                                           │
│            ┌────────────┼────────────┐                              │
│            ▼            ▼            ▼                              │
│      ┌─────────┐  ┌─────────┐  ┌─────────┐                         │
│      │ Success │  │ Waitlist│  │ Abandon │                         │
│      │ Booking │  │  Offer  │  │  Save   │                         │
│      │confirmed│  │         │  │  Draft  │                         │
│      └─────────┘  └─────────┘  └─────────┘                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Edge Cases & Error Handling

### No Availability
```
┌─────────────────────────────────────────┐
│  That date is fully booked              │
│                                         │
│  [Join waitlist]  [View nearby dates]   │
│                                         │
│  Alternative dates with availability:   │
│  [Mar 9] [Mar 10] [Mar 15]              │
└─────────────────────────────────────────┘
```

### Capacity Exceeded
```
┌─────────────────────────────────────────┐
│  35 guests exceeds our maximum (30)     │
│                                         │
│  Options:                               │
│  • Reduce to 30 guests                  │
│  • Contact us for custom arrangement    │
│  • View alternative venues              │
└─────────────────────────────────────────┘
```

### Payment Failed
```
┌─────────────────────────────────────────┐
│  ⚠️ Payment could not be processed      │
│                                         │
│  [Try again]  [Use different card]      │
│                                         │
│  Your booking is held for 15 minutes    │
└─────────────────────────────────────────┘
```

### Session Timeout
```
┌─────────────────────────────────────────┐
│  ⏰ Your session expired                │
│                                         │
│  We've saved your progress.             │
│  [Resume booking]  [Start fresh]        │
└─────────────────────────────────────────┘
```

---

## 8. Accessibility Requirements

- All interactive elements: minimum 44×44px touch target
- Color not sole indicator (icons + patterns for availability)
- Screen reader labels for all icons
- Keyboard navigation support (Tab, Enter, Arrow keys)
- Reduced motion preference respected
- High contrast mode support

---

## 9. Analytics Events

| Event | Trigger | Data |
|-------|---------|------|
| `booking_started` | Widget 1 appears | platform, referrer |
| `event_type_selected` | Tap on event icon | event_type |
| `date_selected` | Tap on calendar date | date, availability_status |
| `time_slot_selected` | Tap on time slot | slot_type, duration |
| `guest_count_changed` | Slider movement | guest_count |
| `room_toggled` | Tap room toggle | room_id, action |
| `addon_toggled` | Tap add-on chip | addon_id, action |
| `quote_expanded` | Tap "View quote" | total_amount |
| `tc_accepted` | Check T&C | — |
| `payment_initiated` | Tap payment button | method |
| `booking_completed` | Payment success | total, items |
| `booking_abandoned` | 5min inactivity | last_widget |

---

## 10. Implementation Checklist

### Phase 1: Core Flow
- [ ] Widget 1: Event type selector
- [ ] Widget 2: Calendar + time slots
- [ ] Widget 3: Capacity slider + room selector
- [ ] Widget 4: Add-on chips
- [ ] Widget 5: Quote + payment
- [ ] Inline editing (pills)
- [ ] Predictive defaults

### Phase 2: Polish
- [ ] Animations (Framer Motion)
- [ ] Voice fallback
- [ ] Error states
- [ ] Loading states
- [ ] Success confetti

### Phase 3: Multi-platform
- [ ] WhatsApp simplified flow
- [ ] Instagram story-style flow
- [ ] Web sidebar progress

### Phase 4: Integrations
- [ ] Shopify payment
- [ ] Airtable sync
- [ ] n8n automation
- [ ] Calendar invites
- [ ] Confirmation emails

---

## Appendix: Quick Reference

### Color Palette
```
Primary:    #1a1a1a (near black)
Secondary:  #666666 (gray)
Accent:     #ff6b6b (coral)
Success:    #22c55e (green)
Warning:    #f59e0b (amber)
Error:      #ef4444 (red)
Background: #fafafa (off-white)
Surface:    #ffffff (white)
```

### Typography Scale
```
Heading:    24px / 32px line / 600 weight
Subheading: 18px / 24px line / 500 weight
Body:       16px / 24px line / 400 weight
Caption:    14px / 20px line / 400 weight
Small:      12px / 16px line / 500 weight
```

### Spacing Scale
```
xs:  4px
sm:  8px
md:  16px
lg:  24px
xl:  32px
2xl: 48px
```

---

*End of Specification*

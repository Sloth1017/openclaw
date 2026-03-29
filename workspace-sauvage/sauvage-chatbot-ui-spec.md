# Sauvage Space Chatbot UI/UX Specification

## Overview

This document defines the interactive widget specifications for the Sauvage Space booking chatbot. The goal is to minimize typing through tap-to-select interfaces while maintaining graceful fallbacks for all platforms.

---

## Widget Specifications

### 1. Event Type Selector

**Purpose:** Allow users to quickly select their event category from visual options.

#### Trigger
- **Phrase:** "What type of event?", "What are you celebrating?", "event type"
- **Stage:** Initial booking flow, after greeting/availability check
- **Keyword triggers:** "birthday", "party", "meeting", "workshop", "corporate"

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  What type of event?        │
│  ─────────────────────────  │
│  🎂 🎉 💼 🎨 🍽️ 🎤 ❓       │
│  Birth Corporate Workshop   │
│  day   Event              │
│                             │
│  [See all 8 options →]      │
└─────────────────────────────┘
```

- 2x2 or 3x2 grid of cards (60x60px touch targets)
- Icon + label below
- "See all" expands to 3x3 grid
- Selected state: filled background, checkmark overlay

#### Interaction Pattern
1. User taps event type card
2. Card animates (scale 0.95 → 1.05 → 1.0, 200ms)
3. Checkmark appears with 150ms fade
4. Auto-advance to next question after 500ms delay
5. Swipe left/right for carousel alternative

#### Fallback
```
Bot: What type of event are you planning?
Options: Birthday, Corporate, Workshop, Dinner, 
         Performance, Other (or type your own)
```

#### Data Format
```json
{
  "widget": "event_type_selector",
  "selection": "birthday",
  "display": "🎂 Birthday Party",
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 2. Date & Time Picker

**Purpose:** Visual calendar and time slot selection with availability indicators.

#### Trigger
- **Phrase:** "When would you like to book?", "Pick a date", "calendar"
- **Stage:** After event type selection
- **Keyword triggers:** "date", "when", "available", "calendar"

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  📅 March 2026              │
│  ← Su Mo Tu We Th Fr Sa →   │
│     1  2  3  4  5  6  7     │
│  8  9 10 11 12 13 14        │
│  15 16 17 18 19 20 21       │
│  22 23 [24] 25 26 27 28     │
│  29 30 31                   │
│  ─────────────────────────  │
│  ⏰ Available slots:        │
│  🟢 10:00  🟢 14:00         │
│  🟡 18:00  🔴 20:00         │
│  ─────────────────────────  │
│  Duration: [━━━●━━━━] 4h    │
└─────────────────────────────┘
```

- Mini calendar (280px wide, 44px day cells)
- Color-coded availability:
  - 🟢 Green: Fully available
  - 🟡 Yellow: Limited availability (<30% slots)
  - 🔴 Red: Fully booked
  - ⚫ Gray: Past dates / blocked
- Time slots in 2-hour increments
- Duration slider: 2h to 12h range

#### Interaction Pattern
1. User taps date → highlights with ring animation
2. Available time slots populate below
3. User taps time slot → fills with brand color
4. Duration slider updates end time in real-time
5. "Confirm" button activates when valid selection

#### Fallback
```
Bot: What date works for you? (e.g., March 24, 2026)
User: March 24
Bot: Great! What time? Morning (9-12), Afternoon (12-18), 
     Evening (18-23), or specify exact time?
```

#### Data Format
```json
{
  "widget": "date_time_picker",
  "date": "2026-03-24",
  "start_time": "18:00",
  "duration_hours": 4,
  "end_time": "22:00",
  "availability_status": "limited",
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 3. Guest Counter

**Purpose:** Visual stepper for guest count with capacity warnings.

#### Trigger
- **Phrase:** "How many guests?", "Number of people", "headcount"
- **Stage:** After date/time selection
- **Keyword triggers:** "people", "guests", "attendees", "how many"

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  How many guests?           │
│  ─────────────────────────  │
│                             │
│    ┌─────┐ ┌───┐ ┌─────┐   │
│    │  −  │ │25 │ │  +  │   │
│    └─────┘ └───┘ └─────┘   │
│                             │
│  ━━━━━━━━━━━━━━━━░░░░░░░░   │
│  25/30 capacity             │
│                             │
│  ⚠️ 5 spots left!           │
│                             │
└─────────────────────────────┘
```

- Large central number (48px font)
- Minus/Plus buttons (56px touch targets)
- Progress bar showing capacity fill:
  - 0-70%: Green
  - 70-90%: Yellow + warning text
  - 90-100%: Red + urgent message
- Haptic feedback on each press (if supported)

#### Interaction Pattern
1. Long-press +/- for rapid increment (100ms intervals)
2. Number animates with spring physics
3. Progress bar fills smoothly
4. Warning appears at 21+ guests
5. Max limit at 30 (button disables with shake animation)
6. Auto-suggest room bundle at 15+ guests

#### Fallback
```
Bot: How many guests will be attending? (Max 30)
User: 25
Bot: ✅ Got it! 25 guests. Note: You're at 83% capacity.
```

#### Data Format
```json
{
  "widget": "guest_counter",
  "guest_count": 25,
  "capacity_percentage": 83,
  "capacity_status": "warning",
  "recommended_rooms": ["upstairs", "kitchen", "cave"],
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 4. Room Selector

**Purpose:** Visual room selection with capacity indicators and bundle pricing.

#### Trigger
- **Phrase:** "Which rooms?", "Select spaces", "room options"
- **Stage:** After guest count (or auto-suggested based on count)
- **Keyword triggers:** "room", "space", "area", "upstairs", "kitchen", "cave"

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  Select your spaces         │
│  ─────────────────────────  │
│                             │
│  ┌─────────────────────┐   │
│  │ [📷 Entrance Hall]  │   │
│  │ ✓ Selected         │   │
│  │ Capacity: 15        │   │
│  │ €50/hr              │   │
│  └─────────────────────┘   │
│                             │
│  ┌─────────────────────┐   │
│  │ [📷 Upstairs]       │   │
│  │ ○ Tap to add        │   │
│  │ Capacity: 20        │   │
│  │ €75/hr              │   │
│  └─────────────────────┘   │
│                             │
│  ┌─────────────────────┐   │
│  │ [📷 Kitchen]        │   │
│  │ [📷 Cave]           │   │
│  └─────────────────────┘   │
│                             │
│  💰 Bundle discount: -€25   │
│  [✓ Confirm Selection]      │
└─────────────────────────────┘
```

- Photo cards with overlay info
- Checkmark toggle on each card
- Real-time bundle discount calculation
- "Recommended" badge for optimal combinations
- Floor plan view toggle (alternative to cards)

#### Interaction Pattern
1. User taps room card → toggles selection
2. Card lifts with shadow (elevation animation)
3. Running total updates in header
4. Bundle discount highlights when 3+ rooms selected
5. Capacity math shown: "Combined capacity: 45"
6. Warning if selected capacity < guest count

#### Fallback
```
Bot: Which rooms would you like?
1. Entrance Hall (15 people) - €50/hr
2. Upstairs (20 people) - €75/hr  
3. Kitchen (10 people) - €40/hr
4. Cave (15 people) - €45/hr

Reply with numbers (e.g., "1,2,4") or names
```

#### Data Format
```json
{
  "widget": "room_selector",
  "selected_rooms": ["entrance", "upstairs", "cave"],
  "total_capacity": 50,
  "hourly_rate": 170,
  "bundle_discount": 25,
  "final_hourly_rate": 145,
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 5. Add-on Checklist

**Purpose:** Toggle-based selection of additional services with running total.

#### Trigger
- **Phrase:** "Any add-ons?", "Extras", "Additional services"
- **Stage:** After room selection
- **Keyword triggers:** "add-on", "extra", "dishware", "staff", "projector"

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  Add extras                 │
│  ─────────────────────────  │
│                             │
│  🍽️ Dishware           ━━●  │
│     Plates, cutlery, etc.   │
│     +€25                    │
│                             │
│  🥂 Glassware              │
│     ○ Stemless      ● Stem │
│     +€15              +€20 │
│                             │
│  👨‍💼 Staff Support    ━━●  │
│     Setup & breakdown       │
│     +€75                    │
│                             │
│  📽️ Projector          ━○  │
│     +€35                    │
│                             │
│  ─────────────────────────  │
│  Running total: +€120       │
│  [Continue →]               │
└─────────────────────────────┘
```

- Toggle switches (iOS-style or Material)
- Radio buttons for mutually exclusive options (glassware)
- Price shown inline
- Running total sticky at bottom
- Grouped by category (Serve → Support → Tech)

#### Interaction Pattern
1. Toggle animates on tap (300ms slide)
2. Price adds to running total with count-up animation
3. Mutually exclusive options auto-deselect others
4. "Skip" button always available
5. Smart defaults based on event type:
   - Birthday: Dishware + Stemless
   - Corporate: Projector + Staff

#### Fallback
```
Bot: Would you like any add-ons?
• Dishware set (+€25) - Reply DISH
• Glassware: Stemless (+€15) or Stem (+€20)
• Staff support (+€75) - Reply STAFF  
• Projector (+€35) - Reply PROJECTOR
• None - Reply SKIP
```

#### Data Format
```json
{
  "widget": "addon_checklist",
  "selections": {
    "dishware": true,
    "glassware_type": "stem",
    "glassware_price": 20,
    "staff_support": true,
    "projector": false
  },
  "addon_total": 120,
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 6. Attribution Selector

**Purpose:** Clean selection of how the user found Sauvage Space.

#### Trigger
- **Phrase:** "How did you hear about us?", "Where did you find us?"
- **Stage:** Near end of booking flow (pre-quote)
- **Keyword triggers:** "found you", "hear about", "referral"

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  How did you find us?       │
│  ─────────────────────────  │
│                             │
│  ┌─────────────────────┐   │
│  │ 📷 Instagram        │   │
│  └─────────────────────┘   │
│  ┌─────────────────────┐   │
│  │ 🔍 Google Search    │   │
│  └─────────────────────┘   │
│  ┌─────────────────────┐   │
│  │ 👤 Referral by...   │   │
│  │    Greg  Dorian  Bart│   │
│  └─────────────────────┘   │
│  ┌─────────────────────┐   │
│  │ 💬 Word of mouth    │   │
│  └─────────────────────┘   │
│  ┌─────────────────────┐   │
│  │ ✏️ Other...         │   │
│  └─────────────────────┘   │
│                             │
└─────────────────────────────┘
```

- Clean list with icons
- Referral expands to show specific people
- "Other" opens text input
- Single selection only

#### Interaction Pattern
1. Tap selects and highlights
2. Referral choice shows sub-options
3. "Other" reveals text field with auto-focus
4. Selection persists visually
5. Auto-advance on selection (except "Other")

#### Fallback
```
Bot: How did you hear about Sauvage Space?
Reply: Instagram, Google, Word of mouth, or tell me more
```

#### Data Format
```json
{
  "widget": "attribution_selector",
  "source": "referral",
  "referral_person": "Greg",
  "custom_text": null,
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 7. Quote Summary Card

**Purpose:** Expandable breakdown of all costs, discounts, and payment terms.

#### Trigger
- **Phrase:** "Here's your quote", "Booking summary", "Total cost"
- **Stage:** After all selections complete
- **Auto-trigger:** When all required fields populated

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  📋 Booking Summary         │
│  ─────────────────────────  │
│                             │
│  🎂 Birthday Party          │
│  📅 March 24, 6:00 PM       │
│  👥 25 guests (4 hours)     │
│                             │
│  Rooms              €580    │
│  ├─ Entrance        €200    │
│  ├─ Upstairs        €300    │
│  ├─ Cave            €180    │
│  └─ Bundle discount -€100   │
│                             │
│  Add-ons            €120    │
│  ├─ Dishware         €25    │
│  ├─ Glassware        €20    │
│  └─ Staff            €75    │
│                             │
│  ─────────────────────────  │
│  Subtotal           €700    │
│  Deposit (50%)      €350    │
│                             │
│  [📄 Full PDF] [✓ Accept]   │
└─────────────────────────────┘
```

- Collapsible sections (Rooms, Add-ons)
- Sticky totals at bottom
- Deposit amount highlighted
- PDF download option
- Edit links for each section

#### Interaction Pattern
1. Sections expand/collapse on header tap
2. Line items show tooltip on long-press
3. "Edit" returns to relevant widget
4. Swipe to see alternative quote options
5. Accept button activates T&C widget

#### Fallback
```
Bot: Here's your quote:

Birthday Party - March 24, 6-10 PM
25 guests

Rooms: €580 (Entrance, Upstairs, Cave)
Add-ons: €120 (Dishware, Glassware, Staff)
─────────────
Total: €700
Deposit (50%): €350

Reply ACCEPT to proceed or EDIT to change
```

#### Data Format
```json
{
  "widget": "quote_summary",
  "quote_id": "Q-20260324-001",
  "event_type": "birthday",
  "date": "2026-03-24",
  "duration_hours": 4,
  "guest_count": 25,
  "line_items": [
    {"type": "room", "name": "Entrance", "amount": 200},
    {"type": "room", "name": "Upstairs", "amount": 300},
    {"type": "room", "name": "Cave", "amount": 180},
    {"type": "discount", "name": "Bundle discount", "amount": -100},
    {"type": "addon", "name": "Dishware", "amount": 25},
    {"type": "addon", "name": "Glassware", "amount": 20},
    {"type": "addon", "name": "Staff", "amount": 75}
  ],
  "subtotal": 700,
  "deposit_amount": 350,
  "currency": "EUR",
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 8. T&C Acceptance

**Purpose:** Checkbox with terms preview and agreement confirmation.

#### Trigger
- **Phrase:** "Please accept our terms", "Terms and conditions"
- **Stage:** After quote acceptance intent
- **Prerequisite:** Quote summary viewed

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  Terms & Conditions         │
│  ─────────────────────────  │
│                             │
│  ┌─────────────────────┐   │
│  │ 📄 Preview          │   │
│  │                     │   │
│  │ • Cancellation: 48h │   │
│  │ • Damage liability  │   │
│  │ • Noise policy      │   │
│  │ • ...               │   │
│  │                     │   │
│  │ [Read full →]       │   │
│  └─────────────────────┘   │
│                             │
│  ┌─────────────────────┐   │
│  │ ☐ I agree to the    │   │
│  │   Terms & Conditions│   │
│  │   and House Rules   │   │
│  └─────────────────────┘   │
│                             │
│  [I Agree - €350]           │
│  (disabled until checked)   │
└─────────────────────────────┘
```

- Scrollable preview of key terms
- "Read full" opens modal/overlay
- Checkbox with label
- Payment button disabled until checked
- Button shows amount due

#### Interaction Pattern
1. User scrolls through preview
2. Checkbox tap enables payment button
3. Button animates from gray to brand color
4. Long-press on preview opens full terms
5. Back button returns to quote if needed

#### Fallback
```
Bot: To proceed, please accept our terms:
• 48-hour cancellation policy
• You're responsible for damages
• Noise curfew at 11 PM

Reply AGREE to accept or TERMS for full details
```

#### Data Format
```json
{
  "widget": "terms_acceptance",
  "accepted": true,
  "terms_version": "2026.1",
  "acceptance_timestamp": "2026-03-24T16:20:00Z",
  "ip_address": "...",
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 9. Payment Button

**Purpose:** Direct Shopify Pay integration with amount display.

#### Trigger
- **Phrase:** "Ready to pay", "Complete booking", "Payment"
- **Stage:** After T&C acceptance
- **Auto-trigger:** When terms checkbox checked

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  Complete Your Booking      │
│  ─────────────────────────  │
│                             │
│  Deposit Due                │
│  ─────────────────────────  │
│                             │
│         €350.00             │
│                             │
│  ┌─────────────────────┐   │
│  │   [Shop Pay Logo]   │   │
│  │                     │   │
│  │   Pay €350.00       │   │
│  │                     │   │
│  │   🔒 Secure checkout│   │
│  └─────────────────────┘   │
│                             │
│  [💳 Other payment methods] │
│                             │
│  You'll receive confirmation│
│  immediately after payment  │
└─────────────────────────────┘
```

- Large amount display
- Shopify Pay button (branded)
- Alternative payment accordion
- Security indicators
- Post-payment expectation set

#### Interaction Pattern
1. Button pulses subtly to draw attention
2. Tap opens Shopify Pay modal/overlay
3. Loading state during processing
4. Success: Confetti animation + confirmation
5. Failure: Error message with retry option

#### Fallback
```
Bot: Ready to pay your €350 deposit?

I'll send you a secure payment link:
https://sauvagespace.shopify.com/pay/...

Or reply PAY for alternative methods
```

#### Data Format
```json
{
  "widget": "payment_button",
  "amount": 350.00,
  "currency": "EUR",
  "payment_method": "shopify_pay",
  "status": "initiated",
  "shopify_checkout_url": "https://...",
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

### 10. Arrival Time Selector

**Purpose:** Quick time picker triggered by arrival-related keywords.

#### Trigger
- **Phrase:** "When will you arrive?", "Setup time?"
- **Keyword triggers:** "arrive", "arrival", "get there", "setup", "coming at"
- **Context:** Can trigger mid-conversation

#### Visual Layout (Mobile-First)
```
┌─────────────────────────────┐
│  What time will you arrive? │
│  ─────────────────────────  │
│                             │
│     ┌───┐ ┌───┐ ┌───┐      │
│     │ ↑ │ │ ↑ │ │ ↑ │      │
│     ├───┤ ├───┤ ├───┤      │
│     │ 5 │ │ : │ │30 │      │
│     ├───┤ ├───┤ ├───┤      │
│     │ ↓ │ │ ↓ │ │ ↓ │      │
│     └───┘ └───┘ └───┘      │
│      hr   :   min          │
│                             │
│  Quick picks:               │
│  [5:00] [5:30] [6:00]       │
│                             │
│  (Event starts at 6:00 PM)  │
│                             │
│  [✓ Confirm]                │
└─────────────────────────────┘
```

- Spinner-style time picker
- Quick-pick chips for common times
- Contextual note showing event start time
- 15-minute increments
- AM/PM toggle if needed

#### Interaction Pattern
1. User types "arrive at 5:30" → widget appears
2. Spinner defaults to 30 min before event
3. Swipe up/down on columns to change
4. Quick-pick chips set spinner instantly
5. Confirm validates (must be before event start)

#### Fallback
```
Bot: What time will you arrive to set up?
(Event starts at 6:00 PM)

Reply with time (e.g., "5:30" or "30 min before")
```

#### Data Format
```json
{
  "widget": "arrival_time_selector",
  "arrival_time": "17:30",
  "event_start_time": "18:00",
  "setup_duration_minutes": 30,
  "trigger_keyword": "arrive",
  "timestamp": "2026-03-24T16:20:00Z"
}
```

---

## Progressive Disclosure Strategy

### Phase 1: Discovery (Always Visible)
- Event Type Selector
- Date & Time Picker (calendar only, expand for times)

### Phase 2: Details (Reveal After Basics)
- Guest Counter (appears after date selected)
- Room Selector (appears after guest count)

### Phase 3: Enhancement (Contextual)
- Add-on Checklist (appears after room selection)
- Arrival Time Selector (on-demand or auto at end)

### Phase 4: Conversion (Final Steps)
- Attribution Selector (pre-quote)
- Quote Summary Card
- T&C Acceptance
- Payment Button

### Smart Defaults
- Skip Room Selector if <10 guests → auto-suggest Upstairs
- Skip Add-ons if Corporate event → auto-include projector
- Show Arrival Time if event type = "workshop" or "corporate"

---

## Accessibility Considerations

### WCAG 2.1 AA Compliance

| Feature | Implementation |
|---------|---------------|
| Touch targets | Minimum 44x44px |
| Color contrast | 4.5:1 for text, 3:1 for UI components |
| Focus indicators | Visible focus rings on all interactive elements |
| Screen reader | ARIA labels on all icons, `aria-expanded` for collapsibles |
| Motion | `prefers-reduced-motion` media query support |
| Error states | Clear visual + text feedback, not color-only |

### Specific Widget Notes

**Event Type Selector:**
- Icons have `aria-label` with full event type name
- Selected state announced: "Birthday Party, selected"

**Date & Time Picker:**
- Calendar grid uses `role="grid"` with `aria-selected`
- Availability colors paired with text labels

**Guest Counter:**
- Number announced on each change
- Warning announced at 21+ guests

**Room Selector:**
- Images have descriptive alt text
- Capacity announced with room name

**Payment Button:**
- Loading state announced
- Success/failure announced with next steps

---

## Platform Differences

### WhatsApp Limitations

| Feature | WhatsApp | Web Chat |
|---------|----------|----------|
| Rich widgets | ❌ List/buttons only | ✅ Full widgets |
| Images in widgets | ⚠️ Limited | ✅ Full support |
| Animations | ❌ None | ✅ CSS/JS animations |
| Real-time updates | ⚠️ New message only | ✅ Live DOM updates |
| Payment integration | ⚠️ External link | ✅ Embedded checkout |

### WhatsApp Fallback Strategy

```
WhatsApp Implementation:
- Use Interactive Messages (buttons/lists)
- Send images as separate messages
- Use numbered options for selection
- External link for payment
- Simple text confirmations

Example WhatsApp flow:
Bot: What type of event?
[Button: Birthday] [Button: Corporate]
[Button: Workshop] [Button: Other]

User taps "Birthday"
Bot: Great! How many guests?
[Button: 10-15] [Button: 16-25]
[Button: 26-30] [Button: Type number]
```

### Web Chat Advantages
- Full widget rendering
- Real-time price calculations
- Embedded payment flow
- Rich media (floor plans, room photos)
- Persistent state across widgets

---

## Implementation Notes for Developers

### Tech Stack Recommendations

```javascript
// Widget Framework
{
  "frontend": "React/Vue component library",
  "styling": "Tailwind CSS + CSS Modules",
  "animations": "Framer Motion (React) or GSAP",
  "icons": "Lucide React or Heroicons",
  "state": "Zustand or Redux Toolkit"
}
```

### Widget Component Structure

```typescript
interface WidgetProps {
  // Core
  widgetId: string;
  conversationId: string;
  
  // Data
  initialData?: Record<string, any>;
  context?: BookingContext;
  
  // Callbacks
  onSubmit: (data: WidgetData) => void;
  onCancel: () => void;
  onEdit: (field: string) => void;
  
  // Platform
  platform: 'web' | 'whatsapp' | 'telegram';
  
  // Accessibility
  ariaLabel?: string;
  autoFocus?: boolean;
}

interface WidgetData {
  widget: string;
  selection: any;
  timestamp: string;
  metadata?: Record<string, any>;
}
```

### State Management

```typescript
// Booking flow state machine
type BookingState = 
  | 'idle'
  | 'selecting_event_type'
  | 'selecting_date_time'
  | 'selecting_guests'
  | 'selecting_rooms'
  | 'selecting_addons'
  | 'selecting_attribution'
  | 'reviewing_quote'
  | 'accepting_terms'
  | 'processing_payment'
  | 'confirmed';

// Widget registry
const widgets: Record<string, WidgetComponent> = {
  event_type_selector: EventTypeSelector,
  date_time_picker: DateTimePicker,
  guest_counter: GuestCounter,
  // ... etc
};
```

### API Integration

```typescript
// Widget data submission
async function submitWidgetData(
  conversationId: string,
  widgetData: WidgetData
): Promise<BotResponse> {
  const response = await fetch('/api/chat/widget-submit', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      conversation_id: conversationId,
      widget_data: widgetData
    })
  });
  
  return response.json(); // Next widget or message
}
```

### Error Handling

```typescript
// Widget error boundary
interface WidgetError {
  type: 'validation' | 'network' | 'timeout' | 'platform_unsupported';
  message: string;
  fallbackText: string;
  retryable: boolean;
}

// Fallback trigger
if (platform === 'whatsapp' || widgetFailed) {
  return <TextFallback options={widgetOptions} />;
}
```

### Analytics Events

```typescript
// Track widget interactions
interface WidgetAnalytics {
  event: 'widget_rendered' | 'widget_interacted' | 'widget_completed' | 'widget_abandoned';
  widget: string;
  conversation_id: string;
  duration_ms: number;
  interaction_count: number;
  platform: string;
}
```

### Testing Checklist

- [ ] All widgets render on mobile (320px width)
- [ ] Touch targets meet 44px minimum
- [ ] Screen reader announces selections
- [ ] Keyboard navigation works (Tab, Enter, Space)
- [ ] Reduced motion respected
- [ ] Fallbacks trigger on widget failure
- [ ] WhatsApp limited mode tested
- [ ] Payment flow end-to-end tested
- [ ] Analytics events fire correctly

---

## Appendix A: Quick Reference Card

| Widget | Trigger | Key Interaction | Fallback |
|--------|---------|-----------------|----------|
| Event Type | "What type?" | Tap card | Numbered list |
| Date & Time | "When?" | Calendar + slots | Text date/time |
| Guest Counter | "How many?" | +/- stepper | Text number |
| Room Selector | "Which rooms?" | Toggle cards | Numbered list |
| Add-on Checklist | "Any extras?" | Toggle switches | Keyword replies |
| Attribution | "How found us?" | Tap list item | Text reply |
| Quote Summary | Auto | Expand sections | Text breakdown |
| T&C Acceptance | Post-quote | Checkbox | Text AGREE |
| Payment Button | Post-T&C | Shopify Pay | Payment link |
| Arrival Time | "arrive" keyword | Spinner | Text time |

---

## Appendix B: Data Schema

```json
{
  "booking_request": {
    "event_type": "string",
    "date": "YYYY-MM-DD",
    "start_time": "HH:MM",
    "duration_hours": "number",
    "guest_count": "number",
    "rooms": ["string"],
    "addons": {
      "dishware": "boolean",
      "glassware_type": "stemless|stem|null",
      "staff_support": "boolean",
      "projector": "boolean"
    },
    "attribution": {
      "source": "string",
      "referral_person": "string|null"
    },
    "arrival_time": "HH:MM|null",
    "quote_accepted": "boolean",
    "terms_accepted": "boolean",
    "payment_status": "pending|completed|failed"
  }
}
```

---

*Document Version: 1.0*
*Last Updated: 2026-03-24*
*Owner: Sauvage Space Product Team*

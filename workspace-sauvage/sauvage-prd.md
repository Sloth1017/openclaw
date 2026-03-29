# Sauvage Space Booking Chatbot — Product Requirements Document

## Overview
A conversational booking system for Sauvage Space, a multi-purpose event venue in Amsterdam. The bot guides customers through event booking with minimal typing, visual selection, and smart defaults.

## Target User
- Private individuals planning birthdays, dinners, celebrations
- Businesses organizing workshops, corporate events, pop-ups
- Primarily mobile users (80%+), some desktop

## Success Metrics
- Time to book: < 90 seconds for simple bookings
- Tap count: < 15 taps for complete booking
- Abandonment rate: < 30% at any step
- Conversion rate: > 40% from inquiry to deposit

---

## User Flow

```
Entry → Event Type → Date/Time → Guests/Rooms → Add-ons → Quote → Payment → Confirmation
```

### Entry Points
- Website embed (iframe)
- Direct link (lovable.app/sauvage-booking)
- WhatsApp (fallback)

---

## Widget Specifications

### Widget 1: Event Type Selector
**Trigger:** Page load

**Visual:**
- Horizontal scrollable row
- 6 event type cards (64×64px touch target)
- Icon + label below
- Selected state: filled icon, scale 1.1x, subtle bounce

**Event Types:**
| Type | Icon | Predictive Defaults |
|------|------|---------------------|
| Birthday | 🎂 | Evening (19:00), 20 guests, Upstairs+Entrance |
| Dinner | 🍽️ | Evening (19:30), 12 guests, Downstairs |
| Workshop | 🎨 | Morning (09:00), 15 guests, Downstairs+Kitchen |
| Corporate | 💼 | Full day, 25 guests, Entire space, Projector |
| Pop-up | 🎪 | Flexible, 30 guests, All rooms |
| Other | ❓ | No defaults |

**Behavior:**
- Tap selects → 400ms delay → auto-advance to Widget 2
- Selected type appears as "pill" above next widget
- Store: `eventType`, `predictedGuests`, `predictedTime`

---

### Widget 2: Availability Calendar
**Trigger:** After event type selected

**Visual:**
- Month view calendar (7-column grid, 44px touch targets)
- Color-coded dates:
  - 🟢 Green: 3+ slots available
  - 🟡 Yellow: 1-2 slots remaining
  - 🔴 Red: Fully booked (disabled, shows waitlist)
  - ⚪ Gray: Past dates (disabled)
- Selected date: filled circle with checkmark
- Today: ring outline

**Time Slots (inline expansion after date tap):**
- Morning (8:00-12:00)
- Afternoon (12:00-17:00)
- Evening (17:00-23:00)
- Custom hours (opens time picker)

**Duration:**
- Auto-suggested based on event type
- Editable via dropdown (2h, 4h, 6h, 8h, Full day)

**Store:** `date`, `startTime`, `endTime`, `duration`

---

### Widget 3: Capacity Slider + Room Visualizer
**Trigger:** After date/time confirmed

**Visual:**
- Large guest count display (animated on change)
- Slider: 1-30 range, thick track (8px), large thumb (28px)
- Floor plan thumbnail showing rooms
- Room toggles as pills below

**Room Capacity:**
| Room | Capacity | Best For |
|------|----------|----------|
| Upstairs | 12 | Main events, dinners |
| Entrance | 8 | Reception, bar area |
| Kitchen | 6 | Cooking, catering prep |
| Cave | 10 | Wine tastings, intimate |

**Auto-recommendation logic:**
- 1-10 guests: Suggest Upstairs OR Downstairs
- 11-20 guests: Suggest Upstairs + Entrance
- 21-30 guests: Suggest Upstairs + Entrance (+ Kitchen if food involved)

**Behavior:**
- Slider movement updates recommendations in real-time
- Floor plan highlights recommended rooms
- Tap room pill to toggle on/off
- Visual feedback: selected rooms colored, unselected gray

**Store:** `guestCount`, `selectedRooms[]`

---

### Widget 4: Add-on Chips
**Trigger:** After rooms confirmed

**Visual:**
- Horizontal scroll of toggle chips
- Each chip: icon + label + price
- Selected chips appear below as "active pills"
- Running total in sticky footer

**Add-ons:**
| Add-on | Icon | Price | Auto-suggest |
|--------|------|-------|--------------|
| Glassware | 🍷 | €5/guest | Dinner, Birthday |
| Dishware | 🍽️ | €4/guest | Dinner, Workshop |
| Staff | 👤 | €150 | Corporate, >20 guests |
| Projector | 📽️ | €75 | Corporate, Workshop |
| Snacks | 🥐 | €8/guest | Morning events |
| Sound system | 🎵 | €100 | Pop-up, Birthday |

**Behavior:**
- Tap to toggle on/off
- Running total animates on change
- "View quote" button expands Widget 5 inline

**Store:** `selectedAddOns[]`, `addOnTotal`

---

### Widget 5: Quote + Pay Card
**Trigger:** After add-ons selected (or tap "View quote")

**Visual:**
- Expandable quote card (accordion style)
- Line items with calculations
- T&C checkbox (required)
- Payment buttons (appear after T&C checked)

**Quote Structure:**
```
Venue (Room 1 + Room 2)
  4 hours × €75/hr = €300

Add-ons
  Glassware (18) = €90
  Staff (1) = €150

Subtotal = €540
VAT (21%) = €113

Total = €653
```

**Payment Flow:**
1. User checks T&C checkbox
2. "Book Now" button becomes active
3. Tap → Shopify checkout opens
4. Success → booking confirmation card

**Store:** `quoteBreakdown`, `totalAmount`, `depositAmount`, `paymentStatus`

---

## Data Model

### Booking Object
```typescript
interface Booking {
  id: string;                    // Airtable record ID
  createdAt: timestamp;
  status: 'draft' | 'confirmed' | 'paid' | 'cancelled';
  
  // Event details
  eventType: string;
  date: date;
  startTime: string;
  endTime: string;
  duration: number;              // hours
  
  // Client info
  customerName: string;
  customerEmail: string;
  customerPhone: string;
  customerType: 'private' | 'business';
  
  // Booking details
  guestCount: number;
  selectedRooms: string[];
  selectedAddOns: AddOn[];
  
  // Pricing
  roomTotal: number;
  addOnTotal: number;
  bundleDiscount: number;
  vatAmount: number;
  totalAmount: number;
  depositAmount: number;
  
  // Tracking
  attribution: string;
  funnelStage: string;
}

interface AddOn {
  id: string;
  name: string;
  price: number;
  quantity: number;
}
```

---

## Error States

### No Availability
- Show: "That date is fully booked"
- Action: [Join waitlist] [View nearby dates]
- Display: 3 nearest available dates as buttons

### Capacity Exceeded (>30 guests)
- Show: "Maximum capacity is 30 guests"
- Action: [Reduce to 30] [Contact for custom]

### Payment Failed
- Show: "Payment could not be processed"
- Action: [Try again] [Different card]
- Hold: Booking reserved for 15 minutes

### Session Timeout (5 min inactivity)
- Show: "Your session expired"
- Action: [Resume booking] [Start fresh]
- Data: Auto-saved to localStorage

---

## Accessibility

- Minimum touch target: 44×44px
- Color not sole indicator (icons + text)
- Screen reader labels for all interactive elements
- Keyboard navigation (Tab, Enter, Arrow keys)
- Reduced motion preference respected

---

## Analytics Events

| Event | Trigger |
|-------|---------|
| booking_started | Widget 1 appears |
| event_type_selected | Tap on event icon |
| date_selected | Tap on calendar date |
| guest_count_changed | Slider movement |
| room_toggled | Tap room pill |
| addon_toggled | Tap add-on chip |
| quote_expanded | Tap "View quote" |
| tc_accepted | Check T&C |
| payment_initiated | Tap payment button |
| booking_completed | Payment success |
| booking_abandoned | 5min inactivity |

---

## Integrations

### Airtable
- Base: "Sauvage Bookings"
- Tables: Bookings, Customers, Waitlist, Analytics
- Sync: Real-time via API

### Shopify
- Products: "Event Deposit €50", "Kitchen Deposit €300"
- Checkout: Embedded buy button
- Webhook: Payment confirmation → Airtable

### n8n (Automation)
- Trigger: New booking created
- Actions: Send confirmation email, calendar invite, Slack notification

### Google Calendar
- Read: Check availability
- Write: Block booked dates

---

## Out of Scope (Future Versions)

- Instagram DM integration
- Telegram bot
- Advanced analytics dashboard
- Multi-language (Dutch translations)
- Recurring bookings
- Gift cards / vouchers

---

## Design References

- UI Style: Minimal, warm, professional
- Inspiration: Airbnb booking flow, Calendly, Typeform
- Components: 21st.dev, shadcn/ui
- Animations: Framer Motion (spring physics)

---

*Last updated: March 2026*

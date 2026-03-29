# Lovable Parallel Prototype Prompts

Use these 5 prompts to kick off simultaneous prototypes in Lovable. Run each in a separate project. Spend 2-3 hours per prototype, then pick the best foundation to iterate on.

---

## Prototype 1: Widget Flow & Navigation

**Goal:** Test the 5-step flow and state management

**Prompt:**
```
Build a booking flow for an event venue with 5 steps:

1. Event type selector - horizontal scroll with 6 cards (Birthday 🎂, Dinner 🍽️, Workshop 🎨, Corporate 💼, Pop-up 🎪, Other ❓). Each card has icon + label. Selected card scales up 1.1x with bounce animation.

2. Calendar picker - month view with color-coded dates (green = available, yellow = limited, red = booked). Tap date expands inline time slots (Morning, Afternoon, Evening, Custom).

3. Guest slider + rooms - slider 1-30 guests, floor plan showing 4 rooms (Upstairs, Entrance, Kitchen, Cave). Rooms highlight based on guest count. Tap room to toggle selection.

4. Add-on chips - horizontal scroll of toggle chips (Glassware, Dishware, Staff, Projector, Snacks). Selected chips show below. Running total in sticky footer.

5. Quote + payment - expandable quote card with line items, T&C checkbox, payment button.

Requirements:
- Smooth slide transitions between steps (Framer Motion)
- Each step shows as "pill" above for inline editing
- Store all selections in React state
- Mobile-first, 480px max-width
- Warm color palette: off-white background (#faf9f7), gold accent (#c4a77d), near-black text (#1a1a1a)

Use shadcn/ui components where possible. Focus on flow and animations, not real data yet.
```

---

## Prototype 2: Calendar Widget Deep Dive

**Goal:** Perfect the calendar and availability display

**Prompt:**
```
Build a production-ready calendar widget for venue booking:

Calendar features:
- Month view with 7-day grid
- Dates color-coded: green (available), yellow (1-2 slots left), red (booked), gray (past)
- Today highlighted with ring border
- Selected date filled with checkmark
- Swipe between months
- Minimum touch target 44px per date

Time slot selector (appears after date tap):
- 3 large cards: Morning (8-12), Afternoon (12-17), Evening (17-23)
- Each shows availability indicator
- "Custom hours" expands to time pickers
- Duration dropdown: 2h, 4h, 6h, 8h, Full day

Mock data:
- Some dates green, some yellow, some red
- Simulate availability changing based on selection

Visual design:
- Warm minimal aesthetic
- Inter font family
- Smooth spring animations (Framer Motion)
- Mobile-first, responsive

Bonus: Connect to mock Airtable API to fetch real availability data.
```

---

## Prototype 3: Room Visualizer & Capacity

**Goal:** Nail the room selection experience

**Prompt:**
```
Build an interactive room visualizer for event venue booking:

Guest slider:
- Large animated number display (1-30 guests)
- Thick slider track with large thumb
- Haptic feedback on snap points
- Real-time capacity warnings as approaching 30

Floor plan:
- Simplified 2D layout showing 4 rooms
- Upstairs (top), Entrance (bottom-left), Kitchen (bottom-right), Cave (side)
- Rooms color-coded when selected
- Tap room to toggle on/off
- Visual connection lines between selected rooms

Auto-recommendations:
- 1-10 guests: highlight Upstairs OR Entrance
- 11-20 guests: highlight Upstairs + Entrance
- 21-30 guests: highlight all main rooms

Room details panel:
- Shows when room selected
- Photo, capacity, description
- "Remove" button

Animations:
- Rooms fade in/out on selection
- Number counts up/down smoothly
- Floor plan subtly rearranges based on selection

Design:
- Warm beige/tan color palette
- 21st.dev components
- Mobile-first
```

---

## Prototype 4: Quote Card & Payment

**Goal:** Perfect the checkout experience

**Prompt:**
```
Build a quote and payment card for venue booking:

Quote card (accordion style):
- Header: "Quote Summary" with chevron, total amount
- Expanded shows line items:
  * Venue: Room 1 (4h × €75) = €300
  * Venue: Room 2 (4h × €60) = €240
  * Add-ons: Glassware (18 × €5) = €90
  * Add-ons: Staff = €150
  * Subtotal = €780
  * VAT (21%) = €164
  * Total = €944
- Each line item has tooltip explaining calculation
- Bundle discount shown as negative line item

T&C acceptance:
- Checkbox with linked "Terms & Conditions"
- Button disabled until checked
- Smooth transition to enabled state

Payment integration:
- Shopify Buy Button embed
- Or mock payment form with card fields
- Apple Pay / Google Pay buttons
- Loading state during processing
- Success animation (confetti)

Error states:
- Payment failed: retry button, error message
- Session expired: resume option

Visual:
- Clean, trustworthy design
- Large, bold total
- Secure payment indicators
- Warm gold accent for primary button
```

---

## Prototype 5: Airtable Integration & Admin

**Goal:** Test data flow and backend connections

**Prompt:**
```
Build a booking system with live Airtable integration:

Airtable setup:
- Base with Bookings table
- Fields: eventType, date, guestCount, rooms (array), addOns (array), totalAmount, customerName, customerEmail, status

Frontend:
- Simple form: event type dropdown, date picker, guest count, name, email
- Submit creates Airtable record
- Shows "Booking saved" confirmation

Real-time sync:
- Fetch booked dates from Airtable
- Block those dates in calendar
- Show availability based on Airtable data

Admin dashboard:
- List all bookings from Airtable
- Filter by status (draft, confirmed, paid)
- Search by customer name
- Quick stats: total bookings, revenue, upcoming events

Webhooks simulation:
- Mock n8n webhook trigger
- Show what data would be sent to automation

Requirements:
- Airtable personal access token (user provides)
- Error handling for API failures
- Loading states
- Mobile-responsive

Focus on data flow working end-to-end, not perfect UI.
```

---

## Evaluation Criteria

After 2-3 hours on each, score 1-5 on:

| Criteria | Weight | What to Look For |
|----------|--------|------------------|
| **Animation quality** | High | Smooth transitions, spring physics, no jank |
| **Code structure** | High | Clean components, good state management |
| **Mobile feel** | High | Touch-friendly, responsive, native-app-like |
| **Visual polish** | Medium | Matches design system, professional look |
| **Extensibility** | Medium | Easy to add features, modify flow |

**Pick the winner:** Combine best parts or iterate on highest-scoring prototype.

---

## Next Steps After Prototypes

1. **Merge best features** from winning prototypes
2. **Add real integrations:** Shopify payments, n8n webhooks
3. **WhatsApp bridge:** Twilio integration for fallback
4. **Polish:** Error states, loading, edge cases
5. **Test:** 5-10 real booking attempts
6. **Launch:** Deploy to Vercel, embed on website

---

*Prompts designed for Lovable.dev with vibe coding principles*

# Sauvage Space Booking Chatbot - Implementation Plan
## 2026 UX Edition | 10-Week Build Timeline

---

## Executive Summary

This implementation plan outlines a 10-week build for a multi-platform booking chatbot for Sauvage Space. The system features a 5-widget smart UI, integrates with Shopify for payments, Airtable for data management, and Google Calendar for availability, with automated notifications via n8n.

**Total Estimated Effort:** 320-400 hours  
**Team Composition:** 1 Full-stack Developer, 1 UI/UX Designer, 1 DevOps/Automation Engineer (part-time)

---

## Phase 1: Foundation (Week 1-2)

### Overview
Establish the technical foundation, data architecture, and initial UI scaffolding. This phase creates the backbone for all subsequent development.

### Week 1 Tasks

#### 1.1 Airtable Schema Design (16 hours)
**Owner:** Full-stack Developer + Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Design core tables structure | 4 | All 6 tables defined with field types |
| Create relationships and lookups | 3 | Linked records properly configured |
| Set up formula fields for pricing | 3 | Dynamic pricing calculations working |
| Create views for different user roles | 3 | Admin, staff, and public views ready |
| Document schema with ERD | 3 | Visual diagram + field descriptions |

**Dependencies:** None  
**Blockers:** Access to existing Sauvage business logic/pricing

#### 1.2 Shopify Storefront API Setup (12 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Create Shopify Partner account | 1 | Account verified and active |
| Set up development store | 2 | Store configured with test products |
| Create deposit products (x3 tiers) | 3 | Small/Medium/Large room deposits as separate products |
| Configure Storefront API access | 3 | API credentials generated, CORS configured |
| Test checkout flow via API | 3 | Successful test transaction in sandbox |

**Dependencies:** Shopify account credentials  
**Blockers:** Approval for Shopify Payments (if new account)

#### 1.3 React App Scaffold (12 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Initialize Next.js 14 project | 2 | TypeScript, Tailwind, App Router configured |
| Set up project structure | 2 | Folder architecture matches widget system |
| Install core dependencies | 2 | Framer Motion, React Query, Zustand installed |
| Configure environment variables | 2 | .env.local template with all required keys |
| Set up linting and formatting | 2 | ESLint, Prettier, Husky pre-commit hooks |
| Deploy to Vercel preview | 2 | CI/CD pipeline working, preview URL accessible |

**Dependencies:** Vercel account access  
**Blockers:** None

### Week 2 Tasks

#### 1.4 Widget 1: Onboarding MVP (20 hours)
**Owner:** Full-stack Developer + Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Design onboarding flow wireframes | 4 | 3-step flow: Occasion → Vibe → Contact |
| Build occasion selector component | 4 | Visual cards for: Meeting, Event, Photoshoot, Workshop, Private Dining |
| Build vibe selector component | 4 | Mood-based selection with imagery |
| Build contact capture form | 4 | Name, email, phone with validation |
| Implement state persistence | 4 | Progress saved to localStorage, URL shareable |

**Dependencies:** React scaffold complete  
**Blockers:** Finalized copy/content for occasion types

#### 1.5 Design System Foundation (12 hours)
**Owner:** UI/UX Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Define color palette | 3 | Primary, secondary, semantic colors documented |
| Create typography scale | 3 | Font families, sizes, weights defined |
| Build component library starter | 4 | Buttons, inputs, cards, modals in Storybook |
| Document animation principles | 2 | Framer Motion variants and timing specs |

**Dependencies:** Brand guidelines from Sauvage  
**Blockers:** None

### Phase 1 Deliverables

| Deliverable | Location | Status Criteria |
|-------------|----------|-----------------|
| Airtable Base | airtable.com | All tables created, sample data populated |
| Shopify Dev Store | myshopify.com | 3 deposit products live, API tested |
| React Repository | GitHub | Clean commit history, README, deployed preview |
| Widget 1 (Onboarding) | /onboarding | Functional 3-step flow, mobile-responsive |
| Design System v0.1 | Figma + Storybook | Core components documented |

### Phase 1 Testing Checklist

- [ ] Airtable API returns expected data structure
- [ ] Shopify Storefront API checkout creates draft order
- [ ] Onboarding flow completes without errors on mobile
- [ ] State persists after page refresh
- [ ] All form validations trigger correctly
- [ ] Preview deployment loads in <3 seconds

### Phase 1 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Shopify approval delays | High | Start with development store, use Shopify Payments test mode |
| Airtable rate limits | Medium | Implement caching layer early, use personal access tokens |
| Scope creep on onboarding | Medium | Lock feature set, mark enhancements as Phase 2+ |

---

## Phase 2: Core Booking Flow (Week 3-4)

### Overview
Build the heart of the booking experience: calendar integration, room selection, add-ons, and payment processing.

### Week 3 Tasks

#### 2.1 Widget 2: Calendar with Google Calendar Sync (24 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Set up Google Calendar API | 4 | OAuth 2.0 flow, calendar access granted |
| Build calendar UI component | 6 | Month view, date selection, unavailable dates greyed |
| Implement availability checker | 4 | Query Google Calendar for conflicts |
| Create time slot selector | 4 | Morning/Afternoon/Evening slots based on availability |
| Sync booking to Google Calendar | 4 | New bookings appear on Sauvage calendar |
| Handle timezone conversion | 2 | CET/CEST for Amsterdam, user timezone detection |

**Dependencies:** Google Calendar access credentials  
**Blockers:** Google Cloud Console project setup

#### 2.2 Widget 3: Capacity + Room Selection (20 hours)
**Owner:** Full-stack Developer + Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Build room cards component | 6 | Visual cards with capacity, amenities, pricing |
| Implement capacity calculator | 4 | Dynamic pricing based on guest count |
| Create room availability logic | 4 | Check room conflicts against selected date/time |
| Add room images and descriptions | 4 | Carousel/gallery for each room type |
| Build comparison view | 2 | Side-by-side room comparison option |

**Dependencies:** Airtable rooms data populated  
**Blockers:** Room photography/assets

### Week 4 Tasks

#### 2.3 Widget 4: Add-ons Selection (16 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Build add-ons grid component | 4 | Visual cards with pricing, quantity selectors |
| Create add-on categories | 3 | Catering, Equipment, Services tabs |
| Implement dynamic pricing | 4 | Real-time quote updates as add-ons change |
| Add conditional logic | 3 | Some add-ons only available with certain rooms |
| Build "recommended" suggestions | 2 | Smart suggestions based on occasion type |

**Dependencies:** Airtable add-ons data  
**Blockers:** Finalized add-on pricing and availability rules

#### 2.4 Widget 5: Quote + Payment (24 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Build quote summary component | 6 | Itemized breakdown, subtotal, deposit amount |
| Integrate Shopify checkout | 8 | Cart creation, checkout redirect, webhook handling |
| Create booking confirmation page | 4 | Success state, booking reference, next steps |
| Implement deposit logic | 4 | 50% deposit calculated, balance due displayed |
| Add cancellation policy display | 2 | Clear terms before payment |

**Dependencies:** Shopify products live, webhooks configured  
**Blockers:** Payment processor approval

#### 2.5 Inline Editing System (16 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Build edit mode toggle | 4 | Any widget can be reopened for editing |
| Implement state rollback | 4 | Changes don't affect downstream until confirmed |
| Create diff visualization | 4 | Show what's changed when editing |
| Add progress indicator | 4 | Visual stepper showing current position |

**Dependencies:** All 5 widgets functional  
**Blockers:** None

### Phase 2 Deliverables

| Deliverable | Location | Status Criteria |
|-------------|----------|-----------------|
| Calendar Widget | /booking/calendar | Date/time selection with Google Calendar sync |
| Room Selection | /booking/rooms | 3 room types with dynamic pricing |
| Add-ons Widget | /booking/addons | 15+ add-ons with categories |
| Payment Flow | /booking/payment | Shopify checkout integration |
| Inline Editing | Global | Any step editable without losing progress |
| End-to-end Booking | /booking | Complete flow from onboarding to confirmation |

### Phase 2 Testing Checklist

- [ ] Calendar blocks unavailable dates from Google Calendar
- [ ] Room pricing updates correctly with guest count changes
- [ ] Add-ons calculate correctly in real-time
- [ ] Shopify checkout creates order with correct deposit amount
- [ ] Booking appears in Google Calendar within 30 seconds
- [ ] Editing a previous step updates downstream pricing correctly
- [ ] All flows work on mobile devices
- [ ] Payment failure shows clear error and retry option

### Phase 2 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Google Calendar API quota | High | Implement aggressive caching, batch requests |
| Shopify webhook failures | High | Add retry logic, manual sync fallback |
| Complex pricing rules | Medium | Start with simple tiered pricing, iterate |
| Mobile performance | Medium | Lazy load images, optimize bundle size |

---

## Phase 3: Polish & Multi-platform (Week 5-6)

### Overview
Add delightful animations, then extend the booking experience to WhatsApp, Instagram, and Telegram.

### Week 5 Tasks

#### 3.1 Framer Motion Animations (20 hours)
**Owner:** Full-stack Developer + Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Page transition animations | 4 | Smooth slide/fade between widgets |
| Micro-interactions | 4 | Button hovers, card selections, loading states |
| Scroll-triggered reveals | 4 | Content animates in as user scrolls |
| Gesture animations | 4 | Swipe gestures for mobile navigation |
| Loading skeletons | 4 | Branded loading states instead of spinners |

**Dependencies:** All widgets built  
**Blockers:** None

#### 3.2 WhatsApp Integration via Twilio (20 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Set up Twilio account | 2 | WhatsApp Business API access granted |
| Configure webhook endpoint | 4 | /webhooks/whatsapp receives messages |
| Build conversation flow | 6 | NLP-based intent detection for booking queries |
| Create message templates | 4 | Welcome, availability, confirmation templates |
| Implement booking via chat | 4 | Complete flow without leaving WhatsApp |

**Dependencies:** Twilio account, WhatsApp Business verification  
**Blockers:** WhatsApp Business API approval (can take 1-2 weeks)

### Week 6 Tasks

#### 3.3 Instagram DM Flow (16 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Set up Meta Business account | 2 | Instagram Professional account connected |
| Configure Instagram Messaging API | 4 | Webhook for DM events |
| Build Instagram-specific flow | 6 | Optimized for visual-first platform |
| Implement quick replies | 4 | Rich media cards for rooms and add-ons |

**Dependencies:** Meta Business verification  
**Blockers:** Instagram API access approval

#### 3.4 Telegram Bot (12 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Create Telegram bot | 2 | @SauvageSpaceBot registered |
| Set up webhook | 3 | /webhooks/telegram endpoint configured |
| Build bot commands | 4 | /start, /book, /availability, /help |
| Implement booking flow | 3 | Inline keyboards for selections |

**Dependencies:** Telegram BotFather access  
**Blockers:** None (fastest to implement)

#### 3.5 Error States & Edge Cases (16 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Design error state components | 4 | Friendly, helpful error messages |
| Implement network error handling | 4 | Retry logic, offline detection |
| Add validation error states | 4 | Inline field errors, form-level errors |
| Create "sold out" flows | 4 | Waitlist option, alternative suggestions |

**Dependencies:** All platforms built  
**Blockers:** None

### Phase 3 Deliverables

| Deliverable | Location | Status Criteria |
|-------------|----------|-----------------|
| Animated Web Experience | /booking | 60fps animations, reduced-motion support |
| WhatsApp Bot | +31 XXX | Full booking flow via chat |
| Instagram DM | @sauvagespace | Rich media responses, quick replies |
| Telegram Bot | @SauvageSpaceBot | Complete booking via inline keyboards |
| Error Handling | Global | Graceful degradation on all platforms |

### Phase 3 Testing Checklist

- [ ] Animations run at 60fps on mid-range mobile devices
- [ ] Reduced-motion preference respected
- [ ] WhatsApp booking completes in under 5 minutes
- [ ] Instagram DM handles image-based room selection
- [ ] Telegram bot responds to all commands correctly
- [ ] Error messages are helpful and actionable
- [ ] Network interruption recovery works smoothly
- [ ] All platforms handle "room unavailable" gracefully

### Phase 3 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| WhatsApp API approval delay | High | Start application in Phase 1, build Telegram first |
| Animation performance | Medium | Test on low-end devices, provide disable option |
| Platform API changes | Medium | Abstract platform layer, version lock dependencies |
| Message template rejection | Medium | Submit templates early, have alternatives ready |

---

## Phase 4: Automation & Notifications (Week 7-8)

### Overview
Build the operational backbone: automated workflows, team notifications, and post-booking experiences.

### Week 7 Tasks

#### 4.1 n8n Workflow Setup (20 hours)
**Owner:** DevOps/Automation Engineer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Deploy n8n instance | 4 | Self-hosted or cloud instance running |
| Configure credentials | 4 | Airtable, Shopify, Google, email, SMS APIs |
| Build webhook listeners | 4 | Endpoints for all booking events |
| Create error monitoring | 4 | Failed workflows alert team |
| Document workflow structure | 4 | Visual diagrams, runbooks |

**Dependencies:** Server/hosting for n8n  
**Blockers:** None

#### 4.2 Smart Notifications to Team (16 hours)
**Owner:** DevOps/Automation Engineer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Design notification routing | 4 | Who gets what, when, via which channel |
| Build high-value booking alerts | 4 | Immediate SMS for bookings >€1000 |
| Create daily digest | 4 | Summary email of day's bookings |
| Implement escalation rules | 4 | Unconfirmed bookings trigger follow-up |

**Dependencies:** Team contact information  
**Blockers:** None

### Week 8 Tasks

#### 4.3 Confirmation Emails (12 hours)
**Owner:** DevOps/Automation Engineer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Design email templates | 4 | Branded, mobile-responsive, accessible |
| Build booking confirmation email | 4 | Sent immediately after payment |
| Build reminder emails | 4 | 24h before, day-of notifications |

**Dependencies:** Email service provider (SendGrid/Mailgun)  
**Blockers:** Domain authentication for email

#### 4.4 Calendar Invites (8 hours)
**Owner:** DevOps/Automation Engineer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Generate .ics files | 4 | Compatible with all major calendar apps |
| Attach to confirmation emails | 2 | Auto-add to customer calendar |
| Include booking details | 2 | Location, time, what to bring |

**Dependencies:** None  
**Blockers:** None

#### 4.5 Post-booking Automations (16 hours)
**Owner:** DevOps/Automation Engineer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Build feedback request flow | 4 | Email sent 24h after event |
| Create rebooking prompts | 4 | "Book again" offers for past customers |
| Implement referral program | 4 | Shareable codes, tracking |
| Add review collection | 4 | Google Reviews, TripAdvisor prompts |

**Dependencies:** None  
**Blockers:** None

### Phase 4 Deliverables

| Deliverable | Location | Status Criteria |
|-------------|----------|-----------------|
| n8n Instance | n8n.sauvage.space | All workflows running, monitored |
| Notification System | n8n workflows | Real-time alerts to team |
| Email Templates | SendGrid/Mailgun | Branded, tested across clients |
| Calendar Integration | Email attachments | .ics files auto-generated |
| Post-booking Flows | n8n workflows | Feedback, rebooking, reviews |

### Phase 4 Testing Checklist

- [ ] All n8n workflows execute without errors
- [ ] High-value booking alerts arrive within 60 seconds
- [ ] Confirmation emails render correctly in Gmail, Outlook, Apple Mail
- [ ] Calendar invites import correctly to Google/Apple/Outlook calendars
- [ ] Post-booking emails send at correct intervals
- [ ] Failed workflows trigger alerts
- [ ] Notification preferences can be updated by team

### Phase 4 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| n8n instance downtime | High | Self-hosted with backup, or use n8n cloud |
| Email deliverability | High | SPF/DKIM/DMARC setup, reputation monitoring |
| Workflow complexity | Medium | Start simple, add conditions iteratively |
| Rate limiting | Medium | Implement queues, respect API limits |

---

## Phase 5: Testing & Launch (Week 9-10)

### Overview
Comprehensive testing, soft launch, and full deployment with monitoring.

### Week 9 Tasks

#### 5.1 End-to-End Testing (20 hours)
**Owner:** Full-stack Developer + Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Write E2E test suite | 6 | Cypress/Playwright tests for all flows |
| Cross-browser testing | 4 | Chrome, Safari, Firefox, Edge |
| Mobile device testing | 4 | iOS Safari, Android Chrome, various screen sizes |
| Load testing | 4 | System handles 10 concurrent bookings |
| Accessibility audit | 2 | WCAG 2.1 AA compliance |

**Dependencies:** All features complete  
**Blockers:** None

#### 5.2 Soft Launch with Friends (12 hours)
**Owner:** Full-stack Developer + Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Select beta testers | 2 | 10-15 friends/family recruited |
| Create feedback form | 2 | Structured questions for each widget |
| Monitor beta bookings | 4 | Real-time support during test bookings |
| Collect and triage feedback | 4 | Issues prioritized, quick fixes applied |

**Dependencies:** Beta tester list  
**Blockers:** None

### Week 10 Tasks

#### 5.3 Analytics Setup (12 hours)
**Owner:** Full-stack Developer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Set up Google Analytics 4 | 4 | Events tracked for all booking steps |
| Configure conversion tracking | 4 | Funnel visualization, drop-off points |
| Build custom dashboard | 4 | Real-time booking metrics |

**Dependencies:** Google Analytics account  
**Blockers:** None

#### 5.4 Documentation (16 hours)
**Owner:** Full-stack Developer + Designer

| Task | Hours | Acceptance Criteria |
|------|-------|---------------------|
| Write user documentation | 4 | How to book, FAQ, troubleshooting |
| Create admin runbook | 4 | How to manage bookings, refunds, changes |
| Document API integrations | 4 | Technical reference for developers |
| Create training materials | 4 | Video walkthroughs for Sauvage team |

**Dependencies:** None  
**Blockers:** None

### Phase 5 Deliverables

| Deliverable | Location | Status Criteria |
|-------------|----------|-----------------|
| Test Suite | GitHub | 80%+ E2E coverage |
| Beta Feedback Report | Google Docs | Prioritized list of improvements |
| Analytics Dashboard | GA4 + Custom | Real-time metrics visible |
| Documentation Site | /docs | Complete user and admin guides |
| Production Deployment | sauvage.space | Live and accepting bookings |

### Phase 5 Testing Checklist

- [ ] All E2E tests pass
- [ ] Beta testers complete bookings without assistance
- [ ] Analytics show accurate conversion funnel
- [ ] Documentation is clear and complete
- [ ] Production deployment uses production API keys
- [ ] SSL certificates valid
- [ ] Backup and recovery procedures tested
- [ ] Team trained on admin functions

### Phase 5 Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Critical bug in production | High | Feature flags, instant rollback capability |
| Overwhelming initial demand | Medium | Waitlist system, capacity alerts |
| Team adoption issues | Medium | Training sessions, dedicated support channel |
| Integration failures | High | Health check dashboard, 24h monitoring |

---

## Airtable Base Schema

### Tables Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Bookings     │────▶│     Rooms       │     │    Add-ons      │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ ID (Auto)       │     │ ID (Auto)       │     │ ID (Auto)       │
│ Customer (Link) │     │ Name            │     │ Name            │
│ Room (Link)     │     │ Capacity        │     │ Category        │
│ Date/Time       │     │ Base Price      │     │ Price           │
│ Add-ons (Link)  │     │ Description     │     │ Description     │
│ Total Price     │     │ Images          │     │ Image           │
│ Deposit Paid    │     │ Amenities       │     │ Room Types      │
│ Status          │     │ Is Active       │     │ Is Active       │
│ Google Cal ID   │     └─────────────────┘     └─────────────────┘
│ Created At      │              │
└─────────────────┘              │
         │                       │
         │              ┌────────┴────────┐
         │              │                 │
         ▼              ▼                 ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Customers     │  │  Pricing Rules  │  │  Availability   │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ ID (Auto)       │  │ ID (Auto)       │  │ ID (Auto)       │
│ Name            │  │ Room (Link)     │  │ Room (Link)     │
│ Email           │  │ Min Guests      │  │ Date            │
│ Phone           │  │ Max Guests      │  │ Is Available    │
│ Company         │  │ Price Per Head  │  │ Block Reason    │
│ Bookings (Link) │  │ Day of Week     │  │ Google Event ID │
│ Tags            │  │ Time Range      │  └─────────────────┘
│ Notes           │  │ Multiplier      │
└─────────────────┘  └─────────────────┘
```

### Detailed Field Specifications

#### Bookings Table

| Field | Type | Description | Formula/Config |
|-------|------|-------------|----------------|
| Booking ID | Formula | Unique identifier | `"SV-" & DATETIME_FORMAT(Created, 'YYYYMMDD') & "-" & Autonumber` |
| Customer | Link | → Customers | Single-select, required |
| Room | Link | → Rooms | Single-select, required |
| Event Date | Date | Date of booking | Date only, required |
| Start Time | Single Select | Time slots | 09:00, 12:00, 15:00, 18:00 |
| End Time | Formula | Auto-calculated | `DATEADD(Start Time, 3, 'hours')` |
| Guest Count | Number | Number of attendees | 1-100, required |
| Add-ons | Link | → Add-ons | Multi-select |
| Occasion | Single Select | Type of event | Meeting, Event, Photoshoot, Workshop, Private Dining |
| Vibe | Single Select | Mood preference | Professional, Creative, Celebration, Intimate |
| Base Price | Lookup | From Room | Room.Base Price |
| Add-ons Total | Rollup | Sum of add-ons | SUM(values) from Add-ons |
| Total Price | Formula | Final calculation | `{Base Price} + {Add-ons Total} + (({Guest Count} - {Room.Min Capacity}) * {Room.Per Head Rate})` |
| Deposit Amount | Formula | 50% of total | `ROUND({Total Price} * 0.5, 2)` |
| Deposit Paid | Currency | Amount received | Manual entry |
| Balance Due | Formula | Remaining amount | `{Total Price} - {Deposit Paid}` |
| Payment Status | Single Select | Current state | Pending, Deposit Paid, Fully Paid, Refunded |
| Booking Status | Single Select | Lifecycle state | Inquiry, Confirmed, Cancelled, Completed |
| Google Calendar ID | Single Line Text | GCal event reference | Populated by automation |
| Shopify Order ID | Single Line Text | Payment reference | Populated by webhook |
| Special Requests | Long Text | Customer notes | Free text |
| Created | Created Time | Auto timestamp | |
| Last Modified | Last Modified Time | Auto timestamp | |

#### Rooms Table

| Field | Type | Description |
|-------|------|-------------|
| Room Name | Single Line Text | e.g., "The Green Room" |
| Slug | Formula | URL-friendly name |
| Capacity Min | Number | Minimum guests |
| Capacity Max | Number | Maximum guests |
| Base Price | Currency | Starting price |
| Per Head Rate | Currency | Additional per person |
| Description | Long Text | Full description |
| Short Description | Single Line Text | Card preview text |
| Images | Attachment | Multiple photos |
| Amenities | Multiple Select | WiFi, Projector, Kitchen, etc. |
| Square Meters | Number | Room size |
| Floor Plan | Attachment | PDF/image |
| Is Active | Checkbox | Available for booking |
| Bookings | Link | ← Bookings |

#### Add-ons Table

| Field | Type | Description |
|-------|------|-------------|
| Name | Single Line Text | e.g., "Coffee & Tea Service" |
| Category | Single Select | Catering, Equipment, Services |
| Price | Currency | Fixed or per-person |
| Pricing Type | Single Select | Fixed, Per Person, Per Hour |
| Description | Long Text | What's included |
| Image | Attachment | Product photo |
| Compatible Rooms | Link | → Rooms (which rooms can use this) |
| Min Quantity | Number | Minimum order |
| Max Quantity | Number | Maximum order |
| Is Active | Checkbox | Available for purchase |

#### Customers Table

| Field | Type | Description |
|-------|------|-------------|
| Full Name | Single Line Text | |
| Email | Email | Unique, required |
| Phone | Phone | |
| Company | Single Line Text | |
| Instagram Handle | Single Line Text | @username |
| Bookings Count | Count | Number of bookings |
| Total Spent | Rollup | Sum of all booking totals |
| Customer Since | Created Time | |
| Tags | Multiple Select | VIP, Regular, Corporate, etc. |
| Notes | Long Text | Internal notes |
| Marketing Consent | Checkbox | GDPR compliance |

#### Pricing Rules Table

| Field | Type | Description |
|-------|------|-------------|
| Room | Link | → Rooms |
| Rule Name | Single Line Text | e.g., "Weekend Premium" |
| Day of Week | Multiple Select | Mon, Tue, Wed, Thu, Fri, Sat, Sun |
| Time Range Start | Single Select | 00:00-23:00 |
| Time Range End | Single Select | 00:00-23:00 |
| Guest Range Min | Number | |
| Guest Range Max | Number | |
| Price Modifier | Currency | Fixed amount to add |
| Percentage Modifier | Percent | Percentage to multiply |
| Is Active | Checkbox | |

#### Availability Table

| Field | Type | Description |
|-------|------|-------------|
| Room | Link | → Rooms |
| Date | Date | |
| Is Available | Checkbox | |
| Block Reason | Single Select | Maintenance, Private Event, Holiday |
| Notes | Long Text | |
| Google Event ID | Single Line Text | Sync reference |

---

## n8n Workflow Diagrams

### Workflow 1: New Booking Received

```
┌─────────────────────────────────────────────────────────────────┐
│                    NEW BOOKING WEBHOOK                          │
│              (Triggered by Shopify order creation)              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. PARSE WEBHOOK DATA                                           │
│    • Extract booking details from Shopify payload               │
│    • Validate required fields                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. CREATE AIRTABLE RECORD                                       │
│    • Create Booking record                                      │
│    • Link to Customer (create if new)                           │
│    • Set status: "Confirmed"                                    │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. CREATE GOOGLE CALENDAR EVENT                                 │
│    • Title: "[Room] - [Customer Name] - [Occasion]"            │
│    • Time: Booking date/time                                    │
│    • Description: Guest count, add-ons, special requests        │
│    • Store Event ID in Airtable                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ 4a. SEND EMAIL  │ │ 4b. SEND SMS    │ │ 4c. NOTIFY TEAM │
│ CONFIRMATION    │ │ CONFIRMATION    │ │                 │
│                 │ │ (Optional)      │ │                 │
│ To: Customer    │ │ To: Customer    │ │ To: Staff       │
│ Include: .ics   │ │ If: High value  │ │ Channel: Slack  │
│ attachment      │ │                 │ │ or Email        │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Workflow 2: Daily Digest

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEDULE TRIGGER                             │
│                    (Every day at 08:00 CET)                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. QUERY AIRTABLE                                               │
│    • Today's bookings                                           │
│    • Tomorrow's bookings                                        │
│    • Pending balance payments                                   │
│    • New inquiries (last 24h)                                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. FORMAT DIGEST                                                │
│    • Group by time slot                                         │
│    • Calculate totals                                           │
│    • Flag action items                                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. SEND TO TEAM                                                 │
│    • Email to management                                        │
│    • Slack message to #bookings                                 │
│    • SMS for urgent items (if any)                              │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow 3: Booking Reminder

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEDULE TRIGGER                             │
│                    (Every hour)                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. QUERY UPCOMING BOOKINGS                                      │
│    • 24 hours from now                                          │
│    • Reminder not yet sent                                      │
│    • Status: Confirmed                                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. SEND REMINDER EMAIL                                          │
│    • Booking details recap                                      │
│    • Location/directions                                        │
│    • Contact number for changes                                 │
│    • What to bring                                              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. UPDATE AIRTABLE                                              │
│    • Mark reminder sent                                         │
│    • Log timestamp                                              │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow 4: Post-Event Follow-up

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCHEDULE TRIGGER                             │
│                    (Every day at 10:00 CET)                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. QUERY COMPLETED BOOKINGS                                     │
│    • End time was yesterday                                     │
│    • Feedback not yet requested                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. SEND FEEDBACK EMAIL                                          │
│    • Thank you message                                          │
│    • Link to feedback form (Typeform/Airtable Form)             │
│    • Incentive for response (discount code)                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. SCHEDULE REBOOKING OFFER                                     │
│    • Wait 7 days                                                │
│    • If no new booking, send "We miss you" email               │
│    • Include referral code                                      │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow 5: High-Value Alert

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONDITIONAL TRIGGER                          │
│         (Booking Total > €1000 OR Corporate booking)            │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. EVALUATE BOOKING                                             │
│    • Calculate total value                                      │
│    • Check customer tags                                        │
│    • Check occasion type                                        │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌─────┴─────┐       ┌─────┴─────┐
              │  HIGH     │       │  STANDARD │
              │  VALUE    │       │  VALUE    │
              └─────┬─────┘       └─────┬─────┘
                    │                   │
                    ▼                   ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│ IMMEDIATE ALERT         │   │ QUEUE FOR DIGEST        │
│ • SMS to manager        │   │ • Include in daily      │
│ • Slack @channel        │   │   summary               │
│ • Email to owner        │   │ • No immediate alert    │
└─────────────────────────┘   └─────────────────────────┘
```

---

## Notification Routing Matrix

### Event Triggers

| Event | Customer | Booking Manager | Owner | Staff | Channel | Timing |
|-------|----------|-----------------|-------|-------|---------|--------|
| **New Booking** | ✅ Email + .ics | ✅ SMS if >€500 | ✅ SMS if >€1000 | ❌ | Email, SMS | Immediate |
| **Payment Received** | ✅ Receipt email | ✅ Confirmation | ✅ Alert if large | ❌ | Email | Immediate |
| **Booking Modified** | ✅ Update email | ✅ Alert | ✅ If significant | ❌ | Email, Slack | Immediate |
| **Booking Cancelled** | ✅ Confirmation | ✅ Alert | ✅ Alert | ❌ | Email, SMS | Immediate |
| **24h Reminder** | ✅ Reminder email | ❌ | ❌ | ❌ | Email | 24h before |
| **Day-of Alert** | ❌ | ✅ Booking list | ✅ Digest | ✅ Shift alert | Slack | 08:00 day-of |
| **Post-Event** | ✅ Feedback request | ❌ | ❌ | ❌ | Email | 24h after |
| **Weekly Summary** | ❌ | ✅ Full report | ✅ Summary | ❌ | Email | Monday 09:00 |
| **System Error** | ❌ | ✅ Alert | ✅ Alert | ❌ | SMS, Email | Immediate |

### Escalation Rules

```
Level 1: Automated Response
├── Booking confirmation emails
├── Standard notifications
└── Digest summaries

Level 2: Human Attention Required
├── High-value bookings (€1000+)
├── Corporate accounts
├── Special requests noted
└── Booking conflicts detected
    ↓
    Notify: Booking Manager (SMS + Slack)
    Timeout: 30 minutes

Level 3: Urgent Intervention
├── Payment failures
├── System errors
├── Double-booking detected
└── Customer complaint
    ↓
    Notify: Owner + Booking Manager (SMS + Call)
    Timeout: 5 minutes
```

### Contact Priority by Role

| Role | Primary Channel | Secondary Channel | After Hours |
|------|-----------------|-------------------|-------------|
| Owner | SMS | Phone Call | SMS (urgent only) |
| Booking Manager | Slack | SMS | SMS (high value only) |
| Staff | Slack | Email | None (unless on-call) |
| Customer | Email | WhatsApp | WhatsApp (day-of only) |

---

## Risk Mitigation Strategies

### Technical Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Google Calendar API outage** | Medium | High | Cache availability 24h ahead; manual override mode in Airtable |
| **Shopify payment failures** | Low | Critical | Multiple payment providers (Stripe backup); manual invoice option |
| **Airtable rate limiting** | Medium | Medium | Implement Redis caching; batch API requests; upgrade plan |
| **n8n workflow failures** | Medium | High | Health checks every 5 min; failed workflow alerts; manual runbooks |
| **WhatsApp API rejection** | Medium | Medium | Build Telegram first; use WhatsApp Business App as fallback |
| **Instagram API limits** | Low | Medium | Queue messages; rate limit handling; fallback to DMs |

### Business Risks

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Double bookings** | Low | Critical | Google Calendar as source of truth; atomic booking creation |
| **Pricing errors** | Low | High | Formula validation; manual approval for large bookings |
| **No-show customers** | Medium | Medium | Deposit requirement; 24h reminder; clear cancellation policy |
| **Team adoption resistance** | Medium | Medium | Training sessions; gradual rollout; feedback loop |
| **Customer confusion** | Medium | Medium | Clear UX copy; help tooltips; human support fallback |

### Mitigation Implementation

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│ • Uptime monitoring (UptimeRobot)                               │
│ • Error tracking (Sentry)                                       │
│ • API health checks (every 5 min)                               │
│ • Booking anomaly detection                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ALERTING LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│ • PagerDuty integration for critical issues                     │
│ • Slack notifications for warnings                              │
│ • Daily health report email                                     │
│ • Escalation after 15 min unacknowledged                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FALLBACK LAYER                               │
├─────────────────────────────────────────────────────────────────┤
│ • Manual booking form (Google Forms → Airtable)                 │
│ • Phone booking process documented                              │
│ • Spreadsheet backup export (daily)                             │
│ • Emergency contact card for staff                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Success Metrics and KPIs

### Primary KPIs (Business)

| Metric | Baseline | Target (3 months) | Target (6 months) |
|--------|----------|-------------------|-------------------|
| **Booking Conversion Rate** | N/A | 15% | 25% |
| **Average Booking Value** | N/A | €800 | €950 |
| **Time to Book (median)** | N/A | 8 minutes | 5 minutes |
| **Customer Satisfaction** | N/A | 4.5/5 | 4.7/5 |
| **Repeat Booking Rate** | N/A | 20% | 30% |

### Secondary KPIs (Operational)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Booking Accuracy** | 99.5% | No double bookings, correct pricing |
| **System Uptime** | 99.9% | Excluding planned maintenance |
| **Notification Delivery** | 99% | Successful email/SMS delivery |
| **Support Ticket Volume** | <5% of bookings | Related to booking system |
| **Staff Time Saved** | 10 hrs/week | vs. manual booking process |

### Platform-Specific Metrics

| Platform | Metric | Target |
|----------|--------|--------|
| **Web** | Completion rate | 70% |
| **WhatsApp** | Completion rate | 60% |
| **Instagram** | Completion rate | 50% |
| **Telegram** | Completion rate | 65% |
| **Cross-platform** | Channel preference | Web 60%, Chat 40% |

### Technical Metrics

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| **Page Load Time** | <2s | >3s |
| **API Response Time** | <500ms | >1s |
| **Error Rate** | <0.1% | >0.5% |
| **Mobile Performance** | Lighthouse 90+ | <70 |
| **Accessibility Score** | Lighthouse 100 | <90 |

### Analytics Dashboard Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXECUTIVE SUMMARY                            │
├─────────────────────────────────────────────────────────────────┤
│ • Revenue today / this week / this month                        │
│ • Bookings today / this week / this month                       │
│ • Conversion rate (funnel visualization)                        │
│ • Average booking value trend                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    BOOKING FUNNEL                               │
├─────────────────────────────────────────────────────────────────┤
│ Onboarding Started ████████████████████ 100% (baseline)        │
│ Date Selected      ████████████████░░░░  85%                   │
│ Room Selected      ██████████████░░░░░░  72%                   │
│ Add-ons Added      ████████████░░░░░░░░  60%                   │
│ Payment Started    ██████████░░░░░░░░░░  45%                   │
│ Payment Completed  ████████░░░░░░░░░░░░  25%                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    PLATFORM BREAKDOWN                           │
├─────────────────────────────────────────────────────────────────┤
│ Web       ████████████████████  60%  │  Conversion: 28%        │
│ WhatsApp  ████████░░░░░░░░░░░░  20%  │  Conversion: 18%        │
│ Telegram  ██████░░░░░░░░░░░░░░  15%  │  Conversion: 22%        │
│ Instagram ██░░░░░░░░░░░░░░░░░░   5%  │  Conversion: 12%        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    OPERATIONAL HEALTH                           │
├─────────────────────────────────────────────────────────────────┤
│ • System uptime: 99.95%                                         │
│ • API error rate: 0.02%                                         │
│ • Avg response time: 245ms                                      │
│ • Failed notifications (24h): 3                                 │
│ • Pending manual actions: 2                                     │
└─────────────────────────────────────────────────────────────────┘
```

### Review Cadence

| Review Type | Frequency | Owner | Focus |
|-------------|-----------|-------|-------|
| **Daily Standup** | Daily | Developer | Blockers, progress |
| **Weekly Metrics** | Weekly | Manager | KPIs, conversion rates |
| **Monthly Review** | Monthly | Owner | Business impact, ROI |
| **Quarterly Planning** | Quarterly | Team | Roadmap, feature backlog |

---

## Appendix

### Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 14 + React + TypeScript | Web application |
| **Styling** | Tailwind CSS + Framer Motion | UI + animations |
| **State** | Zustand + React Query | Client state + server cache |
| **Backend** | Next.js API Routes + Server Actions | API endpoints |
| **Database** | Airtable | Primary data store |
| **Payments** | Shopify Storefront API | Checkout + deposits |
| **Calendar** | Google Calendar API | Availability + events |
| **Automation** | n8n | Workflows + notifications |
| **Hosting** | Vercel | Web app deployment |
| **Chat Platforms** | Twilio (WhatsApp), Meta (IG), Telegram Bot API | Multi-platform |

### Third-Party Services & Costs (Estimated Monthly)

| Service | Tier | Monthly Cost |
|---------|------|--------------|
| Vercel Pro | Team | $20 |
| Airtable Pro | Plus | $20 |
| Shopify Basic | Basic | $39 |
| n8n Cloud | Starter | $20 |
| Twilio WhatsApp | Pay-as-you-go | ~$10-30 |
| SendGrid | Essentials | $19.95 |
| Google Cloud | Calendar API | ~$5 |
| **Total** | | **~$135-155/month** |

### Development Environment Setup

```bash
# Clone and setup
git clone https://github.com/sauvage/booking-chatbot.git
cd booking-chatbot
npm install

# Environment variables
cp .env.example .env.local
# Edit .env.local with your keys

# Run development server
npm run dev

# Run tests
npm test
npm run test:e2e

# Build for production
npm run build
```

### Deployment Checklist

- [ ] Environment variables configured in Vercel
- [ ] Production API keys (not test/sandbox)
- [ ] Domain DNS configured
- [ ] SSL certificate active
- [ ] Google Analytics tracking ID
- [ ] Sentry DSN for error tracking
- [ ] Webhook URLs updated to production
- [ ] Airtable base switched from dev to prod
- [ ] Shopify store switched to live payments
- [ ] Team trained on admin functions
- [ ] Runbooks printed and accessible
- [ ] Emergency contacts documented

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-24 | Implementation Team | Initial plan |

---

*This implementation plan is a living document. Update as requirements change, blockers emerge, or new insights are gained.*

# Sprint 7 Development and Execution Timeline

## Project

Car Dealership Platform

## Sprint Theme

User Engagement and Visibility

## Edwin's Assigned Scope

Edwin is responsible for the frontend implementation of:

1. **Admin Multi-Chat Unified Inbox Hub**
2. **Real-Time Admin Notification Badges**

The implementation must support the end-to-end live inquiry workflow in which a customer sends a vehicle-related message, the backend WebSocket gateway routes the message to the correct inquiry room, the admin inbox receives the message immediately, the unread counter updates without a page reload, and the transcript-storage service persists and reloads the conversation.

---

# 1. Confirmed Starting Point

The Sprint 7 baseline inspection established the following:

- The current clean branch is `feature/edwin-sprint6-profile-booking`.
- The current branch is synchronized with its origin remote.
- The current branch contains the inspected `upstream/main` baseline and is not missing upstream commits.
- No application-level WebSocket, chat-room, conversation, typing-status, unread-message, or transcript implementation exists in the current branch.
- No suitable chat implementation exists in the inspected upstream baseline.
- No WebSocket client or server package is currently declared.
- No chat transcript, conversation-list, message-history, or inquiry endpoint currently exists.
- A reusable authentication provider, protected-route guard, API client, and bearer-header helper already exist.
- The active admin route renders `src/pages/Admin.tsx`.
- A separate legacy admin component also exists at `src/app/components/admin/AdminDashboard.tsx` and must not become a third competing admin application.
- The current test strategy uses direct TypeScript manual tests executed with `tsx`.

---

# 2. Delivery Boundaries

## Included in Edwin's Sprint 7 scope

- Admin conversation inbox interface
- Active-conversation list
- Selected conversation thread
- Admin reply composer
- Typing and connection indicators
- Shared frontend chat state
- Unread-message counting
- Admin notification badge
- WebSocket client adapter matching Devine's confirmed protocol
- Transcript API adapter matching Ronald's confirmed endpoints
- Integration with existing authentication and API utilities
- Responsive, accessible, and failure-aware UI states
- Targeted frontend tests
- Cross-team live inquiry drill
- Sprint documentation and pull-request preparation

## Excluded unless formally reassigned

- Building Devine's production WebSocket server
- Designing Ronald's database schema
- Implementing Ronald's transcript-storage endpoints
- Building Edward's customer-facing chat widget
- Inventing production socket event names or payloads
- Implementing a production message broker
- Replacing the existing authentication architecture
- Creating another independent admin application
- Committing private credentials or production URLs

## Child-process rule

If a required backend, database, or shared contract does not exist, Edwin will not silently invent it. The missing dependency must be handled as one of the following:

1. **Contract clarification:** obtain the exact interface from the responsible teammate.
2. **Frontend-safe adapter:** build an injectable adapter around an explicitly documented provisional contract.
3. **Deterministic mock:** use synthetic development data for isolated frontend validation, clearly marked as mock data.
4. **Child implementation:** implement the missing backend or database module only after ownership and scope are explicitly approved.
5. **External dependency gate:** pause live integration while allowing non-dependent frontend phases to continue.

---

# 3. Proposed Branch Strategy

The Sprint 7 branch should be created only after this timeline is reviewed and approved.

Recommended branch:

```text
feature/edwin-sprint7-admin-chat
```

Recommended starting point:

```text
feature/edwin-sprint6-profile-booking
```

No merge, rebase, or upstream conflict resolution should be performed during timeline approval.

---

# 4. Phase-by-Phase Execution Timeline

## Phase 1: Sprint 7 Branch Setup and Baseline Preservation

### Objective

Create an isolated Sprint 7 feature branch from the verified clean Sprint 6 baseline and record the starting repository state.

### Files to create

```text
docs/sprint7/admin-chat-baseline.md
```

### Files to modify

```text
None, except the baseline document
```

### Activities

- Confirm the Sprint 6 branch is clean and pushed.
- Fetch `origin` and `upstream` without modifying files.
- Record branch, commit, ahead/behind, build, and existing test status.
- Create `feature/edwin-sprint7-admin-chat`.
- Confirm the new branch tracks its intended origin branch after first push.
- Record the absence of existing chat and WebSocket functionality.

### Exit criteria

- Sprint 7 branch exists.
- Working tree is clean.
- Baseline commit is recorded.
- No implementation files have been changed.
- No missing upstream commit is hidden or assumed.

### Phase gate

Stop after completion and request the Phase 2 instructions.

---

## Phase 2: Cross-Team Chat Contract and Ownership Freeze

### Objective

Define one shared inquiry, conversation, message, typing, unread, authentication, and persistence contract before UI or socket integration begins.

### Files to create

```text
docs/sprint7/chat-contract.md
src/features/admin-chat/types/chat.types.ts
src/features/admin-chat/types/index.ts
```

### Files to modify

```text
README.md
```

### Required details from Devine

- WebSocket transport: Socket.io, native WebSocket, or another protocol
- Development and production gateway URLs
- Authentication handshake method
- Connection and reconnection behavior
- Room naming convention
- Room join and leave event names
- Incoming message event name
- Admin reply event name
- Typing-start and typing-stop event names
- Message acknowledgement event
- Error payload shape
- Whether missed events are replayed after reconnect

### Required details from Ronald

- Conversation-list endpoint
- Conversation-history endpoint
- Mark-as-read endpoint
- History pagination contract
- Message identifier type
- Inquiry identifier type
- Sender shape
- Timestamp format and timezone
- Vehicle reference shape
- History ordering
- Duplicate-message constraints

### Required details from Edward

- Customer outgoing message payload
- Customer identity fields
- Vehicle context fields
- Inquiry creation behavior
- Typing payload
- Message acknowledgement expectations

### Provisional frontend domain types

The final names must follow the confirmed contract, but the domain must cover:

```text
ChatUser
ChatParticipant
ChatInquiry
ChatConversationSummary
ChatMessage
ChatSenderRole
ChatConnectionStatus
ChatTypingEvent
ChatMessageEvent
ChatAcknowledgement
ChatError
UnreadConversationState
AdminChatState
```

### Exit criteria

- A written shared contract exists.
- Responsible owners are named for each unresolved field.
- Production event names are not guessed.
- Message IDs, inquiry IDs, sender roles, and timestamps have one agreed representation.
- Frontend types compile.

### Dependency gate

If Devine or Ronald has not implemented the required services, document the pending details and authorize mock-driven frontend work only. Live integration remains blocked.

### Phase gate

Stop after completion and request the Phase 3 instructions.

---

## Phase 3: Deterministic Chat State and Unread Rules

### Objective

Implement framework-independent state transitions for conversations, selected rooms, messages, typing state, unread counts, deduplication, and connection state.

### Files to create

```text
src/features/admin-chat/state/adminChatState.ts
src/features/admin-chat/state/adminChatReducer.ts
src/features/admin-chat/state/unreadRules.ts
src/features/admin-chat/state/messageOrdering.ts
src/features/admin-chat/state/index.ts
src/tests/adminChatState.manual.ts
src/tests/unreadChatBadge.manual.ts
```

### Files to modify

```text
package.json
```

### Rules to implement

- Messages are deduplicated by confirmed message ID.
- Conversations are ordered by latest message time.
- Messages inside a conversation are ordered deterministically.
- Incoming customer messages increment unread count only when the conversation is not actively viewed.
- Opening a conversation marks its currently loaded unread messages as read locally.
- A message acknowledgement does not duplicate the optimistic message.
- Reconnection does not register duplicate event listeners.
- Typing state expires safely if a stop event is missed.
- Unknown rooms do not corrupt the active thread.
- Total unread count is derived from conversation state, not maintained as an unrelated counter.

### Targeted tests

- Empty state initializes safely.
- First incoming message creates or updates a conversation.
- Inactive-room message increments unread count.
- Active-room message does not create a false unread count.
- Selecting a conversation clears the appropriate unread count.
- Duplicate message IDs are ignored.
- Out-of-order timestamps are normalized.
- Typing state starts and stops correctly.
- Reconnection event does not duplicate messages.
- Total badge count matches the sum of unread conversations.

### Exit criteria

- State modules have no transport or UI dependency.
- Targeted tests pass.
- No token, message content, or authorization header is logged by the state layer.

### Phase gate

Stop after completion and request the Phase 4 instructions.

---

## Phase 4: Static Admin Inbox Interface

### Objective

Build the two-panel inbox interface with deterministic local fixtures before connecting network services.

### Files to create

```text
src/features/admin-chat/components/AdminChatInbox.tsx
src/features/admin-chat/components/AdminChatInbox.css
src/features/admin-chat/components/ConversationList.tsx
src/features/admin-chat/components/ConversationListItem.tsx
src/features/admin-chat/components/ConversationThread.tsx
src/features/admin-chat/components/MessageBubble.tsx
src/features/admin-chat/components/MessageComposer.tsx
src/features/admin-chat/components/TypingIndicator.tsx
src/features/admin-chat/components/ChatConnectionBanner.tsx
src/features/admin-chat/components/AdminChatEmptyState.tsx
src/features/admin-chat/components/index.ts
src/features/admin-chat/data/adminChatFixtures.ts
src/pages/AdminChat/AdminChatPage.tsx
```

### Files to modify

```text
src/app/App.tsx
src/pages/Admin.tsx
```

### UI requirements

#### Left panel

- Scrollable conversation list
- Customer or inquiry label
- Vehicle context
- Latest message preview
- Last-message timestamp
- Unread indicator
- Selected state
- Empty state
- Loading state
- Search-ready structure

#### Right panel

- Selected inquiry information
- Message history
- Customer and admin message bubbles
- Time labels
- Typing indicator
- Connection status
- Message composer
- Send button
- Error state
- Disconnected state
- No-selection state

### Responsive behavior

- Two-panel desktop layout
- Conversation-first mobile layout
- Back-to-list action on narrow screens
- Composer remains reachable without covering messages
- Long content wraps safely

### Accessibility requirements

- Meaningful headings
- Keyboard-selectable conversations
- Visible focus indicators
- Accessible unread labels
- Live region for new messages
- Accessible connection and error announcements
- Proper labels for the message composer

### Exit criteria

- `/Admin/chat` is protected by the existing route guard.
- Static UI renders without a WebSocket package.
- No third competing admin application is introduced.
- Local fixtures are isolated and labeled as synthetic.
- Production build passes.

### Phase gate

Stop after completion and request the Phase 5 instructions.

---

## Phase 5: Admin Chat Context and Hooks

### Objective

Connect the deterministic chat state to React through one shared provider and stable hooks.

### Files to create

```text
src/features/admin-chat/context/AdminChatContext.tsx
src/features/admin-chat/hooks/useAdminChat.ts
src/features/admin-chat/hooks/useConversationSelection.ts
src/features/admin-chat/hooks/index.ts
```

### Files to modify

```text
src/app/App.tsx
src/pages/AdminChat/AdminChatPage.tsx
src/features/admin-chat/components/AdminChatInbox.tsx
src/features/admin-chat/components/ConversationList.tsx
src/features/admin-chat/components/ConversationThread.tsx
src/features/admin-chat/components/MessageComposer.tsx
```

### State exposed by the provider

```text
conversations
activeInquiryId
activeConversation
messagesByInquiry
connectionStatus
typingByInquiry
totalUnreadCount
isLoadingConversations
isLoadingHistory
error
```

### Actions exposed by the provider

```text
selectConversation(inquiryId)
receiveMessage(message)
sendMessage(input)
markConversationRead(inquiryId)
setTyping(event)
setConnectionStatus(status)
loadConversations()
loadHistory(inquiryId)
retry()
```

### Exit criteria

- All inbox components consume one shared provider.
- The notification badge can consume the same unread state later.
- No component independently owns the authoritative unread count.
- Provider teardown does not leak timers or listeners.
- Unit-style manual tests still pass.

### Phase gate

Stop after completion and request the Phase 6 instructions.

---

## Phase 6: WebSocket Transport Adapter

### Objective

Implement an isolated real-time transport adapter using Devine's confirmed protocol.

### Files to create

```text
src/features/admin-chat/services/chatSocket.ts
src/features/admin-chat/services/chatSocket.types.ts
src/features/admin-chat/services/index.ts
src/features/admin-chat/hooks/useChatSocket.ts
src/tests/chatSocketAdapter.manual.ts
```

### Files to modify

```text
package.json
package-lock.json
.env.example
src/vite-env.d.ts
src/config/env.ts
src/features/admin-chat/context/AdminChatContext.tsx
docs/sprint7/chat-contract.md
```

### Conditional child process

If Devine confirms Socket.io:

```text
Add socket.io-client with the approved compatible version.
```

If Devine confirms native WebSocket:

```text
Do not install socket.io-client. Use the browser WebSocket API through the adapter.
```

If no transport is confirmed:

```text
Do not install a package. Implement only the adapter interface and a deterministic mock transport.
```

### Transport responsibilities

- Build the gateway URL from public environment configuration.
- Authenticate using the approved handshake.
- Connect once per provider lifecycle.
- Join and leave inquiry rooms.
- Receive messages.
- Send admin replies.
- Send typing events.
- Receive acknowledgements.
- Report connection state.
- Reconnect according to the approved policy.
- Remove listeners on teardown.
- Never log tokens or private headers.

### Environment variables

Final names require contract confirmation. Likely public configuration may include:

```text
VITE_CHAT_GATEWAY_URL
VITE_CHAT_TRANSPORT
VITE_CHAT_MOCK_MODE
```

No backend secret may be exposed through a `VITE_` variable.

### Targeted tests

- Connect uses the expected URL.
- Authentication metadata is attached correctly.
- Join-room payload is correct.
- Incoming message is normalized.
- Admin reply uses the expected event.
- Listener cleanup works.
- Reconnect does not create duplicate listeners.
- Token values are absent from logs and returned errors.

### Exit criteria

- Adapter matches Devine's confirmed contract.
- Mock transport remains available for deterministic frontend testing if needed.
- No event handling bypasses shared chat state.
- Targeted tests pass.

### Phase gate

Stop after completion and request the Phase 7 instructions.

---

## Phase 7: Transcript and Conversation API Integration

### Objective

Integrate Ronald's conversation-list, history, and read-state endpoints through the existing API client.

### Files to create

```text
src/features/admin-chat/services/chatApi.ts
src/features/admin-chat/services/chatNormalization.ts
src/tests/chatApi.manual.ts
src/tests/chatHistoryMerge.manual.ts
```

### Files to modify

```text
src/features/admin-chat/services/index.ts
src/features/admin-chat/context/AdminChatContext.tsx
src/features/admin-chat/hooks/useAdminChat.ts
src/api/client.ts
.env.example
docs/sprint7/chat-contract.md
```

### API responsibilities

```text
getAdminConversations()
getConversationHistory(inquiryId, pagination)
markConversationRead(inquiryId)
```

Add other methods only if Ronald's contract requires them.

### History merge rules

- Stored messages and live messages are deduplicated by message ID.
- Optimistic messages reconcile with server acknowledgements.
- History loading does not erase newer live messages.
- Pagination preserves chronological order.
- Read-state updates are idempotent.
- Malformed records are skipped safely and reported without exposing private data.

### Conditional child process

If Ronald's endpoints do not yet exist:

- document the exact pending endpoints;
- use an injectable mock API;
- implement response normalization against approved sample payloads;
- keep live integration marked as blocked;
- do not create database tables without Ronald's approval.

If Edwin is formally assigned the missing backend child process, create a separate approved backend sub-plan before editing backend files.

### Exit criteria

- Conversation list loads through the shared API client.
- History loads for the selected inquiry.
- Live and stored messages merge correctly.
- Mark-as-read behavior is integrated.
- Targeted API and merge tests pass.

### Phase gate

Stop after completion and request the Phase 8 instructions.

---

## Phase 8: Admin Reply and Typing Workflow

### Objective

Complete the live admin interaction workflow for composing replies, sending messages, receiving acknowledgements, and displaying typing status.

### Files to create

```text
src/features/admin-chat/utils/messageValidation.ts
src/features/admin-chat/utils/typingThrottle.ts
src/tests/adminReplyWorkflow.manual.ts
src/tests/typingIndicator.manual.ts
```

### Files to modify

```text
src/features/admin-chat/components/MessageComposer.tsx
src/features/admin-chat/components/TypingIndicator.tsx
src/features/admin-chat/components/ConversationThread.tsx
src/features/admin-chat/context/AdminChatContext.tsx
src/features/admin-chat/services/chatSocket.ts
```

### Rules

- Empty and whitespace-only messages cannot be sent.
- Maximum length follows the shared contract.
- Sending can be disabled while disconnected if the backend does not queue messages.
- Optimistic messages have an explicit pending state.
- Acknowledged messages transition to sent state.
- Failed messages expose retry behavior without leaking technical details.
- Typing events are throttled.
- Typing-stop is sent after inactivity and on composer teardown.

### Exit criteria

- Admin can send a valid reply.
- Pending, sent, and failed states are distinguishable.
- Typing state behaves predictably.
- Duplicate acknowledgements do not duplicate messages.
- Targeted tests pass.

### Phase gate

Stop after completion and request the Phase 9 instructions.

---

## Phase 9: Real-Time Admin Notification Badge

### Objective

Add a live unread-message badge to the active admin navigation and connect it to the shared admin-chat provider.

### Files to create

```text
src/features/admin-chat/components/UnreadChatBadge.tsx
src/features/admin-chat/components/UnreadChatBadge.css
src/features/admin-chat/components/AdminChatNavLink.tsx
```

### Files to modify

```text
src/pages/Admin.tsx
src/app/App.tsx
src/features/admin-chat/components/index.ts
src/features/admin-chat/context/AdminChatContext.tsx
```

### Badge behavior

- Shows the total unread message count.
- Updates from incoming events without page reload.
- Links to `/Admin/chat`.
- Uses the same centralized unread state as the inbox.
- Decreases when conversations are marked read.
- Caps visual text safely, for example `99+`, if required.
- Includes accessible screen-reader text.
- Does not flash continuously or create visual distraction.
- Does not reset merely because the badge component remounts.

### Targeted tests

- Initial unread count is correct.
- Incoming inactive-room message increments the badge.
- Active-room message does not falsely increment the badge.
- Opening a conversation decreases the badge correctly.
- Duplicate event does not increment the badge twice.
- Badge navigation opens the protected inbox.

### Exit criteria

- Badge appears in the active admin navigation.
- Badge updates without reload.
- Badge count matches shared state.
- Accessibility and targeted tests pass.

### Phase gate

Stop after completion and request the Phase 10 instructions.

---

## Phase 10: Security, Privacy, and Authorization Review

### Objective

Confirm that chat access is admin-only, transport authentication is safe, messages are handled responsibly, and errors do not expose private data.

### Files to create

```text
docs/sprint7/chat-security-review.md
src/tests/chatSecurity.manual.ts
```

### Files to modify

```text
src/features/admin-chat/services/chatSocket.ts
src/features/admin-chat/services/chatApi.ts
src/features/admin-chat/context/AdminChatContext.tsx
src/app/App.tsx
README.md
```

### Review items

- `/Admin/chat` requires authenticated admin access.
- Non-admin users cannot load conversation history.
- Socket authentication uses the approved token mechanism.
- Tokens and authorization headers are never logged.
- Message contents are not written to diagnostic logs.
- User-facing errors are sanitized.
- External redirect behavior remains blocked.
- Unexpected payload fields are ignored.
- Message text is rendered as text, not executable markup.
- Connection teardown occurs on logout.
- Stored chat data is not persisted in unrestricted browser storage unless explicitly approved.
- Mock mode cannot be enabled accidentally in production.

### Backend child-process questions

Before production integration, confirm:

- Does Devine verify the JWT during the socket handshake?
- Does Devine verify admin authorization before joining admin rooms?
- Does Ronald enforce ownership and admin authorization on transcript endpoints?
- What retention policy applies to chat transcripts?
- Are message bodies encrypted in transit and protected at rest?
- What rate limits apply to messages and typing events?

### Exit criteria

- Security test suite passes.
- No frontend secret is introduced.
- No unauthorized route or socket access is accepted in the approved integration environment.
- Outstanding backend security dependencies are documented with owners.

### Phase gate

Stop after completion and request the Phase 11 instructions.

---

## Phase 11: Responsive, Accessibility, and Failure-State Validation

### Objective

Validate the inbox across desktop and mobile layouts and ensure all loading, empty, offline, error, and reconnecting states are usable.

### Files to create

```text
docs/sprint7/admin-chat-ui-validation.md
src/tests/adminChatAccessibility.manual.ts
```

### Files to modify

```text
src/features/admin-chat/components/AdminChatInbox.css
src/features/admin-chat/components/AdminChatInbox.tsx
src/features/admin-chat/components/ConversationList.tsx
src/features/admin-chat/components/ConversationThread.tsx
src/features/admin-chat/components/MessageComposer.tsx
src/features/admin-chat/components/ChatConnectionBanner.tsx
src/features/admin-chat/components/UnreadChatBadge.css
```

### Validation scenarios

- No conversations
- Initial conversation loading
- History loading
- API failure
- Socket disconnection
- Reconnecting state
- Message-send failure
- Very long customer name
- Very long vehicle name
- Long unbroken message text
- High unread count
- Keyboard navigation
- Screen-reader announcement of incoming messages
- Mobile conversation selection and return-to-list behavior

### Exit criteria

- UI remains usable at agreed desktop, tablet, and mobile widths.
- No content overlaps or becomes inaccessible.
- Keyboard and screen-reader affordances are present.
- Failure states offer clear recovery actions.
- Build passes.

### Phase gate

Stop after completion and request the Phase 12 instructions.

---

## Phase 12: Full Frontend Regression and Production Build

### Objective

Run targeted Sprint 7 tests and the existing authentication, routing, profile, booking, availability, filtering, and production-build validations.

### Files to create

```text
docs/sprint7/sprint7-validation-report.md
```

### Files to modify

```text
package.json
README.md
```

### Required test commands

The final scripts should include responsibilities equivalent to:

```text
test:admin-chat-state
test:admin-chat-socket
test:admin-chat-api
test:admin-chat-badge
test:admin-chat-security
test:admin-chat
```

Existing regression suites must also run:

```text
test:auth
test:protected-route
test:auth-persistence
test:profile
test:password
test:booking-history
test:booking-availability
test:availability-selection
test:vehicle-filters
test:api-config
```

### Build validation

- Production build succeeds.
- Generated assets are restored after validation.
- No source maps are included if the established build policy disables them.
- No hardcoded local API or socket origin is found in compiled assets.
- No secret name or private value is found in compiled assets.
- No mock chat fixture is unintentionally enabled in production.

### Exit criteria

- All targeted Sprint 7 tests pass.
- Existing regression suites pass.
- Production build passes.
- Working tree contains only intended source changes.
- Validation evidence is documented.

### Phase gate

Stop after completion and request the Phase 13 instructions.

---

## Phase 13: Cross-Team Live Inquiry Walkthrough

### Objective

Execute the required Friday end-to-end communication drill across Edward's customer widget, Devine's gateway, Edwin's admin inbox, and Ronald's transcript persistence.

### Files to create

```text
docs/sprint7/live-inquiry-drill.md
```

### Files to modify

```text
README.md
```

### Required walkthrough

1. Edward opens a specific vehicle page.
2. Edward's customer widget creates or joins an inquiry.
3. Edward sends a uniquely identifiable test message.
4. Devine's gateway receives and routes the payload to the correct inquiry room.
5. Edwin's admin navigation badge increments immediately.
6. Edwin opens the admin inbox.
7. The correct customer, vehicle, and message appear.
8. Edwin sends an admin reply.
9. Edward receives the reply in real time.
10. Typing status is tested in both approved directions.
11. Ronald confirms the transcript was stored.
12. The conversation is closed and reopened.
13. Ronald's history endpoint restores prior messages.
14. Duplicate messages and unread counts are checked.
15. Reconnection behavior is tested.

### Evidence to record

- Date and time
- Participating team members
- Frontend and backend commits
- Environment used
- Inquiry ID
- Event sequence
- HTTP and socket results
- Unread-count behavior
- Persistence result
- Reopen/history result
- Errors and owners
- Final pass or blocked status

### Exit criteria

- End-to-end message delivery passes in both directions.
- Badge updates correctly.
- Transcript is persisted and reloaded.
- Known defects have owners and follow-up dates.
- No private token or transcript content is committed to documentation.

### Phase gate

Stop after completion and request the Phase 14 instructions.

---

## Phase 14: Documentation, Cleanup, and Pull Request Preparation

### Objective

Finalize documentation, remove temporary development artifacts, confirm repository readiness, and prepare a reviewer-focused pull request.

### Files to create

```text
docs/sprint7/admin-chat-deployment-handoff.md
docs/sprint7/admin-chat-rollback-plan.md
```

### Files to modify

```text
README.md
.env.example
package.json
package-lock.json
```

Additional modified files are permitted only if required by final review findings.

### Cleanup requirements

- Remove unused imports and dead fixtures.
- Confirm mock mode is disabled by default.
- Confirm no duplicate socket adapters exist.
- Confirm no duplicate admin routes or dashboards were introduced.
- Confirm generated assets are not staged.
- Confirm private `.env` files remain ignored.
- Confirm event names and endpoints match approved contracts.
- Confirm the branch is synchronized with its remote.
- Run a read-only comparison with current `upstream/main`.

### Pull request contents

- Summary of admin inbox and unread badge
- WebSocket and transcript contracts
- Screenshots or approved demo link
- Targeted test results
- Production build result
- Cross-team drill result
- Known dependencies
- Security considerations
- Files created and modified
- Administrator integration notes
- Rollback guidance

### Exit criteria

- Documentation is complete.
- Branch is clean and pushed.
- Tests and build pass.
- PR description is accurate.
- Any upstream conflicts are documented without speculative resolution.
- Repository administrator can review the PR before merge.

### Final phase gate

Stop after completion, report Sprint 7 readiness, and wait for explicit approval before any merge or conflict-resolution activity.

---

# 5. Backend and Database Child-Process Decision Tree

## Case A: Devine's WebSocket gateway is ready

Proceed with the confirmed transport and event contract. Do not change Devine's backend unless a verified integration defect is assigned to Edwin.

## Case B: Devine's gateway is incomplete but the contract is confirmed

Implement the frontend adapter and mock transport. Mark live integration as blocked until the gateway is available.

## Case C: Devine's contract is not confirmed

Stop transport implementation. Complete only state, UI, and mock-driven phases that do not require guessed event names.

## Case D: Ronald's transcript endpoints are ready

Integrate through the existing authenticated API client and validate history merging.

## Case E: Ronald's endpoints are incomplete but response samples are approved

Implement an injectable mock API and normalizer. Mark live persistence as blocked.

## Case F: Edwin is asked to implement missing backend or database work

Do not append backend changes casually to the frontend scope. First request a child-phase specification covering:

- ownership approval;
- backend files;
- database migration files;
- route and controller contract;
- authentication and authorization;
- validation;
- rate limiting;
- retention policy;
- tests;
- rollback plan.

Only then create and execute the backend child phase.

---

# 6. Proposed Definition of Done

Sprint 7 is ready for PR review when all applicable criteria below are satisfied:

- [ ] Dedicated Sprint 7 branch exists and is pushed.
- [ ] Shared chat contract is documented.
- [ ] Admin inbox route is protected.
- [ ] Two-panel admin inbox is implemented.
- [ ] Conversation selection works.
- [ ] Message history loads or is clearly gated by the responsible backend dependency.
- [ ] Live messages are normalized and deduplicated.
- [ ] Admin replies work through the confirmed gateway.
- [ ] Typing status follows the confirmed event contract.
- [ ] Unread counts are derived from shared state.
- [ ] Admin navigation badge updates without reload.
- [ ] Badge navigation opens the inbox.
- [ ] Socket listeners are cleaned up correctly.
- [ ] Reconnection does not duplicate events.
- [ ] Tokens and private headers are not logged.
- [ ] Message text is rendered safely.
- [ ] Responsive and accessibility checks pass.
- [ ] Targeted Sprint 7 tests pass.
- [ ] Existing regression tests pass.
- [ ] Production build passes.
- [ ] Cross-team inquiry drill passes or external blockers are explicitly documented.
- [ ] Documentation and rollback guidance are complete.
- [ ] Branch is clean and pushed.
- [ ] PR is prepared for repository administrator review.

---

# 7. Required Questions Before Implementation

The following questions must be answered before their dependent phases begin:

## Devine

1. Is the gateway Socket.io or native WebSocket?
2. What is the exact client package and compatible version?
3. What is the gateway URL in development and production?
4. How does the admin client authenticate?
5. What are the exact event names?
6. What are the exact payload examples?
7. How are rooms named and authorized?
8. What acknowledgement and reconnect behavior is guaranteed?

## Ronald

1. What are the conversation-list and history endpoints?
2. What is the exact response shape?
3. How is pagination represented?
4. How are unread and read states persisted?
5. What identifier uniquely deduplicates a message?
6. What timestamp format and timezone are used?
7. What transcript retention policy applies?

## Edward

1. What exact payload does the customer widget emit?
2. How is the inquiry ID created or obtained?
3. Which vehicle fields are included?
4. How is customer identity represented?
5. Which typing events are emitted?

## Repository administrator or team lead

1. Should the active admin inbox live at `/Admin/chat`?
2. Should Sprint 7 consolidate the two existing admin implementations or avoid that refactor?
3. Is Edwin authorized to implement missing backend child processes if teammates are blocked?
4. Which environment is approved for the Friday live drill?
5. Who resolves upstream integration conflicts before merge?

---

# 8. Execution Policy

For every phase:

1. Inspect existing files before editing.
2. Make only phase-specific changes.
3. Verify targeted behavior before broad testing.
4. Run the agreed tests.
5. Review `git diff` and `git status`.
6. Commit only reviewed files.
7. Push the phase commit.
8. Report evidence and remaining blockers.
9. Stop and request the next-phase instructions.

No phase should begin automatically after the previous phase is completed.

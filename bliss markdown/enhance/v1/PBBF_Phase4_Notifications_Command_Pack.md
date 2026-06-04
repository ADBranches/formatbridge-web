# PBBF BLISS — Phase 4 Command Pack (Notifications Across MVP Workflows)

## Phase 4 objective
Upgrade notifications from a partial foundation into a full MVP operational notification flow. Earlier inspection showed that notifications already exist as real service/repository infrastructure and referral follow-up hooks are present, but appointment confirmations, reminders, reschedules, cancellations, and missed-visit follow-up are not yet wired consistently through the appointment workflow. citeturn74search1turn76search7turn77search7turn86search11

## Outcome target for this phase
By the end of this phase, the platform should support:
- appointment confirmation notifications on booking, citeturn74search1turn77search7turn86search11
- reminder notifications scheduled ahead of visits, citeturn74search1turn77search7turn86search11
- reschedule notifications when appointment timing changes, citeturn74search1turn77search7turn86search11
- cancellation notifications when appointments are cancelled, citeturn74search1turn77search7turn86search11
- retained referral follow-up notifications, citeturn76search7turn77search7turn86search11
- and visible queue/send/fail status through the backend operational notification model. citeturn76search7turn77search7turn86search11

## Inspection boundary (safe vs inspect-first)
This pack follows the same **inspect-before-edit** rule as the earlier phases.

### Files already sufficiently inspected and safe to patch
#### Backend notification core
- `pbbf-api/app/modules/notifications/service.py` citeturn76search7turn79search1turn86search11
- `pbbf-api/app/modules/notifications/repository.py` citeturn76search7turn86search11
- `pbbf-api/app/modules/notifications/schemas.py` citeturn76search7turn86search11
- `pbbf-api/app/modules/notifications/router.py` citeturn76search7turn86search11
- `pbbf-api/app/modules/notifications/tasks.py` citeturn76search7turn86search11
- `pbbf-api/app/modules/notifications/channels.py` citeturn76search7turn86search11

#### Workflow trigger points already inspected
- `pbbf-api/app/modules/appointments/service.py` citeturn76search7turn83search1turn86search11
- `pbbf-api/app/modules/telehealth/service.py` citeturn76search7turn86search11
- `pbbf-api/app/modules/referrals/service.py` citeturn76search7turn83search1turn86search11

#### Frontend notification surface already inspected
- `pbbf-telehealth/src/modules/notifications/components/ReminderBanner.jsx` citeturn76search7turn86search11

### Files that should still be inspected before patching
- any additional notification hooks/services/pages under `pbbf-telehealth/src/modules/notifications/` beyond `ReminderBanner.jsx`, because earlier inspection only surfaced a minimal notification UI surface and suggested broader frontend notification integration was still pending. citeturn76search7turn86search11
- any admin UI surface that will be used to expose queue/send/fail statuses beyond the existing metrics layer, since that belongs near admin hardening and should not be edited blindly here. citeturn77search7turn86search11

So this pack includes:
1. **inspection commands first** for the full notification frontend tree,
2. **safe patch commands** for the known backend notification and appointment trigger files,
3. a **minimal frontend ReminderBanner enhancement** only,
4. and a stop point before any larger notification-center/admin UI build-out. citeturn76search7turn77search7turn86search11

---

# 0) Go to repo root and create a backup area

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
export PHASE4_NOTIFICATIONS_BACKUP_DIR="backups/phase4_notifications_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$PHASE4_NOTIFICATIONS_BACKUP_DIR"
echo "$PHASE4_NOTIFICATIONS_BACKUP_DIR"
```

---

# 1) Inspect the current notification/UI surface before patching

## Why this step exists
Earlier inspection confirmed `ReminderBanner.jsx`, but also showed that the broader frontend notification UI is either minimal or not yet fully visible. Inspect the notification module tree before deciding whether you need more than the banner in this phase. citeturn76search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

echo "===== NOTIFICATION FRONTEND TREE ====="
find pbbf-telehealth/src/modules/notifications -type f 2>/dev/null | sort

echo
echo "===== NOTIFICATION FRONTEND FILES ====="
find pbbf-telehealth/src/modules/notifications -type f 2>/dev/null | sort | xargs -I{} sh -c 'echo "----- {} -----"; sed -n "1,260p" "{}"; echo'

echo
echo "===== ADMIN METRICS HOOK ====="
sed -n '1,320p' pbbf-telehealth/src/modules/admin/hooks/useAdminMetrics.js

echo
echo "===== ADMIN API ====="
sed -n '1,320p' pbbf-telehealth/src/modules/admin/services/adminApi.js
```

### Stop point
Do not patch any additional notification UI beyond `ReminderBanner.jsx` until you have reviewed those outputs.

---

# 2) Back up the confirmed patch targets

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

mkdir -p "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/notifications"
mkdir -p "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/appointments"
mkdir -p "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/telehealth"
mkdir -p "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/referrals"
mkdir -p "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-telehealth/src/modules/notifications/components"

cp pbbf-api/app/modules/notifications/service.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/notifications/service.py"
cp pbbf-api/app/modules/notifications/repository.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/notifications/repository.py"
cp pbbf-api/app/modules/notifications/schemas.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/notifications/schemas.py"
cp pbbf-api/app/modules/notifications/router.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/notifications/router.py"
cp pbbf-api/app/modules/notifications/tasks.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/notifications/tasks.py"
cp pbbf-api/app/modules/notifications/channels.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/notifications/channels.py"
cp pbbf-api/app/modules/appointments/service.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/appointments/service.py"
cp pbbf-api/app/modules/telehealth/service.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/telehealth/service.py"
cp pbbf-api/app/modules/referrals/service.py "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-api/app/modules/referrals/service.py"
cp pbbf-telehealth/src/modules/notifications/components/ReminderBanner.jsx "$PHASE4_NOTIFICATIONS_BACKUP_DIR/pbbf-telehealth/src/modules/notifications/components/ReminderBanner.jsx"
```

---

# 3) Patch backend notification tasks

## What this changes
Adds dedicated builders for appointment lifecycle notifications while keeping the existing referral follow-up builder intact. This is the safest way to centralize message generation before wiring triggers in the appointment workflow. citeturn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/notifications/tasks.py").write_text("""from datetime import timedelta\n\nfrom app.common.utils.datetime import utcnow\n\n\ndef _appointment_label(appointment) -> str:\n    service_type = getattr(appointment, \"appointment_type\", None) or getattr(appointment, \"service_type\", None) or \"care visit\"\n    return str(service_type).replace(\"_\", \" \")\n\n\ndef build_referral_follow_up_notification(*, referral, patient_user_id: int) -> dict:\n    scheduled_for = referral.follow_up_at or (utcnow() + timedelta(hours=24))\n\n    return {\n        \"user_id\": patient_user_id,\n        \"channel\": \"email\",\n        \"notification_type\": \"referral_follow_up\",\n        \"subject\": \"Referral follow-up reminder\",\n        \"body\": (\n            f\"You have a referral for {referral.category.replace('_', ' ')} \"\n            f\"to {referral.destination_name}. Please review your next steps.\"\n        ),\n        \"scheduled_for\": scheduled_for,\n        \"metadata\": {\n            \"referral_id\": referral.id,\n            \"patient_id\": referral.patient_id,\n            \"destination_name\": referral.destination_name,\n        },\n    }\n\n\ndef build_appointment_confirmation_notification(*, appointment, patient_user_id: int) -> dict:\n    return {\n        \"user_id\": patient_user_id,\n        \"channel\": \"email\",\n        \"notification_type\": \"appointment_confirmation\",\n        \"subject\": \"Appointment confirmation\",\n        \"body\": (\n            f\"Your {_appointment_label(appointment)} has been booked for {appointment.scheduled_start}.\"\n        ),\n        \"scheduled_for\": None,\n        \"metadata\": {\n            \"appointment_id\": appointment.id,\n            \"patient_id\": appointment.patient_id,\n            \"provider_id\": appointment.provider_id,\n            \"status\": appointment.status,\n        },\n    }\n\n\ndef build_appointment_reminder_notification(*, appointment, patient_user_id: int) -> dict:\n    scheduled_for = appointment.scheduled_start - timedelta(hours=24)\n    if scheduled_for <= utcnow():\n        scheduled_for = utcnow()\n\n    return {\n        \"user_id\": patient_user_id,\n        \"channel\": \"email\",\n        \"notification_type\": \"appointment_reminder\",\n        \"subject\": \"Upcoming appointment reminder\",\n        \"body\": (\n            f\"Reminder: your {_appointment_label(appointment)} is scheduled for {appointment.scheduled_start}.\"\n        ),\n        \"scheduled_for\": scheduled_for,\n        \"metadata\": {\n            \"appointment_id\": appointment.id,\n            \"patient_id\": appointment.patient_id,\n            \"provider_id\": appointment.provider_id,\n            \"status\": appointment.status,\n        },\n    }\n\n\ndef build_appointment_rescheduled_notification(*, appointment, patient_user_id: int) -> dict:\n    return {\n        \"user_id\": patient_user_id,\n        \"channel\": \"email\",\n        \"notification_type\": \"appointment_rescheduled\",\n        \"subject\": \"Appointment rescheduled\",\n        \"body\": (\n            f\"Your {_appointment_label(appointment)} has been rescheduled to {appointment.scheduled_start}.\"\n        ),\n        \"scheduled_for\": None,\n        \"metadata\": {\n            \"appointment_id\": appointment.id,\n            \"patient_id\": appointment.patient_id,\n            \"provider_id\": appointment.provider_id,\n            \"status\": appointment.status,\n        },\n    }\n\n\ndef build_appointment_cancellation_notification(*, appointment, patient_user_id: int) -> dict:\n    return {\n        \"user_id\": patient_user_id,\n        \"channel\": \"email\",\n        \"notification_type\": \"appointment_cancellation\",\n        \"subject\": \"Appointment cancellation\",\n        \"body\": (\n            f\"Your {_appointment_label(appointment)} scheduled for {appointment.scheduled_start} has been cancelled.\"\n        ),\n        \"scheduled_for\": None,\n        \"metadata\": {\n            \"appointment_id\": appointment.id,\n            \"patient_id\": appointment.patient_id,\n            \"provider_id\": appointment.provider_id,\n            \"status\": appointment.status,\n        },\n    }\n\n\ndef build_missed_visit_follow_up_notification(*, appointment, patient_user_id: int) -> dict:\n    return {\n        \"user_id\": patient_user_id,\n        \"channel\": \"email\",\n        \"notification_type\": \"missed_visit_follow_up\",\n        \"subject\": \"Missed visit follow-up\",\n        \"body\": (\n            f\"We noticed you may have missed your {_appointment_label(appointment)}. Please review next steps and reschedule if needed.\"\n        ),\n        \"scheduled_for\": None,\n        \"metadata\": {\n            \"appointment_id\": appointment.id,\n            \"patient_id\": appointment.patient_id,\n            \"provider_id\": appointment.provider_id,\n            \"status\": appointment.status,\n        },\n    }\n""", encoding="utf-8")'
```

---

# 4) Patch backend notification schemas

## What this changes
Extends the notification type enum to make appointment reschedule an explicit operational type, while preserving the existing notification API surface. If your current schemas already include some of these values, this patch normalizes them into one place. citeturn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/notifications/schemas.py").write_text("""from datetime import datetime\nfrom enum import Enum\n\nfrom pydantic import BaseModel, ConfigDict, Field\n\n\nclass NotificationChannel(str, Enum):\n    EMAIL = \"email\"\n    SMS = \"sms\"\n    IN_APP = \"in_app\"\n\n\nclass NotificationStatus(str, Enum):\n    PENDING = \"pending\"\n    QUEUED = \"queued\"\n    SENT = \"sent\"\n    FAILED = \"failed\"\n\n\nclass NotificationType(str, Enum):\n    GENERIC = \"generic\"\n    APPOINTMENT_CONFIRMATION = \"appointment_confirmation\"\n    APPOINTMENT_REMINDER = \"appointment_reminder\"\n    APPOINTMENT_RESCHEDULED = \"appointment_rescheduled\"\n    APPOINTMENT_CANCELLATION = \"appointment_cancellation\"\n    MISSED_VISIT_FOLLOW_UP = \"missed_visit_follow_up\"\n    REFERRAL_FOLLOW_UP = \"referral_follow_up\"\n\n\nclass NotificationCreateRequest(BaseModel):\n    user_id: int = Field(..., gt=0)\n    channel: NotificationChannel\n    body: str = Field(..., min_length=1, max_length=4000)\n    subject: str | None = Field(default=None, max_length=255)\n    notification_type: NotificationType = NotificationType.GENERIC\n    scheduled_for: datetime | None = None\n    metadata: dict = Field(default_factory=dict)\n\n\nclass NotificationResponse(BaseModel):\n    model_config = ConfigDict(from_attributes=True)\n\n    id: int\n    user_id: int\n    channel: str\n    notification_type: str\n    subject: str | None = None\n    body: str\n    status: str\n    metadata_json: dict | None = None\n    provider_message_id: str | None = None\n    failure_reason: str | None = None\n    scheduled_for: datetime | None = None\n    delivered_at: datetime | None = None\n    created_at: datetime\n    updated_at: datetime\n\n\nclass NotificationListResponse(BaseModel):\n    items: list[NotificationResponse]\n    total: int\n""", encoding="utf-8")'
```

---

# 5) Patch backend notification repository

## What this changes
Adds a helper for listing due scheduled notifications and a helper for marking a notification queued before dispatch. This improves operational queue/send/fail visibility without requiring a new table. citeturn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/notifications/repository.py").write_text("""from sqlalchemy import desc\nfrom sqlalchemy.orm import Session\n\nfrom app.common.utils.datetime import utcnow\nfrom app.db.models import Notification\n\n\nclass NotificationRepository:\n    def __init__(self, db: Session):\n        self.db = db\n\n    def create(\n        self,\n        *,\n        user_id: int,\n        channel: str,\n        notification_type: str,\n        subject: str | None,\n        body: str,\n        status: str,\n        metadata_json: dict | None,\n        scheduled_for,\n    ) -> Notification:\n        notification = Notification(\n            user_id=user_id,\n            channel=channel,\n            notification_type=notification_type,\n            subject=subject,\n            body=body,\n            status=status,\n            metadata_json=metadata_json or {},\n            scheduled_for=scheduled_for,\n        )\n        self.db.add(notification)\n        self.db.commit()\n        self.db.refresh(notification)\n        return notification\n\n    def get_by_id(self, notification_id: int) -> Notification | None:\n        return self.db.query(Notification).filter(Notification.id == notification_id).first()\n\n    def list_for_user(self, user_id: int) -> list[Notification]:\n        return (\n            self.db.query(Notification)\n            .filter(Notification.user_id == user_id)\n            .order_by(desc(Notification.created_at))\n            .all()\n        )\n\n    def list_due_pending(self) -> list[Notification]:\n        now = utcnow()\n        return (\n            self.db.query(Notification)\n            .filter(Notification.status == \"pending\")\n            .filter((Notification.scheduled_for.is_(None)) | (Notification.scheduled_for <= now))\n            .order_by(Notification.created_at.asc())\n            .all()\n        )\n\n    def mark_queued(self, *, notification: Notification, provider_message_id: str | None = None) -> Notification:\n        notification.status = \"queued\"\n        if provider_message_id:\n            notification.provider_message_id = provider_message_id\n        notification.updated_at = utcnow()\n        self.db.add(notification)\n        self.db.commit()\n        self.db.refresh(notification)\n        return notification\n\n    def mark_sent(self, *, notification: Notification, provider_message_id: str) -> Notification:\n        notification.status = \"sent\"\n        notification.provider_message_id = provider_message_id\n        notification.delivered_at = utcnow()\n        notification.updated_at = utcnow()\n        self.db.add(notification)\n        self.db.commit()\n        self.db.refresh(notification)\n        return notification\n\n    def mark_failed(self, *, notification: Notification, failure_reason: str) -> Notification:\n        notification.status = \"failed\"\n        notification.failure_reason = failure_reason\n        notification.updated_at = utcnow()\n        self.db.add(notification)\n        self.db.commit()\n        self.db.refresh(notification)\n        return notification\n""", encoding="utf-8")'
```

---

# 6) Patch backend notification channels

## What this changes
Keeps fake provider message IDs for now, but normalizes the returned status to `queued` consistently across channels. This preserves the MVP operational model even before a real email/SMS provider integration exists. citeturn76search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/notifications/channels.py").write_text("""from uuid import uuid4\n\n\ndef _fake_provider_message_id(prefix: str) -> str:\n    return f\"{prefix}_{uuid4().hex[:12]}\"\n\n\ndef dispatch_email(notification) -> dict:\n    return {\n        \"provider_message_id\": _fake_provider_message_id(\"email\"),\n        \"status\": \"queued\",\n    }\n\n\ndef dispatch_sms(notification) -> dict:\n    return {\n        \"provider_message_id\": _fake_provider_message_id(\"sms\"),\n        \"status\": \"queued\",\n    }\n\n\ndef dispatch_in_app(notification) -> dict:\n    return {\n        \"provider_message_id\": _fake_provider_message_id(\"inapp\"),\n        \"status\": \"queued\",\n    }\n\n\ndef dispatch_channel_message(*, channel: str, notification) -> dict:\n    if channel == \"email\":\n        return dispatch_email(notification)\n    if channel == \"sms\":\n        return dispatch_sms(notification)\n    if channel == \"in_app\":\n        return dispatch_in_app(notification)\n    raise ValueError(f\"Unsupported notification channel: {channel}\")\n""", encoding="utf-8")'
```

---

# 7) Patch backend notification service

## What this changes
- retains referral follow-up support,
- adds appointment confirmation/reminder/reschedule/cancellation/missed-visit helpers,
- adds `dispatch_due_notifications()` for queued scheduled sends,
- keeps audit logging around notification creation and dispatch. citeturn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/notifications/service.py").write_text("""from fastapi import HTTPException, status\nfrom sqlalchemy.orm import Session\n\nfrom app.db.models import Notification, Patient, Referral, User\nfrom app.modules.audit.service import AuditService\nfrom app.modules.notifications.channels import dispatch_channel_message\nfrom app.modules.notifications.repository import NotificationRepository\nfrom app.modules.notifications.schemas import NotificationCreateRequest, NotificationStatus\nfrom app.modules.notifications.tasks import (\n    build_appointment_cancellation_notification,\n    build_appointment_confirmation_notification,\n    build_appointment_reminder_notification,\n    build_appointment_rescheduled_notification,\n    build_missed_visit_follow_up_notification,\n    build_referral_follow_up_notification,\n)\n\n\nclass NotificationService:\n    def __init__(self, db: Session):\n        self.db = db\n        self.repository = NotificationRepository(db)\n        self.audit_service = AuditService(db)\n\n    @staticmethod\n    def _role_name(user: User) -> str:\n        if hasattr(user, \"role_name\") and user.role_name:\n            return str(user.role_name).lower()\n        if hasattr(user, \"role\") and user.role and hasattr(user.role, \"name\"):\n            return str(user.role.name).lower()\n        return \"patient\"\n\n    def _require_actor_can_send(self, actor: User) -> None:\n        role_name = self._role_name(actor)\n        if role_name not in {\"provider\", \"care_coordinator\", \"admin\"}:\n            raise HTTPException(\n                status_code=status.HTTP_403_FORBIDDEN,\n                detail=\"You are not allowed to create notifications.\",\n            )\n\n    def create_notification(self, payload: NotificationCreateRequest, actor: User) -> Notification:\n        self._require_actor_can_send(actor)\n        notification = self.repository.create(\n            user_id=payload.user_id,\n            channel=payload.channel.value,\n            notification_type=payload.notification_type.value,\n            subject=payload.subject,\n            body=payload.body,\n            status=NotificationStatus.PENDING.value,\n            metadata_json=payload.metadata,\n            scheduled_for=payload.scheduled_for,\n        )\n        self.audit_service.log_event(\n            actor_user_id=actor.id,\n            action=\"notification.created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"user_id\": notification.user_id,\n                \"channel\": notification.channel,\n                \"notification_type\": notification.notification_type,\n            },\n        )\n        return notification\n\n    def list_for_user(self, user_id: int) -> list[Notification]:\n        return self.repository.list_for_user(user_id)\n\n    def dispatch_notification(self, notification_id: int, actor: User) -> Notification:\n        notification = self.repository.get_by_id(notification_id)\n        if not notification:\n            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=\"Notification not found.\")\n\n        role_name = self._role_name(actor)\n        if role_name == \"patient\" and actor.id != notification.user_id:\n            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=\"You are not allowed to dispatch this notification.\")\n\n        try:\n            dispatch_result = dispatch_channel_message(channel=notification.channel, notification=notification)\n            notification = self.repository.mark_queued(\n                notification=notification,\n                provider_message_id=dispatch_result.get(\"provider_message_id\"),\n            )\n            notification = self.repository.mark_sent(\n                notification=notification,\n                provider_message_id=dispatch_result[\"provider_message_id\"],\n            )\n        except Exception as exc:  # pragma: no cover\n            notification = self.repository.mark_failed(notification=notification, failure_reason=str(exc))\n\n        self.audit_service.log_event(\n            actor_user_id=actor.id,\n            action=\"notification.dispatched\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"status\": notification.status,\n                \"channel\": notification.channel,\n            },\n        )\n        return notification\n\n    def dispatch_due_notifications(self, *, actor: User) -> list[Notification]:\n        self._require_actor_can_send(actor)\n        due = self.repository.list_due_pending()\n        return [self.dispatch_notification(notification.id, actor) for notification in due]\n\n    def _resolve_patient_user_id(self, patient_id: int) -> int | None:\n        patient = self.db.query(Patient).filter(Patient.id == patient_id).first()\n        if not patient:\n            return None\n        return getattr(patient, \"user_id\", None)\n\n    def _create_from_payload(self, *, payload: dict) -> Notification:\n        return self.repository.create(\n            user_id=payload[\"user_id\"],\n            channel=payload[\"channel\"],\n            notification_type=payload[\"notification_type\"],\n            subject=payload[\"subject\"],\n            body=payload[\"body\"],\n            status=NotificationStatus.PENDING.value,\n            metadata_json=payload[\"metadata\"],\n            scheduled_for=payload[\"scheduled_for\"],\n        )\n\n    def create_referral_follow_up_hook(self, referral: Referral, actor: User) -> Notification | None:\n        patient_user_id = self._resolve_patient_user_id(referral.patient_id)\n        if not patient_user_id:\n            return None\n\n        payload = build_referral_follow_up_notification(referral=referral, patient_user_id=patient_user_id)\n        notification = self._create_from_payload(payload=payload)\n        self.audit_service.log_event(\n            actor_user_id=actor.id,\n            action=\"notification.referral_follow_up_created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"referral_id\": referral.id,\n                \"user_id\": notification.user_id,\n            },\n        )\n        return notification\n\n    def create_appointment_confirmation_hook(self, *, appointment, actor: User | None = None) -> Notification | None:\n        patient_user_id = self._resolve_patient_user_id(appointment.patient_id)\n        if not patient_user_id:\n            return None\n        payload = build_appointment_confirmation_notification(appointment=appointment, patient_user_id=patient_user_id)\n        notification = self._create_from_payload(payload=payload)\n        self.audit_service.log_event(\n            actor_user_id=getattr(actor, \"id\", None),\n            action=\"notification.appointment_confirmation_created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"appointment_id\": appointment.id,\n                \"user_id\": notification.user_id,\n            },\n        )\n        return notification\n\n    def create_appointment_reminder_hook(self, *, appointment, actor: User | None = None) -> Notification | None:\n        patient_user_id = self._resolve_patient_user_id(appointment.patient_id)\n        if not patient_user_id:\n            return None\n        payload = build_appointment_reminder_notification(appointment=appointment, patient_user_id=patient_user_id)\n        notification = self._create_from_payload(payload=payload)\n        self.audit_service.log_event(\n            actor_user_id=getattr(actor, \"id\", None),\n            action=\"notification.appointment_reminder_created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"appointment_id\": appointment.id,\n                \"user_id\": notification.user_id,\n            },\n        )\n        return notification\n\n    def create_appointment_rescheduled_hook(self, *, appointment, actor: User | None = None) -> Notification | None:\n        patient_user_id = self._resolve_patient_user_id(appointment.patient_id)\n        if not patient_user_id:\n            return None\n        payload = build_appointment_rescheduled_notification(appointment=appointment, patient_user_id=patient_user_id)\n        notification = self._create_from_payload(payload=payload)\n        self.audit_service.log_event(\n            actor_user_id=getattr(actor, \"id\", None),\n            action=\"notification.appointment_rescheduled_created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"appointment_id\": appointment.id,\n                \"user_id\": notification.user_id,\n            },\n        )\n        return notification\n\n    def create_appointment_cancellation_hook(self, *, appointment, actor: User | None = None) -> Notification | None:\n        patient_user_id = self._resolve_patient_user_id(appointment.patient_id)\n        if not patient_user_id:\n            return None\n        payload = build_appointment_cancellation_notification(appointment=appointment, patient_user_id=patient_user_id)\n        notification = self._create_from_payload(payload=payload)\n        self.audit_service.log_event(\n            actor_user_id=getattr(actor, \"id\", None),\n            action=\"notification.appointment_cancellation_created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"appointment_id\": appointment.id,\n                \"user_id\": notification.user_id,\n            },\n        )\n        return notification\n\n    def create_missed_visit_follow_up_hook(self, *, appointment, actor: User | None = None) -> Notification | None:\n        patient_user_id = self._resolve_patient_user_id(appointment.patient_id)\n        if not patient_user_id:\n            return None\n        payload = build_missed_visit_follow_up_notification(appointment=appointment, patient_user_id=patient_user_id)\n        notification = self._create_from_payload(payload=payload)\n        self.audit_service.log_event(\n            actor_user_id=getattr(actor, \"id\", None),\n            action=\"notification.missed_visit_follow_up_created\",\n            entity_type=\"notification\",\n            entity_id=notification.id,\n            details={\n                \"appointment_id\": appointment.id,\n                \"user_id\": notification.user_id,\n            },\n        )\n        return notification\n\n    def create_password_reset_hook(self, *, user: User, reset_link: str) -> Notification:\n        notification = self.repository.create(\n            user_id=user.id,\n            channel=\"email\",\n            notification_type=\"generic\",\n            subject=\"Reset your password\",\n            body=(\n                \"We received a request to reset your password. \"\n                f\"Use this link to continue: {reset_link}\"\n            ),\n            status=NotificationStatus.PENDING.value,\n            metadata_json={\n                \"purpose\": \"password_reset\",\n                \"reset_link\": reset_link,\n            },\n            scheduled_for=None,\n        )\n        return notification\n""", encoding="utf-8")'
```

---

# 8) Patch backend notification router

## What this changes
Adds an admin/care-coordinator dispatch endpoint for due notifications so queued reminders can be flushed operationally without waiting for a future scheduler phase. citeturn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-api/app/modules/notifications/router.py").write_text("""from fastapi import APIRouter, Depends, status\nfrom sqlalchemy.orm import Session\n\nfrom app.db.session import get_db\nfrom app.modules.auth.dependencies import get_current_user\nfrom app.modules.notifications.schemas import (\n    NotificationCreateRequest,\n    NotificationListResponse,\n    NotificationResponse,\n)\nfrom app.modules.notifications.service import NotificationService\n\nrouter = APIRouter(prefix=\"/notifications\", tags=[\"notifications\"])\n\n\n@router.post(\"/\", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)\ndef create_notification(payload: NotificationCreateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):\n    service = NotificationService(db)\n    return service.create_notification(payload=payload, actor=current_user)\n\n\n@router.get(\"/me\", response_model=NotificationListResponse)\ndef list_my_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):\n    service = NotificationService(db)\n    items = service.list_for_user(current_user.id)\n    return NotificationListResponse(items=items, total=len(items))\n\n\n@router.post(\"/{notification_id}/dispatch\", response_model=NotificationResponse)\ndef dispatch_notification(notification_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):\n    service = NotificationService(db)\n    return service.dispatch_notification(notification_id=notification_id, actor=current_user)\n\n\n@router.post(\"/dispatch-due\", response_model=NotificationListResponse)\ndef dispatch_due_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):\n    service = NotificationService(db)\n    items = service.dispatch_due_notifications(actor=current_user)\n    return NotificationListResponse(items=items, total=len(items))\n""", encoding="utf-8")'
```

---

# 9) Patch backend appointments service trigger points

## What this changes
Wires notification creation into appointment booking, rescheduling, and cancellation. It also schedules a reminder when an appointment is created or rescheduled. citeturn74search1turn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; p=Path("pbbf-api/app/modules/appointments/service.py"); text=p.read_text(encoding="utf-8"); text=text.replace("from app.modules.appointments.repository import AppointmentsRepository", "from app.modules.appointments.repository import AppointmentsRepository\nfrom app.modules.notifications.service import NotificationService"); text=text.replace("        self.repository = AppointmentsRepository(db)", "        self.repository = AppointmentsRepository(db)\n        self.notification_service = NotificationService(db)"); text=text.replace("        appointment = self.repository.create_appointment(\n            patient_id=patient_profile.id,\n            provider_id=payload.provider_id,\n            appointment_type=payload.service_type,\n            reason=payload.reason,\n            timezone_name=payload.timezone,\n            scheduled_start=payload.start_at,\n            scheduled_end=payload.end_at,\n            status=\"booked\" if payload.provider_id else \"requested\",\n        )\n        return self._serialize(appointment)", "        appointment = self.repository.create_appointment(\n            patient_id=patient_profile.id,\n            provider_id=payload.provider_id,\n            appointment_type=payload.service_type,\n            reason=payload.reason,\n            timezone_name=payload.timezone,\n            scheduled_start=payload.start_at,\n            scheduled_end=payload.end_at,\n            status=\"booked\" if payload.provider_id else \"requested\",\n        )\n        self.notification_service.create_appointment_confirmation_hook(appointment=appointment, actor=current_user)\n        self.notification_service.create_appointment_reminder_hook(appointment=appointment, actor=current_user)\n        return self._serialize(appointment)"); text=text.replace("        appointment.status = \"cancelled\"\n        appointment.cancellation_reason = payload.reason\n        appointment = self.repository.save(appointment)\n        return self._serialize(appointment)", "        appointment.status = \"cancelled\"\n        appointment.cancellation_reason = payload.reason\n        appointment = self.repository.save(appointment)\n        self.notification_service.create_appointment_cancellation_hook(appointment=appointment, actor=current_user)\n        return self._serialize(appointment)"); text=text.replace("        appointment.status = \"rescheduled\"\n        appointment = self.repository.save(appointment)\n        return self._serialize(appointment)", "        appointment.status = \"rescheduled\"\n        appointment = self.repository.save(appointment)\n        self.notification_service.create_appointment_rescheduled_hook(appointment=appointment, actor=current_user)\n        self.notification_service.create_appointment_reminder_hook(appointment=appointment, actor=current_user)\n        return self._serialize(appointment)"); p.write_text(text, encoding="utf-8")'
```

---

# 10) Patch backend telehealth service for missed-visit follow-up trigger

## What this changes
Creates a missed-visit follow-up notification when a session transitions to `no_show`. This keeps missed-visit follow-up aligned with session state rather than overloading appointment create/reschedule logic. citeturn74search1turn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; p=Path("pbbf-api/app/modules/telehealth/service.py"); text=p.read_text(encoding="utf-8"); text=text.replace("from app.modules.telehealth.repository import TelehealthRepository", "from app.modules.telehealth.repository import TelehealthRepository\nfrom app.modules.notifications.service import NotificationService"); text=text.replace("        self.provider = get_virtual_visit_provider()", "        self.provider = get_virtual_visit_provider()\n        self.notification_service = NotificationService(repository.db)"); old="        return self.repository.update_status(session, new_status=new_status)"; new="        updated = self.repository.update_status(session, new_status=new_status)\n        if new_status == \"no_show\":\n            appointment = self.repository.get_appointment(updated.appointment_id)\n            if appointment is not None:\n                self.notification_service.create_missed_visit_follow_up_hook(appointment=appointment, actor=current_user)\n        return updated"; text=text.replace(old, new); p.write_text(text, encoding="utf-8")'
```

---

# 11) Patch frontend ReminderBanner

## What this changes
Makes the banner wording explicitly reflect reminder-style notification behavior coming from the backend-driven upcoming session/appointment surface, without attempting to build a full notification center prematurely. citeturn76search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth
python3 -c 'from pathlib import Path; Path("pbbf-telehealth/src/modules/notifications/components/ReminderBanner.jsx").write_text("""import { Link } from \"react-router-dom\";\nimport { ROUTES } from \"../../../shared/constants/routes\";\n\nfunction formatDateTime(value) {\n  if (!value) return \"Not scheduled\";\n  const date = new Date(value);\n  if (Number.isNaN(date.getTime())) return value;\n\n  return new Intl.DateTimeFormat(undefined, {\n    dateStyle: \"medium\",\n    timeStyle: \"short\",\n  }).format(date);\n}\n\nexport default function ReminderBanner({ session }) {\n  if (!session) return null;\n\n  return (\n    <section className=\"rounded-3xl border border-sky-200 bg-sky-50 p-6\">\n      <div className=\"flex flex-col gap-4 md:flex-row md:items-center md:justify-between\">\n        <div>\n          <p className=\"text-sm font-medium uppercase tracking-[0.18em] text-sky-700\">Upcoming visit reminder</p>\n          <h2 className=\"mt-2 text-xl font-semibold text-sky-950\">\n            {session.serviceType}\n          </h2>\n          <p className=\"mt-2 text-sm text-sky-900\">\n            {formatDateTime(session.appointmentTime)} with {session.providerName}\n          </p>\n          <p className=\"mt-2 text-sm leading-6 text-sky-800\">\n            {session.reminderMessage || \"Your visit reminder is available here. Review session readiness and prepare to join on time.\"}\n          </p>\n        </div>\n\n        <Link\n          to={ROUTES.patient.session}\n          className=\"inline-flex rounded-xl bg-sky-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-800\"\n        >\n          View session access\n        </Link>\n      </div>\n    </section>\n  );\n}\n""", encoding="utf-8")'
```

---

# 12) Inspect current tests before editing any notification-specific test files

## Why this step exists
Earlier inspection suggested that notification coverage was sparse compared with appointment, telehealth, and auth coverage. Inspect existing tests before adding or modifying any notification tests so we preserve the inspect-first rule. citeturn76search7turn77search7turn86search11

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth

find pbbf-api/tests -type f 2>/dev/null | grep -E 'notifications|appointments|telehealth|referrals' | sort | xargs -I{} sh -c 'echo "----- {} -----"; sed -n "1,260p" "{}"; echo'

find pbbf-telehealth/src -type f 2>/dev/null | grep -i notification | sort | xargs -I{} sh -c 'echo "----- {} -----"; sed -n "1,260p" "{}"; echo'
```

---

# 13) Validate backend syntax after patching

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-api
source .venv/bin/activate
python -m py_compile \
  app/modules/notifications/service.py \
  app/modules/notifications/repository.py \
  app/modules/notifications/schemas.py \
  app/modules/notifications/router.py \
  app/modules/notifications/tasks.py \
  app/modules/notifications/channels.py \
  app/modules/appointments/service.py \
  app/modules/telehealth/service.py
```

---

# 14) Build the frontend after the ReminderBanner update

```bash
cd /home/trovas/Downloads/projects/byupw/block3_2026/BLISS/bliss-telehealth/pbbf-telehealth
npm run build
```

---

# 15) Manual verification checklist for Phase 4

```text
[ ] Booking an appointment creates an appointment_confirmation notification.
[ ] Booking an appointment also schedules an appointment_reminder notification.
[ ] Rescheduling an appointment creates appointment_rescheduled and a fresh reminder notification.
[ ] Cancelling an appointment creates an appointment_cancellation notification.
[ ] Marking a telehealth session as no_show creates a missed_visit_follow_up notification.
[ ] Referral follow-up notifications still work after the notification service changes.
[ ] /notifications/dispatch-due can flush pending scheduled notifications for admin/coordinator operations.
[ ] ReminderBanner still renders safely when a session exists and remains hidden when no session exists.
```

---

# 16) Stop point before any larger notification-center/admin UI rollout

This pack intentionally stops after backend workflow triggers and a minimal ReminderBanner enhancement. If inspection reveals you want a **full patient notification list** or a richer **admin notification operations UI**, treat that as a follow-on build after reviewing the inspected notification frontend tree and admin metrics surface. That work overlaps with later admin hardening and should not be patched blindly here. citeturn77search7turn86search11

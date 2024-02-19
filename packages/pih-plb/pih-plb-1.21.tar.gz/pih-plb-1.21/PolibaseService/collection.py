from typing import Any
from datetime import datetime
from dataclasses import dataclass

import ipih

from pih.collections import ThresholdedText

@dataclass
class PolibaseDocument:
    file_path: str
    pin: int
    document_name: str


@dataclass
class PolibasePersonBase:
    pin: int | None = None
    FullName: str | None = None
    telephoneNumber: str | None = None


@dataclass
class PolibasePerson(PolibasePersonBase):
    Birth: datetime | None = None
    Comment: str | None = None
    ChartFolder: str | None = None
    email: str | None = None
    barcode: str | None = None
    registrationDate: datetime | None = None
    telephoneNumber2: str | None = None
    telephoneNumber3: str | None = None
    telephoneNumber4: str | None = None


@dataclass
class PolibasePersonVisitDS(PolibasePersonBase):
    id: int | None = None
    registrationDate: str | None = None
    beginDate: str | None = None
    completeDate: str | None = None
    status: int | None = None
    cabinetID: int | None = None
    doctorID: int | None = None
    doctorFullName: str | None = None
    serviceGroupID: int | None = None


@dataclass
class PolibasePersonVisitSearchCritery:
    vis_no: Any | None = None
    vis_pat_no: Any | None = None
    vis_pat_name: Any | None = None
    vis_place: Any | None = None
    vis_reg_date: Any | None = None
    vis_date_ps: Any | None = None
    vis_date_pf: Any | None = None
    vis_date_fs: Any | None = None
    vis_date_ff: Any | None = None


@dataclass
class PolibasePersonVisitNotificationDS:
    visitID: int | None = None
    messageID: int | None = None
    type: int | None = None


@dataclass
class PolibasePersonNotificationConfirmation:
    recipient: str | None = None
    sender: str | None = None
    status: int = 0


@dataclass
class PolibasePersonVisitNotification(PolibasePersonVisitDS, PolibasePersonVisitNotificationDS):
    pass


@dataclass
class PolibasePersonVisit(PolibasePersonVisitDS):
    registrationDate: datetime | None = None
    beginDate: datetime | None = None
    completeDate: datetime | None = None
    beginDate2: datetime | None = None
    completeDate2: datetime | None = None


@dataclass
class PolibasePersonQuest:
    step: int | None = None
    stepConfirmed: bool | None = None
    timestamp: int | None = None


@dataclass
class PolibasePersonInformationQuest(PolibasePersonBase):
    confirmed: int | None = None
    errors: int | None = None


@dataclass
class PolibasePersonReviewQuest(PolibasePersonQuest):
    beginDate: str | None = None
    completeDate: str | None = None
    grade: int | None = None
    message: str | None = None
    informationWay: int | None = None
    feedbackCallStatus: int | None = None


@dataclass
class PolibaseDocumentDescription(ThresholdedText):
    title_top: int = 0
    title_height: int = 0
    page_count: int = 1

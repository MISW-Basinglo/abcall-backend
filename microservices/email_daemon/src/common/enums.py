from enum import Enum


class UserStatus(Enum):
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    INACTIVE = "INACTIVE"


class UserRoles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    CLIENT = "CLIENT"
    AGENT = "AGENT"


class IssueType(Enum):
    REQUEST = "REQUEST"
    COMPLAINT = "COMPLAINT"
    CLAIM = "CLAIM"
    SUGGESTION = "SUGGESTION"
    PRAISE = "PRAISE"

    @classmethod
    def get_keywords(cls):
        return {
            cls.REQUEST: [r"\bsolicit[ao]?\b", r"\brequerimient[oa]\b", r"\bpetici[oó]n\b", r"\bpedido\b", r"\basistencia\b", r"\bsolicitando\b", r"\bnecesito\b", r"\bquiero\b"],
            cls.COMPLAINT: [
                r"\bquej[ao]\b",
                r"\breclam[ao]\b",
                r"\binconformidad\b",
                r"\bproblema\b",
                r"\bdescontent[ao]\b",
                r"\binsatisfacci[oó]n\b",
                r"\bmal[ao]\b",
                r"\bdeficiencia\b",
                r"\bmalo\b",
                r"\bdefectuoso\b",
            ],
            cls.CLAIM: [r"\bcompensaci[oó]n\b", r"\bresarcimiento\b", r"\bindemnizaci[oó]n\b", r"\breclamaci[oó]n\b", r"\bsolicito\b", r"\bexigiendo\b", r"\bcompensar\b"],
            cls.SUGGESTION: [r"\bsugerencia\b", r"\bidea\b", r"\bpropuesta\b", r"\brecomendaci[oó]n\b", r"\bmejorar\b", r"\binnovaci[oó]n\b", r"\bsugerir\b", r"\bproponer\b"],
            cls.PRAISE: [
                r"\bfelicitaci[oó]n\b",
                r"\bagradecimiento\b",
                r"\bexcelente\b",
                r"\bfelicitar\b",
                r"\bbuena\b",
                r"\bmaravilloso\b",
                r"\bespectacular\b",
                r"\bperfecto\b",
                r"\bgenial\b",
                r"\bmuy bueno\b",
                r"\bincre[ií]ble\b",
                r"\bmuy satisfecho\b",
            ],
        }

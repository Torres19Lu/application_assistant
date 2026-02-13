from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.schemas.university import UniversityCreate, UniversityResponse, UniversityUpdate
from app.schemas.major import MajorCreate, MajorResponse, MajorUpdate
from app.schemas.guide import GuideCreate, GuideResponse, GuideUpdate
from app.schemas.collection import CollectionCreate, CollectionResponse
from app.schemas.case import CaseCreate, CaseResponse, CaseUpdate, RecommendationRequest, RecommendationResult

__all__ = [
    "UserCreate", "UserResponse", "UserLogin", "Token",
    "UniversityCreate", "UniversityResponse", "UniversityUpdate",
    "MajorCreate", "MajorResponse", "MajorUpdate",
    "GuideCreate", "GuideResponse", "GuideUpdate",
    "CollectionCreate", "CollectionResponse",
    "CaseCreate", "CaseResponse", "CaseUpdate", "RecommendationRequest", "RecommendationResult"
]

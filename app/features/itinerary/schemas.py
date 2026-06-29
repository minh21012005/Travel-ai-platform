from pydantic import BaseModel, Field


class GenerateItineraryRequest(BaseModel):
    destination: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Travel destination.",
    )

    days: int = Field(
        ...,
        ge=1,
        le=30,
        description="Number of travel days.",
    )

    budget: float = Field(
        ...,
        gt=0,
        description="Budget in VND.",
    )

    interests: list[str] = Field(
        default_factory=list,
        description="Traveler interests.",
    )


class DailyPlan(BaseModel):
    day: int

    activities: list[str]


class GenerateItineraryResponse(BaseModel):
    title: str

    summary: str

    daily_plan: list[DailyPlan]

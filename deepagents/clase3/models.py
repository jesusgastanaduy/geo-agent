from pydantic import BaseModel, Field


class RegionCount(BaseModel):
    """Fire count for a single Peru department."""
    region: str = Field(description="Department name (NAME_1)")
    n_fires: int = Field(description="Number of fire detections in this region")


class FireAnalysisReport(BaseModel):
    """Structured response returned by the agent at the end of every turn."""
    summary: str = Field(
        description="Conversational answer to show the user, in plain language."
    )
    year: int | None = Field(
        default=None, description="Year analyzed, if a fire analysis was run this turn."
    )
    total_fires: int | None = Field(
        default=None, description="Total fire detections after aggregation, if available."
    )
    top_regions: list[RegionCount] = Field(
        default_factory=list,
        description="Top regions by fire count, if an aggregation was run.",
    )

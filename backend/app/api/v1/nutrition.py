"""
Nutrition endpoints: bioavailability and RDA coverage
"""

from fastapi import APIRouter, HTTPException

from app.schemas.nutrition_schema import (
    BioavailabilityRequest,
    BioavailabilityResponse,
    RDACoverageRequest,
    RDACoverageResponse,
)
from app.services.bioavailability_service import bioavailability_engine
from app.services.rda_service import rda_calculator
from app.services.recommendation_service import generate_recommendations


router = APIRouter(prefix="/nutrition", tags=["Nutrition"])


@router.post("/bioavailability", response_model=BioavailabilityResponse)
async def compute_bioavailability(req: BioavailabilityRequest):
    try:
        result = bioavailability_engine.compute(
            ingredients=req.ingredients,
            cooking_method=req.cooking_method,
            stress_level=req.stress_level,
            age=req.age,
            post_workout=req.post_workout,
        )
        return BioavailabilityResponse(
            base_nutrients=result["base_nutrients"],
            adjusted_nutrients=result["adjusted_nutrients"],
            adjustment_factors=result["adjustment_factors"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rda-coverage", response_model=RDACoverageResponse)
async def rda_coverage(req: RDACoverageRequest):
    try:
        coverage = rda_calculator.coverage(
            nutrients=req.adjusted_nutrients,
            age=req.age,
            weight=req.weight_kg,
            height=req.height_cm,
        )
        recs = generate_recommendations(coverage)
        return RDACoverageResponse(
            rda_coverage=coverage,
            user_profile={
                "age": req.age,
                "weight_kg": req.weight_kg,
                "height_cm": req.height_cm,
            },
            recommendations=recs,
            recommendation_count=len(recs),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



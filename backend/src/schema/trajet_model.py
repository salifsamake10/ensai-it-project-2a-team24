from datetime import datetime

from pydantic import BaseModel, Field


class TrajetInput(BaseModel):
	ligne_id: int = Field(gt=0)
	date_heure_depart: datetime
	capacite: int
	tarif_base: float
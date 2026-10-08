from datetime import date

import psycopg
import requests
from fastapi import APIRouter, Depends, HTTPException, Query, Response

from business_object.role import Role
from controller.dependencies import require_roles
from schema.trajet_model import TrajetInput
from service.trajet_service import TrajetImpossibleError, TrajetService

router = APIRouter(prefix="/trips", tags=["Trajets"])
staff = Depends(require_roles(Role.COLLABORATEUR, Role.CLIENT))


def trajet_data(trajet):
	return {
		"id": trajet.id_trajet,
		"line_id": trajet.ligne.id_ligne_exploitation,
		"departure_time": trajet.date_heure_depart,
		"arrival_time": trajet.date_heure_arrivee,
		"duration": trajet.duree_minutes,
		"duration_minutes": trajet.duree_minutes,
		"price": trajet.tarif_base,
		"seats": trajet.capacite,
		"available_seats": max(0, trajet.capacite - trajet.places_reservees),
		"departure_station_id": trajet.ligne.gare_depart.id_sncf,
		"departure_station_name": trajet.ligne.gare_depart.nom,
		"arrival_station_id": trajet.ligne.gare_arrivee.id_sncf,
		"arrival_station_name": trajet.ligne.gare_arrivee.nom,
		"status": trajet.statut.value,
	}


@router.get("/search")
def rechercher_trajets(
	departure_station_id: str = Query(min_length=1),
	arrival_station_id: str = Query(min_length=1),
	date: date = Query(),
):
	if departure_station_id == arrival_station_id:
		raise HTTPException(status_code=422, detail="Les gares doivent être différentes.")
	try:
		trajets = TrajetService().rechercher(departure_station_id, arrival_station_id, date)
		return [trajet_data(trajet) for trajet in trajets]
	except RuntimeError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error


@router.get("")
def liste_trajets(_user=staff):
	try:
		return [trajet_data(trajet) for trajet in TrajetService().lister()]
	except RuntimeError as error:
		raise HTTPException(status_code=503, detail=str(error)) from error


@router.post("", status_code=201)
def create_trip(data: TrajetInput, _user=staff):
	try:
		trajet = TrajetService().creer_trajet(
			data.line_id, data.departure_time, data.seats, data.price
		)
		return trajet_data(trajet)
	except TrajetImpossibleError as error:
		raise HTTPException(status_code=422, detail=str(error)) from error
	except LookupError as error:
		raise HTTPException(status_code=404, detail=str(error)) from error
	except ValueError as error:
		raise HTTPException(status_code=400, detail=str(error)) from error
	except requests.RequestException as error:
		raise HTTPException(status_code=502, detail="Le service SNCF est indisponible.") from error


@router.patch("/{trip_id}")
def update_trip(trip_id: int, data: TripInput, _user=staff):
	try:
		trip = TrajetService().modifier_trajet(
			trip_id, data.line_id, data.departure_time, data.seats, data.price
		)
		return trip_data(trip)
	except TrajetImpossibleError as error:
		raise HTTPException(status_code=422, detail=str(error)) from error
	except LookupError as error:
		raise HTTPException(status_code=404, detail=str(error)) from error
	except ValueError as error:
		raise HTTPException(status_code=400, detail=str(error)) from error
	except requests.RequestException as error:
		raise HTTPException(status_code=502, detail="Le service SNCF est indisponible.") from error


@router.delete("/{trip_id}", status_code=204)
def delete_trip(trip_id: int, _user=staff):
	try:
		TrajetService().delete_trajet(trip_id)
	except LookupError as error:
		raise HTTPException(status_code=404, detail=str(error)) from error
	except psycopg.errors.ForeignKeyViolation as error:
		raise HTTPException(status_code=409, detail="Ce trajet possède des réservations.") from error
	return Response(status_code=204)

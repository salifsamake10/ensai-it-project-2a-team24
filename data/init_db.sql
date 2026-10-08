CREATE TABLE utilisateur (
    id_utilisateur        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username              VARCHAR(100) NOT NULL UNIQUE,
    password_hash         VARCHAR(255) NOT NULL,
    role                  VARCHAR(20) NOT NULL DEFAULT 'CLIENT',
    CONSTRAINT check_role
        CHECK (role IN ('CLIENT', 'COLLABORATEUR', 'ADMIN'))
);

CREATE TABLE gare (
    id_sncf               VARCHAR(100) PRIMARY KEY,
    nom                   VARCHAR(255) NOT NULL
);

CREATE TABLE ligne_exploitation (
    id_ligne_exploitation INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    gare_depart_id        VARCHAR(100) NOT NULL,
    gare_arrivee_id       VARCHAR(100) NOT NULL,

    CONSTRAINT fk_ligne_gare_depart
        FOREIGN KEY (gare_depart_id)
        REFERENCES gare(id_sncf),

    CONSTRAINT fk_ligne_gare_arrivee
        FOREIGN KEY (gare_arrivee_id)
        REFERENCES gare(id_sncf),

    CONSTRAINT check_gares_differentes
        CHECK (gare_depart_id <> gare_arrivee_id)
);


CREATE TABLE trajet (
    id_trajet             INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    ligne_id              INTEGER NOT NULL,
    date_heure_depart     TIMESTAMP NOT NULL,
    date_heure_arrivee    TIMESTAMP NOT NULL,
    duree_minutes         INTEGER NOT NULL,
    capacite              INTEGER NOT NULL,
    places_reservees      INTEGER NOT NULL DEFAULT 0,
    tarif_base            NUMERIC(10, 2) NOT NULL,
    statut                VARCHAR(20) NOT NULL DEFAULT 'PLANIFIE',

    CONSTRAINT fk_trajet_ligne
        FOREIGN KEY (ligne_id)
        REFERENCES ligne_exploitation(id_ligne_exploitation),

    CONSTRAINT check_duree_positive
        CHECK (duree_minutes > 0),

    CONSTRAINT check_capacite_positive
        CHECK (capacite > 0),

    CONSTRAINT check_tarif_non_negatif
        CHECK (tarif_base >= 0),

    CONSTRAINT check_arrivee_apres_depart
        CHECK (date_heure_arrivee > date_heure_depart),

    CONSTRAINT check_statut_trajet
        CHECK (statut IN ('PLANIFIE', 'ANNULE'))
);

CREATE TABLE reservation (
    id_reservation        INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    utilisateur_id        INTEGER NOT NULL,
    trajet_id             INTEGER NOT NULL,
    date_reservation      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    statut                VARCHAR(20) NOT NULL DEFAULT 'CONFIRMEE',
    prix_total            NUMERIC(10, 2) NOT NULL,

    CONSTRAINT fk_reservation_utilisateur
        FOREIGN KEY (utilisateur_id)
        REFERENCES utilisateur(id_utilisateur),

    CONSTRAINT fk_reservation_trajet
        FOREIGN KEY (trajet_id)
        REFERENCES trajet(id_trajet),

    CONSTRAINT check_statut_reservation
        CHECK (statut IN ('CONFIRMEE', 'ANNULEE')),

    CONSTRAINT check_prix_total_non_negatif
        CHECK (prix_total >= 0)
);

CREATE TABLE passager (
    id_passager           INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reservation_id        INTEGER NOT NULL,
    age                   INTEGER NOT NULL,
    classe_voyage         VARCHAR(20) NOT NULL,
    prix                  NUMERIC(10, 2) NOT NULL,

    CONSTRAINT fk_passager_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES reservation(id_reservation)
        ON DELETE CASCADE,

    CONSTRAINT check_age
        CHECK (age >= 0),

    CONSTRAINT check_classe_voyage
        CHECK (classe_voyage IN ('CLASSIQUE', 'PREMIUM')),

    CONSTRAINT check_prix_passager_non_negatif
        CHECK (prix >= 0)
);
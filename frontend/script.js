const API_BASE_URL = (window.TRAVERSE_API_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
const API = {
    stations: "/stations",
    login: "/auth/login",
    register: "/auth/register",
    search: "/trips/search",
    reservations: "/reservations",
    lines: "/lines",
    trips: "/trips"
};

const state = {
    token: localStorage.getItem("traverse-token"),
    user: JSON.parse(localStorage.getItem("traverse-user") || "null"),
    authMode: "login",
    debounce: new Map()
};

const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const escapeHtml = value => String(value ?? "").replace(/[&<>"']/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
}[character]));

async function request(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (state.token) headers.set("Authorization", `Bearer ${state.token}`);
    if (options.body && !(options.body instanceof FormData)) headers.set("Content-Type", "application/json");
    const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
    const text = await response.text();
    let data = null;
    if (text) {
        try { data = JSON.parse(text); } catch { data = { detail: text }; }
    }
    if (!response.ok) {
        const detail = data?.detail || data?.message || `Erreur ${response.status}`;
        throw new Error(Array.isArray(detail) ? detail.map(item => item.msg).join(", ") : detail);
    }
    return data;
}

function listFrom(data, keys = ["items", "results", "data", "trips", "stations", "lines", "reservations"]) {
    if (Array.isArray(data)) return data;
    for (const key of keys) if (Array.isArray(data?.[key])) return data[key];
    return [];
}

function stationLabel(station) {
    return station.name || station.label || station.commercial_name || station.nom || "Gare sans nom";
}

function setupStationAutocomplete(inputId, hiddenId, suggestionsId) {
    const input = $(`#${inputId}`);
    const hidden = $(`#${hiddenId}`);
    const suggestions = $(`#${suggestionsId}`);

    input.addEventListener("input", () => {
        hidden.value = "";
        window.clearTimeout(state.debounce.get(inputId));
        const query = input.value.trim();
        if (query.length < 2) {
            suggestions.replaceChildren();
            suggestions.classList.remove("is-open");
            return;
        }
        state.debounce.set(inputId, window.setTimeout(async () => {
            try {
                const data = await request(`${API.stations}?q=${encodeURIComponent(query)}`);
                const stations = listFrom(data, ["items", "results", "data", "stations"]);
                suggestions.innerHTML = stations.slice(0, 7).map(station => `
                    <button class="suggestion" type="button" role="option" data-id="${escapeHtml(station.id ?? station.uic ?? station.station_id)}" data-name="${escapeHtml(stationLabel(station))}">
                        <span class="suggestion-pin" aria-hidden="true">·</span><span>${escapeHtml(stationLabel(station))}</span>
                    </button>`).join("");
                if (!stations.length) suggestions.innerHTML = `<div class="suggestion-empty">Aucune gare trouvée</div>`;
                suggestions.classList.add("is-open");
            } catch (error) {
                suggestions.innerHTML = `<div class="suggestion-empty">${escapeHtml(error.message)}</div>`;
                suggestions.classList.add("is-open");
            }
        }, 260));
    });

    suggestions.addEventListener("click", event => {
        const option = event.target.closest(".suggestion");
        if (!option) return;
        input.value = option.dataset.name;
        hidden.value = option.dataset.id === "undefined" ? "" : option.dataset.id;
        suggestions.classList.remove("is-open");
        suggestions.replaceChildren();
    });

    document.addEventListener("click", event => {
        if (!event.target.closest(`#${suggestionsId}`) && event.target !== input) suggestions.classList.remove("is-open");
    });
}

function notify(message, isError = false) {
    const toast = $("#toast");
    toast.textContent = message;
    toast.classList.toggle("is-error", isError);
    toast.classList.add("is-visible");
    window.clearTimeout(notify.timeout);
    notify.timeout = window.setTimeout(() => toast.classList.remove("is-visible"), 3600);
}

function formatDateTime(value) {
    if (!value) return "Hora à confirmer";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return escapeHtml(value);
    return new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeStyle: "short" }).format(date);
}

function updateAccountView() {
    const loggedIn = Boolean(state.user && state.token);
    $("#login-button").hidden = loggedIn;
    $("#register-button").hidden = loggedIn;
    $("#logout-button").hidden = !loggedIn;
    $("#account-name").hidden = !loggedIn;
    $("#account-name").textContent = loggedIn ? state.user.username || state.user.name || "Mon compte" : "";
    const role = String(state.user?.role || state.user?.habilitation || "").toUpperCase();
    const staffAccess = loggedIn && ["COLLABORATEUR", "ADMIN"].includes(role);
    $("#open-workspace").hidden = !staffAccess;
    $("#workspace").hidden = !staffAccess;
}

function showAuth(mode = "login") {
    state.authMode = mode;
    $$(".auth-tab").forEach(tab => tab.classList.toggle("active", tab.dataset.authMode === mode));
    $("#auth-title").textContent = mode === "login" ? "Content de vous revoir." : "Bienvenue à bord.";
    $("#auth-password").autocomplete = mode === "login" ? "current-password" : "new-password";
    $(".auth-submit").innerHTML = mode === "login" ? 'Se connecter <span aria-hidden="true">↗</span>' : 'Créer mon compte <span aria-hidden="true">↗</span>';
    $("#auth-message").textContent = "";
    $("#auth-dialog").showModal();
}

async function handleAuth(event) {
    event.preventDefault();
    const username = $("#auth-username").value.trim();
    const password = $("#auth-password").value;
    const message = $("#auth-message");
    const button = $(".auth-submit");
    button.disabled = true;
    message.textContent = "Connexion en cours…";
    try {
        const path = state.authMode === "login" ? API.login : API.register;
        const data = await request(path, { method: "POST", body: JSON.stringify({ username, password }) });
        if (state.authMode === "register" && !data.access_token && !data.token) {
            message.textContent = "Compte créé. Vous pouvez maintenant vous connecter.";
            state.authMode = "login";
            $$(".auth-tab").forEach(tab => tab.classList.toggle("active", tab.dataset.authMode === "login"));
            $("#auth-title").textContent = "Content de vous revoir.";
            $("#auth-password").value = "";
            button.innerHTML = 'Se connecter <span aria-hidden="true">↗</span>';
            return;
        }
        state.token = data.access_token || data.token;
        state.user = data.user || data.account || { username, role: data.role || "CLIENT" };
        if (!state.token) throw new Error("La réponse API ne contient pas de jeton d’accès.");
        localStorage.setItem("traverse-token", state.token);
        localStorage.setItem("traverse-user", JSON.stringify(state.user));
        updateAccountView();
        $("#auth-dialog").close();
        $("#auth-form").reset();
        notify("Vous êtes connecté·e. Bon voyage !");
    } catch (error) {
        message.textContent = error.message;
    } finally {
        button.disabled = false;
    }
}

function renderTrips(trips) {
    const container = $("#results-list");
    $("#results-count").textContent = `${trips.length} ${trips.length === 1 ? "TRAJET" : "TRAJETS"}`;
    if (!trips.length) {
        container.innerHTML = `<div class="empty-state"><span class="empty-mark">↗</span><strong>Pas de trajet pour cette date.</strong><span>Essayez une autre date ou vérifiez les gares sélectionnées.</span></div>`;
        return;
    }
    container.innerHTML = trips.map(trip => {
        const departure = trip.departure_station?.name || trip.departure_station_name || trip.departure_name || trip.origin || "Gare de départ";
        const arrival = trip.arrival_station?.name || trip.arrival_station_name || trip.arrival_name || trip.destination || "Gare d’arrivée";
        const price = trip.price ?? trip.fare ?? trip.tarif;
        const seats = trip.available_seats ?? trip.remaining_seats ?? trip.seats_remaining;
        const duration = trip.duration || trip.travel_time || trip.duration_minutes;
        const durationText = typeof duration === "number" ? `${duration} min` : duration || "Durée communiquée par le transporteur";
        return `<article class="trip-card">
            <div class="trip-route"><div class="trip-station"><span class="route-dot"></span><strong>${escapeHtml(departure)}</strong><span>${escapeHtml(formatDateTime(trip.departure_time || trip.departure_datetime || trip.date))}</span></div><div class="route-journey"><span>${escapeHtml(durationText)}</span><span class="route-line"></span><span>Direct</span></div><div class="trip-station arrival-station"><span class="route-dot"></span><strong>${escapeHtml(arrival)}</strong><span>Arrivée estimée</span></div></div>
            <div class="trip-details">${seats != null ? `<span class="seat-count">${escapeHtml(seats)} places restantes</span>` : ""}<strong class="trip-price">${price != null ? `${escapeHtml(Number(price).toFixed(2).replace(".", ","))} €` : "Tarif à confirmer"}</strong><button class="button button-dark reserve-button" type="button" data-trip-id="${escapeHtml(trip.id ?? trip.trip_id)}">Réserver <span aria-hidden="true">↗</span></button></div>
        </article>`;
    }).join("");
    container.querySelectorAll(".reserve-button").forEach(button => button.addEventListener("click", () => reserveTrip(button.dataset.tripId)));
}

async function searchTrips(event) {
    event.preventDefault();
    const departureId = $("#departure-id").value;
    const arrivalId = $("#arrival-id").value;
    const date = $("#travel-date").value;
    const message = $("#search-message");
    if (!departureId || !arrivalId) {
        message.textContent = "Choisissez les gares dans la liste de suggestions pour lancer la recherche.";
        message.classList.add("message-error");
        return;
    }
    if (departureId === arrivalId) {
        message.textContent = "Les gares de départ et d’arrivée doivent être différentes.";
        message.classList.add("message-error");
        return;
    }
    message.classList.remove("message-error");
    message.textContent = "Recherche des trajets…";
    $("#results-section").hidden = false;
    $("#results-list").innerHTML = `<div class="loading-state">On regarde les horaires disponibles<span class="loading-dots">···</span></div>`;
    try {
        const params = new URLSearchParams({ departure_station_id: departureId, arrival_station_id: arrivalId, date });
        const data = await request(`${API.search}?${params}`);
        renderTrips(listFrom(data));
        message.textContent = "Les horaires et trajets sont fournis par notre réseau.";
        $("#results-section").scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
        $("#results-list").innerHTML = `<div class="empty-state"><strong>Impossible de charger les trajets.</strong><span>${escapeHtml(error.message)}</span><span>Vérifie que l’API est lancée et que la route ${escapeHtml(API.search)} existe.</span></div>`;
        message.textContent = "La recherche n’a pas abouti.";
    }
}

async function reserveTrip(tripId) {
    if (!state.token) {
        showAuth("login");
        $("#auth-message").textContent = "Connectez-vous pour réserver votre trajet.";
        return;
    }
    try {
        await request(API.reservations, { method: "POST", body: JSON.stringify({ trip_id: tripId }) });
        notify("Trajet réservé. Bon voyage !");
    } catch (error) {
        notify(`Réservation impossible : ${error.message}`, true);
    }
}

async function loadReservations() {
    if (!state.token) {
        showAuth("login");
        $("#auth-message").textContent = "Connectez-vous pour retrouver vos réservations.";
        return;
    }
    const dialog = $("#reservations-dialog");
    const container = $("#reservations-list");
    container.innerHTML = `<div class="loading-state">Chargement de vos voyages…</div>`;
    if (!dialog.open) dialog.showModal();
    try {
        const reservations = listFrom(await request(API.reservations));
        container.innerHTML = reservations.length ? reservations.map(item => `<article class="reservation-item"><div><strong>${escapeHtml(item.trip?.departure_station?.name || item.departure_station_name || "Votre trajet")} → ${escapeHtml(item.trip?.arrival_station?.name || item.arrival_station_name || "Destination")}</strong><span>${escapeHtml(formatDateTime(item.trip?.departure_time || item.departure_time))}</span></div><button class="button button-quiet cancel-reservation" type="button" data-id="${escapeHtml(item.id ?? item.reservation_id)}">Annuler</button></article>`).join("") : `<div class="empty-state">Aucune réservation pour le moment.</div>`;
        container.querySelectorAll(".cancel-reservation").forEach(button => button.addEventListener("click", async () => {
            try {
                await request(`${API.reservations}/${encodeURIComponent(button.dataset.id)}`, { method: "DELETE" });
                notify("Réservation annulée.");
                await loadReservations();
            } catch (error) { notify(`Annulation impossible : ${error.message}`, true); }
        }));
    } catch (error) {
        container.innerHTML = `<div class="empty-state">Impossible de charger les réservations. ${escapeHtml(error.message)}</div>`;
    }
}

function renderManageList(kind, items) {
    const container = $(`#${kind}s-list`);
    if (!items.length) {
        container.innerHTML = `<div class="empty-state">Aucun ${kind === "line" ? "ligne" : "trajet"} enregistré.</div>`;
        return;
    }
    container.innerHTML = items.map(item => {
        const label = kind === "line" ? item.name || item.label || `Ligne ${item.id}` : `${item.departure_station_name || item.line?.name || `Ligne ${item.line_id}`} · ${formatDateTime(item.departure_time)}`;
        const detail = kind === "line" ? `${item.departure_station_name || item.departure_station_id || "Départ"} → ${item.arrival_station_name || item.arrival_station_id || "Terminus"}` : `${item.seats ?? item.available_seats ?? "—"} places · ${item.price != null ? `${item.price} €` : "Tarif à définir"}`;
        return `<article class="manage-item"><div><strong>${escapeHtml(label)}</strong><span>${escapeHtml(detail)}</span></div><div class="manage-actions"><button class="icon-button edit-item" type="button" data-kind="${kind}" data-id="${escapeHtml(item.id)}" aria-label="Modifier" title="Modifier">✎</button><button class="icon-button delete-item" type="button" data-kind="${kind}" data-id="${escapeHtml(item.id)}" aria-label="Supprimer" title="Supprimer">×</button></div></article>`;
    }).join("");
    container.querySelectorAll(".edit-item").forEach(button => button.addEventListener("click", () => editItem(kind, items.find(item => String(item.id) === button.dataset.id))));
    container.querySelectorAll(".delete-item").forEach(button => button.addEventListener("click", () => deleteItem(kind, button.dataset.id)));
}

async function loadManageItems(kind) {
    const list = $(`#${kind}s-list`);
    list.innerHTML = `<div class="loading-state">Chargement…</div>`;
    try {
        renderManageList(kind, listFrom(await request(API[`${kind}s`]), ["items", "results", "data", `${kind}s`]));
    } catch (error) {
        list.innerHTML = `<div class="empty-state">${escapeHtml(error.message)}<br>Vérifie que la route ${escapeHtml(API[`${kind}s`])} existe.</div>`;
    }
}

function editItem(kind, item) {
    if (!item) return;
    const form = $(`#${kind}-form`);
    $(`#${kind}-id`).value = item.id;
    if (kind === "line") {
        $("#line-name").value = item.name || item.label || "";
        $("#line-departure").value = item.departure_station_name || item.departure_station?.name || item.departure_station_id || "";
        $("#line-departure-id").value = item.departure_station_id || "";
        $("#line-arrival").value = item.arrival_station_name || item.arrival_station?.name || item.arrival_station_id || "";
        $("#line-arrival-id").value = item.arrival_station_id || "";
        $("#line-form-title").textContent = "Modifier la ligne";
    } else {
        $("#trip-line-id").value = item.line_id || "";
        $("#trip-departure-time").value = item.departure_time ? new Date(item.departure_time).toISOString().slice(0, 16) : "";
        $("#trip-seats").value = item.seats ?? item.available_seats ?? "";
        $("#trip-price").value = item.price ?? "";
        $("#trip-form-title").textContent = "Modifier le trajet";
    }
    $(`[data-cancel="${kind}"]`).hidden = false;
    form.scrollIntoView({ behavior: "smooth", block: "center" });
}

async function submitManageForm(event, kind) {
    event.preventDefault();
    const form = event.currentTarget;
    const idField = kind === "line" ? "#line-id" : "#trip-id";
    const id = $(idField).value;
    const fields = kind === "line" ? ["name", "departure_station_id", "arrival_station_id"] : ["line_id", "departure_time", "seats", "price"];
    const payload = Object.fromEntries(fields.map(field => [field, form.elements[field].value]));
    if (kind === "trip") {
        payload.seats = Number(payload.seats);
        payload.price = Number(payload.price);
    }
    try {
        await request(id ? `${API[`${kind}s`]}/${encodeURIComponent(id)}` : API[`${kind}s`], { method: id ? "PATCH" : "POST", body: JSON.stringify(payload) });
        form.reset();
        $(idField).value = "";
        $(`#${kind}-form-title`).textContent = kind === "line" ? "Créer une ligne" : "Planifier un trajet";
        $(`[data-cancel="${kind}"]`).hidden = true;
        notify(kind === "line" ? "Ligne enregistrée." : "Trajet enregistré.");
        await loadManageItems(kind);
    } catch (error) { notify(`Enregistrement impossible : ${error.message}`, true); }
}

async function deleteItem(kind, id) {
    if (!window.confirm("Supprimer cet élément ? Cette action est définitive.")) return;
    try {
        await request(`${API[`${kind}s`]}/${encodeURIComponent(id)}`, { method: "DELETE" });
        notify(kind === "line" ? "Ligne supprimée." : "Trajet supprimé.");
        await loadManageItems(kind);
    } catch (error) { notify(`Suppression impossible : ${error.message}`, true); }
}

function init() {
    const today = new Date();
    const localToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    $("#travel-date").min = localToday;
    $("#travel-date").value = localToday;
    setupStationAutocomplete("departure", "departure-id", "departure-suggestions");
    setupStationAutocomplete("arrival", "arrival-id", "arrival-suggestions");
    setupStationAutocomplete("line-departure", "line-departure-id", "line-departure-suggestions");
    setupStationAutocomplete("line-arrival", "line-arrival-id", "line-arrival-suggestions");
    $("#search-form").addEventListener("submit", searchTrips);
    $("#swap-stations").addEventListener("click", () => {
        for (const suffix of ["", "-id"]) {
            const departure = $(`#departure${suffix}`);
            const arrival = $(`#arrival${suffix}`);
            [departure.value, arrival.value] = [arrival.value, departure.value];
        }
    });
    $$("[data-date-offset]").forEach(button => button.addEventListener("click", () => {
        const date = new Date();
        date.setDate(date.getDate() + Number(button.dataset.dateOffset));
        $("#travel-date").value = new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    }));
    $("#login-button").addEventListener("click", () => showAuth("login"));
    $("#register-button").addEventListener("click", () => showAuth("register"));
    $("#auth-form").addEventListener("submit", handleAuth);
    $$("[data-auth-mode]").forEach(button => button.addEventListener("click", () => showAuth(button.dataset.authMode)));
    $$("[data-close-dialog]").forEach(button => button.addEventListener("click", () => button.closest("dialog").close()));
    $("#open-reservations").addEventListener("click", loadReservations);
    $("#logout-button").addEventListener("click", () => {
        state.token = null;
        state.user = null;
        localStorage.removeItem("traverse-token");
        localStorage.removeItem("traverse-user");
        updateAccountView();
        notify("Vous êtes déconnecté·e.");
    });
    $$("[data-workspace-tab]").forEach(button => button.addEventListener("click", () => {
        const tab = button.dataset.workspaceTab;
        $$("[data-workspace-tab]").forEach(item => {
            const active = item === button;
            item.classList.toggle("active", active);
            item.setAttribute("aria-selected", String(active));
        });
        $("#lines-panel").hidden = tab !== "lines";
        $("#trips-panel").hidden = tab !== "trips";
        loadManageItems(tab === "lines" ? "line" : "trip");
    }));
    $("#line-form").addEventListener("submit", event => submitManageForm(event, "line"));
    $("#trip-form").addEventListener("submit", event => submitManageForm(event, "trip"));
    $$(".cancel-edit").forEach(button => button.addEventListener("click", () => {
        const kind = button.dataset.cancel;
        $(`#${kind}-form`).reset();
        $(`#${kind}-id`).value = "";
        $(`#${kind}-form-title`).textContent = kind === "line" ? "Créer une ligne" : "Planifier un trajet";
        button.hidden = true;
    }));
    updateAccountView();
}

init();
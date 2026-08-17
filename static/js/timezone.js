document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll("tr[data-utc]").forEach(row => {

        const utc = row.dataset.utc;

        const date = new Date(utc);

        row.querySelector(".race-day").textContent =
            date.toLocaleDateString(undefined, {
                weekday: "short"
            });

        row.querySelector(".race-date").textContent =
            date.toLocaleDateString(undefined, {
                day: "numeric",
                month: "short"
            });

        row.querySelector(".race-time").textContent =
            date.toLocaleTimeString(undefined, {
                hour: "numeric",
                minute: "2-digit",
                timeZoneName: "short"
            });

    });

});
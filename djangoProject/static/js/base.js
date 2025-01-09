import {getToCloseToast} from "./toast-template.js";

document.addEventListener("DOMContentLoaded", () => {


    // Define the API endpoints
    const getIsToCloseAPI = `/raspberry/get_is_to_close/`;
    let refreshTime = 10000
    let lastToCloseStatus = null;

    const showToast = (message, isToClose) => {
        const existingToast = $('#ToCloseToast');
        if (existingToast.length) {
            existingToast.toast('hide');
            existingToast.remove();
        }
    // Create a toast with the help off toast-template.js
        const toastTemplate = getToCloseToast(message, isToClose);
        $('#toast-container').append(toastTemplate);
        const toCloseToast = $('#ToCloseToast');

        toCloseToast.toast('show');

        toCloseToast.on('hidden.bs.toast', function () {
            toCloseToast.remove();
        });
    };


    // Makes a get request on the is_to_close variable from the database.
    // If that is different from the last status it wil push a toast to the browser
    const fetchStatuses = () => {

        const fetchIsToCloseStatus = fetch(getIsToCloseAPI, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        });

        Promise.any([ fetchIsToCloseStatus])
            .then(([onlineData, isToCloseData]) => {
                const is_to_close = isToCloseData.is_to_close;
                // Show toast if is-to-close status changes
                if (lastToCloseStatus !== null && lastToCloseStatus !== is_to_close) {
                    const message = is_to_close ? "You are too close to the screen." : "You are now at a safe distance from your screen.";
                    showToast(message, false, is_to_close); // Pass `true` for is-to-close status
                }

                // Update last statuses
                lastToCloseStatus = is_to_close;
            })
            .catch(error => {
                console.error("Error fetching statuses:", error);
            });
    };

    // Call fetchStatuses at regular intervals (e.g., every 5 seconds)
    setInterval(fetchStatuses, refreshTime);
});
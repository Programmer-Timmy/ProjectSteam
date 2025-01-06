import {getToCloseToast} from "./toast-template.js";

document.addEventListener("DOMContentLoaded", () => {
    // if (hasRaspberry){


    // Define the API endpoints
    const getOnlineStatusAPI = `/raspberry/get_status/`;
    const getIsToCloseAPI = `/raspberry/get_is_to_close/`;
    let refreshTime = 10000
    let lastOnlineStatus = null;
    let lastToCloseStatus = null;

    const showToast = (message, isOnline, isToClose) => {
        const existingToast = $('#ToCloseToast');
        if (existingToast.length) {
            existingToast.toast('hide');
            existingToast.remove();
        }

        const toastTemplate = getToCloseToast(message, isToClose);
        $('#toast-container').append(toastTemplate);
        const toCloseToast = $('#ToCloseToast');

        toCloseToast.toast('show');

        toCloseToast.on('hidden.bs.toast', function () {
            toCloseToast.remove();
        });
    };

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
        const fetchOnlineStatus = fetch(getOnlineStatusAPI, {
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



        Promise.all([fetchOnlineStatus, fetchIsToCloseStatus])
            .then(([onlineData, isToCloseData]) => {
                const is_online = onlineData.is_online;
                const is_to_close = isToCloseData.is_to_close;

                // Show toast if online status changes
                if (lastOnlineStatus !== null && lastOnlineStatus !== is_online) {
                    const message = is_online ? "The user is now online." : "The user is now offline.";
                    showToast(message, is_online, false); // Pass `false` for online status
                }

                // Show toast if is-to-close status changes
                if (lastToCloseStatus !== null && lastToCloseStatus !== is_to_close) {
                    const message = is_to_close ? "You are too close to the screen." : "You are now at a safe distance from your screen.";
                    showToast(message, false, is_to_close); // Pass `true` for is-to-close status
                }

                // Update last statuses
                lastOnlineStatus = is_online;
                lastToCloseStatus = is_to_close;
            })
            .catch(error => {
                console.error("Error fetching statuses:", error);
            });
    };

    // Call fetchStatuses at regular intervals (e.g., every 5 seconds)
    setInterval(fetchStatuses, refreshTime);
        // }
});
document.addEventListener("DOMContentLoaded", () => {
    // Define the API endpoints
    const getOnlineStatusAPI = `/raspberry/get_status/`;
    const getIsToCloseAPI = `/raspberry/get_is_to_close/`;

    let lastOnlineStatus = null;
    let lastToCloseStatus = null;

    const createToastContainer = () => {
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.style.position = 'fixed';
            toastContainer.style.top = '20px';
            toastContainer.style.right = '20px';
            toastContainer.style.zIndex = '1050';
            document.body.appendChild(toastContainer);
        }
        return toastContainer;
    };

    const showToast = (message, isOnline, isToClose) => {
        const toastContainer = createToastContainer();

        const toastElement = document.createElement('div');
        toastElement.className = 'toast';
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');

        // Determine the toast color based on the status
        if (isToClose) {
            toastElement.style.backgroundColor = 'red';
        } else if (isOnline) {
            toastElement.style.backgroundColor = 'green';
        } else {
            toastElement.style.backgroundColor = 'grey';
        }

        toastElement.innerHTML = `
            <div class="toast-header ${isToClose ? 'bg-danger text-white' : (isOnline ? 'bg-success text-white' : 'bg-success text-black')}">
                <strong class="me-auto">Status Update</strong>
                <small>just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body text-black">
                ${message}
            </div>
        `;

        toastContainer.appendChild(toastElement);

        const bootstrapToast = new bootstrap.Toast(toastElement);
        bootstrapToast.show();

        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
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

                // Update DOM for user status
                const userInfoDiv = document.getElementById("user-info");
                if (userInfoDiv) {
                    userInfoDiv.innerHTML = `
                        <h1>User Status</h1>
                        <p>User: ${onlineData.user_id}</p>
                        <p>Status: 
                            <span style="color: ${is_online ? 'green' : 'red'};">${is_online ? 'Online' : 'Offline'}</span>
                        </p>
                    `;
                }

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
    setInterval(fetchStatuses, 5000);

});

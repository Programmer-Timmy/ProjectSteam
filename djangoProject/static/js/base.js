document.addEventListener("DOMContentLoaded", () => {
    // Define the API endpoint
    const getOnlineStatusAPI = `/raspberry/get_status`; //
    const getIsToCloseAPI = `/raspberry/get_is_to_close_status`;

    let lastOnlineStatus = null; //

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

    const showToast = (message, isOnline) => {
        const toastContainer = createToastContainer();

        const toastElement = document.createElement('div');
        toastElement.className = 'toast';
        toastElement.setAttribute('role', 'alert');
        toastElement.setAttribute('aria-live', 'assertive');
        toastElement.setAttribute('aria-atomic', 'true');


        toastElement.style.backgroundColor = isOnline ? 'green' : 'red';

        toastElement.innerHTML = `
            <div class="toast-header ${isOnline ? 'bg-success text-white' : 'bg-danger text-white'}">
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

const fetchIsToCloseStatus = () => {
    fetch(getIsToCloseAPI, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => {
            if(!response.ok){
                throw new Error(`HTTP error! Status ${response.status}`);
            }
            return response
        })
        .then(data => {
            var is_to_close = data.is_to_close
            if(lastToCloseStatus !== null && lastToCloseStatus !== is_to_close){
                const message = is_to_close ? "You are to close to the screen" :"You are now at a safe distance of your screen";
                showToast(message, is_to_close)
            }

            const lastToCloseStatus = is_to_close
        })
        .catch(error => {
            console.error("Error fetching user data:", error)
        })
}
    const fetchUserStatus = () => {
        fetch(getOnlineStatusAPI, {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            var is_online = data.is_online

            const userInfoDiv = document.getElementById("user-info");
            if (userInfoDiv) {
                // Update the DOM with the fetched data
                userInfoDiv.innerHTML = `
                    <h1>User Status</h1>
                    <p>User: ${data.user_id}</p>
                    <p>Status: 
                        <span style="color: ${data.is_online ? 'green' : 'red'};">${data.is_online ? 'Online' : 'Offline'}</span>
                    </p>
                `;
            }


            if (lastOnlineStatus !== null && lastOnlineStatus !== is_online) {
                const message = is_online ? "The user is now online." : "The user is now offline.";
                showToast(message, is_online);
            }

            lastOnlineStatus = is_online; // Update the previous status
        })
        .catch(error => {
            console.error("Error fetching user data:", error);
        });
    };


    fetchUserStatus();
    fetchIsToCloseStatus()

    setInterval(fetchUserStatus, 5000); // Adjust polling interval as needed
});

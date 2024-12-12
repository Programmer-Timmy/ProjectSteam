document.addEventListener("DOMContentLoaded", () => {
    // Define the API endpoint
    const apiUrl = `/raspberry/get_status`; //

    let lastStatus = null; //

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

    const fetchUserStatus = () => {
        fetch(apiUrl, {
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
            console.log("User data fetched successfully:", data);

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


            if (lastStatus !== null && lastStatus !== data.is_online) {
                const message = data.is_online ? "The user is now online." : "The user is now offline.";
                showToast(message, data.is_online);
            }

            lastStatus = data.is_online; // Update the previous status
        })
        .catch(error => {
            console.error("Error fetching user data:", error);
        });
    };


    fetchUserStatus();


    setInterval(fetchUserStatus, 5000); // Adjust polling interval as needed
});

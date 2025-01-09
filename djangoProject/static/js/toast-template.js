//Creates a toast with a message. Toast gets a custom color depending on the type.

export function getToCloseToast(message, type) {
    return `
        <div class="toast" id="ToCloseToast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
           <div class="toast-header text-white ${type ? 'bg-danger' : 'bg-success'}">
                <strong class="me-auto">Status Update</strong>
                <small>just now</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body text-white">
                ${message}
            </div>
        </div>
    `;
}
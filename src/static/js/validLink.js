document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const destLinkInput = form.querySelector('input[name="dest_link"]');
    const customLinkInput = form.querySelector('input[name="custom_link"]');
    const destLinkError = document.createElement('p');
    const customLinkError = document.createElement('p');

    destLinkError.classList.add('error-message');
    customLinkError.classList.add('error-message');

    // Append error messages right after inputs
    destLinkInput.parentNode.insertBefore(destLinkError, destLinkInput.nextSibling);
    customLinkInput.parentNode.insertBefore(customLinkError, customLinkInput.nextSibling);

    // Function to validate URLs
    const isValidURL = (url) => {
        const pattern = new RegExp(
            '^(https?:\\/\\/)?' + // Protocol (http or https)
            '(([a-zA-Z0-9_-]+\\.)+[a-zA-Z]{2,6})' + // Domain name
            '(\\/[a-zA-Z0-9@:%_\\+.~#?&//=]*)?$', // Path, query, or fragment
            'i'
        );
        return pattern.test(url);
    };

    // Function to add https:// if missing
    const addHttpsIfMissing = (url) => {
        if (!/^https?:\/\//i.test(url)) {
            return 'https://' + url;
        }
        return url;
    };

    // Validate destination link on input
    destLinkInput.addEventListener('blur', () => {
        // Auto-correct the URL if missing protocol
        destLinkInput.value = addHttpsIfMissing(destLinkInput.value);

        // Validate URL
        if (!isValidURL(destLinkInput.value)) {
            destLinkError.textContent = 'Please enter a valid URL (e.g., https://example.com)';
        } else {
            destLinkError.textContent = '';
        }
    });

    // Validate custom link for valid characters
    customLinkInput.addEventListener('input', () => {
        if (customLinkInput.value && /[^a-zA-Z0-9_-]/.test(customLinkInput.value)) {
            customLinkError.textContent = 'Custom link can only contain letters, numbers, dashes, and underscores.';
        } else {
            customLinkError.textContent = '';
        }
    });

    // Validate form on submit
    form.addEventListener('submit', (event) => {
        let isValid = true;

        // Auto-correct the URL if missing protocol
        destLinkInput.value = addHttpsIfMissing(destLinkInput.value);

        if (!isValidURL(destLinkInput.value)) {
            destLinkError.textContent = 'Please enter a valid URL (e.g., https://example.com)';
            isValid = false;
        }

        if (customLinkInput.value && /[^a-zA-Z0-9_-]/.test(customLinkInput.value)) {
            customLinkError.textContent = 'Custom link can only contain letters, numbers, dashes, and underscores.';
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const destLinkInput = form.querySelector('input[name="dest_link"]');
    const customLinkInput = form.querySelector('input[name="custom_link"]');
    const destLinkError = document.createElement('p');
    const customLinkError = document.createElement('p');

    destLinkError.classList.add('error-message');
    customLinkError.classList.add('error-message');

    destLinkInput.parentNode.insertBefore(destLinkError, destLinkInput.nextSibling);
    customLinkInput.parentNode.insertBefore(customLinkError, customLinkInput.nextSibling);

    const isValidURL = (url) => {
        const pattern = new RegExp(
            '^(https?:\\/\\/)' +
            '(([a-zA-Z0-9_-]+\\.)+[a-zA-Z]{2,})' +
            '(\\:\\d+)?' +
            '(\\/[a-zA-Z0-9@:%_\\+.~#?&//=~-]*)?$',
            'i'
        );
    
        return pattern.test(url);
    };
    

    const addHttpsIfMissing = (url) => {
        if (!/^https?:\/\//i.test(url)) {
            return 'https://' + url;
        }
        return url;
    };

    destLinkInput.addEventListener('blur', () => {
        destLinkInput.value = addHttpsIfMissing(destLinkInput.value);

        if (!isValidURL(destLinkInput.value)) {
            destLinkError.textContent = 'Please enter a valid URL (e.g., https://example.com)';
        } else {
            destLinkError.textContent = '';
        }
    });

    customLinkInput.addEventListener('input', () => {
        if (customLinkInput.value && /[^a-zA-Z0-9_-]/.test(customLinkInput.value)) {
            customLinkError.textContent = 'Custom link can only contain letters, numbers, dashes, and underscores.';
        } else {
            customLinkError.textContent = '';
        }
    });

    form.addEventListener('submit', (event) => {
        let isValid = true;

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
            event.preventDefault();
        }
    });
});

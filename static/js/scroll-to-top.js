document.body.addEventListener('htmx:afterSwap', function (evt) {
    const container = evt.detail.target;
    if (container.id === 'content-container') {
        requestAnimationFrame(() => {
            container.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        });
    }
});
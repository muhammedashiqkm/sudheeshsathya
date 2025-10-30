document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('content-container');
    if (!container) return;

    function scrollToCard() {
        const urlParams = new URLSearchParams(window.location.search);
        const fromId = urlParams.get('from');
        if (!fromId) return;

        const targetCard = container.querySelector(`[data-id="${fromId}"]`);
        if (!targetCard) return;

        // Clean URL
        const cleanSearch = window.location.search
            .replace(/[?&]from=[^&]+/g, '')
            .replace(/&$/, '');
        const cleanUrl = window.location.pathname + cleanSearch + window.location.hash;
        history.replaceState({}, '', cleanUrl);

        requestAnimationFrame(() => {
            targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            targetCard.classList.add('highlight-card');
            setTimeout(() => targetCard.classList.remove('highlight-card'), 2000);
        });
    }

    scrollToCard();

    document.body.addEventListener('htmx:afterSwap', function (evt) {
        if (evt.detail.target.id === 'content-container') {
            setTimeout(scrollToCard, 100);
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    // 1. Select all the elements you want to animate
    const sectionsToFade = document.querySelectorAll('.fade-in-section');

    if (!sectionsToFade.length) {
        return; // No sections to observe, so stop.
    }

    // 2. Set up the observer options
    const options = {
        root: null, // Observe intersections relative to the viewport
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% of the element is visible
    };

    // 3. Create the observer callback function
    const callback = (entries, observer) => {
        entries.forEach(entry => {
            // If the element is on screen
            if (entry.isIntersecting) {
                // Add the .is-visible class to trigger the CSS transition
                entry.target.classList.add('is-visible');
                
                // Stop observing this element so the animation only runs once
                observer.unobserve(entry.target);
            }
        });
    };

    // 4. Create the observer and start observing
    const observer = new IntersectionObserver(callback, options);
    sectionsToFade.forEach(section => {
        observer.observe(section);
    });
});
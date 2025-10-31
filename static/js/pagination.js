/**
 * ==========================================================================
 * PORTFOLIO SITE MAIN JAVASCRIPT FILE
 * ==========================================================================
 */

/**
 * --------------------------------------------------------------------------
 * SECTION: RESPONSIVE PAGINATION
 * --------------------------------------------------------------------------
 * Manages responsive pagination by showing a "window"
 * of page numbers centered around the active page.
 */
function updatePaginationView() {
    // Find all pagination components on the page
    const paginations = document.querySelectorAll('.pagination');
    if (paginations.length === 0) return; // No pagination found

    const screenWidth = window.innerWidth;
    let visibleCount;

    // 1. Set how many numbers to show based on screen width

    if (screenWidth <= 350) {
        visibleCount = 2;
    }
    else if (screenWidth <= 480) {
        visibleCount = 3;
    }
     else if (screenWidth <= 768) {
        visibleCount = 6;
    } else {
        visibleCount = 10;
    }

    paginations.forEach(pagination => {
        // Get all items and filter out any "Prev" or "Next" links
        const allItems = Array.from(pagination.querySelectorAll('.page-item'));
        
        const numberedItems = allItems.filter(item => {
            const linkText = item.querySelector('.page-link')?.textContent.trim();
            // Keep it if it's active OR if its text is a number
            return item.classList.contains('active') || !isNaN(parseInt(linkText, 10));
        });

        // Always show non-numbered items (like "Prev", "Next")
        allItems.filter(item => !numberedItems.includes(item))
               .forEach(item => item.style.display = 'block');
        
        // If we don't have enough pages to hide, show them all and stop
        if (numberedItems.length <= visibleCount) {
            numberedItems.forEach(item => item.style.display = 'block');
            return;
        }

        // 2. Find the active page
        const activeItem = numberedItems.find(item => item.classList.contains('active'));
        let activeIndex = numberedItems.indexOf(activeItem);
        if (activeIndex === -1) activeIndex = 0; // Default to page 1

        // 3. Hide all numbered items first
        numberedItems.forEach(item => item.style.display = 'none'); 

        // 4. Calculate the "window" of pages to show
        let half = Math.floor(visibleCount / 2);
        let start = activeIndex - half;
        let end = activeIndex + half;
        
        // Adjust for even numbers (e.g., 10)
        if (visibleCount % 2 === 0) {
            end--;
        }

        // Adjust for edge case (near the start)
        if (start < 0) {
            start = 0;
            end = visibleCount - 1;
        }

        // Adjust for edge case (near the end)
        if (end >= numberedItems.length) {
            end = numberedItems.length - 1;
            start = end - visibleCount + 1;
            if (start < 0) start = 0; // Final check for very few pages
        }

        // 5. Show only the pages in our calculated window
        for (let i = start; i <= end; i++) {
            if (numberedItems[i]) {
                numberedItems[i].style.display = 'block';
            }
        }
    });
}


/**
 * --------------------------------------------------------------------------
 * SECTION: EVENT LISTENERS
 * --------------------------------------------------------------------------
 * Runs all site functions at the appropriate times.
 */
document.addEventListener('DOMContentLoaded', function () {
    
    // --- 1. PAGINATION: Run on Initial Page Load ---
    updatePaginationView();
    
    // --- 2. PAGINATION: Re-run on Window Resize ---
    window.addEventListener('resize', updatePaginationView);

    // --- 3. PAGINATION: Re-run after any HTMX content swap ---
    // This is the fix for pagination clicks
    document.body.addEventListener('htmx:afterSwap', function() {
        updatePaginationView();
    });


    // --- 4. SCROLL-TO-CARD: Logic for blog/video list pages ---
    const params = new URLSearchParams(window.location.search);
    const scrollTo = params.get('scroll_to');
    
    if (scrollTo) {
        const target = document.getElementById('card-' + scrollTo);
        if (target) {
            // Scroll to the card
            target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Highlight the card
            target.style.transition = 'background-color 0.6s ease';
            target.style.backgroundColor = '#fff8e1'; // A light yellow highlight
            
            // Remove the highlight after a moment
            setTimeout(() => {
                target.style.backgroundColor = '';
            }, 1800);
        }
        
        // Clean the URL so it doesn't run again on refresh
        params.delete('scroll_to');
        const newUrl = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
        history.replaceState(null, '', newUrl);
    }
});
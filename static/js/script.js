document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.slider').forEach(slider => {
        const container = slider.querySelector('.NGContainer, .allgames-container');
        const cards = container.querySelectorAll('.game-card, .all-games-card');
        const prevArrow = slider.querySelector('.arrow--prev');
        const nextArrow = slider.querySelector('.arrow--next');

        let visibleCount = 3;
        if (slider.classList.contains('slider')) visibleCount = 5;

        let start = 0;

        function showCards() {
            cards.forEach((card, index) => {
                card.style.display = (index >= start && index < start + visibleCount) ? 'block' : 'none';
            });
        }

        if (prevArrow) {
            prevArrow.addEventListener('click', () => {
                if (start > 0) {
                    start--;
                    showCards();
                }
            });
        }

        if (nextArrow) {
            nextArrow.addEventListener('click', () => {
                if (start < cards.length - visibleCount) {
                    start++;
                    showCards();
                }
            });
        }

        showCards(); // საწყისში გაჩვენოს
    });

    // პაგინაციის ისრებისთვის (All Games ბოლოში)
    const btns = document.querySelectorAll('.btn');
    const paginationWrapper = document.querySelector('.pagination-wrapper');

    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (btn.classList.contains('btn--prev')) {
                paginationWrapper.classList.add('transition-prev');
            } else {
                paginationWrapper.classList.add('transition-next');
            }

            setTimeout(() => {
                paginationWrapper.classList.remove('transition-next');
                paginationWrapper.classList.remove('transition-prev');
            }, 500);
        });
    });
});

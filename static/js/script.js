var btns = document.querySelectorAll('.btn');
var paginationWrapper = document.querySelector('.pagination-wrapper');
var bigDotContainer = document.querySelector('.big-dot-container');
var littleDot = document.querySelector('.little-dot');

for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', btnClick);
}

function btnClick() {
    if (this.classList.contains('btn--prev')) {
        paginationWrapper.classList.add('transition-prev');
    } else {
        paginationWrapper.classList.add('transition-next');
    }

    var timeout = setTimeout(cleanClasses, 500);
}

function cleanClasses() {
    if (paginationWrapper.classList.contains('transition-next')) {
        paginationWrapper.classList.remove('transition-next')
    } else if (paginationWrapper.classList.contains('transition-prev')) {
        paginationWrapper.classList.remove('transition-prev')
    }
}

function setupSlider(sliderSelector, cardSelector, visibleCount = 3) {
    const slider = document.querySelector(sliderSelector);
    if (!slider) return;
    const cards = slider.querySelectorAll(cardSelector);
    let start = 0;

    function showCards() {
        cards.forEach((card, i) => {
            card.style.display = (i >= start && i < start + visibleCount) ? '' : 'none';
        });
    }

    slider.querySelector('.arrow--prev').onclick = function () {
        if (start > 0) start--;
        showCards();
    };
    slider.querySelector('.arrow--next').onclick = function () {
        if (start < cards.length - visibleCount) start++;
        showCards();
    };

    showCards();
}

setupSlider('.slider-new', '.game-card', 3);
setupSlider('.slider-recommended', '.game-card', 3);
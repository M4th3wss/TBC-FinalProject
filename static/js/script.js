document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.game-container');
    const windows = document.querySelectorAll('.game-window');
    const leftBtn = document.querySelector('.left-btn');
    const rightBtn = document.querySelector('.right-btn');
    const progressBar = document.querySelector('.progress-bar');
    let scrollPos = 0;
    const maxScroll = container.scrollWidth - container.clientWidth;

    leftBtn.addEventListener('click', () => {
        scrollPos = Math.max(0, scrollPos - 200);
        container.scrollLeft = scrollPos;
        updateProgress();
    });

    rightBtn.addEventListener('click', () => {
        scrollPos = Math.min(maxScroll, scrollPos + 200);
        container.scrollLeft = scrollPos;
        updateProgress();
    });

    windows.forEach(window => {
        window.addEventListener('mouseover', () => {
            window.style.transform = 'scale(1.1)';
            const desc = document.createElement('div');
            desc.className = 'desc-window';
            desc.textContent = window.getAttribute('data-desc');
            window.appendChild(desc);
        });

        window.addEventListener('mouseout', () => {
            window.style.transform = 'scale(1)';
            const desc = window.querySelector('.desc-window');
            if (desc) desc.remove();
        });
    });

    container.addEventListener('scroll', updateProgress);
    function updateProgress() {
        const scrollPercentage = (container.scrollLeft / maxScroll) * 100;
        progressBar.style.width = `${scrollPercentage}%`;
    }

    windows.forEach(window => {
        window.addEventListener('mouseover', () => {
            windows.forEach(w => {
                if (w !== window) w.style.transform = 'scale(0.9)';
            });
        });
        window.addEventListener('mouseout', () => {
            windows.forEach(w => w.style.transform = 'scale(1)');
        });
    });
});
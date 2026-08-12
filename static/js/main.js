// main.js — students will add JavaScript here as features are built

(function () {
    var overlay = document.getElementById('how-it-works-overlay');
    var trigger = document.getElementById('how-it-works-trigger');
    var closeBtn = document.getElementById('how-it-works-close');
    var iframe = document.getElementById('how-it-works-iframe');

    if (!overlay || !trigger || !closeBtn || !iframe) return;

    var videoSrc = iframe.dataset.src;

    function openModal(event) {
        event.preventDefault();
        iframe.src = videoSrc + '?autoplay=1';
        overlay.hidden = false;
    }

    function closeModal() {
        overlay.hidden = true;
        iframe.src = '';
    }

    trigger.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function (event) {
        if (event.target === overlay) closeModal();
    });
})();

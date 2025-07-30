import { CountUp } from './countUp.min.js';

function runCounters() {
    if (typeof CountUp === 'undefined') return;

    const counters = document.querySelectorAll('[data-value]');
    counters.forEach(counter => {
        if (counter.hasAttribute('data-animated')) return;

        const endVal = parseFloat(counter.getAttribute('data-value'));
        const suffix = counter.getAttribute('data-suffix') || '';
        const options = {
            duration: 2.5,
            separator: ".",
            suffix: ` ${suffix}`,
            useEasing: true,
        };

        const countUp = new CountUp(counter.id, endVal, options);
        if (!countUp.error) {
            countUp.start();
            counter.setAttribute('data-animated', 'true');
        } else {
            console.error(`CountUp error on #${counter.id}:`, countUp.error);
        }
    });
}

document.body.addEventListener('htmx:load', function() {
    runCounters();
});
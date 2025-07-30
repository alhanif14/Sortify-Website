import { CountUp } from './countUp.min.js';

function runAllCountUps() {
    if (typeof CountUp === 'undefined') return;

    const counters = document.querySelectorAll('[data-value]');
    counters.forEach(counter => {
        if (counter.countUp) counter.countUp.reset();

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
            counter.countUp = countUp;
        } else {
            console.error(`CountUp.js error on #${counter.id}:`, countUp.error);
        }
    });
}

document.addEventListener('DOMContentLoaded', runAllCountUps);
document.body.addEventListener('htmx:afterSwap', runAllCountUps);
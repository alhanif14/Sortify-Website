import { CountUp } from './countUp.min.js';

function runAllCountUps() {
    console.log("runAllCountUps function has been called.");

    if (typeof CountUp === 'undefined') {
        console.error('CountUp class is NOT available.');
        return;
    }
    console.log('CountUp class is available.');

    const counters = document.querySelectorAll('[data-value]');
    console.log(`Found ${counters.length} elements with [data-value].`);
    
    counters.forEach(counter => {
        console.log(`Processing counter: #${counter.id}`);
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
            console.log(`-> Started CountUp for #${counter.id} to value ${endVal}`);
        } else {
            console.error(`-> CountUp.js error on #${counter.id}:`, countUp.error);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    console.log("DOMContentLoaded event fired. Running CountUp...");
    runAllCountUps();
});
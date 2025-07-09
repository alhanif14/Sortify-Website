import { CountUp } from "./countUp.min.js";

document.addEventListener("DOMContentLoaded", function () {
    /**
     * @param {string} id
     * @param {number} endVal
     * @param {object} options
     */
    function startCountUp(id, endVal, options = {}) {
        // Opsi default untuk semua hitungan
        const defaultOptions = {
            duration: 3.0,
            separator: ".",
            useEasing: true,
        };

        const finalOptions = { ...defaultOptions, ...options };
        
        const element = document.getElementById(id);
        if (!element) {
            return;
        }

        const countUp = new CountUp(id, endVal, finalOptions);

        if (!countUp.error) {
            countUp.start();
        } else {
            console.error(`CountUp.js error on #${id}:`, countUp.error);
        }
    }

    startCountUp("stat-pengguna", 12000, { suffix: "+" });
    startCountUp("stat-sampah", 5, { suffix: " Ton" });
    startCountUp("stat-hadiah", 100, { suffix: "+" });
    startCountUp("stat-komunitas", 45);
});

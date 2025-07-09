/**
 * Fungsi utama untuk mengatur link navigasi yang aktif.
 * Fungsi ini dipanggil langsung dari atribut onclick di HTML.
 * @param {string} activePath - Path dari link yang diklik, misal: '/know'.
 */
function setActiveNav(activePath) {
    // Ambil SEMUA link navigasi, baik desktop maupun mobile
    const allNavLinks = document.querySelectorAll('[data-path]');

    allNavLinks.forEach(link => {
        const linkPath = link.getAttribute('data-path');

        // Jika path link cocok dengan path yang diklik, tambahkan kelas 'active'.
        // Jika tidak, hapus kelas 'active'.
        if (linkPath === activePath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}


/**
 * Fungsi untuk menangani visibilitas password.
 */
function initTogglePassword() {
    document.querySelectorAll(".toggle-password").forEach(icon => {
        const newIcon = icon.cloneNode(true);
        icon.parentNode.replaceChild(newIcon, icon);

        newIcon.addEventListener("click", () => {
            const inputId = newIcon.getAttribute("data-target");
            const input = document.getElementById(inputId);
            if (!input) return;

            if (input.type === "password") {
                input.type = "text";
                newIcon.textContent = "visibility_off";
            } else {
                input.type = "password";
                newIcon.textContent = "visibility";
            }
        });
    });
}


// --- EVENT LISTENERS ---

// 1. Jalankan saat halaman pertama kali dimuat
document.addEventListener('DOMContentLoaded', () => {

    // Set 'Home' sebagai link aktif secara default saat halaman baru dibuka
    setActiveNav('/landing');
    initTogglePassword();
});

// 2. Jalankan setiap kali konten baru ditambahkan oleh HTMX
// Ini penting untuk memastikan fungsionalitas seperti toggle password tetap bekerja
document.body.addEventListener("htmx:afterSwap", () => {
    initTogglePassword();
});

// scroll top
window.onscroll = function() {
    var scrollTopButton = document.querySelector('.scrolltop-button');

    if (scrollTopButton) {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            scrollTopButton.style.display = "block";
        } else {
            scrollTopButton.style.display = "none";
        }
    }
};
// function setActiveNav(activePath) {
//     const allNavLinks = document.querySelectorAll('[data-path]');

//     allNavLinks.forEach(link => {
//         const linkPath = link.getAttribute('data-path');

//         if (linkPath === activePath) {
//             link.classList.add('active');
//         } else {
//             link.classList.remove('active');
//         }
//     });
// }


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

    function handleScrollTopButton() {
        const scrollTopButton = document.querySelector('.scrolltop-button');
        if (!scrollTopButton) return;

        const isLargeScreen = window.innerWidth >= 992;
        const isScrolled = document.body.scrollTop > 20 || document.documentElement.scrollTop > 20;

        if (isLargeScreen && isScrolled) {
            scrollTopButton.style.display = "flex";
        } else {
            scrollTopButton.style.display = "none";
        }
    }


document.addEventListener('DOMContentLoaded', () => {
    // setActiveNav('/landing');
    initTogglePassword();
    handleScrollTopButton();
});

document.body.addEventListener("htmx:afterSwap", () => {
    initTogglePassword();
});

document.body.addEventListener('htmx:pushedIntoHistory', () => {
});

window.addEventListener('scroll', handleScrollTopButton);
window.addEventListener('resize', handleScrollTopButton);

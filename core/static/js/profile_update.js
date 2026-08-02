/* ===========================================================
   PROFILE UPDATE PAGE
   Alumni Management System
=========================================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ===========================
       Auto Hide Success Message
    ============================ */

    const alert = document.querySelector(".success-message");

    if (alert) {

        setTimeout(() => {

            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";

            setTimeout(() => {

                alert.remove();

            }, 400);

        }, 3000);

    }

    /* ===========================
       Input Animation
    ============================ */

    const inputs = document.querySelectorAll("input:not([readonly])");

    inputs.forEach(input => {

        input.addEventListener("focus", () => {

            input.parentElement.classList.add("active");

        });

        input.addEventListener("blur", () => {

            input.parentElement.classList.remove("active");

        });

    });

    /* ===========================
       Mobile Number Validation
    ============================ */

    function allowOnlyNumbers(event) {

        event.target.value = event.target.value.replace(/\D/g, "");

    }

    const mobile = document.querySelector("input[name='contact']");
    const parent = document.querySelector("input[name='parent_contact']");

    if (mobile) {

        mobile.addEventListener("input", allowOnlyNumbers);

    }

    if (parent) {

        parent.addEventListener("input", allowOnlyNumbers);

    }

    /* ===========================
       Form Validation
    ============================ */

    const form = document.getElementById("profileForm");

    if (form) {

        form.addEventListener("submit", function (e) {

            const email = document.querySelector("input[name='email']");
            const mobile = document.querySelector("input[name='contact']");
            const parent = document.querySelector("input[name='parent_contact']");

            /* Email */

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

            if (!emailRegex.test(email.value.trim())) {

                alert("Please enter a valid email address.");

                email.focus();

                e.preventDefault();

                return;

            }

            /* Mobile */

            if (mobile.value.length !== 10) {

                alert("Mobile number must contain exactly 10 digits.");

                mobile.focus();

                e.preventDefault();

                return;

            }

            /* Parent */

            if (parent.value.length !== 10) {

                alert("Parent contact number must contain exactly 10 digits.");

                parent.focus();

                e.preventDefault();

                return;

            }

            /* Save Button Animation */

            const btn = document.querySelector(".btn-save");

            btn.disabled = true;

            btn.innerHTML = `
                <i class="fa-solid fa-spinner fa-spin"></i>
                Saving...
            `;

        });

    }

    /* ===========================
       Card Hover Effect
    ============================ */

    const cards = document.querySelectorAll(".section");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-4px)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0px)";

        });

    });

});
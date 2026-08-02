document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       Show / Hide Password
    ========================== */

    const toggle = document.getElementById("togglePassword");
    const password = document.getElementById("password");

    if(toggle){

        toggle.addEventListener("click", () => {

            if(password.type === "password"){

                password.type = "text";

                toggle.classList.remove("fa-eye");
                toggle.classList.add("fa-eye-slash");

            }else{

                password.type = "password";

                toggle.classList.remove("fa-eye-slash");
                toggle.classList.add("fa-eye");

            }

        });

    }

    /* ==========================
       Success Message
    ========================== */

    const alertBox = document.querySelector(".success-message");

    if(alertBox){

        setTimeout(() => {

            alertBox.style.transition = ".4s";
            alertBox.style.opacity = "0";
            alertBox.style.transform = "translateY(-10px)";

            setTimeout(() => {

                alertBox.remove();

            },400);

        },3000);

    }

    /* ==========================
       Password Validation
    ========================== */

    const form = document.getElementById("passwordForm");

    if(form){

        form.addEventListener("submit",(e)=>{

            const value=password.value.trim();

            const regex=/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

            if(!regex.test(value)){

                e.preventDefault();

                alert(
                    "Password must contain at least:\n\n" +
                    "• 8 characters\n" +
                    "• One uppercase letter\n" +
                    "• One lowercase letter\n" +
                    "• One number"
                );

                password.focus();

                return;
            }

            const btn=document.querySelector(".update-btn");

            btn.disabled=true;

            btn.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Updating...';

        });

    }

});
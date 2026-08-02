const alerts = document.querySelectorAll(".alert");

alerts.forEach(alert=>{

    setTimeout(()=>{

        alert.classList.add("fade");

        setTimeout(()=>{

            alert.remove();

        },500);

    },3000);

});
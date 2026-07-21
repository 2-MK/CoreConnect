function getCookie(name){

    let cookieValue = null;

    if(document.cookie){

        const cookies = document.cookie.split(";");

        for(let cookie of cookies){

            cookie = cookie.trim();

            if(cookie.startsWith(name + "=")){

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
            }
        }
    }

    return cookieValue;
}

function showMessage(message,type){

    const box =
        document.getElementById("message-box");

    box.innerHTML = `
        <div class="${type}">
            ${message}
        </div>
    `;

    setTimeout(()=>{
        box.innerHTML="";
    },3000);
}

async function addUser(){

    const csrftoken = getCookie("csrftoken");

    const response = await fetch("/add-user",{

        method:"POST",

        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":csrftoken
        },

        body:JSON.stringify({
            ktu_id:document.getElementById("ktu_id").value,
            name:document.getElementById("name").value,
            passout_year:document.getElementById("passout_year").value,
            email:document.getElementById("email").value,
            contact:document.getElementById("contact").value
        })
    });

    const result = await response.json();

    showMessage(result.message,"success");
}

async function updateUser(){

    const csrftoken = getCookie("csrftoken");

    const response = await fetch("/update-user",{

        method:"PUT",

        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":csrftoken
        },

        body:JSON.stringify({
            ktu_id:document.getElementById("update_ktu_id").value,
            name:document.getElementById("update_name").value,
            passout_year:document.getElementById("update_passout_year").value,
            email:document.getElementById("update_email").value,
            contact:document.getElementById("update_contact").value
        })
    });

    const result = await response.json();

    showMessage(result.message,"success");
}

async function deleteUser(){

    const csrftoken = getCookie("csrftoken");

    const response = await fetch("/delete-user",{

        method:"DELETE",

        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":csrftoken
        },

        body:JSON.stringify({
            ktu_id:document.getElementById("delete_ktu_id").value
        })
    });

    const result = await response.json();

    showMessage(result.message,"success");
}
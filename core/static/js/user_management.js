function getCookie(name) {
    let cookieValue = null;

    if (document.cookie) {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
            }
        }
    }

    // Fallback: if cookie not set, try to read token from template CSRF input
    if (!cookieValue) {
        const tpl = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (tpl && tpl.value) {
            cookieValue = tpl.value;
        }
    }

    return cookieValue;
}

function showMessage(message, type) {
    const box = document.getElementById("message-box");

    box.innerHTML = `
        <div class="${type}">
            ${message}
        </div>
    `;

    setTimeout(() => {
        box.innerHTML = "";
    }, 3000);
}

// ---------------- ADD USER ----------------

async function addUser() {
    const csrftoken = getCookie("csrftoken");

    try {
        const response = await fetch("/add-user", {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({
                ktu_id: document.getElementById("ktu_id").value,
                name: document.getElementById("name").value,
                passout_year: document.getElementById("passout_year").value,
                email: document.getElementById("email").value,
                ritemail: document.getElementById("ritemail").value,
                contact: document.getElementById("contact").value
            })
        });

        const result = await response.json();

        if (response.ok) {

            showMessage(
                `${result.message}<br><br><strong>Temporary Password : ${result.temporary_password}</strong>`,
                "success"
            );

        } else {

            showMessage(result.message, "error");
        }

    } catch (error) {
        console.error(error);
        showMessage("Failed to connect to server.", "error");
    }
}

// ---------------- UPDATE USER ----------------

async function updateUser() {

    const csrftoken = getCookie("csrftoken");

    try {

        const response = await fetch("/update-user", {

            method: "PUT",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({

                ktu_id: document.getElementById("update_ktu_id").value,
                name: document.getElementById("update_name").value,
                passout_year: document.getElementById("update_passout_year").value,
                email: document.getElementById("update_email").value,
                ritemail: document.getElementById("update_ritemail").value,
                contact: document.getElementById("update_contact").value

            })

        });

        const result = await response.json();

        if (response.ok) {
            showMessage(result.message, "success");
        } else {
            showMessage(result.message, "error");
        }

    } catch (error) {

        console.error(error);
        showMessage("Failed to connect to server.", "error");

    }
}

// ---------------- DELETE USER ----------------

async function deleteUser() {

    const csrftoken = getCookie("csrftoken");

    try {

        const response = await fetch("/delete-user", {

            method: "DELETE",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },

            body: JSON.stringify({
                ktu_id: document.getElementById("delete_ktu_id").value
            })

        });

        const result = await response.json();

        if (response.ok) {
            showMessage(result.message, "success");
        } else {
            showMessage(result.message, "error");
        }

    } catch (error) {

        console.error(error);
        showMessage("Failed to connect to server.", "error");

    }
}
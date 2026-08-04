// Delete Confirmation

document.querySelectorAll(".delete-link").forEach(button => {

    button.addEventListener("click", function (e) {

        if (!confirm("Are you sure you want to delete this event?")) {

            e.preventDefault();

        }

    });

});

// Search Table

const searchInput = document.getElementById("searchInput");

searchInput.addEventListener("keyup", function () {

    const value = this.value.toLowerCase();

    const rows = document.querySelectorAll("#eventTable tbody tr");

    rows.forEach(row => {

        const text = row.innerText.toLowerCase();

        row.style.display = text.includes(value) ? "" : "none";

    });

});
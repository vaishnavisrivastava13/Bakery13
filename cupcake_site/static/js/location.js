document.addEventListener("DOMContentLoaded", function () {

    const btn = document.getElementById("locationBtn");

    if (!btn) {
        alert("Location button NOT found");
        return;
    }

    btn.addEventListener("click", function (e) {
        e.preventDefault();
        getLocation();
    });
});

function getLocation() {

    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function () {
            document.getElementById("user-location").innerText = "Location Found";
            alert("Location permission granted");
        },
        function () {
            alert("Location permission denied");
        }
    );
}

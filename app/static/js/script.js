document.addEventListener("DOMContentLoaded", function () {
    const processForm = document.getElementById("processForm");
    const processVideo = document.getElementById("processVideo");
    const subT_SelecVid = document.getElementById("subT-SelecVid");
    const subT_VidDisp = document.getElementById("subT-VidDisp")
    const spinner = document.getElementById("spinner");
    const progressMessage = document.getElementById("progressMessage");
    const rubricasContainer = document.getElementById("rubricasContainer");
    const videoList = document.getElementById("videoList");
    
    // Función para mostrar el spinner
    function showSpinner(message) {
        spinner.style.display = "block";
        progressMessage.textContent = message;
        uploadForm.style.display = "none";
        processVideo.style.display = "none";
        videoList.style.display = "none";
        subT_SelecVid.style.display = "none";
        subT_VidDisp.style.display = "none";
    }

    // Función para ocultar el spinner
    function hideSpinner() {
        spinner.style.display = "none";
        uploadForm.style.display = "block";
        processForm.style.display = "block";
        videoList.style.display = "block";
        subT_SelecVid.style.display = "block";
        subT_VidDisp.style.display = "block";
        processVideo.style.display = "block";
    }

    // Manejador del evento de envío del formulario de carga de video
    uploadForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(uploadForm);

        // Mostrar el spinner antes de cargar
        showSpinner("Cargando video...");

        // Hacer el request POST para cargar el video
        fetch("/upload-video/", {
            method: "POST",
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                // Esperar un momento antes de redirigir
                setTimeout(() => {
                    // Redirigir a la página principal después de cargar
                    hideSpinner(); // Asegúrate de ocultar el spinner antes de redirigir
                    window.location.href = "/";
                }, 1000); // 1000 ms (1 segundo) de espera opcional para mostrar el spinner
            } else {
                console.error("Error al cargar el video.");
                hideSpinner(); // Ocultar el spinner en caso de error
            }
        })
        .catch(error => {
            console.error("Error:", error);
            hideSpinner(); // Ocultar el spinner en caso de error
        });
    });

    // Manejador del evento de envío del formulario de procesamiento de video
    processForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const formData = new FormData(processForm);
        const videoFile = formData.get("video_file");

        // Conectar con el WebSocket
        const socket = new WebSocket("ws://localhost:8000/ws/progress");

        socket.onopen = function () {
            console.log("WebSocket conectado");
            showSpinner(`Procesando el video: ${videoFile}...`);
        };

        socket.onmessage = function (event) {
            const message = event.data;
            progressMessage.textContent = message;
        };

        socket.onclose = function () {
            console.log("WebSocket cerrado");
            hideSpinner();
        };

        socket.onerror = function (error) {
            console.log("Error en WebSocket: ", error);
            hideSpinner();
        };

        socket.onmessage = function (event) {
            if (event.data === "Procesamiento completado.") {
                hideSpinner();
                window.location.href = "/results";
            }
        };

        // Hacer el request POST para iniciar el procesamiento del video
        fetch("/process-video/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.text())
        .then(result => {
            rubricasContainer.innerHTML = result;
            hideSpinner();
        })
        .catch(error => {
            console.error("Error:", error);
            hideSpinner();
        });
    });
});

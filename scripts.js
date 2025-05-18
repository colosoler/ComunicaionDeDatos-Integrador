document.getElementById("enviar").addEventListener("click", async () => {
    const resolucionStr = document.getElementById("resolucion").value;
    const bitsStr = document.getElementById("bits").value;
    const imagenInput = document.getElementById("imageInput");

    if (!imagenInput.files.length) {
        alert("Selecciona una imagen.");
        return;
    }

    const formData = new FormData();
    formData.append("imagen", imagenInput.files[0]);

    // Extrae solo la resolución sin texto (ej: "1920 × 1080" => "1920x1080")
    const resMatch = resolucionStr.match(/(\d+)\s*×\s*(\d+)/);
    if (!resMatch) {
        alert("Selecciona una resolución válida.");
        return;
    }
    const resolucion = `${resMatch[1]}x${resMatch[2]}`;
    const bits = parseInt(bitsStr);

    formData.append("resolucion", resolucion);
    formData.append("bits", bits);
    formData.append("calidad", 70); // opcional

    try {
        const response = await fetch("http://localhost:5000/procesar", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Error procesando la imagen");

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // Mostrar imágenes
        const originalURL = URL.createObjectURL(imagenInput.files[0]);
        document.getElementById("img_original").innerHTML = `<img src="${originalURL}">`;
        document.getElementById("img_modificada").innerHTML = `<img src="${url}">`;

        // Actualizar textos
        document.getElementById("res_original").textContent = "Resolución: " + resolucionStr;
        document.getElementById("bits_original").textContent = "Profundidad de bits: " + bitsStr;
        document.getElementById("res_mod").textContent = "Resolución: " + resolucionStr;
        document.getElementById("bits_mod").textContent = "Profundidad de bits: " + bitsStr;

    } catch (err) {
        alert("Error: " + err.message);
    }
});

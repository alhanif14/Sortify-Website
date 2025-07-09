let currentStream = null; // Global untuk simpan stream aktif

function detectQRCode(video) {
    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    function stopCamera() {
        if (video.srcObject) {
            video.srcObject.getTracks().forEach(track => track.stop());
            video.srcObject = null;
            currentStream = null;
            console.log("Kamera dihentikan.");
        }
    }

    function scanFrame() {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const qrCode = jsQR(imageData.data, canvas.width, canvas.height);

        if (qrCode) {
            try {
                const data = JSON.parse(qrCode.data);
                const wasteTypes = data.waste_type || [];
                const point = data.point || 0;
                const timestamp = data.timestamp || null;
                const disposeId = data.id || null;

                console.log("✅ QR Code Data:", data);

                stopCamera(); // stop camera saat berhasil scan

                // ✅ Build parameters for the request
                const params = new URLSearchParams({
                    waste_type: wasteTypes.join(","),
                    point: point.toString()
                });
                
                if (timestamp) {
                    params.append('timestamp', timestamp.toString());
                }
                
                if (disposeId) {
                    params.append('id', disposeId.toString());
                }

                console.log("✅ Redirecting to scan_result with params:", params.toString());

                // ✅ Option 1: Direct to scan_result (points added there)
                htmx.ajax("GET", "/scan_result?" + params.toString(), {
                    target: "#mainContent",
                    swap: "innerHTML"
                });

                return; // stop loop
            } catch (e) {
                console.error("❌ QR tidak berisi JSON valid:", e);
                alert("QR Code tidak valid. Pastikan QR code berisi data yang benar.");
            }
        }

        requestAnimationFrame(scanFrame);
    }

    scanFrame();
}

document.body.addEventListener("htmx:afterSwap", function (evt) {
    const video = document.getElementById("camera");

    if (!video) return;

    console.log("🎥 Memulai kamera...");

    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then((stream) => {
            video.srcObject = stream;
            currentStream = stream;

            video.addEventListener("loadedmetadata", () => {
                video.play();
                console.log("🎥 Kamera aktif, mulai deteksi QR...");
                detectQRCode(video);
            });
        })
        .catch((err) => {
            console.error("❌ Gagal membuka kamera:", err);
            alert("Tidak dapat mengakses kamera. Periksa izin browser dan pastikan menggunakan HTTPS.");
        });
});

// ✨ Stop kamera saat pindah halaman
document.body.addEventListener("htmx:beforeSwap", function (evt) {
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        currentStream = null;
        console.log("🎥 Kamera dimatikan sebelum ganti halaman.");
    }
});
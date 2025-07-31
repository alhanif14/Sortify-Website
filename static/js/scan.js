let currentStream = null;

console.log("scan.js loaded!");

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
            console.log("camera stopped.");
        }
    }

    function scanFrame() {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        const qrCode = jsQR(imageData.data, canvas.width, canvas.height);

        if (qrCode) {
            console.log("QR Detected:", qrCode.data);

            try {
                const data = JSON.parse(qrCode.data);
                console.log("Parsed Data:", data);

                const wasteTypes = data.waste_type || [];
                const point = data.point || 0;
                const timestamp = data.timestamp || null;
                const disposeId = data.id || null;

                stopCamera();

                const params = new URLSearchParams({
                    waste_type: wasteTypes.join(","),
                    point: point.toString(),
                });

                if (timestamp) {
                    params.append("timestamp", timestamp.toString());
                }
                if (disposeId) {
                    params.append("id", disposeId.toString());
                }

                console.log("Calling /process_scan with:", params.toString());

        fetch("/process_scan?" + params.toString())
    .then(response => {
        if (!response.ok) throw new Error("Fetch failed: " + response.status);
        return response.json();
    })
    .then(data => {
        console.log("Response from /process_scan:", data);

        if (data.status === "ok") {
            const resultParams = new URLSearchParams({
                waste_type: data.waste_type,
                point: data.point,
                timestamp: data.timestamp,
                id: data.id
            });

            console.log("Navigating to /scan_result with:", resultParams.toString());
            htmx.ajax("GET", "/scan_result?" + resultParams.toString(), {
                target: "#mainContent",
                swap: "innerHTML"
            });
        }
        else if (data.message === 'used') {
            const claimedBy = data.claimed_by || 'another user';
            console.log("QR already used, navigating to used page.");
            htmx.ajax("GET", `/scan_used?claimed_by=${claimedBy}`, {
                target: "#mainContent",
                swap: "innerHTML"
            });
        }
        else {
            console.error("Error from /process_scan:", data.message);
            alert("Process scan failed: " + data.message);
        }
    })
    .catch(err => {
        console.error("Fetch error:", err);
        alert("Fetch failed: " + err.message);
    });

                return;

            } catch (e) {
                console.error("QR parsing error:", e);
                alert("QR no valid.");
            }
        }

        requestAnimationFrame(scanFrame);
    }

    scanFrame();
}

function startCameraAndDetect() {
    const video = document.getElementById("camera");
    if (!video) {
        console.log("Video element not found.");
        return;
    }

    console.log("Starting camera...");

    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then((stream) => {
            video.srcObject = stream;
            currentStream = stream;

            video.addEventListener("loadedmetadata", () => {
                video.play();
                console.log("Camera is active, starting QR detection...");
                detectQRCode(video);
            });
        })
        .catch((err) => {
            console.error("Failed to open camera:", err);
            alert("Cannot access camera. Check browser permissions and ensure HTTPS is used.");
        });
}

document.body.addEventListener("htmx:afterSwap", function (evt) {
    console.log("HTMX swap complete. Checking for #camera...");
    const video = document.getElementById("camera");
    if (video) {
        console.log("Camera found, starting QR detection...");
        startCameraAndDetect();
    }
});

document.body.addEventListener("htmx:beforeSwap", function (evt) {
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        currentStream = null;
        console.log("Camera stopped before page change.");
    }
});
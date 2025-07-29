if (typeof Chart === 'undefined') {
    console.error("Chart.js not loaded yet.");
} else {
    const binData = {
        organic: 0,
        recycle: 0,
        paper: 0,
        others: 0,
    };
    let binAvailabilityChart = null;

    function initializeBinChart() {
        const ctx = document.getElementById('binAvailabilityChart')?.getContext('2d');
        if (!ctx) return; 

        if (binAvailabilityChart) {
            binAvailabilityChart.destroy();
        }

        binAvailabilityChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Organic', 'Recycle', 'Paper', 'Others'],
                datasets: [{
                    data: [binData.organic, binData.recycle, binData.paper, binData.others],
                    backgroundColor: ['#198754', '#0D6EFD', '#FFC107', '#6C757D'],
                    borderColor: '#FFFFFF',
                    borderWidth: 4,
                    hoverOffset: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }
    function updateDashboardUI() {
        if (!document.getElementById('binAvailabilityChart')) return;

        if (binAvailabilityChart) {
            binAvailabilityChart.data.datasets[0].data = [
                binData.organic,
                binData.recycle,
                binData.paper,
                binData.others
            ];
            binAvailabilityChart.update();
        }

        document.getElementById('legend-organic').textContent = `${binData.organic}%`;
        document.getElementById('legend-recycle').textContent = `${binData.recycle}%`;
        document.getElementById('legend-paper').textContent = `${binData.paper}%`;
        document.getElementById('legend-others').textContent = `${binData.others}%`;

        const overall = (binData.organic + binData.recycle + binData.paper + binData.others) / 4;
        const overallRounded = Math.round(overall);
        document.getElementById('overall-percentage').textContent = `${overallRounded}%`;

        const statusTextElement = document.getElementById('overall-status-text');
        if (overallRounded <= 30) {
            statusTextElement.textContent = "Overall Empty";
            statusTextElement.className = "text-muted small";
        } else if (overallRounded <= 70) {
            statusTextElement.textContent = "Partially Full";
            statusTextElement.className = "text-primary small";
        } else if (overallRounded <= 90) {
            statusTextElement.textContent = "Almost Full";
            statusTextElement.className = "text-warning small";
        } else {
            statusTextElement.textContent = "Overall Full";
            statusTextElement.className = "text-danger small";
        }
    }

    function connectToMQTT() {
        if (window.mqttClient && window.mqttClient.isConnected()) return;

        waitForPaho(() => {
            const client = new Paho.Client("broker.emqx.io", 8084, "/mqtt", "dashboard_client_" + Math.random());
            window.mqttClient = client;

            const topicMap = {
                "waste/sensor1": "organic",
                "waste/sensor2": "recycle",
                "waste/sensor3": "paper",
                "waste/sensor4": "others"
            };

            client.onMessageArrived = (message) => {
                const topic = message.destinationName;
                const value = parseInt(message.payloadString, 10);
                const binType = topicMap[topic];
                
                if (binType && !isNaN(value)) {
                    console.log(`MQTT -> ${binType}: ${value}%`);
                    binData[binType] = value;
                    updateDashboardUI();
                }
            };

            client.connect({
                useSSL: true,
                onSuccess: () => {
                    console.log("MQTT Dashboard Connected!");
                    Object.keys(topicMap).forEach(topic => client.subscribe(topic));
                },
                onFailure: (err) => console.error("MQTT Connection Failed:", err)
            });
        });
    }

    function waitForPaho(callback) {
        if (window.Paho) {
            callback();
        } else {
            setTimeout(() => waitForPaho(callback), 100);
        }
    }
    function init() {
        if (document.getElementById('binAvailabilityChart')) {
            initializeBinChart();
            connectToMQTT();
        }
    }

    document.addEventListener('DOMContentLoaded', init);
    document.body.addEventListener('htmx:afterSwap', init);
}
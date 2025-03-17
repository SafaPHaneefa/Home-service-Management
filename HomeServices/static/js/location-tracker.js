class LocationTracker {
    constructor() {
        this.map = null;
        this.workerMarker = null;
        this.destinationMarker = null;
        this.routingControl = null;
        this.updateInterval = null;
        this.trafficLayer = null;
        this.satelliteLayer = null;
        this.defaultLayer = null;
        this.isSatelliteView = false;
    }

    async initialize(workerId, bookingId) {
        // Show the modal
        const modal = document.getElementById('locationTrackingModal');
        const overlay = document.getElementById('modalOverlay');
        modal.style.display = 'block';
        overlay.style.display = 'block';

        // Initialize map
        this.map = L.map('worker-map').setView([9.5916, 76.5222], 13); // Center on Kottayam initially

        // Add the tile layer (map background)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Get current location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const { latitude, longitude } = position.coords;
                    await this.startSharing(workerId, bookingId, latitude, longitude);
                },
                (error) => {
                    console.error('Error getting location:', error);
                    // Use default Kerala coordinates if location access is denied
                    this.startSharing(workerId, bookingId, 8.5241, 76.9366);
                }
            );
        }

        // Force map to recalculate its size after modal is shown
        setTimeout(() => {
            this.map.invalidateSize();
        }, 100);
    }

    async startSharing(workerId, bookingId, latitude, longitude) {
        try {
            // Create custom markers
            const workerIcon = L.divIcon({
                className: 'worker-marker',
                html: '<i class="fas fa-hard-hat"></i>',
                iconSize: [30, 30]
            });

            const destinationIcon = L.divIcon({
                className: 'destination-marker',
                html: '<i class="fas fa-map-marker-alt"></i>',
                iconSize: [30, 30]
            });

            // Add markers
            this.workerMarker = L.marker([latitude, longitude], { icon: workerIcon }).addTo(this.map);
            this.destinationMarker = L.marker([9.5916, 76.5222], { icon: destinationIcon })
                .bindPopup('Destination: Kottayam')
                .addTo(this.map);

            // Add routing
            this.routingControl = L.Routing.control({
                waypoints: [
                    L.latLng(latitude, longitude),
                    L.latLng(9.5916, 76.5222)
                ],
                routeWhileDragging: false,
                lineOptions: {
                    styles: [{ color: '#2196F3', weight: 4, opacity: 0.8 }]
                }
            }).addTo(this.map);

            // Fit map to show both points
            const bounds = L.latLngBounds([
                [latitude, longitude],
                [9.5916, 76.5222]
            ]);
            this.map.fitBounds(bounds, { padding: [50, 50] });

            // Start periodic updates
            this.startUpdating(workerId, bookingId);

        } catch (error) {
            console.error('Error starting location sharing:', error);
        }
    }

    startUpdating(workerId, bookingId) {
        this.updateInterval = setInterval(() => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    async (position) => {
                        const { latitude, longitude } = position.coords;
                        if (this.workerMarker) {
                            this.workerMarker.setLatLng([latitude, longitude]);
                            this.routingControl.setWaypoints([
                                L.latLng(latitude, longitude),
                                L.latLng(9.5916, 76.5222)
                            ]);
                        }
                    }
                );
            }
        }, 10000); // Update every 10 seconds
    }

    cleanup() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        if (this.map) {
            this.map.remove();
            this.map = null;
        }
    }

    // Add these methods for the control buttons
    zoomIn() {
        if (this.map) this.map.zoomIn();
    }

    zoomOut() {
        if (this.map) this.map.zoomOut();
    }

    resetNorth() {
        if (this.map) this.map.setView(this.map.getCenter(), this.map.getZoom());
    }

    centerOnWorker() {
        if (this.map && this.workerMarker) {
            this.map.setView(this.workerMarker.getLatLng(), 15);
        }
    }

    toggleTraffic() {
        // Implementation for traffic layer toggle
        console.log('Traffic toggle clicked');
    }

    toggleSatellite() {
        // Implementation for satellite view toggle
        console.log('Satellite toggle clicked');
    }

    refreshRoute() {
        if (this.routingControl && this.workerMarker) {
            const currentPos = this.workerMarker.getLatLng();
            this.routingControl.setWaypoints([
                L.latLng(currentPos.lat, currentPos.lng),
                L.latLng(9.5916, 76.5222)
            ]);
        }
    }

    updateRouteInfo(route) {
        const routeInfo = document.getElementById('route-info');
        if (route && route.instructions && route.instructions.length > 0) {
            const nextInstruction = route.instructions[0];
            routeInfo.textContent = nextInstruction.text;
        }
    }
}

// Add close button handler
document.getElementById('closeTrackingModal').onclick = function() {
    const modal = document.getElementById('locationTrackingModal');
    const overlay = document.getElementById('modalOverlay');
    modal.style.display = 'none';
    overlay.style.display = 'none';
    
    if (locationTracker) {
        locationTracker.cleanup();
        locationTracker = null;
    }
};

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 
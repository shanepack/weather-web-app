export function InputUserLocation(setUserLocation){
    const locationInput = document.getElementById('locationInput');

    locationInput.addEventListener('keydown', function(event){
        if(event.key === 'Enter'){
            const userLocation = locationInput.value;
            setUserLocation(userLocation);
        }
    });
}
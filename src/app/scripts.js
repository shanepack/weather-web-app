export function InputUserLocation(setUserLocation){
    const locationInput = document.getElementById('locationInput');

    let userLocation = 'Pearland';

    locationInput.addEventListener('keydown', function(event){
        if(event.key === 'Enter'){
            userLocation = locationInput.value;
            setUserLocation(userLocation);
        }
    });
}
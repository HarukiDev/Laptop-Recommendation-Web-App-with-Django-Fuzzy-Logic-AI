document.addEventListener('DOMContentLoaded', (event) => {
    const ramSelect = document.getElementById('ram-select');
    const memorySelect = document.getElementById('memory-select');

    const memoryOptions = {
        '8': ['64','128', '256'],
        '16': ['256','512', '1024'],
        '32': ['512', '1024', '2048']
    };

    ramSelect.addEventListener('change', (event) => {
        const selectedRam = event.target.value;
        const availableMemory = memoryOptions[selectedRam];
        // Clear current memory options
        memorySelect.innerHTML = '';
        // Add new memory options based on selected RAM
        availableMemory.forEach(memoryValue => {
            const option = document.createElement('option');
            option.value = memoryValue;
            option.textContent = memoryValue;
            memorySelect.appendChild(option);
        });
    });
    // Trigger change event to set initial memory options based on default RAM selection
    ramSelect.dispatchEvent(new Event('change'));
});

document.getElementById('form-laptop').addEventListener('submit', function(event) {
    event.preventDefault(); // Menghentikan aksi default form submit
    
    var formData = new FormData(this); // Membuat objek FormData dari form
    tutupMarqueeGIF();
    
    // Kirim permintaan AJAX ke server Flask
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Ambil respons JSON dari server
    .then(data => {
        var kecepatanStr = data.kecepatan;
        tampilkanKecepatan(kecepatanStr);
        tampilkanLaptopList(data.laptop_serupa);
        scrollToOutputSection();
    })
    .catch(error => console.error('Error:', error)); // Tangkap dan tampilkan error jika ada
});

function tampilkanLaptopList(laptopList) {
    var laptopListContainer = document.getElementById('laptop-list');
    laptopListContainer.innerHTML = '';

    if (laptopList.length > 0) {
        laptopListContainer.parentElement.style.display = 'block'; // Show the list container
    } else {
        laptopListContainer.parentElement.style.display = 'none'; // Hide the list container if empty
    }

    laptopList.forEach(function(laptop) {
        var listItem = document.createElement('li');
        listItem.textContent = `Company: ${laptop.Company}, Series: ${laptop.Product}, Type: ${laptop.TypeName}, RAM: ${laptop.Ram_int} GB, Memory: ${laptop.Memory_GB} GB`;
        laptopListContainer.appendChild(listItem);
    });
}

function tampilkanKecepatan(kecepatan) {
    var kecepatanOutput = document.getElementById('kecepatan-output');
    var kecepatanContainer = document.querySelector('.kecepatan');

    if (kecepatan === 'Sangat Cepat') {
        kecepatanOutput.textContent = 'Kecepatan: Sangat Cepat';
        kecepatanContainer.style.display = 'block';
    } else if (kecepatan === 'Cepat') {
        kecepatanOutput.textContent = 'Kecepatan: Cepat';
        kecepatanContainer.style.display = 'block'; 
    } else if (kecepatan === 'Sedang') {
        kecepatanOutput.textContent = 'Kecepatan: Sedang';
        kecepatanContainer.style.display = 'block'; 
    } else if (kecepatan === 'Lambat') {
        kecepatanOutput.textContent = 'Kecepatan: Lambat';
        kecepatanContainer.style.display = 'block';  
    } else {
        kecepatanContainer.style.display = 'none';
    }
}

function tutupKecepatan() {
    var kecepatanContainer = document.querySelector('.kecepatan');
    var laptopListContainer = document.getElementById('laptop-list');
    var loadingGif = document.querySelector('.loading-gif');

    kecepatanContainer.style.display = 'none';
    laptopListContainer.parentElement.style.display = 'none';
    window.open("http://127.0.0.1:5000/", "_blank_");
}

function tutupMarqueeGIF() {
    var loadingGif = document.querySelector('.loading-gif');

    loadingGif.style.display = 'none';
}

function scrollToOutputSection() {
    const section = document.getElementById('output-section');
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}
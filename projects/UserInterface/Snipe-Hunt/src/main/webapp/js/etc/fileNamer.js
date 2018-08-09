function displayFileName() {
	// Pull the the file uploaded
	var file = document.getElementById('fileInput');
	// Get the file name
	var fname = file.value;
	// Cut off fake path in file name
	fname = fname.substring(12); 
	// Get the HTML element to show it in
	var display = document.getElementById('showFileName');
	// Set the element to display file name
	display.innerHTML = fname;
}
var jcrop_api;
var f;
var max_size = 524288; // 0.5 MB
var uploaded = false;

function initializecrop() 
{
	initJcrop();
	document.getElementById('files').addEventListener('change', handleFileSelect, false);
}

// Initialize on every new upload
function initJcrop() {
	$('#img_crop').Jcrop({
		onSelect: setBounds,
		aspectRatio: 1,
		setSelect:   [ 100, 100, 50, 50 ],
		boxHeight: 400
	}, function(){ 
		var bounds = this.getBounds();
		boundx = bounds[1];
		boundy = bounds[2];
		jcrop_api = this; 
	});

};

function setBounds(c)
{				
	// draw preview
	canvas = document.getElementById('canvas')
	ctx = canvas.getContext('2d');  
	ctx.drawImage(document.getElementById('preview'), c.x, c.y, c.w, c.h, 0, 0, 150, 150);
	
	// draw to hidden canvas
	$('#canvashidden').attr("height", c.h);
	$('#canvashidden').attr("width", c.w);
	canvas = document.getElementById('canvashidden')
	ctx = canvas.getContext('2d');  
	ctx.drawImage(document.getElementById('preview'), c.x, c.y, c.w, c.h, 0, 0, c.w, c.h);
}

// Force crop modal
function forceCrop()
{
	// Trigger modal
	$("#modal_trigger").click();
}

// finish crop
function finishcrop()
{
	//document.getElementById('picturedata').value = document.getElementById('canvas').toDataURL();
	if (uploaded) {
		document.getElementById('picturedata').innerHTML = document.getElementById('canvashidden').toDataURL();
	}
}

// Delete button script 
function refresh() {
	document.getElementById('file_div').innerHTML = "<input type=\"file\" id=\"files\" name=\"files[]\" accept=\"image/*\" /\>";
	document.getElementById('files').addEventListener('change', handleFileSelect, false);
	$('#preview').attr("class", "hidden");
	$('#delete').attr("class", "hidden");
	$('#crop_btn').attr("class", "hidden");
	$('#canvas').attr("class", "hidden");
	if (hasImage) {
		$('#old_img').attr("class", "previewthumb");
	}
	
	uploaded = false;
}

// Handle new upload
function handleFileSelect(evt) {
		var files = evt.target.files; // FileList object

		// Loop through the FileList and render image files as thumbnails.
		for (var i = 0, f; f = files[i]; i++) {

			// Only process image files.
			if (!f.type.match('image.*')) {
				document.getElementById('error_txt').innerHTML = "Only images are allowed";
				refresh();
				continue;
			}
			
			// Image size limitation
			if (f.size > max_size) {
				document.getElementById('error_txt').innerHTML = "Size is too large (max is 0.5MB)";
				refresh();
				continue;
			}
			
			// clear errors
			document.getElementById('error_txt').innerHTML = "";

			// Refresh jcrop API - step 1
			jcrop_api.destroy();

			// Trigger modal
			$("#modal_trigger").click();

			var reader = new FileReader();

			// Closure to capture the file information.
			reader.onload = (function(inFile) {
			return function(e) {
				// preview pane on main page
				document.preview.src = e.target.result;
				document.preview.title = escape(inFile.name);
				$('#preview').attr('class', 'hidden');

				// cropping pane
				document.img_crop.src = e.target.result;
				document.img_crop.title = escape(inFile.name);
				
				// delete and crop button
				$('#delete').attr('class', 'btn btn-danger');
				$('#crop_btn').attr('class', 'btn');

				// canvas
				$('#canvas').attr('class', 'top-padded bottom-padded');
				
				// old image
				if (hasImage) {
					$('#old_img').attr("class", "hidden");
				}
				
				uploaded = true;
				
				initJcrop(); // refresh jcrop API - step 2
		  
			};
			})(f);

			// Read in the image file as a data URL.
			reader.readAsDataURL(f);
		}
}
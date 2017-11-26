function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();
	localStorage.setItem("image", profile.getImageUrl());
	localStorage.setItem("email", profile.getEmail());
	localStorage.setItem("name", profile.getName());
	
	window.location="http://localhost/ogd/index.html";
}

function signOut() {
	alert("You have signed out sucessfully");
	window.location="http://localhost/ogd/login.html";
}

function topbarSave() {
	//add method
	alert("Save here");
}

function topbarLoad() {
	//add method
	alert("Load here");
	
}

function topbarExtra() {
	//add method
	alert("Extra here");
}

function onLoadHome() {
	$("#pic").attr('src',localStorage.getItem("image"));
	$("#email").text(localStorage.getItem("email"));
	
	updateDatabase(localStorage.getItem("name"), localStorage.getItem("email"));
}

function updateDatabase(name, email) {
	var posting = $.post("test.php", {
		name: name,	
		email: email
	});
	
	posting.done(function(data){
		// alert(data);
	});
	
	posting.fail(function(data){
		// alert("DB query failed");
	});
}

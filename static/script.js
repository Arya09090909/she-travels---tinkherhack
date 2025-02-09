document.addEventListener("DOMContentLoaded", () => {
    displayProfile();

    // Attach event listeners for category navigation
    document.querySelectorAll(".category").forEach(item => {
        item.addEventListener("click", () => {
            openCategory(item.dataset.category);
        });
    });
});

// Function to preview profile image before saving
function previewImage(event) {
    const reader = new FileReader();
    reader.onload = () => {
        const profilePreview = document.getElementById("profilePreview");
        profilePreview.src = reader.result;
        profilePreview.style.display = "block";
    };
    reader.readAsDataURL(event.target.files[0]);
}

// Function to save user profile details
function saveProfile() {
    const profilePic = document.getElementById("profilePreview").src;
    const username = document.getElementById("username").value.trim();
    const bio = document.getElementById("bio").value.trim();
    const instagram = document.getElementById("instagram").value.trim();
    const facebook = document.getElementById("facebook").value.trim();
    const twitter = document.getElementById("twitter").value.trim();
    const location = document.getElementById("location").value.trim();

    if (!username) {
        alert("⚠ Please enter a username!");
        return;
    }

    const profileData = { profilePic, username, bio, instagram, facebook, twitter, location };
    localStorage.setItem("userProfile", JSON.stringify(profileData));

    displayProfile();
}

// Function to display the user profile from localStorage
function displayProfile() {
    const profileData = JSON.parse(localStorage.getItem("userProfile"));

    if (profileData) {
        document.getElementById("viewProfilePic").src = profileData.profilePic || "default-profile.png";
        document.getElementById("viewUsername").innerText = profileData.username || "Unknown User";
        document.getElementById("viewBio").innerText = profileData.bio || "No bio available.";
        document.getElementById("viewInstagram").href = profileData.instagram ? `https://instagram.com/${profileData.instagram}` : "#";
        document.getElementById("viewInstagram").innerText = profileData.instagram || "Not provided";
        document.getElementById("viewFacebook").href = profileData.facebook ? `https://facebook.com/${profileData.facebook}` : "#";
        document.getElementById("viewFacebook").innerText = profileData.facebook || "Not provided";
        document.getElementById("viewTwitter").href = profileData.twitter ? `https://twitter.com/${profileData.twitter}` : "#";
        document.getElementById("viewTwitter").innerText = profileData.twitter || "Not provided";
        document.getElementById("viewLocation").innerText = profileData.location || "Unknown Location";

        document.getElementById("profileForm").style.display = "none";
        document.getElementById("profileView").style.display = "block";
    }
}

// Function to enable profile editing
function editProfile() {
    document.getElementById("profileForm").style.display = "block";
    document.getElementById("profileView").style.display = "none";
}

// Function to send a request to another user
function sendRequest() {
    let requests = JSON.parse(localStorage.getItem("requests")) || [];
    const username = document.getElementById("viewUsername").innerText;

    if (!requests.includes(username)) {
        requests.push(username);
        localStorage.setItem("requests", JSON.stringify(requests));
        alert("✅ Request sent successfully!");
    } else {
        alert("⚠ You have already sent a request.");
    }
}

// Function to navigate to the messages page
function openMessages() {
    window.location.href = "/messages";
}

// Function to open category pages
function openCategory(category) {
    window.location.href = `/${category}`;
}
async function fetchActivities() {
    const response = await fetch('/get_activities');
    const activities = await response.json();
    let container = document.getElementById('activity-container');
    container.innerHTML = ""; 

    activities.forEach(activity => {
        let listItem = document.createElement('li');
        listItem.innerHTML = `<strong>${activity.date}:</strong> ${activity.description}`;
        container.appendChild(listItem);
    });
}

// Call the function to load activities on page load
fetchActivities();

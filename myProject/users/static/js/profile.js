document.addEventListener("DOMContentLoaded", function () {
  const profileContainer = document.querySelector(".group");
  const changeOverlay = document.getElementById("change-overlay");
  const fileInput = document.getElementById("file-input");
  const modal = document.getElementById("upload-modal");
  const dropZone = document.getElementById("drop-zone");
  const browseBtn = document.getElementById("browse-btn");
  const cancelBtn = document.getElementById("cancel-btn");
  const uploadBtn = document.getElementById("upload-btn");
  const imagePreview = document.getElementById("image-preview");
  const previewImage = document.getElementById("preview-image");
  const profilePicture = document.getElementById("profile-picture");

  let selectedFile = null;

  // Open modal when clicking on profile picture
  if (changeOverlay) {
    changeOverlay.addEventListener("click", () => {
      modal.classList.remove("hidden");
    });
  }

  // Browse files button
  browseBtn.addEventListener("click", () => {
    fileInput.click();
  });

  // File input change
  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length) {
      handleFileSelection(e.target.files[0]);
    }
  });

  // Drag and drop
  ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, highlight, false);
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, unhighlight, false);
  });

  function highlight() {
    dropZone.classList.add("border-blue-500", "bg-blue-50");
  }

  function unhighlight() {
    dropZone.classList.remove("border-blue-500", "bg-blue-50");
  }

  dropZone.addEventListener("drop", (e) => {
    const dt = e.dataTransfer;
    const file = dt.files[0];
    if (file && file.type.match("image.*")) {
      handleFileSelection(file);
    }
  });

  // Handle file selection
  function handleFileSelection(file) {
    selectedFile = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.src = e.target.result;
      imagePreview.classList.remove("hidden");
      uploadBtn.disabled = false;
    };
    reader.readAsDataURL(file);
  }

  // Cancel button
  cancelBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
    resetModal();
  });

  // Form submission

  // Reset modal state
  function resetModal() {
    selectedFile = null;
    fileInput.value = "";
    imagePreview.classList.add("hidden");
    uploadBtn.disabled = true;
    unhighlight();
  }
});
// Form submission for profile data

// const modal = document.getElementById("delete-modal");
// const openBtn = document.getElementById("delete-openModal");
// const cancelBtn = document.getElementById("delete-cancelBtn");
// const confirmBtn = document.getElementById("delete-confirmDelete");

// openBtn.addEventListener("click", () => {
//   modal.classList.remove("hidden");
//   modal.classList.add("flex");
// });

// cancelBtn.addEventListener("click", () => {
//   modal.classList.remove("flex");
//   modal.classList.add("hidden");
// });

// confirmBtn.addEventListener("click", () => {
//   modal.classList.remove("flex");
//   modal.classList.add("hidden");
// });
// Profile field editing functionality
function editField(field) {
  const textEl = document.getElementById(`${field}Text`);
  const inputEl = document.getElementById(`${field}Input`);

  if (textEl && inputEl) {
    textEl.classList.add("hidden");
    inputEl.classList.remove("hidden");
    inputEl.value = textEl.textContent.trim();
    document.getElementById("saveChanges").classList.remove("hidden");
  }
}

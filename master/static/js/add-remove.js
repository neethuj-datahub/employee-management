// document.addEventListener("DOMContentLoaded", function () {
//   const addButton = document.getElementById("addButton");
//   const deleteButton = document.getElementById("deleteButton");
//   const textAreaContainer = document.getElementById("textAreaContainer");
//   let pairCount = 0;

//   addButton.addEventListener("click", function () {
//     pairCount++;

//     const label = document.createElement("label");
//     label.textContent = "Method / Specification " + pairCount;

//     const textarea = document.createElement("textarea");
//     textarea.name = "siteInspSbName[]";
//     textarea.cols = "1";
//     textarea.rows = "2";
//     textarea.className = "form-control mb-3";
//     textAreaContainer.appendChild(label);
//     textAreaContainer.appendChild(textarea);
//     deleteButton.style.display = "inline";
//   });

//   deleteButton.addEventListener("click", function () {
//     const labels = textAreaContainer.querySelectorAll("label");
//     const textareas = textAreaContainer.querySelectorAll("textarea");
//     if (labels.length > 0 && textareas.length > 0) {
//       textAreaContainer.removeChild(labels[labels.length - 1]);
//       textAreaContainer.removeChild(textareas[textareas.length - 1]);
//       pairCount--;
//     }
//     if (labels.length === 0 || textareas.length === 0) {
//       deleteButton.style.display = "none";
//     }
//   });
//   deleteButton.style.display = "none";
// });



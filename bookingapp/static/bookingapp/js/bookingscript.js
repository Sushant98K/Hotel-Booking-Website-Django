function checkDate() {
   document.addEventListener("DOMContentLoaded", function () {
     const today = new Date();
     const checkInInput = document.getElementById("check_in");
     const checkOutInput = document.getElementById("check_out");

     // Set the minimum date for check-in and check-out to today
     const formattedDate = today.toISOString().split("T")[0];
     checkInInput.setAttribute("min", formattedDate);
     checkOutInput.setAttribute("min", formattedDate);

     checkInInput.addEventListener("change", function () {
       const checkInDate = new Date(checkInInput.value);
       if (checkInDate < today) {
         alert("Check-in date cannot be in the past.");
         checkInInput.value = formattedDate; // Reset to today
       }
       checkOutInput.value = ""; // Reset check-out date
     });

     checkOutInput.addEventListener("change", function () {
       const checkInDate = new Date(checkInInput.value);
       const checkOutDate = new Date(checkOutInput.value);
       if (checkOutDate < checkInDate) {
         alert("Check-out date cannot be earlier than check-in date.");
         checkOutInput.value = ""; // Reset check-out date
       }
     });
   });
}



checkDate();

const form = document.querySelector('form');
const fullName = document.getElementById("name");
const email = document.getElementById("email");
const phone = document.getElementById("phone");
const subject = document.getElementById("subject");
const mess = document.getElementById("message");

function sendEmail() {
  const bodyMessage = `Full Name : ${fullName.value}<br> Email: ${email.value}<br> Phone Number: ${phone.value}<br> Message: ${mess.value}`;
  
  Email.send({
    Host: "smtp.elasticemail.com",
    Username: "jacob@raskguitars.com",
    Password: "FCA823CDDCC9097326B9E97ADBD4ACA0D571",
    To: 'jacob@raskguitars.com',
    From: "you@isp.com",
    Subject: subject.value,
    Body: bodyMessage
}).then(
  message => {
    if (message == "OK") {
        Swal.fire({
          title: "Success!",
          text: "Message sent successfully!",
          icon: "success"
        });  
    }
);
}

form.addEventListener("submit", (e) => {
  e.preventDefault();

  sendEmail();
});

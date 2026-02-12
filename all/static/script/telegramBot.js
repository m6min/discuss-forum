/* 
   THIS FILE HOLDS THE TELEGRAM API FOR CONTACT PAGE, FEEDBACK AREA
   NOTE: YOU SHOULD ENTER YOUR API TOKEN.
*/
const token = "EnterYourToken";
const chat_id = "Enter your chat_id as string.";
const button = document.querySelector("#send");
button.addEventListener("click", () => {
    let input = document.querySelector("#feedback").value;
    if (input.length == 0) {
        button.textContent = "The text is empty!";
        setTimeout(() => {
            button.innerHTML = "<i class='fa-solid fa-paper-plane'></i> Send";
        }, 2000);
    }
    else {
        sendMessage(input);
    }
});
const sendMessage = async (text) => {
    const url = `https://api.telegram.org/bot${token}/sendMessage`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: chat_id,
                text: text
            })
        });
        const result = await response.json();
        if(result.ok){
            button.textContent = "Send successfully, thanks for your time!";
            document.querySelector("#feedback").value = "";
            setTimeout(() => {
            button.innerHTML = "<i class='fa-solid fa-paper-plane'></i> Send";
        }, 2000);
        }
        else {
            button.textContent = "There is an error occured. Please try again later.";
            setTimeout(() => {
            button.innerHTML = "<i class='fa-solid fa-paper-plane'></i> Send";
        }, 2000);
        }
    } catch (error) {
        console.log("Request is declined: ", error);
        button.textContent = "There is an error occured. Please check the console logs.";
        setTimeout(() => {
            button.innerHTML = "<i class='fa-solid fa-paper-plane'></i> Send";
        }, 2000);
    }
}
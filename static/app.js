let time = 60;
let lockBoard = false;
let score = 0;

$input = $("#input");
$board = $("main");
$alert = $(".alert");
//Executes as soon as the app opens - Timmer logic that locks the board once the timmer runs out
(function setTimmer() {
  const interval = setInterval(() => {
    time--;
    $(".timmer").text(`${time} seconds`);
    if (time === 0) {
      lockBoard = true;
      $(".alert").hide();
      $("#reset").toggleClass("hidden");
      //Sends the new high score to the server
      setHighScore(score);
      clearInterval(interval);
    }
  }, 1000);
})();

$(".score").text(`Score: 0`);
//Sumbit the guees logic
$("body").on("submit", "#form", async (evt) => {
  evt.preventDefault();
  if (lockBoard) return;
  input = $input.val();
  if (!input) return;
  //Sends the answer to the server and responds with if the answer is correct
  response = await checkWord(input);
  //Sends user input if the answer is found or not
  displayResult(response, input);

  $input.val("");
});

$("#reset").on("click", () => location.reload());
//Function that sends the reques to the server
async function checkWord(input) {
  const response = await axios.get("/check-word", { params: { word: input } });
  return response.data.result;
}
//Manipulates the DOM, and gives feedback on answer
const displayResult = (response, input) => {
  if (response === "ok") {
    $alert.text("Word was found");
    $alert.removeClass("alert-danger");
    $alert.addClass("alert-success");
    score += input.length;
    $(".score").text(`Score: ${score}`);
  } else {
    $alert.text("Word was not found or already found");
    $alert.removeClass("alert-success");
    $alert.addClass("alert-danger");
  }
};
//Sends the high score to the sever to be stored
async function setHighScore(score) {
  response = await axios.post("/end-game", { "high-score": score });
  console.log(response);
}
